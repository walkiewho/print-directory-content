# Print Directory Content
A Python script that recursively prints the contents of all files in a directory

## Features
- Recursive directory traversal
- Binary file detection
- Customizable separators for file content
- Tree view of directory structure
- UTF-8 encoding support

## Installation
```bash
git clone https://github.com/walkiewho/print-directory-content
chmod +x print_directory_contents.py
```

## Options
    -r  --recursive [N]        Recursively print subdirectories (N = depth, no value = infinite)
    -t  --tree                 Display directory tree
    -s  --separator SEP        Sets open and close separators for content of file
    -so --separator-open SEP   Sets open separator for content of file (Has priority over -s)
    -sc --separator-close SEP  Sets close separator for content of file (Has priority over -s)

## Usage
### Basic usage
```bash
./print_directory_contents.py ~/Documents/
```

### Recursive with depth
```bash
./print_directory_contents.py ~/Downloads/ -r 3
```

### Recursive with tree
```bash
./print_directory_contents.py ~/Projects/ -r -t
```

### Custom separators
```bash
./print_directory_contents.py ./src/ -so "/*" -sc "*/"
```
