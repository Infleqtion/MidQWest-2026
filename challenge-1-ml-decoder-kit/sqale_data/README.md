# Measured counts from Sqale

Measurement outcomes of Infleqtion's Sqale neutral-atom processor.

- **Source.** Zenodo record https://doi.org/10.5281/zenodo.17137995 (version 0.0.2), the data
  of arXiv:2509.13247. `shor-counts.json` and `cdcx-counts.json` are copied unchanged from
  its `paper-data/` folder.
- **License.** The record is published under CC BY 4.0. `LICENSE` is the Apache 2.0 file of
  the archive.

## Format

Each file maps an experiment to `{outcome: number of shots}`. An outcome has one character
per measured atom: `0`, `1`, or `2` for an atom that was not detected (atom loss).

```bash
python sqale_data/summary.py
```

| experiment | shots | atoms | shots with a lost atom |
|------------|-------|-------|------------------------|
| `shor_unencoded` | 5275 | 3 | 9% |
| `shor_2row` | 5275 | 20 | 34% |
| `shor_3row` | 5274 | 20 | 52% |
| `shor_2row_ld` (with leakage detection) | 10,549 | 20 | 43% |
| `cdcx_encoded`, ten input states | about 2110 each | 20 | 51% to 55% |
| `cdcx_unencoded`, ten input states | about 2110 each | 8 | 18% to 21% |

- `shor_*` are the circuits of Shor's algorithm in the paper. Without noise the three
  logical bits read 000, 010, 101 or 111 with probability 1/4 each.
- `cdcx_*` are the constant-depth CNOT ladder circuits. The key of each entry is the input
  state.
- Encoded circuits use blocks of five atoms: one flag atom, then the four atoms of a
  [[4,2,2]] code block. `cdcx_encoded` has four blocks. The Shor circuits use atoms 10 to 19
  (`shor_2row`), 5 to 19 (`shor_3row`) and 5 to 14 (`shor_2row_ld`, where atoms 1 to 4 and
  16 to 19 detect leakage).

## What the archive adds

Download the archive from the Zenodo record for:

- `experiments_superstaq/iceberg_demos/circuits.py`: the circuits.
- `experiments_superstaq/iceberg_demos/analysis.py`: postselection and decoding of the
  outcomes (`decode_shor_2row`, `decode_shor_3row`, `decode_shor_2row_ld`,
  `decode_cdcx_encoded`).
- `experiments_superstaq/simulation/`: a simulator with a five-level model of each atom
  (qubit states, two leakage states, loss) and the parameter values used in the paper.
- `paper-data/shor_sim_data/`: simulated counts.

The appendix of arXiv:2509.13247 lists the model: state preparation fidelity 97.9%, a phase
error of 0.73% per atom in a CZ gate, transition probabilities between the five levels for
CZ and Rz, readout errors of 0.2% and 2.3%, and a phase error of 4.1% for a moved atom.
