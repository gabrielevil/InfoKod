import sys
from encoder import GolayEncoder
from decoder import GolayDecoder

def main():
    encoder = GolayEncoder()
    decoder = GolayDecoder()

    print("Enter a binary sequence (only 0 and 1):")
    input_data = input().strip()
    if not all(bit in '01' for bit in input_data):
                print("Invalid input. Please provide a sequence consisting only of 0s and 1s.")
                sys.exit(1)
            
            # Encode the input data
    encoded_chunks, tail = encoder.encode_long_sequence(input_data)
    encoded_data = ''.join(encoded_chunks) + tail
    print("Encoded:")
    print(encoded_data)

            # Decode encoded data
    word_count = len(encoded_data) // 24
    bits = 24 * word_count
    # print(encoded_data[:bits])
    decoded_data = decoder.decode(encoded_data[:bits])
    print("Decoded:")
    print(decoded_data)

if __name__ == "__main__":
    main()