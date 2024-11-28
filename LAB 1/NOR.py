def NOR_gate(input1, input2, input3):
    return not (input1 or input2 or input3)

# Test the NOR gate
inputs = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)]
print("Inputs\tNOR")
for inp in inputs:
    a, b, c = inp
    print(f"{inp}\t{NOR_gate(a, b, c)}")
