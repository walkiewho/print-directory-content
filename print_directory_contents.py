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

    print(f"FILE: \"{prefix}{os.path.basename(file_path)}\"\n```")

    if not is_text_file(file_path):
        print("Файл бинарный, нет возможности прочитать")
    else:
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                print(file.read().strip())
        except FileNotFoundError:
            print("Файл не найден")
        except PermissionError:
            print("Нет прав на чтение файла")
        except OSError as e:
            print(f"Другая ошибка при открытии: {e}")
    print('```\n')
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
    print("Usage: python print_directory_contents.py <DIRECTORY_PATH>")
    print("Flags: -r --recursive Recursively print directories")
    exit(int(error))

if __name__ == "__main__":
    if len(argv) < 2:
        print_help()

    path = ''
    recursive = 0
    print_tree = False

    arg_index = 1
    while arg_index < len(argv):
        arg = argv[arg_index]
        if arg == '-t' or arg == 'tree':
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
        elif arg[0] == '-':
            print_help()
        elif not path:
            path = arg
        else:
            print(f"Warning: ignored extra argument '{arg}'")
        arg_index += 1


    if not path:
        print_help(error=True)


    path = os.path.abspath(path)

    if print_tree:
        os.system(f"tree {path} {f"-L {recursive + 1}" if recursive != -1 else ""}")
    else:
        print(path, end='\n\n')

    print_directory(path, recursive)
