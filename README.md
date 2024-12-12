# UniLang Script (ULS) Interpreter

**UniLang Script (ULS)** is a simple, interpreted programming language designed for beginners. It draws inspiration from Python and JavaScript, striving to provide a straightforward, accessible environment for learning fundamental programming concepts.

## Features

- **Beginner-Friendly Syntax:**  
  ULS uses braces `{}` to denote code blocks and supports both line breaks and optional semicolons `;` as statement separators.
  
- **Familiar Data Types:**
  - **Numbers:** `int` and `float`  
  - **Strings:** `"Hello, World!"` (with escape sequences)  
  - **Booleans:** `true`, `false`  
  - **Lists:** `[1, 2, 3]` or `["apple", "banana"]`  
  - **Triple-Quoted Strings:** `"""Multi-line text here..."""`
  
- **Control Structures:**
  - `if/else` conditions  
  - `while` loops  
  - `for i in range(...)` loops
  - `break` to exit loops
  
- **Functions:**
  Define and call functions:
  ```uls
  define greet(name) {
      result "Hello, " + name + "!"
  }

  print(greet("ULS User"))
  ```
  
- **Built-in Functions:**
  - **I/O:** `print()`, `input()`
  - **Conversions:** `str()`, `int()`, `float()`
  - **Math & Utilities:** `abs()`, `round()`, `min()`, `max()`, `sqrt()`, `pow()`, `sin()`, `cos()`, `tan()`, `log()`
  - **Strings:** `replace()`, `upper()`, `lower()`, `capitalize()`, `find()`, `substring()`, `split()`, `join()`
  - **Lists:** `append()`, `remove()`, `len()`, `sum()`, `any()`, `all()`, `sorted()`, `reverse()`, `random_choice()`, `random_shuffle()`
  - **Random:** `randomint(min, max)`
  - **Date/Time:** `current_time()`, `current_date()`
  - **File I/O:** `read_file()`, `write_file()`, `append_file()`
  - **Networking:** `http_get(url)`

- **Advanced Features:**
  - `eval(code)`: Execute ULS code at runtime.
  - `python_eval(expr)`: Evaluate a Python expression at runtime (for trusted code only).
  - `try/except/finally` blocks for basic exception handling.
  - Optional semicolon `;` as a statement separator.
  - Escape sequences in strings (`\n`, `\t`, etc.) and support for ANSI codes in strings if the terminal supports them.
  
- **Empty `print()` for New Lines:**
  Just call `print()` with no arguments to print a blank line.

## Installation

1. **Requirements:**  
   - Python or PyPy  
   - `ply` and `colorama` Python packages  
   - `requests` for `check_for_update()` function

   If any dependencies are missing, which are later automatially installed if they are, you can manually run:
   ```bash
   pip install ply colorama requests
   ```

2. **Clone the Repo:**
   ```bash
   git clone https://github.com/UN7X/unilang.git
   cd unilang
   ```

3. **Initialize the Interpreter:**
   ```bash
   pypy interpreter.py --init
   ```
   
   Or use Python if PyPy is not available:
   ```bash
   python interpreter.py --init
   ```

4. **Run the Interpreter:**
   (PyPy)
   ```bash
   pypy interpreter.py example_scripts/test_features.uls
   ```
   (Python)
   ```bash
   python interpreter.py example_scripts/test_features.uls
   ```

## Usage

- **Run a Script:**
  ```bash
  pypy interpreter.py my_script.uls
  ```

- **Show the Manual:**
  ```bash
  pypy interpreter.py --man
  pypy interpreter.py --man 3
  ```
  Use `--man <page>` to navigate the included manual pages.

- **About:**
  ```bash
  pypy interpreter.py --about
  ```

- **Init (First-Time Setup OR changes made to the Interpreter itself):**
  ```bash
  pypy interpreter.py --init
  ```
  
- **Check for Updates:**
  ```bash
  pypy interpreter.py --check
  ```

## Example

```uls
# example.uls
x = 10
if (x > 5) {
    print("x is greater than 5")
} else {
    print("x is 5 or less")
}

lst = [1, 2, 3]
append(lst, 4)
print("List after append: " + str(lst))  # [1, 2, 3, 4]

# Using a function
define add(a, b) {
    result a + b
}
print(add(5,7))  # 12

# File I/O example:
write_file("out.txt", "Hello, ULS!")
print(read_file("out.txt"))
```

Run it:
```bash
pypy interpreter.py example.uls
```

## Development

Contributions are welcome! Key areas that might need improvement:
- More robust escape sequence handling in strings.
- Better error messages and debugging tools.
- More built-in functions or libraries.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

For questions or suggestions, open an issue on GitHub or visit [https://un7x.net/unilang-script](https://un7x.net/unilang-script). (Site WIP)
