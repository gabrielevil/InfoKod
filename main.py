from encoder import Encoder

encoder = Encoder()
file_path = 'input.txt'
character_counts = encoder.read_input(file_path)
print("probabilities")
if character_counts:
    probabilities = encoder.calculate_probabilities()
    huffman_codes = encoder.huffman_encoding(4)