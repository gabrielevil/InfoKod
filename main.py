from encoder2 import Encoder
from decoder import Decoder
import argparse


def main():
    parser = argparse.ArgumentParser(description="Process program call arguments.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input file path")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file path")
    parser.add_argument('-n', '--number_of_encoded_symbols', type=int, default=8, help="Amount of symbols Huffman's code encodes (default: 8)")
    args = parser.parse_args()

    # Step 1: Encoding
    encoder = Encoder()
    input_file = args.input
    output_file = args.output
    n = args.number_of_encoded_symbols

    print("Encoding...")
    encoder.read_input(input_file, n)
    encoder.calculate_probabilities()
    encoder.huffman_encoding()
    encoder.encode_to_file(input_file, output_file, n)

    decoder = Decoder()
    print("Decoding...")

    # Read and decode the output file
    decoded_binary = decoder.read_encoded_file(output_file)  # Read and decode the binary data
    decoded_result = decoder.decode_data(decoded_binary)  # Decode the binary Huffman-encoded data

    # Convert decoded binary to UTF-8
    utf_decoded = "".join(
        chr(int(decoded_result[i:i + 8], 2)) for i in range(0, len(decoded_result), 8)
    )

    # Print decoded value to the terminal
    print("\nDecoded Value (UTF-8):")
    print(utf_decoded)


if __name__ == "__main__":
    main()
