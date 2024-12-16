import numpy as np

class GolayDecoder:
    def __init__(self):
        self.check_matrix = np.array([
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ], dtype=int)
        self.generator_matrix = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],#
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],#
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],#
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],#
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],#
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],#
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],#
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],#
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],#
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],#
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],#
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],#
        ], dtype=int)
        self.A = self.check_matrix[:, :12]

    def syndrome_weight(self, syndrome):
        return np.count_nonzero(syndrome)

    def calculate_syndromes(self, x):
        x = np.array(x, dtype=int)
        s1 = np.dot(x, self.generator_matrix.T) % 2
        s2 = np.dot(x, self.check_matrix.T) % 2
        return s1, s2

    def decode_word(self, x):
        print("Decoding..")
        x = np.array([int(b) for b in x], dtype=int)
        s1, s2 = self.calculate_syndromes(x)
        # print(f"s1: {s1}")
        # print(f"s2: {s2}")
        w_s1 = self.syndrome_weight(s1)
        w_s2 = self.syndrome_weight(s2)
        # print(f"w_s1: {w_s1}")
        # print(f"w_s2: {w_s2}")

        if w_s1 <= 3 and w_s2 >= 5:
            print(f"Flipping bits based on syndrome s1: {np.where(s1 == 1)[0]}")
            x = (x - np.concatenate([s1, np.zeros(12, dtype=int)])) % 2
        elif w_s2 <= 3 and w_s1 >= 5:
            print(f"Flipping bits based on syndrome s2: {np.where(s2 == 1)[0] + 12}")
            x = (x - np.concatenate([np.zeros(12, dtype=int), s2])) % 2
        elif w_s2 >= 5 and w_s1 >= 5:
            count_w_s1 = 0
            count_w_s2 = 0
            for j in range(12):
                ej = np.zeros(12, dtype=int)
                ej[j] = 1
                ejA = np.dot(ej, self.A) % 2
                ejA = np.array(ejA, dtype=int)
                s1j = (s1 + ejA) % 2
                s2j = (s2 + ejA) % 2
                # print(self.syndrome_weight(s1j))
                # print(self.syndrome_weight(s2j))
                if self.syndrome_weight(s1j) >= 4:
                    count_w_s1 += 1
                if self.syndrome_weight(s2j) >= 4:
                    count_w_s2 += 1

            for i in range(12):
                ei = np.zeros(12, dtype=int)
                ei[i] = 1
                eiA = np.dot(ei, self.A) % 2
                eiA = np.array(eiA, dtype=int)
                s1 = np.array(s1, dtype=int)
                s2 = np.array(s2, dtype=int)
                s1i = (s1 + eiA) % 2
                # print(f"s1i: {s1i}")
                s2i = (s2 + eiA) % 2
                # print(f"s2i: {s2i}")
                if self.syndrome_weight(s1i) <= 2 and count_w_s1 == 11:
                    print(f"Flipping bit {12 + i} due to s1 correction")
                    x = (x - np.concatenate([np.zeros(12, dtype=int), ei])) % 2
                    x = self.decode_word(x)
                    break
                elif self.syndrome_weight(s2i) <= 2 and count_w_s2 == 11:
                    print(f"Flipping bit {i} due to s2 correction")
                    x = (x - np.concatenate([ei, np.zeros(12, dtype=int)])) % 2
                    x = self.decode_word(x)
                    break
        else:
            print("Cannot decode word")
            

        return ''.join(map(str, x[:12]))

    def decode(self, data):
        if len(data) == 0:
            return ""  # Return empty if no input
        
        leftover_bits = data[len(data) - len(data) % 24:]  # Extract leftover bits if present
        chunks = [data[i:i+24] for i in range(0, len(data) - len(leftover_bits), 24)]
        decoded_messages = [self.decode_word(chunk) for chunk in chunks]

        # Properly concatenate decoded messages and leftover bits
        if leftover_bits:
            decoded_messages.append(leftover_bits)
        
        return ''.join(decoded_messages)
