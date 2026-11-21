"""Shots and atom loss in the measured Sqale counts.

  python sqale_data/summary.py

An outcome is one character per measured atom: 0, 1, or 2 for an atom that was not detected.
"""
import json
from pathlib import Path

import numpy as np

FOLDER = Path(__file__).parent
LOST = 2


def load_counts():
    """{experiment: {outcome: shots}} for the four Shor circuits and the two CNOT-ladder circuits.

    The CNOT-ladder counts of the ten input states are kept apart as "name input".
    """
    experiments = json.loads((FOLDER / "shor-counts.json").read_text())
    ladder = json.loads((FOLDER / "cdcx-counts.json").read_text())
    for name, by_input in ladder.items():
        experiments.update({f"{name} {bits}": counts for bits, counts in by_input.items()})
    return experiments


def as_arrays(counts):
    """(outcomes, shots): one row of symbols per distinct outcome, and how often it occurred."""
    outcomes = np.array([[int(symbol) for symbol in outcome] for outcome in counts])
    return outcomes, np.array(list(counts.values()))


def loss_summary(counts):
    """(shots, atoms, fraction of shots with a lost atom, loss fraction of every atom)."""
    outcomes, shots = as_arrays(counts)
    lost = outcomes == LOST
    per_atom = (lost * shots[:, None]).sum(axis=0) / shots.sum()
    return shots.sum(), outcomes.shape[1], (lost.any(axis=1) * shots).sum() / shots.sum(), per_atom


def main():
    for name, counts in load_counts().items():
        shots, atoms, with_loss, per_atom = loss_summary(counts)
        print(f"{name:22s} {shots:6d} shots  {atoms:2d} atoms  shots with a loss {with_loss:5.1%}  "
              f"loss per atom {per_atom.min():.1%} to {per_atom.max():.1%}")


if __name__ == "__main__":
    main()
