import random

def generate_sequence(length: int) -> str:
    return ''.join(random.choices(['A', 'C', 'G', 'T'], k=length))

def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")

def main():
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq = generate_sequence(length)
    print("Test: wygenerowano sekwencję o długości", length)

if __name__ == "__main__":
    main()