import random


def generate_sequence(length: int, weights: dict = None) -> str:
    if weights:
        nucs = list(weights.keys())
        probs = list(weights.values())
        return ''.join(random.choices(nucs, weights=probs, k=length))
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
        lines.append(sequence[i:i + line_width])
    return '\n'.join(lines)


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


def get_custom_distribution() -> dict:
    print("Skonfiguruj rozkład nukleotydów (suma musi wynosić 100).")
    while True:
        try:
            a = float(input("Procent A: "))
            c = float(input("Procent C: "))
            g = float(input("Procent G: "))
            t = float(input("Procent T: "))
            if abs((a + c + g + t) - 100.0) < 0.001:
                return {'A': a, 'C': c, 'G': g, 'T': t}
            print("Błąd: suma nie wynosi 100%.")
        except ValueError:
            print("Błąd: należy podać liczby.")


def search_motif(sequence: str, motif: str) -> list:
    positions, start = [], 0
    while True:
        pos = sequence.find(motif, start)
        if pos == -1: break
        positions.append(pos + 1)
        start = pos + 1
    return positions


def get_complements(sequence: str) -> tuple:
    comp = sequence.translate(str.maketrans('ACGT', 'TGCA'))
    return comp, comp[::-1]


def transcribe_to_mrna(sequence: str) -> str:
    return sequence.replace('T', 'U')


def main():
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = input("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    use_custom = input("Czy chcesz podać własny rozkład nukleotydów? (t/n): ").strip().lower()
    weights = get_custom_distribution() if use_custom == 't' else None

    base_seq = generate_sequence(length, weights)
    final_seq = insert_name(base_seq, name)
    print("Główna logika gotowa.")


if __name__ == "__main__":
    main()