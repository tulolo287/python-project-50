import argparse

from .parser import generate_diff


def main():
    parser = argparse.ArgumentParser(
        prog="gendiff",
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")

    args = parser.parse_args()

    if args.first_file and args.second_file:
        formatter = args.format if args.format else "stylish"
        diff = generate_diff(args.first_file, args.second_file, formatter)
        print(diff)


if __name__ == "__main__":
    main()
