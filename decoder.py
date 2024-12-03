class Decoder:
    def __init__(self):
        self.huffman_tree = None
        self.n = None

    def read_encoded_file(self, input_file):
        """
        Reads the encoded file sequentially to extract `n`, the Huffman tree, and the encoded data.
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                # Step 1: Read the first 4 bits to extract `n`
                n_binary = file.read(4)
                self.n = int(n_binary, 2) + 2
                print(f"Decoded n: {self.n}")

                # Step 2: Read the Huffman tree progressively
                encoded_tree = self._read_tree(file)
                print(f"Encoded Huffman Tree: {encoded_tree}")

                # Step 3: Decode the Huffman tree
                self.huffman_tree = self.decode_huffman_tree(encoded_tree, self.n)
                print(f"Reconstructed Huffman Tree: {self.huffman_tree}")

                # Step 4: Read the rest of the file as the encoded data
                encoded_data = file.read()
                print(f"Encoded Data: {encoded_data}")

                return encoded_data
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")
            return None

    def _read_tree(self, file):
        """
        Reads the Huffman tree from the file using pre-order traversal, respecting `n` bits per symbol.
        """
        tree = []
        stack = []

        while True:
            bit = file.read(1)
            if not bit:
                raise ValueError("Unexpected end of file while reading the Huffman tree.")

            if bit == '1':  # Leaf node
                # Read the next `n` bits as the symbol
                symbol = file.read(self.n)
                if len(symbol) != self.n:
                    raise ValueError("Incomplete symbol in Huffman tree.")
                tree.append(f"1{symbol}")
                stack.append('1')  # Mark this as a leaf node
            elif bit == '0':  # Internal node
                tree.append('0')
                stack.append('0')  # Mark this as an internal node

            # Pop pairs when a subtree is complete
            while len(stack) >= 3 and stack[-3] == '0' and stack[-2] != '0' and stack[-1] != '0':
                stack.pop()
                stack.pop()
                stack.pop()
                stack.append('1')  # Replace the subtree with a single node

            # If the entire tree is reconstructed
            if len(stack) == 1 and stack[0] == '1':
                break

        return "".join(tree)

    def decode_huffman_tree(self, encoded_tree, n):
        """
        Decodes the Huffman tree from its encoded representation, respecting `n` bits per symbol.
        """
        def build_tree(iterator):
            value = next(iterator)
            if value == '0':  # Internal node
                return {'0': build_tree(iterator), '1': build_tree(iterator)}
            elif value == '1':  # Leaf node
                # Extract the next `n` bits as the symbol
                symbol = "".join(next(iterator) for _ in range(n))
                return {'symbol': symbol}

        # Create an iterator for the encoded tree string
        iterator = iter(encoded_tree)
        return build_tree(iterator)

    def decode_data(self, encoded_data):
        """
        Decodes the encoded binary data using the reconstructed Huffman tree.
        """
        decoded_text = []
        node = self.huffman_tree

        for bit in encoded_data:
            if bit == '0':
                node = node.get('0', {})
            elif bit == '1':
                node = node.get('1', {})

            # If a leaf node is reached
            if 'symbol' in node:
                decoded_text.append(node['symbol'])
                node = self.huffman_tree  # Reset to the root for the next symbol

        return "".join(decoded_text)

    def decode_file(self, input_file):
        """
        Decodes the contents of the input file and returns the decoded text as UTF-8.
        """
        encoded_data = self.read_encoded_file(input_file)
        if not encoded_data:
            return None
    
        # Decode binary Huffman-encoded data
        decoded_text = self.decode_data(encoded_data)
    
        # Convert binary to UTF-8
        utf_decoded = "".join(
            chr(int(decoded_text[i:i + 8], 2)) for i in range(0, len(decoded_text), 8)
        )
    
        return utf_decoded
