from sage.all import load
import os
import argparse

def check_file_exists(directory, base, exts, expected_line_count):
    """Check if files exist based on base name and extensions in a directory."""
    missing_or_incorrect = []
    for ext in exts:
        filename = os.path.join(directory, base + ext)
        if not os.path.isfile(filename):
            missing_or_incorrect.append(filename)
        elif ext == ".csv":  # Checking the line count if it's a table file
            actual_line_count = count_lines_in_table(filename)
            if actual_line_count != expected_line_count:
                print(f"Table file {filename} exists but has wrong line count.")
                print(f"Deleting file: {filename}")
                os.remove(filename)
                missing_or_incorrect.append(f"{filename} (incorrect line count: {actual_line_count})")
    return missing_or_incorrect

def count_lines_in_file(filename):
    if filename.endswith(".sobj"):
        data = load(filename)
        return len(data)

def count_lines_in_table(filename):
    with open(filename, 'r') as f:
        return sum(1 for line in f)

def format_decimal(n):
    """Format the number to have two decimal points."""
    return "{:.2f}".format(n)

def main():
    all_files_correct = True
    MATRICES_DIR = "MATRICES"
    subbed_mat_types = [".pickle", ".powers.pickle", ".precomputed_paths.pickle"]
    table_types = [".csv"]

    path_descriptions = [d for d in os.listdir(MATRICES_DIR) if os.path.isdir(os.path.join(MATRICES_DIR, d))]

    tallies = {path_desc: 0 for path_desc in path_descriptions}

    for path_desc in path_descriptions:
        expected_line_count_path = os.path.join(MATRICES_DIR, path_desc, "all_path_combinations.sobj")
        print(path_desc)
        if os.path.exists(expected_line_count_path):
            expected_line_count = count_lines_in_file(expected_line_count_path) + 1
        else:
            print(f"Warning: Missing all_path_combinations.sobj file for {path_desc}")
            expected_line_count = None

        for i in range(101):
            print(i)
            for j in range(101 - i):
                x_val = i / 100
                y_val = j / 100

                x_str = format_decimal(x_val)
                y_str = format_decimal(y_val)

                subbed_mat_base = f"{path_desc}/subbed_mat_u{x_str}_d{y_str}"
                table_base = f"{path_desc}/table_u{x_str}_d{y_str}"

                missing_or_incorrect_subbed = check_file_exists(MATRICES_DIR, subbed_mat_base, subbed_mat_types, expected_line_count)
                missing_or_incorrect_table = check_file_exists(MATRICES_DIR, table_base, table_types, expected_line_count)

                missing_or_incorrect = missing_or_incorrect_subbed + missing_or_incorrect_table

                tallies[path_desc] += len(missing_or_incorrect_table)

                if missing_or_incorrect:
                    all_files_correct = False
                    print(f"Missing or incorrect files for x={x_str}, y={y_str}, path={path_desc}:\n" + "\n".join(missing_or_incorrect))

    # Print out the tallies
    for path_desc, count in tallies.items():
        print(f"Total missing or incorrect table files for path={path_desc}: {count}")

    if all_files_correct:
        print(f"All files exist and are correct for every combination of x and y for all path descriptions.")


if __name__ == "__main__":
    main()

