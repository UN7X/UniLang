import subprocess
try:
    import pkg_resources
    from pkg_resources import DistributionNotFound
except ModuleNotFoundError:
        print(f"\033[93m[WARNING]Required package: ['Setuptools'] not found. Installing missing package...\033[0m")
        os.system(f"{sys.executable} -m pip install setuptools")
import time
import random
import re
import math
import argparse
import difflib
import os
from os import path
import platform
import sys

try:
    parser_arg = argparse.ArgumentParser(description='UniLang Interpreter')
    parser_arg.add_argument('script', nargs="?", help='Path to the UniLang script file')
    parser_arg.add_argument('--fo', action='store_true', help='Fail open on syntax errors')
    parser_arg.add_argument('--fc', action='store_true', help='Fail close on syntax errors')
    parser_arg.add_argument('--init', action='store_true', help='Prapare and ensure the interpreter is ready for first use.')
    parser_arg.add_argument('--about', action='store_true', help='Show information about the interpreter.')
    parser_arg.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser_arg.add_argument('--man', nargs='?', const='1', help='Show the ULS manual. Provide a page number optionally.')
    parser_arg.add_argument('--debug', action='store_true', help='Enable debug mode.')
    parser_arg.add_argument('--check', action='store_true', help='Check for updates.')  

    args = parser_arg.parse_args()
except argparse.ArgumentError as e:
    print(f"\033[93m[WARNING] {e}\033[0m")
    exit(1)

manual_pages = [
    # Page 1
    """UniLang Script (ULS) Manual - Page 1
====================================
Welcome to UniLang Script!

UniLang Script (ULS) is a simple, interpreted programming language designed for beginners. It is inspired by Python and JavaScript, aiming to be easy to learn and use.

Use the command line argument '--man <page>' to navigate to specific pages of this manual.

Topics:
 - Getting Started
 - Basic Syntax
 - Variables and Data Types
 - Operators
 - Control Structures
 - Functions
 - Built-in Functions

Example:
pypy interpreter.py --man 2""",

    # Page 2
    """UniLang Script (ULS) Manual - Page 2
====================================
Getting Started:

To run a UniLang Script file, use the interpreter followed by the script filename:

Example:
pypy interpreter.py my_script.uls

Scripts should have the '.uls' extension.

Use '--man 3' to continue to Basic Syntax.""",

    # Page 3
    """UniLang Script (ULS) Manual - Page 3
====================================
Basic Syntax:

- Statements end with a newline.
- Use braces { } to denote blocks of code.
- Comments start with '#' and continue to the end of the line.

Example:
# This is a comment
print("Hello, World!")

Use '--man 4' to learn about Variables and Data Types.""",

    # Page 4
    """UniLang Script (ULS) Manual - Page 4
====================================
Variables and Data Types:

Variables are used to store information. You can assign a value to a variable using the '=' operator.

Example:
x = 10
name = "Alice"
is_active = true

Data Types:
- Numbers: integers (e.g., 10, -5)
- Strings: text enclosed in double quotes (e.g., "Hello")
- Booleans: true or false

Use '--man 5' to learn about Operators.""",

    # Page 5
    """UniLang Script (ULS) Manual - Page 5
====================================
Operators:

Arithmetic Operators:
- Addition: +
- Subtraction: -
- Multiplication: *
- Division: /
- Modulo: %

Comparison Operators:
- Equal to: ==
- Not equal to: !=
- Greater than: >
- Less than: <
- Greater than or equal to: >=
- Less than or equal to: <=

Logical Operators:
- And: and
- Or: or
- Not: not

Example:
if (x > 0) and (x < 10) {
    print("x is between 1 and 9")
}

Use '--man 6' to learn about Control Structures.""",

    # Page 6
    """UniLang Script (ULS) Manual - Page 6
====================================
Control Structures:

If/Else Statements:
if condition {
    # code to execute if condition is true
} else {
    # code to execute if condition is false
}

Example:
if x > 10 {
    print("x is greater than 10")
} else {
    print("x is 10 or less")
}

While Loops:
while condition {
    # code to execute while condition is true
}

Example:
i = 0
while i < 5 {
    print(i)
    i = i + 1
}

For Loops:
for variable in range(start, end) {
    # code to execute for each value
}

Example:
for i in range(1, 5) {
    print(i)
}

Use '--man 7' to learn about Functions.""",

    # Page 7
    """UniLang Script (ULS) Manual - Page 7
====================================
Functions:

Functions are blocks of reusable code that perform a specific task. You can define a function using the 'define' keyword.

Syntax:
define function_name(parameters) {
    # code to execute
    return value
}

Example:
define greet(name) {
    return "Hello, " + name + "!"
}

Call the function:
message = greet("Alice")
print(message)

Use '--man 8' to learn about Built-in Functions.""",

    # Page 8
    """UniLang Script (ULS) Manual - Page 8
====================================
Built-in Functions:

UniLang provides several built-in functions to perform common tasks.

- print(value): Display the value to the console.
- input(prompt): Get input from the user.
- str(value): Convert value to a string.
- int(value): Convert value to an integer.
- length(value): Get the length of a string.
- randomint(min, max): Generate a random integer between min and max.
- sqrt(value): Calculate the square root of a number.

Example:
name = input("Enter your name: ")
print("Hello, " + name + "!")
rand_num = randomint(1, 100)
print("Random number between 1 and 100: " + str(rand_num))

Use '--man 9' to see additional resources.""",

    # Page 9
    """UniLang Script (ULS) Manual - Page 9
====================================
Additional Resources:

For more examples and detailed documentation, please visit:

https://un7x.net/unilang-script

Thank you for using UniLang Script!

That's all for the manual. Use '--man <page>' to revisit any section.
"""
]


