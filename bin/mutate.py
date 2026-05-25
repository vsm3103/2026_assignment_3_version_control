#!/usr/bin/env python3

from random import random
import sys

MAX_UPPERCASE = 3
MAX_XXX = 3
MUTATE_CHANCE = 0.2
MAX_PASSES = 100

def mutate_lines(original_lines):
    """Apply random mutations, returning (mutated_lines, num_uppercase, num_xxx)."""
    num_uppercase = 0
    num_xxx = 0
    mutated_lines = []
    for line in original_lines:
        words = line.split(" ")
        if len(words) > 1 and random() < 0.6:  # Skip 40% of actual text lines
            new_words = []
            for word in words:
                if num_uppercase < MAX_UPPERCASE:
                    if random() < MUTATE_CHANCE:
                        word = word.upper()
                        num_uppercase += 1

                if num_xxx < MAX_XXX:
                    if random() < MUTATE_CHANCE:
                        new_words.append("XXXXXXX")
                        num_xxx += 1
                new_words.append(word)
            line = " ".join(new_words)
        mutated_lines.append(line)
    return mutated_lines, num_uppercase, num_xxx


def main():
    script_name = sys.argv[0]
    if len(sys.argv) != 2:
        raise ValueError(f"Usage: {script_name} text_file")

    filename = sys.argv[1]
    with open(filename) as f:
        original_lines = f.readlines()

    # Mutation is probabilistic, so an unlucky pass may apply no mutations at
    # all. Retry until we get at least one of each, then write the result.
    for _ in range(MAX_PASSES):
        mutated_lines, num_uppercase, num_xxx = mutate_lines(original_lines)
        if num_uppercase >= 1 and num_xxx >= 1:
            break
    else:
        raise ValueError(f"{filename} couldn't be mutated after {MAX_PASSES} passes!")

    with open(filename, "wt") as f:
        f.writelines(mutated_lines)


if __name__ == "__main__":
    main()
