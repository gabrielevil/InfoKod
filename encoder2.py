from collections import Counter
import heapq


class Encoder:
    def read_input(self, input_file, n=8):
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()

            # Step 1: Print the original text
            print("Original Text:")
            print(text)

            # Step 2: Convert the text to binary and print it
            binary_representation = "".join(format(ord(char), '08b') for char in text)
            print("\nBinary Representation:")
            print(binary_representation)

            # Step 3: Split the binary representation into chunks of 'n' bits
            self.binary_chunks = [
                binary_representation[i:i + n]
                for i in range(0, len(binary_representation), n)
            ]

            # Step 4: Retain the tail (leftover bits that don't fit into 'n' bits)
            self.tail = binary_representation[len(binary_representation) - (len(binary_representation) % n):]
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
        if not hasattr(self, 'char_count') or not self.char_count:
            print("Error: No character counts available. Please run 'read_input' first.")
            return None

        total_chunks = sum(self.char_count.values())
        self.probabilities = {chunk: count / total_chunks for chunk, count in self.char_count.items()}

        print("\nChunk Probabilities:")
        for chunk, prob in self.probabilities.items():
            print(f"'{chunk}' : {prob:.4f}")

        return self.probabilities

    def huffman_encoding(self):
        if not hasattr(self, 'probabilities') or not self.probabilities:
            print("Error: No probabilities available. Please run 'calculate_probabilities' first.")
            return None

        # Build a priority queue (min-heap) from the probabilities
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

        # Extract the Huffman codes
        huffman_codes = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[1]), p))
        self.huffman_dict = {chunk: code for chunk, code in huffman_codes}

        print("\nHuffman Codes:")
        for chunk, code in self.huffman_dict.items():
            print(f"'{chunk}': {code}")

        return self.huffman_dict

    def encode_huffman_tree(self):
        """
        Encodes the Huffman tree into a compact binary representation using pre-order traversal.

        Returns:
            str: Encoded representation of the Huffman tree.
        """
        def build_tree(huffman_dict):
            root = {}
            for symbol, code in self.huffman_dict.items():
                current_node = root
                for bit in code:
                    if bit == '0':
                        current_node = current_node.setdefault('0', {})
                    else:
                        current_node = current_node.setdefault('1', {})
                current_node['symbol'] = symbol  # Store the symbol at the leaf
            return root

        def traverse(node):
            if 'symbol' in node:  # It's a leaf node
                return f"1{node['symbol']}"  # 1 followed by the symbol
            # Internal node: Traverse left and right
            left = traverse(node.get('0', {})) if '0' in node else ''
            right = traverse(node.get('1', {})) if '1' in node else ''
            return f"0{left}{right}"

        # Build the Huffman tree from the dictionary
        huffman_tree = build_tree(self.huffman_dict)

        # Encode the tree
        return traverse(huffman_tree)

    def encode_to_file(self, input_file, output_file, n):
        if not hasattr(self, 'huffman_dict') or not self.huffman_dict:
            print("Error: Huffman codes not generated. Please run 'huffman_encoding' first.")
            return
    
        try:
            # Encode binary chunks using Huffman codes
            encoded_binary = "".join(self.huffman_dict[chunk] for chunk in self.binary_chunks if chunk in self.huffman_dict)
    
            # Append the tail (if any) to the encoded data
            if self.tail:
                print(f"\nAdding leftover tail to the encoded output: {self.tail}")
                encoded_binary += self.tail  # You can also pad the tail if necessary
    
            # Convert (n - 2) to a 4-bit binary representation
            n_binary = format(n - 2, '04b')  # Ensure n - 2 fits into 4 bits
            print(f"n - 2 in binary: {n_binary}")
    
            # Encode the Huffman tree
            encoded_tree = self.encode_huffman_tree()
            print(f"\nEncoded Huffman Tree: {encoded_tree}")
    
            # Combine n_binary, the encoded tree, and the encoded data
            final_output = n_binary + encoded_tree + encoded_binary
    
            # Write the final encoded data to the output file
            with open(output_file, 'w', encoding='utf-8') as output:
                output.write(final_output)
    
            print(f"\nEncoded data with n (4-bit prefix) and Huffman tree written to '{output_file}'.")
        except KeyError as e:
            print(f"Error: Chunk '{e.args[0]}' not found in Huffman codes.")
        except Exception as e:
            print(f"Error: {str(e)}")


    def is_prefix_free(self):
        if not hasattr(self, 'huffman_dict') or not self.huffman_dict:
            print("Error: Huffman codes not generated. Please run 'huffman_encoding' first.")
            return False

        codes = list(self.huffman_dict.values())
        for i, code1 in enumerate(codes):
            for j, code2 in enumerate(codes):
                if i != j and code2.startswith(code1):
                    return False
        return True