if args.man:
    try:
        page_number = int(args.man)
    except ValueError:
        page_number = 1
    page_index = page_number - 1
    if 0 <= page_index < len(manual_pages):
        print(manual_pages[page_index])
    else:
        print(f"No manual page {page_number}. Available pages: 1-{len(manual_pages)}")
    sys.exit(0)

try: 
    import ply.lex as lex
    import ply.yacc as yacc
    from colorama import init, Fore, Style
    init(autoreset=True)
    import requests
    import sys
except ImportError or ModuleNotFoundError:
    if not args.init:
        print("Required packages not found. Please run the interpreter with the --init flag to install the required packages.")
        exit(1)
    def is_setuptools_installed():
        return any(os.path.isdir(os.path.join(path, 'setuptools')) for path in sys.path)

    if not is_setuptools_installed():
        print("setuptools not found. Installing...")
        os.system(f"{sys.executable} -m pip install setuptools")


    try:
        pkg_resources.get_distribution('ply')
        print("\033[36m[INFO]ply is already installed.\033[0m")
        pkg_resources.get_distribution('colorama')
        print("\033[36m[INFO]colorama is already installed.\033[0m")
        pkg_resources.get_distribution('requests')
        print("\033[36m[INFO]requests is already installed.\033[0m")
        pkg_resources.get_distribution('tqdm')
        print("\033[36m[INFO]tqdm is already installed.\033[0m")
    except pkg_resources.DistributionNotFound as e:
        missing_packages = [str(e).split("'")[1]]
        print(f"\033[93m[WARNING]Required package(s): {missing_packages} not found. Installing missing package(s)...\033[0m")

        for package in missing_packages:
            subprocess.call([sys.executable, "-m", "pip", "install", package])
            


if not args.init and not args.about and not args.script and not args.check:
    parser_arg.error("the following arguments are required: script")

current_version = "1.1.3"

