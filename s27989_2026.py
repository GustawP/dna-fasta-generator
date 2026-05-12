# Numer albumu: s27989
# Data: 2026-05-12
# Opis: Generator losowych sekwencji DNA w formacie FASTA.
# Program rozszerzony o: własny rozkład nukleotydów, generowanie nici komplementarnych, transkrypcję oraz wyszukiwanie motywów.

import random


def generate_sequence(length: int, weights: dict = None) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości.
    Jeśli podano wagi (weights), generuje sekwencję zgodnie z określonym rozkładem."""
    if weights:
        nucs = list(weights.keys())
        probs = list(weights.values())
        return ''.join(random.choices(nucs, weights=probs, k=length))
    return ''.join(random.choices(['A', 'C', 'G', 'T'], k=length))


def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T", "gc_ratio_A" (wartości float, %)."""
    length = len(sequence)
    if length == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "gc_ratio_A": 0.0}

    counts = {n: sequence.count(n) for n in ['A', 'C', 'G', 'T']}
    stats = {n: (counts[n] / length) * 100 for n in counts}
    stats["gc_ratio_A"] = ((counts['G'] + counts['C']) / length) * 100
    return stats


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    if not name:
        return sequence
    name = name.lower()
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name + sequence[pos:]


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    header = f">{seq_id} {description}".strip()
    lines = [header]
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])
    return '\n'.join(lines)


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu.
    W przypadku błędu powtarza pytanie."""
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


# --- FUNKCJONALNOŚCI DODATKOWE ---

def get_custom_distribution() -> dict:
    """Pobiera od użytkownika procentowy rozkład nukleotydów. Waliduje sumę (100%)."""
    print("Skonfiguruj rozkład nukleotydów (suma musi wynosić 100).")
    while True:
        try:
            a = float(input("Procent A: "))
            c = float(input("Procent C: "))
            g = float(input("Procent G: "))
            t = float(input("Procent T: "))
            if abs((a + c + g + t) - 100.0) < 0.001:
                return {'A': a, 'C': c, 'G': g, 'T': t}
            else:
                print("Błąd: suma nie wynosi 100%. Spróbuj ponownie.")
        except ValueError:
            print("Błąd: należy podać wartości liczbowe.")


def search_motif(sequence: str, motif: str) -> list:
    """Wyszukuje motyw w sekwencji i zwraca listę pozycji (indeksowane od 1)."""
    positions = []
    start = 0
    while True:
        pos = sequence.find(motif, start)
        if pos == -1:
            break
        positions.append(pos + 1)
        start = pos + 1
    return positions


def get_complements(sequence: str) -> tuple:
    """Zwraca sekwencję komplementarną oraz odwrotnie komplementarną jako krotkę."""
    complement_map = str.maketrans('ACGT', 'TGCA')
    comp = sequence.translate(complement_map)
    rev_comp = comp[::-1]
    return comp, rev_comp


def transcribe_to_mrna(sequence: str) -> str:
    """Generuje sekwencję mRNA na podstawie DNA (T -> U)."""
    return sequence.replace('T', 'U')


# --- FUNKCJA GŁÓWNA ---

def main():
    """Zarządza logiką programu."""
    length = validate_positive_int("Podaj długość sekwencji: ")

    while True:
        seq_id = input("Podaj ID sekwencji: ")
        if " " not in seq_id and len(seq_id) > 0:
            break
        print("Błąd: ID nie może być puste ani zawierać białych znaków.")

    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    use_custom = input("Czy chcesz podać własny rozkład nukleotydów? (t/n): ").strip().lower()
    weights = None
    if use_custom == 't':
        weights = get_custom_distribution()

    base_sequence = generate_sequence(length, weights)
    stats = calculate_stats(base_sequence)
    final_sequence = insert_name(base_sequence, name)

    comp_seq, rev_comp_seq = get_complements(base_sequence)
    mrna_seq = transcribe_to_mrna(base_sequence)

    filename = f"{seq_id}.fasta"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(format_fasta(seq_id, description, final_sequence) + "\n")
        f.write(format_fasta(f"{seq_id}_comp", "Nici komplementarna", comp_seq) + "\n")
        f.write(format_fasta(f"{seq_id}_revcomp", "Nici odwrotnie komplementarna", rev_comp_seq) + "\n")
        f.write(format_fasta(f"{seq_id}_mRNA", "Transkrypt mRNA", mrna_seq) + "\n")

        f.write("\n# EOF_1\n")

    print(f"\nSekwencja zapisana do pliku: {filename}\n")

    print(f"Statystyki sekwencji (n={length}):")
    print(f"  A: {stats['A']:.2f}%")
    print(f"  C: {stats['C']:.2f}%")
    print(f"  G: {stats['G']:.2f}%")
    print(f"  T: {stats['T']:.2f}%")
    print(f"  GC-content: {stats['gc_ratio_A']:.2f}%\n")

    motif = input(
        "Podaj motyw do wyszukania w czystej sekwencji (np. ATG) lub wciśnij Enter by pominąć: ").strip().upper()
    if motif:
        positions = search_motif(base_sequence, motif)
        if positions:
            print(f"Znaleziono motyw {motif} na pozycjach: {positions}")
        else:
            print(f"Nie znaleziono motywu {motif}.")


if __name__ == "__main__":
    main()