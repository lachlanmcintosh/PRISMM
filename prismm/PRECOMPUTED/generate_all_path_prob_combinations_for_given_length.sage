import argparse

# Create a parser to get the argument from command-line
parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument('number', metavar='N', type=int, help='A number to use in filename')
args = parser.parse_args()

# Load the .sobj file with the given number in the filename
filename = f'MATRICES/p{args.number}_v5/all_path_combinations.sobj'
data = load(filename)

# Generate all combinations of p_up and p_down
combinations = [(p_up/100.0, p_down/100.0) for p_up in range(101) for p_down in range(101) if p_up + p_down <= 100]

# Create a table with these combinations
table = []
for combo in combinations:
    p_up, p_down = combo
    formatted_p_up = "{:.2f}".format(p_up)
    formatted_p_down = "{:.2f}".format(p_down)

    for path in data:
        # Assuming value is derived from path; adjust this part based on your requirements
        table.append((formatted_p_up, formatted_p_down, path))

# Save the table to a new .sobj file with the given number in the filename
output_filename = f'MATRICES/p{args.number}_v5/all_path_prob_combinations.sobj'
save(table, output_filename)

print(f"Table saved to {output_filename}!")

