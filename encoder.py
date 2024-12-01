from collections import Counter
import heapq

#Huffman's code realization

class Encoder:
    def read_input(self, input_file, n=1):
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()

            # Count occurrences of n-length symbols with overlapping chunks
            if n < 1:
                print("Error: 'n' must be at least 1.")
                return None

            self.char_count = Counter(text[i:i + n] for i in range(0, len(text) - n + 1, n))

            for char, count in self.char_count.items():
                print(f"'{char}' : {count}")

            return self.char_count
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")

    def calculate_probabilities(self):
        if not hasattr(self, 'char_count') or not self.char_count:
            print("Error: No character counts available. Please run 'read_input' first.")
            return None

        total_chars = sum(self.char_count.values())
        self.probabilities = {char: count / total_chars for char, count in self.char_count.items()}

        for char, prob in self.probabilities.items():
            print(f"'{char}' : {prob:.4f}")

        return self.probabilities

    def huffman_encoding(self):
        if not hasattr(self, 'probabilities') or not self.probabilities:
            print("Error: No probabilities available. Please run 'calculate_probabilities' first.")
            return None

        # Build a priority queue (min-heap) from the character probabilities
        heap = [[prob, [char, ""]] for char, prob in self.probabilities.items()]
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
        self.huffman_dict = {char: code for char, code in huffman_codes}

        print("Huffman Codes:")
        for char, code in self.huffman_dict.items():
            print(f"'{char}': {code}")

        return self.huffman_dict

    def encode_to_file(self, input_file, output_file, n=1):
        if not hasattr(self, 'huffman_dict') or not self.huffman_dict:
            print("Error: Huffman codes not generated. Please run 'huffman_encoding' first.")
            return

        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()

            with open(output_file, 'w', encoding='utf-8') as output:
                for i in range(0, len(text) - n + 1, n):
                    symbol = text[i:i + n]
                    if symbol in self.huffman_dict:
                        output.write(self.huffman_dict[symbol])
                    else:
                        print(f"Warning: Symbol '{symbol}' not found in Huffman codes.")

            print(f"Encoded data written to '{output_file}'.")
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")
        except KeyError as e:
            print(f"Error: Character sequence '{e.args[0]}' not found in Huffman codes.")
    
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
