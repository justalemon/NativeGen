from argparse import ArgumentParser
from pathlib import Path

URL = "https://github.com/justalemon/NativeGen"


def parse_arguments():
    parser = ArgumentParser(prog="nativegen",
                            description="Native File Generator for GTA V and RDR2",
                            epilog=f"For more information, visit {URL}")
    parser.add_argument("output",
                        help="the output file")
    parser.add_argument("format", choices=["shvdn", "cfxlua"],
                        help="the format of the file")
    parser.add_argument("--natives", choices=["gtav", "rdr2", "fivem"], nargs="+", default=["gtav"],
                        help="the different sets of natives to add")

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    path = Path(arguments.output).absolute()

    print(f"Saving Natives to {path}")
    print(f"Using format {arguments.format} and natives {arguments.natives}")

    return


if __name__ == "__main__":
    main()
