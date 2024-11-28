def NAND_gate(input1, input2, input3):
    return not (input1 and input2 and input3)

# Test the NAND gate
inputs = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)]
print("Inputs\tNAND")
for inp in inputs:
    a, b, c = inp
    print(f"{inp}\t{NAND_gate(a, b, c)}")
