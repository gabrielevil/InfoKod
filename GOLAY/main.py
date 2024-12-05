import sys
from encoder import GolayEncoder

def main():
    encoder = GolayEncoder()
    
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
        
        # Input the corrupted binary sequence
        print("Write binary sequence (with mistakes):")
        wrong_data = input().strip()
        if len(wrong_data) != len(encoded_data):
            print("Invalid input. The length of the wrong data must match the encoded data length.")
            sys.exit(1)
        
        # Count mistakes
        mistakes = sum(1 for a, b in zip(encoded_data, wrong_data) if a != b)
        print(f"Number of mistakes: {mistakes}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
