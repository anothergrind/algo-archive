class Solution:
    def decode_patient_reading(self, diagnostic_code: str) -> int:
        # Valid Characters and their values
        # I = 1
        # V = 5
        # X = 10
        # L = 50
        # C = 100
        # D = 500
        # M = 1000

        # steps
        # 1) iterate through the whole string
        #     a) convert the value of the character 
        #     b) check the next value of the characters, to see if its bigger
        #        i) if its bigger, subtract
        #        ii) otherwise add

        current, future = 0, 1
        values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D':500, 'M':1000}
        final = 0
        
        for i in range(len(diagnostic_code) - 1):
            current = diagnostic_code[i]
            future = diagnostic_code[i + 1]
            
            if values[future] > values[current]:
                final = final - values[current]
            else:
                final = final + values[current]

        final = final + values[diagnostic_code[-1]]
        return final