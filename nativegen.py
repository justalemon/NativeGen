from argparse import ArgumentParser

URL = "https://github.com/justalemon/NativeGen"


def parse_arguments():
    parser = ArgumentParser(prog="nativegen",
                            description="Native File Generator for GTA V and RDR2",
                            epilog=f"For more information, visit {URL}")
    parser.add_argument("output",
                        help="The output file")
    parser.add_argument("format", choices=["shvdn", "cfxlua"],
                        help="The format of the file")
    parser.add_argument("-n", "--natives", choices=["gtav", "rdr2", "fivem"],
                        help="The different sets of natives to add")

    return parser.parse_args()


def main():
    arguments = parse_arguments()


if __name__ == "__main__":
    main()
