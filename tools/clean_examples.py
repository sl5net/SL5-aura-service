import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Map tagger clean_example")
    parser.add_argument("filter_path", nargs="?", help="filename to clean examples from")
    args = parser.parse_args()

    if not args.filter_path:
        print("Error: No file path provided.")
        parser.print_help()
        sys.exit(1)

    filepath = args.filter_path
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = [line for line in lines if not line.lstrip().startswith('# EXAMPLE:')]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    print(f"Removed # EXAMPLE: tags from {filepath}")

if __name__ == '__main__':
    main()
