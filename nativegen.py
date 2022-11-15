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
LUA_EQUIVALENTS = {
    "int": "number",
    "const char*": "string",
    "Any*": "any",
    "Hash": "number",
    "float": "number",
    "Ped": "number",
    "BOOL": "boolean",
    "Any": "any",
    "Entity": "number",
    "Vehicle": "number",
    "float*": "number",
    "int*": "int",
    "Object": "any",
    "Cam": "number",
    "Player": "number",
    "BOOL*": "boolean",
    "Vector3": "vector3",
    "Vector3*": "vector3",
    "ScrHandle*": "number",
    "ScrHandle": "number",
    "Entity*": "number",
    "Ped*": "number",
    "Vehicle*": "number",
    "Object*": "number",
    "Hash*": "number",
    "FireId": "number",
    "Blip": "number",
    "Pickup": "number",
    "Blip*": "number",
    "Interior": "number",
    "char*": "string",  # not sure
    "func": "function",
    "long": "number",
    "bool": "boolean",
    "object": "any"
}
# From Lua Manual: 2.1 - Lexical Conventions
LUA_KEYWORDS = [
    "and",
    "break",
    "do",
    "else",
    "elseif",
    "end",
    "false",
    "for",
    "function",
    "if",
    "in",
    "local",
    "nil",
    "not",
    "or",
    "repeat",
    "return",
    "then",
    "true",
    "until",
    "while"
]


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
        comment = data.get("comment", None)

        if format == "shvdn" or format == "cfxmono":
            if comment is not None:
                file.write(f"        /// <summary>\n")
                for line in comment.splitlines():
                    file.write(f"        /// {line}\n")
                file.write(f"        /// </summary>\n")

            file.write(f"        {name} = {nhash},\n")
        elif format == "cfxlua":
            parameter_names = []

            if comment is not None:
                for line in comment.splitlines():
                    file.write(f"--- {line}\n")

            for parameter in data["params"]:
                param_name = parameter["name"]
                param_desc = parameter.get("description", "")
                param_type = LUA_EQUIVALENTS.get(parameter["type"], None) or parameter["type"]

                if param_name in LUA_KEYWORDS:
                    param_name = f"_{param_name}"

                if param_name in parameter_names:
                    param_name = f"{param_name}_{len(parameter_names)}"

                file.write(f"--- @param {param_name} {param_type} {param_desc}\n")

                parameter_names.append(param_name)

            name = format_lua_name(name)
            parameters = ", ".join(parameter_names)

            file.write(f"function {name}({parameters}) end\n\n")


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
