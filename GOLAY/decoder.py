import numpy as np

class GolayDecoder:
    def __init__(self):
        self.check_matrix = np.array([
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ], dtype=int)
        self.generator_matrix = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        ], dtype=int)
        self.A = self.check_matrix[:, :12]

    def syndrome_weight(self, syndrome):
        return np.count_nonzero(syndrome)
    
    def calculate_syndromes(self, x):
        x = np.array(x, dtype=int)
        if x.shape[0] != 24:
            raise ValueError("Input vector x must be exactly 24 bits long.")
        s1 = np.dot(x, self.generator_matrix.T) % 2
        s2 = np.dot(x, self.check_matrix.T) % 2
        return s1, s2

    def decode_word(self, x):
        x = np.array([int(b) for b in x], dtype=int)
        s1, s2 = self.calculate_syndromes(x)
        w_s1 = self.syndrome_weight(s1)
        w_s2 = self.syndrome_weight(s2)

        if w_s1 <= 3 and w_s2 >= 5:
            x = (x - np.concatenate([s1, np.zeros(12, dtype=int)])) % 2
            print(x)
        elif w_s2 <= 3 and w_s1 >= 5:
            x = (x - np.concatenate([np.zeros(12, dtype=int), s2])) % 2
            print(x)

        if w_s2 >= 5 and w_s1 >= 5:
            ws_4 = 0
            for i in range(12):
                ei = np.zeros(12, dtype=int)
                ei[i] = 1
                s1i = (s1 + np.dot(ei, self.A)) % 2
                if self.syndrome_weight(s1i) >= 4:
                    ws_4 += 1
            for i in range(12):
                ei = np.zeros(12, dtype=int)
                ei[i] = 1
                s1i = (s1 + np.dot(ei, self.A)) % 2
                if self.syndrome_weight(s1i) <= 2 and ws_4 == 11:
                    x = (x - np.concatenate([np.zeros(12, dtype=int), ei])) % 2
                    x = self.decode_word(x)
            ws_4 = 0
            for i in range(12):       
                ei = np.zeros(12, dtype=int)
                ei[i] = 1
                s2i = (s2 + np.dot(ei, self.A)) % 2
                if self.syndrome_weight(s2i) >= 4:
                    ws_4 += 1
            for i in range(12):       
                ei = np.zeros(12, dtype=int)
                ei[i] = 1
                s2i = (s2 + np.dot(ei, self.A)) % 2
                if self.syndrome_weight(s2i) <= 2 and ws_4 == 11:
                    x = (x - np.concatenate([np.zeros(12, dtype=int), ei])) % 2
                    x = self.decode_word(x)

        return ''.join(map(str, x[:12]))
    
    def decode(self, data):
        # Ensure the length of the data is a multiple of 24
        if len(data) % 24 != 0:
            raise ValueError("Input length must be a multiple of 24 bits.")
        # print(data)
        # Split the data into 24-bit chunks
        chunks = [data[i:i+24] for i in range(0, len(data), 24)]
        # print(chunks)
        decoded_messages = []
        for chunk in chunks:
            # Decode the 24-bit codeword
            corrected_codeword = self.decode_word(chunk)
            # Extract the first 12 bits as the original message
            decoded_messages.append(corrected_codeword[:12])
        
        # Concatenate all decoded 12-bit messages
        return ''.join(decoded_messages)