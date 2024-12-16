from encoder import Encoder
from decoder import Decoder
import argparse


def main():
    parser = argparse.ArgumentParser(description="Huffman Encoding and Decoding")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input file path")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output encoded file path")
    parser.add_argument('-n', '--number_of_encoded_symbols', type=int, default=8, help="Number of bits per symbol (default: 8)")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    n = args.number_of_encoded_symbols

    # Step 1: Encoding
    print("Encoding...")
    encoder = Encoder()
    encoder.read_input(input_file, n)
    encoder.calculate_probabilities()
    encoder.huffman_encoding()
    encoder.encode_to_file(output_file, n)

    print(f"\nFile encoded successfully: {output_file}\n")

if __name__ == "__main__":
    main()
