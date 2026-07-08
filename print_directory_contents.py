#!/usr/bin/env python3
import os
from sys import argv


def print_file(file_path: str, recursive_left=0, prefix=''):
    if not os.path.exists(file_path):
        return None

    if not os.path.isfile(file_path):
        if recursive_left != 0:
            if recursive_left > 0:
                print_directory(file_path, recursive_left - 1, f"{prefix}{os.path.basename(file_path)}/")
            else:
                print_directory(file_path, -1, f"{prefix}{os.path.basename(file_path)}/")

        return None

    print(f"FILE: \"{prefix}{os.path.basename(file_path)}\"\n{separator_open}")

    if not is_text_file(file_path):
        print("<Binary file, can't read>")
    else:
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                print(file.read().strip())
        except FileNotFoundError:
            print("File not found")
        except PermissionError:
            print("No permission to read file")
        except OSError as e:
            print(f"Other error while opening file: {e}")
    print(f'{separator_close}\n')
    return None


def print_directory(directory_path: str, recursive_left=0, prefix=''):
    list_directory = os.listdir(directory_path)

    for file_name in sorted(list_directory):
        print_file(f"{directory_path}{'/' if directory_path[-1] != '/' else ''}{file_name}", recursive_left=recursive_left, prefix=prefix)


def is_text_file(file_path, sample_size=1024):
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(sample_size)

            raw_data.decode('utf-8')

            return True
    except UnicodeDecodeError:
        return False
    except (FileNotFoundError, PermissionError, OSError):
        return False

def print_help(error=False):
    print("Usage: python print_directory_contents.py <DIRECTORY_PATH> -r [N] -t -so SEP -sc SEP")
    print("Flags: -r  --recursive [N]      \tRecursively print subdirectories (N = depth, no value = infinite)")
    print("       -t  --tree               \tDisplay directory tree")
    print("       -s  --separator SEP      \tSets open and close separators for content of file")
    print("       -so --separator-open SEP \tSets open separator for content of file (Has priority over -s)")
    print("       -sc --separator-close SEP\tSets close separator for content of file (Has priority over -s)")
    exit(int(error))

separator_open = ''
separator_close = ''

if __name__ == "__main__":
    if len(argv) < 2:
        print_help()

    path = ''
    recursive = 0
    print_tree = False
    separator = '```'

    arg_index = 1
    while arg_index < len(argv):
        arg = argv[arg_index]
        if arg == '-t' or arg == '--tree':
            print_tree = True
        elif arg == '-r' or arg == '--recursive':
            arg_index += 1

            if len(argv) <= arg_index:
                recursive = -1
                break

            arg = argv[arg_index]
            if not arg.isnumeric():
                recursive = -1
                continue

            recursive = int(argv[arg_index])
        elif arg == '-s' or arg == '--separator':
            arg_index += 1

            if len(argv) <= arg_index:
                print_help(error=True)
                break

            arg = argv[arg_index]
            separator = arg
        elif arg == '-so' or arg == '--separator-open':
            arg_index += 1

            if len(argv) <= arg_index:
                print_help(error=True)
                break

            arg = argv[arg_index]
            separator_open = arg
        elif arg == '-sc' or arg == '--separator-close':
            arg_index += 1

            if len(argv) <= arg_index:
                print_help(error=True)
                break

            arg = argv[arg_index]
            separator_close = arg
        elif arg[0] == '-':
            print_help()
        elif not path:
            path = arg
        else:
            print(f"Warning: ignored extra argument '{arg}'")
        arg_index += 1


    if not path:
        print_help(error=True)
    if not os.path.exists(path):
        print("No such directory")
        exit(1)

    separator_open = separator_open if separator_open else separator
    separator_close = separator_close if separator_close else separator

    if print_tree:
        if os.name == 'nt':  # Windows
            os.system(f'tree "{path}" /F')
        else:
            os.system(f'tree "{path}" {f"-L {recursive + 1}" if recursive != -1 else ""}')

    print_directory(path, recursive)
