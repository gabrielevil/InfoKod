from encoder import Encoder

encoder = Encoder()
input_file = 'input.txt'
output_path = 'output.txt'
character_counts = encoder.read_input(input_file)
print("probabilities")
if character_counts:
    probabilities = encoder.calculate_probabilities()
    huffman_codes = encoder.huffman_encoding()
    encoder.encode_to_file(input_file, output_path)