import string
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TextIO

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
    parser.add_argument("format", choices=["shvdn", "cfxmono", "cfxlua"],
                        help="the format of the file")
    parser.add_argument("--natives", choices=list(NATIVES.keys()), nargs="+", default=["gtav"],
                        help="the different sets of natives to add")

    return parser.parse_args()


def format_lua_name(name: str):
    return string.capwords(name.lower().replace("0x", "N_0x").replace("_", " ")).replace(" ", "")


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


def write_header(file: TextIO, format: str):
    if format == "cfxlua":
        return

    if format == "shvdn":
        file.write("namespace GTA.Native\n")
    elif format == "cfxmono":
        file.write("namespace CitizenFX.Core.Native\n")

    if format == "shvdn" or format == "cfxmono":
        file.write("{\n")
        file.write("    public enum Hash : ulong\n")
        file.write("    {\n")


def write_natives(file: TextIO, format: str, namespace: str, natives: dict):
    if format == "shvdn" or format == "cfxmono":
        file.write(f"        // {namespace}\n")
    elif format == "cfxlua":
        file.write(f"-- {namespace}\n\n")

    for nhash, data in natives.items():
        name = data["name"]

        if format == "shvdn" or format == "cfxmono":
           file.write(f"        {name} = {nhash},\n")
        elif format == "cfxlua":
            name = format_lua_name(name)
            file.write(f"function {name}() end\n\n")


def write_footer(file: TextIO, format: str):
    if format == "cfxlua":
        return

    if format == "shvdn" or format == "cfxmono":
        file.write("    }\n")
        file.write("}\n")


def write_natives_to(path: Path, format: str, all_natives: dict[str, dict]):
    with open(path, "w", encoding="utf-8") as file:
        write_header(file, format)

        for game, namespaces in all_natives.items():
            for namespace, natives in namespaces.items():
                write_natives(file, format, namespace, natives)

        write_footer(file, format)


def main():
    arguments = parse_arguments()

    path = Path(arguments.output).absolute()

    print(f"Saving Natives to {path}")
    print(f"Using format {arguments.format} and natives {arguments.natives}")

    natives = fetch_natives(arguments.natives)
    write_natives_to(path, arguments.format, natives)

    return


if __name__ == "__main__":
    main()
