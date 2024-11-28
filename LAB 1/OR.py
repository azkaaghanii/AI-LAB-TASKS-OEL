def OR_gate(input1, input2, input3):
    return input1 or input2 or input3

# Test the OR gate
inputs = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)]
print("Inputs\tOR")
for inp in inputs:
    a, b, c = inp
    print(f"{inp}\t{OR_gate(a, b, c)}")
