from encoder import Encoder
import argparse

def main():
    parser = argparse.ArgumentParser(description="Process program call arguments.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input file path")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file path")
    parser.add_argument('-n', '--number_of_encoded_symbols', type=int, default=1, help="Amount of symbols Huffman's code encodes(default: 1)")
    args = parser.parse_args()
    
    encoder = Encoder()
    input_file = args.input
    output_path = args.output
    n = args.number_of_encoded_symbols
    character_counts = encoder.read_input(input_file, n) #kol kas teskto "uodegos" (jei tokiu yra) yra nukertamos ir nekoduojamos
    print("probabilities")

    probabilities = encoder.calculate_probabilities()
    huffman_codes = encoder.huffman_encoding() #uzkodavimo algoritmas

    print("Prefix-free check:", encoder.is_prefix_free())
    encoder.encode_to_file(input_file, output_path, n) #input tekstas uzkoduojamas i output faila  

if __name__ == "__main__":
    main()