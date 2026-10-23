# DNA FASTA Generator

A Python command-line tool that generates random DNA sequences, computes their composition and writes them in FASTA format together with their complementary strands and mRNA transcript. Built for the bioinformatics programming course (PBIO) at PJAIT.

## Features

- **Random DNA of a chosen length**, either uniform or with a custom nucleotide distribution (percentages for A, C, G and T, validated to sum to 100%)
- **Composition statistics**: share of each nucleotide and GC content
- **Complementary and reverse-complementary strands**
- **Transcription to mRNA** (T → U)
- **Motif search**: every position of a motif such as `ATG`, 1-indexed, overlapping matches included
- **FASTA output** with 80-character lines, one record per sequence
- Input validation throughout: length range, sequence ID without whitespace, numeric distribution

## Usage

Requires Python 3.9+, no external packages.

```bash
python dna_fasta_generator.py
```

The program asks for the sequence length, ID, description and a name, then optionally a custom distribution. It writes `<ID>.fasta` with four records and prints the statistics:

```
>seq1 Example sequence
ACGTTAGCgustawTTACG...
>seq1_comp Nici komplementarna
...
>seq1_revcomp Nici odwrotnie komplementarna
...
>seq1_mRNA Transkrypt mRNA
...
```

Finally it offers to search the sequence for a motif.

The name is inserted into the first record in lowercase at a random position. This was part of the course assignment, as a visible marker of who generated the file. Statistics, complements, transcript and motif search are all computed on the sequence without the name.

## Implementation notes

- Weighted generation uses `random.choices` with the given weights.
- Complements use `str.maketrans`/`translate`, so the whole strand is converted in one pass.
- Motif search advances one position past each match, so overlapping occurrences (e.g. `AA` in `AAA`) are all found.

## Possible extensions

- A command-line interface with arguments (`argparse`) instead of interactive prompts, so it can be scripted.
- A seed option for reproducible sequences.
- Translation of the mRNA into a protein sequence.
