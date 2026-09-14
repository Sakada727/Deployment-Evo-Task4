import random
import string
import datetime
import os

MIN_LENGTH = 7
MAX_LENGTH = 10

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))

def main():
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    log_path = os.path.join(output_dir, "passwords.log")

    print("=== Password Generator ===")

    while True:
        length_input = input(f"Enter password length ({MIN_LENGTH}-{MAX_LENGTH}): ").strip()
        if length_input.isdigit() and MIN_LENGTH <= int(length_input) <= MAX_LENGTH:
            length = int(length_input)
            break
        print(f"Please enter a whole number between {MIN_LENGTH} and {MAX_LENGTH}.")

    while True:
        count_input = input("How many passwords to generate? (e.g. 1): ").strip()
        if count_input.isdigit() and int(count_input) > 0:
            count = int(count_input)
            break
        print("Please enter a positive whole number.")

    print(f"\nGenerating {count} password(s) of length {length}...\n")

    with open(log_path, "a") as f:
        for _ in range(count):
            pwd = generate_password(length)
            timestamp = datetime.datetime.utcnow().isoformat() + "Z"
            line = f"{timestamp} | length={length} | {pwd}"
            print(line)
            f.write(line + "\n")

    print(f"\nDone. Results appended to {log_path}")

if __name__ == "__main__":
    main()