def about():
    print(f"""
\033[36mUni\033[97;46mLang\033[0m | \033[107;30mScript Interpreter\033[0m
by UN7X
 __  __     __         ______     __    
/\ \/\ \   /\ \       /\  ___\   /\ \   
\ \ \_\ \  \ \ \____  \ \___  \  \ \ \  
 \ \_____\  \ \_____\  \/\_____\  \ \_\ 
  \/_____/   \/_____/   \/_____/   \/_/ 
""")
    labels = ["Date:", "Connected to Internet:", "Interpreter path:", "UniLang Version:", "Operating System:", "OS Version:", "Machine Name:", "Processor:", "Architecture:", "Python Version:", "Type:",]
    values = [
        time.strftime('%Y-%m-%d %H:%M:%S'),
        str(requests.get('https://google.com').status_code == 200),
        os.path.abspath(__file__),
        current_version,
        platform.system(),
        platform.version(),
        platform.machine(),
        platform.processor(),
        str(platform.architecture()).replace("('", "").replace("', '", ": ").replace("')", ""),
        platform.python_version(),
        platform.python_implementation()
    ]
    
    max_label_width = max(len(label) for label in labels)
    max_value_width = max(len(value) for value in values)
    
    for label, value in zip(labels, values):
        print(f"{label:<{max_label_width}} {value:<{max_value_width}}")
    print("""\n\033[36mUni\033[97;46mLang\033[0m is a simple, interpreted programming language designed for beginners. 
It is inspired by Python and JavaScript, and aims to be easy to learn and use. 
The interpreter is written in Python using the PLY library for lexing and parsing. 
And it also includes built-in functions for common tasks such as input/output, math, and string manipulation. 
The language supports basic features such as variables, expressions, control structures, functions, and more. 
It's designed to be extensible, so additional features and pure-python libraries can be added easily. 
The goal of \033[36mUni\033[97;46mLang\033[0m is to provide a simple and fun way to learn programming and create small projects.\n""")
    print("For more info, please visit https://un7x.net/unilang-script\n")
    exit(0)

def check_and_install_package(package_names):
    for package_name in package_names:
        try:
            pkg_resources.get_distribution(package_name)
            print(f"{package_name} is already installed.")
        except DistributionNotFound:
            print(f"{package_name} not found. Installing...")
            subprocess.call(['pip', 'install', package_name])
    return True
GITHUB_API_URL = 'https://api.github.com/repos/UN7X/unilang/releases/latest'

def check_for_updates():
    try:
        response = requests.get(GITHUB_API_URL)
        latest_release = response.json()['name']
        if current_version < latest_release:
            print(f"\033[93m[WARNING] A newer version ({latest_release}) is available. Please update for best stability.\033[0m")
        else:
            print("\033[92m[INFO] You are using the latest version.\033[0m")
    except Exception as e:
        print("\033[91m[ERROR] Could not check for updates.\033[0m", e)    

if bool(requests.get('https://google.com').status_code == 200) and args.check:
    check_for_updates()

if args.init:  
    check_for_updates()
    print("\033[36m[INFO] Initializing interpreter...\033[0m")
    if platform.python_implementation() != 'PyPy':
        print("\033[93m[WARNING] PyPy interpreter not detected. It is recommended to use PyPy for best performance.\033[0m")

    
if args.about:
    about()

# ---------------- LEXER -----------------

reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'define': 'DEFINE',
    'result': 'RESULT',
    'not': 'NOT',
    'wait': 'WAIT',
    'for': 'FOR',
    'in': 'IN',
    'or': 'OR',
    'and': 'AND',
    'range': 'RANGE',
    'true': 'TRUE',
    'false': 'FALSE',
    'import': 'IMPORT',
    'break': 'BREAK'
}

tokens = [
    'NUMBER', 'STRING', 'IDENTIFIER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'EQUALS', 'LPAREN', 'RPAREN', 'COMMA',
    'LT', 'GT', 'EQ', 'NEQ', 'LE', 'GE', 'DOT',
    'LBRACE', 'RBRACE', 'INCREMENT', 'DECREMENT', 'PLUS_EQUALS', 'MINUS_EQUALS',
] + list(reserved.values())

t_DOT = r'\.'


