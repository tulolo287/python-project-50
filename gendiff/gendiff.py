import argparse
from gendiff.parser import generate_diff


def gendiff():
    parser = argparse.ArgumentParser(
        prog="gendiff",
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")

    args = parser.parse_args()

    if args.first_file and args.second_file:
        diff = generate_diff(args.first_file, args.second_file)
        print(diff)

