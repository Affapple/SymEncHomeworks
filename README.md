# Symmetric Key Cryptography — Homeworks

Five homework assignments for the *Symmetric Key Cryptography* course (University of Luxembourg, spring 2026), by João Gaspar.

Each homework is a written report (PDF plus its LaTeX source) together with the code that produced the results quoted in it. The report is the primary deliverable; the code is there so every number in it can be regenerated.

## Overview

| # | Topic | Report | Code |
|---|-------|--------|------|
| 1 | Cryptanalysis of Enigma (method of batons, Turing–Welchman bombe), M-209 collisions | [PDF, 7 p.](homework1/Report/report_JoaoGaspar.pdf) | C |
| 2 | Stream and block ciphers (LFSRs, correlation attack on a Geffe generator, a linear RC5 variant) | [PDF, 4 p.](homework2/homework2_report_JoaoGaspar.pdf) | Python |
| 3 | AES internals, meet-in-the-middle on double AES, differential cryptanalysis of DES, Even–Mansour | [PDF, 5 p.](homework3/homework3_report_JoaoGaspar.pdf) | Python |
| 4 | Hash functions and MACs (collisions, second preimages, sponge, MAC forgery) | [PDF, 6 p.](homework4/homework4_report_JoaoGaspar.pdf) | Python |
| 5 | Authenticated encryption, algebraic degree of AES, integral attack on 4-round AES | [PDF, 6 p.](homework5/homework5_report_JoaoGaspar.pdf) | Python |

Every folder follows the same pattern:

- the assignment statement (`hw.pdf` / `HW<n>.pdf`),
- the report (`*report_JoaoGaspar.pdf`) and its source (`main.tex`),
- one script per exercise (`Ex<exercise>.py`, or `ex<n>_*.c` in homework 1),
- the personal problem instance handed out for the homework (`data.json`, or `exercise/` and `sol/` in homework 1).

Exercises with no script listed below are pen-and-paper answers that live only in the report.

## Homework 1 — Cryptanalysis of Enigma

| Ex. | Task | Outcome | Code |
|-----|------|---------|------|
| 1 | Method of batons on a plugboard-less Enigma | Start position of rotor N is uniquely `Q` (crib `THEREISN`) | `ex1_batons.c` |
| 2.1 | Build the crib graph, choose loops, estimate false positives | 3 loops through `V`; about 26 false candidates expected | report |
| 2.2 | Turing attack using loops | 18 candidate rotor settings, each with one hypothesis for the plug of `V` | `ex2_turing_loops.c` |
| 2.3 | Full Turing–Welchman attack (diagonal board) | 2 candidate settings (`RRM`, `CRR`) with the surviving plugboard options per letter | `ex3_turing_welchman.c` |
| 3 | M-209 state collisions | Probability of a repeated state answered (≈ 1); the expected maximum overlap is **not answered** | report |

`enigma.c` is the model of the homework's Enigma machine that the attacks build on. `exercise/` holds the ciphertexts and `sol/` the matching known plaintexts.

```sh
cd homework1
make ex1                          # builds and runs exercise 1
make ex2 && ./ex2_turing_loops    # < 1 s
make ex3 && ./ex3_turing_welchman # < 1 s
```

## Homework 2 — Stream and block ciphers

| Ex. | Task | Outcome | Code |
|-----|------|---------|------|
| 1.1.1 | Recover the LFSR state behind a 256-bit keystream | The state is the first 128 keystream bits; verified by regenerating the stream | `Ex1.py` |
| 1.1.2 | State after 2^64 + 13 steps | Computed with square-and-multiply on the 128×128 transition matrix over GF(2) | `Ex2.py` |
| 1.2 | Divide-and-conquer attack on a Geffe-like generator | All three 16-bit LFSR states recovered; 200/200 keystream bits match | `Ex3.py` |
| 1.3.1 | Degree of a filtered-LFSR keystream bit | Degree 2 | report |
| 1.3.2 | Linearization attack (optional, bonus) | **Not attempted** | — |
| 2 | Modified RC5 without non-linear operations | Shown to be affine in the key: one known plaintext/ciphertext pair is enough to encrypt any message, whatever the number of rounds | `Ex4.py` |

`implementation.py` contains the cipher models (`LFSR`, `Geffe`, `FilteredLFSR`, `ModifiedRC5`) that the attack scripts import.

```sh
cd homework2
pip install numpy   # only Ex2.py needs it
python3 Ex1.py
python3 Ex2.py
python3 Ex3.py      # ~10 s
python3 Ex4.py      # uses a fresh random key each run
```

## Homework 3 — Differential cryptanalysis

| Ex. | Task | Outcome | Code |
|-----|------|---------|------|
| 1.1 | Push one column through `SubBytes` and `MixColumns`, then invert for a given output difference | `b = 60 e8 f4 90`, `a* = f0 64 e8 25`, `b* = 8c 43 9b 3f` | `Ex1_1.py` |
| 1.2 | AES without `ShiftRows` | Key recovered as four independent 32-bit column searches (2^34 work instead of 2^128) | `Ex1_2.py` |
| 1.3 | Importance of `MixColumns` | **Not attempted** (stated in the report) | — |
| 1.4 | Double AES with two 24-bit keys | Meet-in-the-middle: `k1 = cbb938`, `k2 = 4a8a53` | `Ex1_4.py` |
| 2.1 | Difference analysis of DES S-box 1 | Compatible input pairs and resulting key candidates | `Ex2.py` |
| 2.2 | Differential attack on 7-round DES | Last-round subkey candidates per S-box, then exhaustive search over the remainder: master key `0xA8480C7EDE445AEE` | `Ex2.py`, `DES_util.py` |
| 3 | Even–Mansour with AES | 2^128 attack described; 2^64 slidex attack summarised from the literature | report |