t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_MOD      = r'%'
t_EQUALS   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_COMMA    = r','
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_LT       = r'<'
t_GT       = r'>'
t_EQ       = r'=='
t_NEQ      = r'!='
t_LE       = r'<='
t_GE       = r'>='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_PLUS_EQUALS = r'\+='
t_MINUS_EQUALS = r'-='

t_ignore = ' \t'

def t_COMMENT(t):
    r'\#.*'

def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"{Fore.YELLOW}[WARNING] Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

if not args.about:
    try:
        if args.init:
            print("\033[36m[INFO] Initializing lexer...\033[0m")
        lexer = lex.lex()
        if args.init:
            print("\033[32m[SUCCESS] Lexer initialized.\033[0m")
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[FATAL] {e}")
        exit(1)

class Node: pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Block(Node):
    def __init__(self, statements):
        self.statements = statements

class Number(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print(Node):
    def __init__(self, expression):
        self.expression = expression

class If(Node):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDef(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Return(Node):
    def __init__(self, value):
        self.value = value

class Wait(Node):
    def __init__(self, duration):
        self.duration = duration

class Import(Node):
    def __init__(self, module_name):
        self.module_name = module_name

class MemberAccess(Node):
    def __init__(self, obj, member):
        self.obj = obj
        self.member = member

class CompoundAssignment(Node):
    def __init__(self, name, op, value):
        self.name = name
        self.op = op
        self.value = value

class MethodCall(Node):
    def __init__(self, obj, method_name, args):
        self.obj = obj
        self.method_name = method_name
        self.args = args

class Boolean(Node):
    def __init__(self, value):
        self.value = value

class ForLoop(Node):
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

class RangeExpression(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Break(Node):
    pass

class Function:
    def __init__(self, params, body):
        self.params = params
        self.body = body

class ExecutionContext:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {} if parent is None else parent.functions
        self.parent = parent
        self.return_value = None

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Undefined variable '{name}'")

    def set_variable(self, name, value):
        if name in self.variables or self.parent is None:
            self.variables[name] = value
        else:
            self.parent.set_variable(name, value)

    def define_function(self, name, function):
        self.functions[name] = function

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise NameError(f"Undefined function '{name}'")

class BuiltInFunction(Function):
    def __init__(self, func):
        self.func = func

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# Precedence to handle unary minus
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT', 'UMINUS'),
)

# ---------------- GRAMMAR -----------------

def p_program(p):
    '''program : statement_list'''
    p[0] = Program(p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_statement(p):
    '''statement : assignment
                 | print_statement
                 | if_statement
                 | while_statement
                 | function_def
                 | for_loop
                 | return_statement
                 | wait_statement
                 | block
                 | expression_statement
                 | import_statement
                 | BREAK'''
    p[0] = Break() if p.slice[1].type == 'BREAK' else p[1]

def p_block(p):
    '''block : LBRACE statement_list RBRACE
             | LBRACE RBRACE'''
    p[0] = Block(p[2]) if len(p) == 4 else Block([])

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : IDENTIFIER EQUALS expression'''
    p[0] = Assignment(p[1], p[3])

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN'''
    p[0] = Print(p[3])

def p_if_statement(p):
    '''if_statement : IF expression block
                    | IF expression block ELSE block'''
    p[0] = If(p[2], p[3]) if len(p) == 4 else If(p[2], p[3], p[5])

def p_for_loop(p):
    '''for_loop : FOR IDENTIFIER IN iterable block'''
    p[0] = ForLoop(p[2], p[4], p[5])

def p_iterable(p):
    '''iterable : expression
                | RANGE LPAREN expression COMMA expression RPAREN'''
    p[0] = p[1] if len(p) == 2 else RangeExpression(p[3], p[5])

def p_while_statement(p):
    '''while_statement : WHILE expression block'''
    p[0] = While(p[2], p[3])

def p_function_def(p):
    '''function_def : DEFINE IDENTIFIER LPAREN RPAREN block
                    | DEFINE IDENTIFIER LPAREN param_list RPAREN block'''
    if len(p) == 6:
        p[0] = FunctionDef(p[2], [], p[5])
    else:
        p[0] = FunctionDef(p[2], p[4], p[6])

def p_param_list(p):
    '''param_list : IDENTIFIER
                  | param_list COMMA IDENTIFIER
                  | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_import_statement(p):
    '''import_statement : IMPORT IDENTIFIER'''
    p[0] = Import(p[2])

def p_return_statement(p):
    '''return_statement : RESULT expression'''
    p[0] = Return(p[2])

def p_wait_statement(p):
    '''wait_statement : WAIT expression'''
    p[0] = Wait(p[2])

def p_expression(p):
    '''expression : logic_or_expr'''
    p[0] = p[1]

def p_logic_or_expr(p):
    '''logic_or_expr : logic_or_expr OR logic_and_expr
                     | logic_and_expr'''
    p[0] = BinaryOp('or', p[1], p[3]) if len(p) == 4 else p[1]

def p_logic_and_expr(p):
    '''logic_and_expr : logic_and_expr AND equality_expr
                      | equality_expr'''
    p[0] = BinaryOp('and', p[1], p[3]) if len(p) == 4 else p[1]

def p_equality_expr(p):
    '''equality_expr : relational_expr
                     | equality_expr EQ relational_expr
                     | equality_expr NEQ relational_expr'''
    p[0] = p[1] if len(p) == 2 else BinaryOp(p[2], p[1], p[3])

def p_relational_expr(p):
    '''relational_expr : additive_expr
                       | relational_expr LT additive_expr
                       | relational_expr GT additive_expr
                       | relational_expr LE additive_expr
                       | relational_expr GE additive_expr'''
    p[0] = p[1] if len(p) == 2 else BinaryOp(p[2], p[1], p[3])

def p_additive_expr(p):
    '''additive_expr : additive_expr PLUS term
                     | additive_expr MINUS term
                     | term'''
    p[0] = BinaryOp(p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | term MOD factor
            | factor'''
    p[0] = BinaryOp(p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_factor(p):
    '''factor : PLUS factor
              | MINUS factor %prec UMINUS
              | NOT factor
              | primary'''
    p[0] = UnaryOp(p[1], p[2]) if len(p) == 3 else p[1]

def p_primary(p):
    '''primary : atom
               | primary DOT IDENTIFIER
               | primary DOT IDENTIFIER LPAREN arg_list RPAREN
               | primary DOT IDENTIFIER LPAREN RPAREN
               | primary LPAREN arg_list RPAREN
               | primary LPAREN RPAREN'''
    if len(p) == 2:
        # atom
        p[0] = p[1]
    elif len(p) == 4 and p[2] == '.':
        # primary DOT IDENTIFIER
        p[0] = MemberAccess(p[1], p[3])
    elif len(p) == 6 and p[3] != '(':
        # primary DOT IDENTIFIER LPAREN RPAREN
        # means primary.member()
        p[0] = MethodCall(p[1], p[3], [])
    elif len(p) == 7:
        # primary DOT IDENTIFIER LPAREN arg_list RPAREN
        p[0] = MethodCall(p[1], p[3], p[5])
    elif len(p) == 5 and p[2] == '(':
        # primary LPAREN arg_list RPAREN
        p[0] = FunctionCall(p[1], p[3])
    elif len(p) == 4 and p[2] == '(':
        # primary LPAREN RPAREN
        p[0] = FunctionCall(p[1], [])


def p_arg_list(p):
    '''arg_list : expression
                | arg_list COMMA expression
                | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_atom(p):
    '''atom : IDENTIFIER
            | NUMBER
            | STRING
            | TRUE
            | FALSE
            | LPAREN expression RPAREN'''
    if len(p) == 2:
        t = p.slice[1].type
        if t == 'IDENTIFIER':
            p[0] = Variable(p[1])
        elif t == 'NUMBER':
            p[0] = Number(p[1])
        elif t == 'STRING':
            p[0] = String(p[1])
        elif t == 'TRUE':
            p[0] = Boolean(True)
        elif t == 'FALSE':
            p[0] = Boolean(False)
    else:
        p[0] = p[2]

def p_expression_increment(p):
    '''expression : expression INCREMENT
                  | expression DECREMENT'''
    if p[2] == '++':
        p[0] = UnaryOp('increment', p[1])
    else:
        p[0] = UnaryOp('decrement', p[1])

def p_expression_compound_assignment(p):
    '''expression : IDENTIFIER PLUS_EQUALS expression
                  | IDENTIFIER MINUS_EQUALS expression'''
    if p[2] == '+=':
        p[0] = CompoundAssignment(p[1], '+', p[3])
    else:
        p[0] = CompoundAssignment(p[1], '-', p[3])

def p_empty(p):
    '''empty :'''
    p[0] = None

def p_error(p):
    if p:
        token_value = str(p.value)
        suggestions = difflib.get_close_matches(token_value, list(reserved.keys()) + ['(', ')', '{', '}', '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>='], n=1, cutoff=0.8)
        error_message = f"[ERROR] Syntax error at '{token_value}' on line {p.lineno}"
        if suggestions:
            error_message += f". Did you mean '{suggestions[0]}'?"
        print(Fore.RED + error_message)
    else:
        print(f"{Fore.RED}[ERROR] Syntax error at EOF")

if not args.about:
    # build parser, i think
    try:
        if args.init:
            print("\033[36m[INFO] Initializing parser...\033[0m")
        class ColorStream:
            def __init__(self, stream, debug=False):
                self.stream = stream
                self.debug_mode = debug
                self.printed_messages = set()
        
            def write(self, data):
                if str(data).startswith("WARNING:"):
                    #remove the warning prefix, replacing it with our own [WARNING]
                    data = str(data).replace("WARNING:", "[WARNING]")
                    self.stream.write(Fore.YELLOW + data + "\033[0m\n")
                else:
                    self.stream.write("\033[93m" + data + "\033[0m")
        
            def flush(self):
                self.stream.flush()

            def info(self, message, *args):
                if not self.debug_mode:
                    if not hasattr(self, 'printed_messages'):
                        self.printed_messages = set()
                    if message not in self.printed_messages and message != "":
                        self.write("\033[36m[INFO] " + message + "\033[0m\n")
                        self.printed_messages.add(message)
                else:
                    self.write("\033[36m[INFO] " + message + "\033[0m\n")
                

            def success(self, message, *args):
                self.write("\033[32m[SUCCESS] " + message + "\033[0m\n")

            def fatal(self, message, *args):
                self.write(f"{Fore.LIGHTRED_EX}[FATAL] {message}" + "\n")

            def warning(self, message, *args):
                self.write(f"{Fore.YELLOW}[WARNING] {message}" + "\n")

            def debug(self, message, *args):
                if self.debug_mode:
                    self.write("\033[35m[DEBUG] " + message + "\033[0m\n")        
        parser = yacc.yacc(start='program', debug=True, debuglog=ColorStream(sys.stdout, debug=args.debug), write_tables=True, optimize=True)
        if args.init:
            print("\033[32m[SUCCESS] Parser initialized.\033[0m")
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[FATAL] {e}")
        exit(1)
    if args.init:
        print("\033[32m[SUCCESS] Interpreter initialization complete!\033[0m")
        exit(0)

# ---------------- EXECUTION -----------------
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

from colorama import Fore
import math, time, random, requests

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

def execute(node, context):
    if node is None:
        return None
    if handler := NODE_HANDLERS.get(type(node)):
        return handler(node, context)
    else:
        raise TypeError(f"Unknown node type '{type(node).__name__}'")

def handle_program(node, context):
    for stmt in node.statements:
        val = execute(stmt, context)
        # If a break is encountered at top-level, it just stops executing further statements
        if val == 'break':
            break
    return None

def handle_import(node, context):
    module_name = node.module_name
    try:
        module = __import__(module_name)
        context.set_variable(module_name, module)
    except ImportError:
        print(f"{Fore.RED}[ERROR] Module '{module_name}' not found")

def handle_block(node, context):
    for stmt in node.statements:
        val = execute(stmt, context)
        if val == 'break':
            return 'break'
    return None

def handle_number(node, context):
    return node.value

def handle_string(node, context):
    return node.value

def handle_variable(node, context):
    return context.get_variable(node.name)

def handle_assignment(node, context):
    value = execute(node.value, context)
    context.set_variable(node.name, value)

def handle_print(node, context):
    value = execute(node.expression, context)
    print(value)

def handle_wait(node, context):
    duration = execute(node.duration, context)
    time.sleep(duration)

def handle_boolean(node, context):
    return node.value

def handle_if(node, context):
    if condition := execute(node.condition, context):
        return execute(node.then_branch, context)
    elif node.else_branch:
        return execute(node.else_branch, context)
    return None

def handle_function_def(node, context):
    func = Function(node.params, node.body)
    context.define_function(node.name, func)

def handle_function_call(node, context):
    func_name = node.name.name if hasattr(node.name, 'name') else node.name
    func = context.get_function(func_name)
    args = [execute(arg, context) for arg in node.args]

    if isinstance(func, BuiltInFunction):
        return func.func(*args)
    elif isinstance(func, Function):
        if len(func.params) != len(args):
            raise TypeError(f"Function '{func_name}' expected {len(func.params)} arguments, got {len(args)}")
        func_context = ExecutionContext(parent=context)
        for param, arg in zip(func.params, args):
            func_context.set_variable(param, arg)
        try:
            execute(func.body, func_context)
        except ReturnException as e:
            return e.value
        return func_context.return_value
    else:
        raise TypeError(f"'{func_name}' is not a function")

def handle_return(node, context):
    value = execute(node.value, context)
    raise ReturnException(value)

def handle_method_call(node, context):
    obj = execute(node.obj, context)
    args = [execute(arg, context) for arg in node.args]

    if not hasattr(obj, node.method_name):
        raise AttributeError(f"'{type(obj).__name__}' object has no attribute '{node.method_name}'")
    method = getattr(obj, node.method_name)
    if callable(method):
        return method(*args)
    else:
        raise TypeError(f"Attribute '{node.method_name}' of object '{type(obj).__name__}' is not callable")

def handle_binary_op(node, context):
    left = execute(node.left, context)
    right = execute(node.right, context)
    ops = {
        '+': lambda l,r: l+r,
        '-': lambda l,r: l-r,
        '*': lambda l,r: l*r,
        '/': lambda l,r: l/r,
        '%': lambda l,r: l%r,
        '<': lambda l,r: l<r,
        '>': lambda l,r: l>r,
        '<=': lambda l,r: l<=r,
        '>=': lambda l,r: l>=r,
        '==': lambda l,r: l==r,
        '!=': lambda l,r: l!=r,
        'and': lambda l,r: l and r,
        'or': lambda l,r: l or r
    }
    return ops[node.op](left, right)

def handle_unary_op(node, context):
    operand = execute(node.operand, context)
    if node.op == 'increment':
        if not isinstance(node.operand, Variable):
            raise TypeError("Increment target must be a variable")
        result = operand + 1
        context.set_variable(node.operand.name, result)
        return result
    elif node.op == 'decrement':
        if not isinstance(node.operand, Variable):
            raise TypeError("Decrement target must be a variable")
        result = operand - 1
        context.set_variable(node.operand.name, result)
        return result
    elif node.op == 'not':
        return not operand
    elif node.op == '-':
        return -operand
    else:
        raise ValueError(f"Unknown unary operator '{node.op}'")

def handle_compound_assignment(node, context):
    value = context.get_variable(node.name)
    right = execute(node.value, context)
    result = value + right if node.op == '+' else value - right
    context.set_variable(node.name, result)
    return result

def handle_for_loop(node, context):
    iterable = execute(node.iterable, context)
    if not hasattr(iterable, '__iter__'):
        raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
    for item in iterable:
        loop_context = ExecutionContext(parent=context)
        loop_context.set_variable(node.var_name, item)
        val = execute(node.body, loop_context)
        if val == 'break':
            break

def handle_while(node, context):
    while execute(node.condition, context):
        val = execute(node.body, context)
        if val == 'break':
            break
        if context.return_value is not None:
            break

def handle_range_expression(node, context):
    start = execute(node.start, context)
    end = execute(node.end, context)
    return range(start, end)

def handle_break(node, context):
    return 'break'

# Map node types to handlers
NODE_HANDLERS = {}

# Register handlers
NODE_HANDLERS[Program] = handle_program
NODE_HANDLERS[Import] = handle_import
NODE_HANDLERS[Block] = handle_block
NODE_HANDLERS[Number] = handle_number
NODE_HANDLERS[String] = handle_string
NODE_HANDLERS[Variable] = handle_variable
NODE_HANDLERS[Assignment] = handle_assignment
NODE_HANDLERS[Print] = handle_print
NODE_HANDLERS[Wait] = handle_wait
NODE_HANDLERS[Boolean] = handle_boolean
NODE_HANDLERS[If] = handle_if
NODE_HANDLERS[FunctionDef] = handle_function_def
NODE_HANDLERS[FunctionCall] = handle_function_call
NODE_HANDLERS[Return] = handle_return
NODE_HANDLERS[MethodCall] = handle_method_call
NODE_HANDLERS[BinaryOp] = handle_binary_op
NODE_HANDLERS[UnaryOp] = handle_unary_op
NODE_HANDLERS[CompoundAssignment] = handle_compound_assignment
NODE_HANDLERS[ForLoop] = handle_for_loop
NODE_HANDLERS[While] = handle_while
NODE_HANDLERS[RangeExpression] = handle_range_expression
NODE_HANDLERS[Break] = handle_break

source_code = ''
if __name__ == '__main__' and not args.init and not args.about and not args.check:
    with open(args.script, 'r') as f:
        source_code = f.read()

    # Parse the source code
    try:
        ast = parser.parse(source_code)
    except SyntaxError as e:
        print(f"{Fore.LIGHTRED_EX}[FATAL] {e}")
        if args.fc:
            exit(1)


global_context = ExecutionContext()
global_context.define_function('str', BuiltInFunction(str))
global_context.define_function('int', BuiltInFunction(int))
global_context.define_function('float', BuiltInFunction(float))
global_context.define_function('abs', BuiltInFunction(abs))
global_context.define_function('round', BuiltInFunction(round))
global_context.define_function('min', BuiltInFunction(min))
global_context.define_function('max', BuiltInFunction(max))

# Input/Output
global_context.define_function('input', BuiltInFunction(lambda prompt='': input(str(prompt))))

# Random
global_context.define_function('randomint', BuiltInFunction(lambda min_val, max_val: random.randint(int(min_val), int(max_val))))

# String utilities
global_context.define_function('length', BuiltInFunction(lambda s: len(str(s))))
global_context.define_function('substring', BuiltInFunction(lambda s, start, end: str(s)[int(start):int(end)]))
global_context.define_function('find', BuiltInFunction(lambda s, sub: str(s).find(str(sub))))
global_context.define_function('split', BuiltInFunction(lambda s, delim=' ': str(s).split(str(delim))))
global_context.define_function('join', BuiltInFunction(lambda delim, lst: str(delim).join(str(x) for x in lst)))

# Math utilities
global_context.define_function('sqrt', BuiltInFunction(lambda x: math.sqrt(float(x))))

# Networking
global_context.define_function('http_get', BuiltInFunction(lambda url: requests.get(url).text))


if not (args.init or args.about or args.check):
    # Execute the parsed AST
    try:
        execute(ast, global_context)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[FATAL] {e}")
