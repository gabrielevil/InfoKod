class Decoder:
    def __init__(self):
        self.huffman_tree = None
        self.n = None
        self.tail_length = 0

    def read_encoded_file(self, input_file):
        try:
            with open(input_file, 'rb') as file:
                # Read file and convert to binary string
                binary_data = file.read()
                binary_string = ''.join(f'{byte:08b}' for byte in binary_data)

            # Ignore all leading zeros and the first '1'
            start_index = binary_string.find('1') + 1
            if start_index == 0:
                raise ValueError("Invalid file format: Missing start bit '1'.")

            # Remove trash bits
            binary_string = binary_string[start_index:]

            # Extract header info
            n_binary = binary_string[:4]
            self.n = int(n_binary, 2) + 1
            print(f"Decoded n: {self.n}")

            tail_length_binary = binary_string[4:8]
            self.tail_length = int(tail_length_binary, 2)
            # print(f"Tail Length: {self.tail_length}")

            # Extract tail
            self.tail = binary_string[8:8 + self.tail_length]
            # print(f"Extracted Tail: {self.tail}")

            # Remaining string after header and tail
            remaining_string = binary_string[8 + self.tail_length:]

            # Extract Huffman Tree
            tree_end_index, encoded_tree = self._extract_huffman_tree(remaining_string)
            # print(f"Encoded Huffman Tree: {encoded_tree}")

            # Rebuild Huffman Tree
            self.huffman_tree = self.decode_huffman_tree(encoded_tree, self.n)
            # print(f"Reconstructed Huffman Tree: {self.huffman_tree}")

            # Extract Encoded Text
            encoded_data = remaining_string[tree_end_index:]
            # print(f"Encoded Data: {encoded_data}")

            return encoded_data
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def _extract_huffman_tree(self, binary_string):
        """
        Extracts the Huffman tree from the binary string using pre-order traversal.
        """
        iterator = iter(binary_string)
        tree = []
        stack = []

        while True:
            try:
                bit = next(iterator)
            except StopIteration:
                raise ValueError("Unexpected end of file while reading the Huffman tree.")

            if bit == '1':  # Leaf node
                symbol = ''.join(next(iterator) for _ in range(self.n))
                tree.append(f"1{symbol}")
                stack.append('1')
            elif bit == '0':  # Internal node
                tree.append('0')
                stack.append('0')

            while len(stack) >= 3 and stack[-3:] == ['0', '1', '1']:
                stack.pop()
                stack.pop()
                stack.pop()
                stack.append('1')  # Collapse subtree

            if len(stack) == 1 and stack[0] == '1':
                break

        encoded_tree = ''.join(tree)
        tree_end_index = len(encoded_tree)
        return tree_end_index, encoded_tree

    def decode_huffman_tree(self, encoded_tree, n):
        """
        Decodes the Huffman tree from its binary representation.
        """
        def build_tree(iterator):
            value = next(iterator)
            if value == '0':  # Internal node
                return {'0': build_tree(iterator), '1': build_tree(iterator)}
            elif value == '1':  # Leaf node
                symbol = ''.join(next(iterator) for _ in range(n))
                return {'symbol': symbol}

        iterator = iter(encoded_tree)
        return build_tree(iterator)

    def decode_data(self, encoded_data):
        """
        Decodes the encoded binary data using the reconstructed Huffman tree.
        """
        decoded_text = []
        node = self.huffman_tree

        for bit in encoded_data:
            node = node.get(bit, {})
            if 'symbol' in node:
                decoded_text.append(node['symbol'])
                node = self.huffman_tree  # Reset to the root for the next symbol

        return ''.join(decoded_text)

    def decode_file(self, input_file):
        """
        Decodes the contents of the input file and returns the decoded text.
        """
        encoded_data = self.read_encoded_file(input_file)
        if not encoded_data:
            return None

        # Decode binary Huffman-encoded data
        decoded_text = self.decode_data(encoded_data)

        # print("\nDecoded Value (UTF-8):")
        # print(decoded_text)
        return decoded_text
