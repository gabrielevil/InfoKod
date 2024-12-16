from encoder import Encoder
from decoder import Decoder
import argparse


def main():
    parser = argparse.ArgumentParser(description="Huffman Encoding and Decoding")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output encoded file path")
    parser.add_argument('-d', '--decoded', type=str, required=True, help="Output decoded file path")
    args = parser.parse_args()

    output_file = args.output
    decoded_file = args.decoded

    # Step 2: Decoding
    print("Decoding...")
    decoder = Decoder()
    decoded_result = decoder.decode_file(output_file)

    if decoded_result:
        # print("\nDecoded Result:")
        # print(decoded_result)

        # Write decoded content to a file
        with open(decoded_file, 'wb') as file:
            file.write(bytes(int(decoded_result[i:i + 8], 2) for i in range(0, len(decoded_result), 8)))

        print(f"\nDecoded content written to: {decoded_file}")
    else:
        print("\nDecoding failed. Please check the file format.")


if __name__ == "__main__":
    main()
