import sys
from collections import defaultdict

def read_genome():
    """Reads the genome from standard input and returns it as a string."""
    genome = sys.stdin.read().strip()
    return genome

def compute_k_grams(genome, k):
    """Computes the frequency of k-grams in the genome."""
    k_gram_counts = defaultdict(int)
    total_k_grams = 0

    # Iterate through the genome to count k-grams
    for i in range(len(genome) - k + 1):
        k_gram = genome[i:i + k]
        k_gram_counts[k_gram] += 1
        total_k_grams += 1

    return k_gram_counts, total_k_grams

def compute_frequencies(k_gram_counts, total_k_grams):
    """Computes the frequency percentages of k-grams."""
    frequencies = {}
    for k_gram, count in k_gram_counts.items():
        frequency = (count / total_k_grams) * 100
        frequencies[k_gram] = frequency
    return frequencies

def get_top_k_grams(frequencies, top_n=10):
    """Returns the top N k-grams sorted by frequency."""
    sorted_k_grams = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    return sorted_k_grams[:top_n]

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 <your_file_name>.py <k>")
        sys.exit(1)

    k = int(sys.argv[1])
    genome = read_genome()
    
    k_gram_counts, total_k_grams = compute_k_grams(genome, k)
    frequencies = compute_frequencies(k_gram_counts, total_k_grams)
    top_k_grams = get_top_k_grams(frequencies)

    # Output the results
    for k_gram, frequency in top_k_grams:
        print(f"{k_gram} with frequency {frequency:.02f} %")

if __name__ == "__main__":
    main()
