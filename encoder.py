from collections import Counter
import heapq

class Encoder:
    def read_input(self, input_file, n=8):
        try:
            with open(input_file, 'rb') as file:
                binary_data = file.read()

            # Convert binary data to a binary string
            binary_representation = ''.join(f'{byte:08b}' for byte in binary_data)

            print("\nBinary Representation:")
            print(binary_representation)

            # Handle leftover bits
            remainder = len(binary_representation) % n
            self.tail = binary_representation[-remainder:] if remainder else ""

            # Split the binary representation into chunks of 'n' bits
            self.binary_chunks = [
                binary_representation[i:i + n]
                for i in range(0, len(binary_representation)-remainder, n)
            ]

            if self.tail:
                print(f"\nTail (leftover bits): {self.tail}")

            print(f"\nBinary Chunks ({n} bits each):")
            print(self.binary_chunks)

            # Count occurrences of the chunks
            self.char_count = Counter(self.binary_chunks)
            print("\nChunk Frequencies:")
            for chunk, count in self.char_count.items():
                print(f"'{chunk}' : {count}")

            return self.char_count
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")

    def calculate_probabilities(self):
        total_chunks = sum(self.char_count.values())
        self.probabilities = {chunk: count / total_chunks for chunk, count in self.char_count.items()}

        print("\nChunk Probabilities:")
        for chunk, prob in self.probabilities.items():
            print(f"'{chunk}' : {prob:.4f}")

        return self.probabilities

    def huffman_encoding(self):
        heap = [[prob, [chunk, ""]] for chunk, prob in self.probabilities.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        huffman_codes = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[1]), p))
        self.huffman_dict = {chunk: code for chunk, code in huffman_codes}

        print("\nHuffman Codes:")
        for chunk, code in self.huffman_dict.items():
            print(f"'{chunk}': {code}")

        return self.huffman_dict

    def encode_huffman_tree(self):
        def build_tree(huffman_dict):
            root = {}
            for symbol, code in huffman_dict.items():
                current_node = root
                for bit in code:
                    current_node = current_node.setdefault(bit, {})
                current_node['symbol'] = symbol
            return root

        def traverse(node):
            if 'symbol' in node:
                return f"1{node['symbol']}"
            left = traverse(node.get('0', {})) if '0' in node else ''
            right = traverse(node.get('1', {})) if '1' in node else ''
            return f"0{left}{right}"

        huffman_tree = build_tree(self.huffman_dict)
        encoded_tree = traverse(huffman_tree)

        print("\nEncoded Huffman Tree:")
        print(encoded_tree)

        return encoded_tree

    def encode_to_file(self, output_file, n):
        try:
            # Prepare header
            n_binary = format(n - 1, '04b')
            tail_length_binary = format(len(self.tail), '04b')

            # Encode Huffman tree
            encoded_tree = self.encode_huffman_tree()

            # Encode text using Huffman codes
            encoded_text = ''.join(self.huffman_dict[chunk] for chunk in self.binary_chunks)
            if self.tail:
                print(f"\nAdding leftover tail to the encoded output: {self.tail}")
                encoded_text += self.tail

            # Combine all segments
            final_output = '1' + n_binary + tail_length_binary + self.tail + encoded_tree + encoded_text

            # Write to file
            with open(output_file, 'wb') as output:
                # Convert binary string to bytes and write
                output.write(int(final_output, 2).to_bytes((len(final_output) + 7) // 8, byteorder='big'))

            print(f"\nEncoded data written to '{output_file}'.")
        except KeyError as e:
            print(f"Error: Missing chunk '{e.args[0]}' in Huffman codes.")
        except Exception as e:
            print(f"Error: {str(e)}")