`AES.py` is a round-by-round AES used by exercises 1.1 and 1.2; `DES_util.py` holds the DES tables, permutations and a 7-round encryption.

```sh
cd homework3
uv sync                     # Python 3.12, dependencies from pyproject.toml / uv.lock
uv run python Ex1_1.py
uv run python Ex1_2.py      # ~20 min on 4 cores (figure from the report), fresh random key each run
uv run python Ex1_4.py      # ~2 min, needs about 2 GB of RAM for the 2^24-entry table
uv run python Ex2.py        # ~2.5 min; ~7 s with pypy3 (which then needs tqdm installed)
```

## Homework 4 — Hash functions and MACs

| Ex. | Task | Outcome | Code |
|-----|------|---------|------|
| 1 | Collisions for concatenated hash functions | Multicollision attack in about n·2^(n/2); extension to three functions | report |
| 2 | Memoryless collision on SHA-256 truncated to 48 bits | Floyd cycle finding; `Joao‖5e5b39d274b7` and `Joao‖92c489a4bdd7` collide | `Ex2.py` |
| 3 | Meaningful second preimage on a 16-bit hash | Synonym substitution (about 2^23.9 variants of one text) reaches any 16-bit target; the program's own hash prefix matches that of the author's name | `Ex3.py`, `Ex3_filehash.py` |
| 4 | Second preimage on a sponge in 2^(c/2) | Algorithm described | report |
| 5 | Forgery on a PMAC variant (bonus) | Valid tag `473b156defe648e39bafd0f6706eddc3` built by XOR-ing five oracle answers | report |

```sh
cd homework4
pip install -r requirements.txt
python3 Ex2.py        # ~1 min; random start, so each run finds a different collision
python3 Ex3.py 8008   # argument: target digest as 4 hex digits
```

The collision quoted above can be checked without running the search (the suffix is raw bytes, shown in hex):

```sh
python3 -c "import hashlib; [print(hashlib.sha256(b'Joao'+bytes.fromhex(s)).hexdigest()[:12]) for s in ('5e5b39d274b7','92c489a4bdd7')]"
```

Two things to know about exercise 3:

- `Ex3.py` is itself part of the answer: the first 16 bits of its SHA-256 equal those of SHA-256(`Joao`), namely `5f2e`. Compare `sha256sum Ex3.py` with `echo -n Joao | sha256sum`. Any edit to the file, even reformatting, breaks this.
- `Ex3_filehash.py` is the tool that produced that property by appending a nonce comment to `Ex3.py`. Running it again modifies `Ex3.py`.

Exercise 5 has no script: the tags came from the course's signing oracle and were combined by hand. The derivation and a screenshot of the accepted forgery are in the report.

## Homework 5 — Authenticated encryption

| Ex. | Task | Outcome | Code |
|-----|------|---------|------|
| 1 | Four encrypt-with-redundancy constructions | CTR-based ones broken with explicit attacks; CBC-based ones argued secure | report |
| 2 | CCA security of `E(x ‖ r ‖ x⊕r)` | Argued CCA-secure | report |
| 3 | Reusing one key for encryption and MAC | Decryption, CPA and MAC proofs, and the break of the combined scheme | report |
| 4 | Sponge-based authenticated encryption | Decryption algorithm and a truncation forgery | report |
| 5 | Algebraic degree of 2-round AES | Degree 31 via the Super-S-box; count of maximum-degree monomials | report |
| 6 | Integral property of 3-round AES and key recovery on 4 rounds | Zero-sum confirmed over 8 random keys; full last-round key recovered from at most 3 sets of 256 chosen plaintexts | `aes_integral.py` |

```sh
cd homework5
python3 aes_integral.py   # no dependencies, < 1 s, random key each run
```

`chat/` holds an AI-assistant draft of the same script and its explanatory notes (see the next section).

## Third-party and AI-assisted code

The reports and source comments declare the following, collected here for convenience:

- **Homework 3, `AES.py`** — adapted from the open-source AES implementation by *bluekeybo*, extended with inverse operations and a "simplified" mode without `ShiftRows`.
- **Homework 3, `Ex1_2.py`** — the attack was first written as a plain loop (kept at the bottom of the file as `original_unoptimized_version`); the batched NumPy and multiprocessing version was produced with Claude from that original.
- **Homework 3, `DES_util.py`** — the permutation helpers and the 7-round DES are marked `AI Generated Code` in their docstrings, some with manual adjustments.
- **Homework 5, `aes_integral.py`** — the AES primitives between the `AI GENERATED CODE` markers are AI-written; the integral check and the key-recovery attack are the author's, written with Copilot assistance.

## Notes for running

- Run every script from inside its homework folder; `data.json` and input files are opened by relative path.
- Homework 1 needs `gcc` and `make`. Linux x86-64 binaries are committed, but rebuilding is quick.
- Every program was re-run against this revision and printed the values quoted here, apart from `homework3/Ex1_2.py` (too long) and `homework4/Ex3_filehash.py` (it rewrites `Ex3.py`).
- Run times are indicative, measured on one machine.
- `homework3/HW4.pdf` is not the statement for homework 3: it is a previous year's edition of the hash-function assignment. The homework 3 statement is not in the repository, so the exercise titles above are taken from the report.
