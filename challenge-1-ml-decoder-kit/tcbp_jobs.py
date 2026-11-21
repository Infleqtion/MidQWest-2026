"""Step 1: run NVIDIA's TCBP-JOBS decoder on the shots of baseline.py.

  pip install cudaq-qec==0.9.0      # needs an NVIDIA GPU
  python tcbp_jobs.py --p 0.004 --shots 10000

TCBP-JOBS (arXiv:2611.21321) runs 10 iterations of BP, ranks the error mechanisms with a small
neural network that reads the BP messages, and searches for a correction. The network is
fitted on simulated shots of the detector matrix first, which takes about a minute per basis.
The shots, the scoring and the output line are those of baseline.py.
"""
import argparse

import numpy as np

from baseline import memory_experiments
from circuit import GROSS_CIRCUITS
from decoders import print_score, score

PRESET = "tcbp-jobs"   # the configuration of the paper


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--circuits", nargs=2, default=[GROSS_CIRCUITS["X"], GROSS_CIRCUITS["Z"]],
                        metavar=("X_CIRCUIT", "Z_CIRCUIT"), help="the X memory and the Z memory circuit")
    parser.add_argument("--cycles", type=int, default=12, help="noisy syndrome cycles in the circuit")
    parser.add_argument("--p", type=float, default=0.004, help="physical noise strength")
    parser.add_argument("--shots", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=1)
    return parser.parse_args()


def tcbp_jobs_decoder(H, priors):
    """TCBP-JOBS for one detector matrix, with its network fitted on that matrix."""
    import cudaq_qec as qec
    from cudaq_qec.plugins import nv_qldpc
    H, priors = H.toarray(), list(priors)
    model = nv_qldpc.init_tcbp_model(H, error_rate_vec=priors)
    options = nv_qldpc.preset(PRESET, tcbp_model=model)
    return qec.get_decoder("nv-qldpc-decoder", H, error_rate_vec=priors, **options)


def decode_function(decoder):
    """A function that maps one syndrome to an error vector, as decoders.score expects."""
    def decode(syndrome):
        return np.round(decoder.decode(syndrome.astype(float).tolist()).result)
    return decode


def score_experiment(experiment):
    """(failed, seconds) of TCBP-JOBS on the shots of one experiment, one shot at a time."""
    decoder = tcbp_jobs_decoder(experiment.H, experiment.priors)
    return score(decode_function(decoder), experiment.L, experiment.det, experiment.obs)


def main():
    args = parse_args()
    experiments = memory_experiments(args.circuits, args.p, args.shots, args.seed)
    print(f"{args.shots} shots at p={args.p}, {args.cycles} cycles, failures listed as [X Z]")
    failed, seconds = zip(*[score_experiment(experiment) for experiment in experiments], strict=True)
    print_score("tcbp-jobs", np.column_stack(failed), np.column_stack(seconds), args.cycles)


if __name__ == "__main__":
    main()
