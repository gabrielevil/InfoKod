from collections import Counter

#Huffman's code realization
class Encoder:
    def read_input(self, input_file):
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()

            self.char_count = Counter(text)

            for char, count in self.char_count.items():
                print(f"'{char}' : {count}")

            return self.char_count
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")
    
