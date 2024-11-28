def AND_gate(input1, input2, input3):
    return input1 and input2 and input3

# Test the AND gate
inputs = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)]
print("Inputs\tAND")
for inp in inputs:
    a, b, c = inp
    print(f"{inp}\t{AND_gate(a, b, c)}")
