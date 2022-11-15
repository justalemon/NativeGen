import sys
from argparse import ArgumentParser
from pathlib import Path

import requests

URL = "https://github.com/justalemon/NativeGen"
NATIVES = {
    "gtav": "https://raw.githubusercontent.com/alloc8or/gta5-nativedb-data/master/natives.json",
    "rdr3": "https://raw.githubusercontent.com/alloc8or/rdr3-nativedb-data/master/natives.json",
    "fivem": "https://runtime.fivem.net/doc/natives_cfx.json"
}


def parse_arguments():
    parser = ArgumentParser(prog="nativegen",
                            description="Native File Generator for GTA V and RDR2",
                            epilog=f"For more information, visit {URL}")
    parser.add_argument("output",
                        help="the output file")
    parser.add_argument("format", choices=["shvdn", "cfxlua"],
                        help="the format of the file")
    parser.add_argument("--natives", choices=list(NATIVES.keys()), nargs="+", default=["gtav"],
                        help="the different sets of natives to add")

    return parser.parse_args()


def fetch_natives(natives: list[str]):
    result = {}

    for native in natives:
        url = NATIVES[native]
        response = requests.get(url)

        if not response.ok:
            print(f"Unable to fetch {url}", file=sys.stderr)
            sys.exit(3)

        data = response.json()
        result[native] = data

    return result


def main():
    arguments = parse_arguments()

    path = Path(arguments.output).absolute()

    print(f"Saving Natives to {path}")
    print(f"Using format {arguments.format} and natives {arguments.natives}")

    natives = fetch_natives(arguments.natives)

    return


if __name__ == "__main__":
    main()
