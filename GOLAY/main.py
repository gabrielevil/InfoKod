import sys
from encoder import GolayEncoder
from decoder import GolayDecoder

def main():
    encoder = GolayEncoder()
    decoder = GolayDecoder()

    print("Enter a binary sequence (only 0 and 1):")
    try:
        input_data = input().strip()
        if not all(bit in '01' for bit in input_data):
            print("Invalid input. Please provide a sequence consisting only of 0s and 1s.")
            sys.exit(1)
        
        # Encode the input data
        encoded_chunks, tail = encoder.encode_long_sequence(input_data)
        encoded_data = ''.join(encoded_chunks) + tail
        print("Encoded:")
        print(encoded_data)

        # Ask for bit positions to change
        print("Encoded data lenght is", len(encoded_data))
        print("Enter the indexes of bits to change (comma-separated, 0-based):")
        indexes_to_change = input().strip()
        try:
            indexes = list(map(int, indexes_to_change.split(',')))
        except ValueError:
            print("Invalid indexes. Please enter numbers separated by commas.")
            sys.exit(1)

        # Introduce errors based on user input
        wrong_data = list(encoded_data)
        for idx in indexes:
            if 0 <= idx < len(wrong_data):
                wrong_data[idx] = '1' if wrong_data[idx] == '0' else '0'
            else:
                print(f"Index {idx} is out of range.")
                sys.exit(1)

        wrong_data = ''.join(wrong_data)
        print("Corrupted Data:")
        print(wrong_data)
        
        # Count mistakes
        mistakes = sum(1 for a, b in zip(encoded_data, wrong_data) if a != b)
        print(f"Number of mistakes: {mistakes}")
        
        #dekoduoti sugadinta - grazina istaisyta ir parodo istaisyma (ar tas pats originalus ar jau kitas?)

        decoded_data = decoder.decode(wrong_data)
        print("Decoded corrupted data:")
        print(decoded_data)
        print(input_data)
        

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
