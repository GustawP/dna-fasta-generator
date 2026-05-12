import random

def generate_sequence(length: int) -> str:
    return ''.join(random.choices(['A', 'C', 'G', 'T'], k=length))

def calculate_stats(sequence: str) -> dict:
    length = len(sequence)
    if length == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "gc_ratio_A": 0.0}
    counts = {n: sequence.count(n) for n in ['A', 'C', 'G', 'T']}
    stats = {n: (counts[n] / length) * 100 for n in counts}
    stats["gc_ratio_A"] = ((counts['G'] + counts['C']) / length) * 100
    return stats

def insert_name(sequence: str, name: str) -> str:
    if not name:
        return sequence
    name = name.lower()
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name + sequence[pos:]

def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    header = f">{seq_id} {description}".strip()
    lines = [header]
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i+line_width])
    return '\n'.join(lines)

def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_