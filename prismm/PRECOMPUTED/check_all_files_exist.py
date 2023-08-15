import os
import argparse

def check_file_exists(directory, base, exts):
    """Check if files exist based on base name and extensions in a directory."""
    missing = []
    for ext in exts:
        filename = os.path.join(directory, base + ext)
        if not os.path.isfile(filename):
            missing.append(filename)  # It might be useful to return the full missing filename.
    return missing

def format_decimal(n):
    """Format the number to have one or two decimal points as necessary."""
    if n % 1 == 0:  # If the number is an integer
        return "{:.1f}".format(n)
    else:
        return "{:.2f}".format(n)
    
def main(path_length):
    all_files_exist = True
    MATRICES_DIR = "MATRICES"
    subbed_mat_types = [".pickle", ".powers.pickle", ".precomputed_paths.pickle"]
    collated_types = [".csv"]

    for i in range(101):
        for j in range(101 - i):
            x_val = i / 100
            y_val = j / 100

            x_str = format_decimal(x_val)
            y_str = format_decimal(y_val)

            subbed_mat_base = f"p{path_length}_v5/subbed_mat_u{x_str}_d{y_str}"
            collated_base = f"p{path_length}_v5/collated_u{x_str}_d{y_str}"

            missing_subbed = check_file_exists(MATRICES_DIR, subbed_mat_base, subbed_mat_types)
            missing_collated = check_file_exists(MATRICES_DIR, collated_base, collated_types)

            missing = missing_subbed + missing_collated

            if missing:
                all_files_exist = False
                print(f"Missing files for x={x_str}, y={y_str}:\n" + "\n".join(missing))

    if all_files_exist:
        print(f"All files exist for every combination of x and y with path length {path_length}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for missing matrix files.')
    parser.add_argument('path_length', type=int, help='The path length for the matrix files.')
    args = parser.parse_args()
    
    main(args.path_length)

