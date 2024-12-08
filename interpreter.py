import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound
import time
import difflib
import random
import re
import argparse

def check_and_install_package(package_name):
    try:
        pkg_resources.get_distribution(package_name)
        print(f"{package_name} is already installed.")
    except DistributionNotFound:
        print(f"{package_name} not found. Installing...")
        subprocess.call(['pip', 'install', package_name])

# Check and install PLY if necessary
check_and_install_package('ply')
import ply.lex as lex
import ply.yacc as yacc

# Reserved words (RWs) IF YOU CAN SEE THIS, THE SYNC WORKED! :3
reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'define': 'DEFINE',
    'result': 'RESULT',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'wait': 'WAIT',
    'for': 'FOR',
    'in': 'IN',
    'range': 'RANGE',
    'true': 'TRUE',
    'false': 'FALSE',
}
# token names list including RWs
tokens = [
    'NUMBER', 'STRING', 'IDENTIFIER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'EQUALS', 'LPAREN', 'RPAREN', 'COMMA',
    'LT', 'GT', 'EQ', 'NEQ', 'LE', 'GE', 'DOT',
    'LBRACE', 'RBRACE', 'INCREMENT', 'DECREMENT', 'PLUS_EQUALS', 'MINUS_EQUALS',
    'AND_OP', 'OR_OP',
] + list(reserved.values())

# Regular expression rules for simple tokens
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
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_DOT = r'\.'

# List of operator symbols
operator_symbols = [
    '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
    '(', ')', '{', '}', ',', '.', '&&', '||', '!', '++', '--', '+=', '-='
]

# Known tokens for error correction
known_tokens = list(reserved.keys()) + operator_symbols

t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # reserved words dectector
    return t

# Ignore comments starting with #
def t_COMMENT(t):
    r'\#.*'
    pass  # comment remover 9000 (tm) (r) (c) (patent pending)

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove quotation marks
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_FSTRING(t):
    r'f"(?:\\.|[^"])*"'
    t.value = t.value[2:-1]  # Remove the leading f" and trailing "
    return t

tokens.append('FSTRING')


# error handling; im too lazy to write a proper error message
# wait i just got a genius idea, what if the small errors, like mispellings and similar, were fixed by the interpreter itself?
# that would be cool

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# build lexer; kill me
lexer = lex.lex()

# pre rules for operators
precedence = (
    ('left', 'OR_OP'),
    ('left', 'AND_OP'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT', 'UMINUS'),
)

# AST node class thingies
class Node:
    pass

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

# grandma's granular grammy gramtastic grammar grammathon grammation rules

def p_program(p):
    'program : statement_list'
    p[0] = Program(p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

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
    '''
    p[0] = p[1]

def p_expression_statement(p):
    'expression_statement : expression'
    p[0] = p[1]

def p_expression_increment(p):
    '''expression : expression INCREMENT
                  | expression DECREMENT
    '''
    if p[2] == '++':
        p[0] = UnaryOp('increment', p[1])
    elif p[2] == '--':
        p[0] = UnaryOp('decrement', p[1])

def p_expression_compound_assignment(p):
    '''expression : IDENTIFIER PLUS_EQUALS expression
                  | IDENTIFIER MINUS_EQUALS expression
    '''
    if p[2] == '+=':
        p[0] = CompoundAssignment(p[1], '+', p[3])
    elif p[2] == '-=':
        p[0] = CompoundAssignment(p[1], '-', p[3])


def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression'
    p[0] = Assignment(p[1], p[3])

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN'
    p[0] = Print(p[3])

def p_if_statement(p):
    '''
    if_statement : IF expression block
                 | IF expression block ELSE block
    '''
    if len(p) == 4:
        p[0] = If(p[2], p[3])
    else:
        p[0] = If(p[2], p[3], p[5])

def p_for_loop(p):
    'for_loop : FOR IDENTIFIER IN iterable block'
    p[0] = ForLoop(p[2], p[4], p[5])

def p_iterable(p):
    '''iterable : expression
                | RANGE LPAREN expression COMMA expression RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = RangeExpression(p[3], p[5])

def p_expression_fstring(p):
    'expression : FSTRING'
    p[0] = FString(p[1])

def p_while_statement(p):
    'while_statement : WHILE expression block'
    p[0] = While(p[2], p[3])

def p_function_def(p):
    '''function_def : DEFINE IDENTIFIER LPAREN RPAREN block
                    | DEFINE IDENTIFIER LPAREN param_list RPAREN block
    '''
    if len(p) == 6:
        p[0] = FunctionDef(p[2], [], p[5])
    else:
        p[0] = FunctionDef(p[2], p[4], p[6])

def p_param_list(p):
    '''param_list : IDENTIFIER
                  | param_list COMMA IDENTIFIER
                  | empty
    '''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_return_statement(p):
    'return_statement : RESULT expression'
    p[0] = Return(p[2])

def p_expression(p):
    'expression : logic_expr'
    p[0] = p[1]

def p_logic_expr(p):
    '''logic_expr : logic_expr OR_OP logic_term
                  | logic_term
    '''
    if len(p) == 4:
        p[0] = BinaryOp('or', p[1], p[3])
    else:
        p[0] = p[1]

def p_logic_term(p):
    '''logic_term : logic_term AND_OP equality_expr
                  | equality_expr
    '''
    if len(p) == 4:
        p[0] = BinaryOp('and', p[1], p[3])
    else:
        p[0] = p[1]

def p_equality_expr(p):
    '''equality_expr : equality_expr EQ relational_expr
                     | equality_expr NEQ relational_expr
                     | relational_expr
    '''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_relational_expr(p):
    '''relational_expr : relational_expr LT additive_expr
                       | relational_expr LE additive_expr
                       | relational_expr GT additive_expr
                       | relational_expr GE additive_expr
                       | additive_expr
    '''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_additive_expr(p):
    '''additive_expr : additive_expr PLUS term
                     | additive_expr MINUS term
                     | term
    '''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | term MOD factor
            | factor
    '''
    if len(p) == 4:
        p[0] = BinaryOp(p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : PLUS factor
              | MINUS factor %prec UMINUS
              | NOT factor
              | primary
    '''
    if len(p) == 3:
        p[0] = UnaryOp(p[1], p[2])
    else:
        p[0] = p[1]

def p_primary(p):
    '''primary : primary DOT IDENTIFIER
               | primary DOT IDENTIFIER LPAREN arg_list RPAREN
               | function_call
               | TRUE
               | FALSE
               | NUMBER
               | STRING
               | IDENTIFIER
               | LPAREN expression RPAREN
    '''
    if len(p) == 4 and p.slice[2].type == 'DOT':
        # primary : primary DOT IDENTIFIER
        p[0] = MethodCall(p[1], p[3], [])
    elif len(p) == 7 and p.slice[2].type == 'DOT':
        # primary : primary DOT IDENTIFIER LPAREN arg_list RPAREN
        p[0] = MethodCall(p[1], p[3], p[5])
    elif len(p) == 2:
        # single element on the right-hand side  handloing
        if p.slice[1].type == 'function_call':
            p[0] = p[1]
        elif p.slice[1].type == 'TRUE':
            p[0] = Boolean(True)
        elif p.slice[1].type == 'FALSE':
            p[0] = Boolean(False)
        elif p.slice[1].type == 'NUMBER':
            p[0] = Number(p[1])
        elif p.slice[1].type == 'STRING':
            p[0] = String(p[1])
        elif p.slice[1].type == 'IDENTIFIER':
            p[0] = Variable(p[1])
        else:
            raise SyntaxError(f"Unexpected token '{p.slice[1].type}' in primary")
    elif len(p) == 4 and p.slice[1].type == 'LPAREN':
        # primary : LPAREN expression RPAREN
        p[0] = p[2]
    else:
        raise SyntaxError(f"Invalid primary expression at '{p.slice[1].type}'")


def p_wait_statement(p):
    'wait_statement : WAIT expression'
    p[0] = Wait(p[2])

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN RPAREN
                     | IDENTIFIER LPAREN arg_list RPAREN
    '''
    if len(p) == 4:
        p[0] = FunctionCall(p[1], [])
    else:
        p[0] = FunctionCall(p[1], p[3])

def p_arg_list(p):
    '''arg_list : expression
                | arg_list COMMA expression
                | empty
    '''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_block(p):
    '''block : LBRACE RBRACE
             | LBRACE statement_list RBRACE'''
    if len(p) == 3:
        p[0] = Block([])
    else:
        p[0] = Block(p[2])

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        token_value = str(p.value)
        # Get possible matches - cutoff is set to 0.8, yet to be functional
        suggestions = difflib.get_close_matches(token_value, known_tokens, n=1, cutoff=0.8)
        if suggestions:
            print(f"Syntax error at '{token_value}' on line {p.lineno}. Did you mean '{suggestions[0]}'?")
        else:
            print(f"Syntax error at '{token_value}' on line {p.lineno}")
        p.lexer.skip(1)  # continue parsing
    else:
        print("Syntax error at EOF")



# build parser, i think
parser = yacc.yacc(start='program')

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

class FString(Node):
    def __init__(self, value):
        self.value = value

class BuiltInFunction(Function):
    def __init__(self, func):
        self.func = func

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

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

def execute(node, context):
    if isinstance(node, Program):
        for stmt in node.statements:
            execute(stmt, context)
    elif isinstance(node, Block):
        for stmt in node.statements:
            execute(stmt, context)
    elif isinstance(node, Number):
        return node.value
    elif isinstance(node, String):
        return node.value
    elif isinstance(node, Variable):
        return context.get_variable(node.name)
    elif isinstance(node, Assignment):
        value = execute(node.value, context)
        context.set_variable(node.name, value)
    elif isinstance(node, Print):
        value = execute(node.expression, context)
        print(value)
    elif isinstance(node, Wait):
        duration = execute(node.duration, context)
        time.sleep(duration)
    elif isinstance(node, Boolean):
        return node.value
    elif isinstance(node, If):
        condition = execute(node.condition, context)
        if condition:
            execute(node.then_branch, context)
        elif node.else_branch:
            execute(node.else_branch, context)
    elif isinstance(node, While):
        while execute(node.condition, context):
            execute(node.body, context)
            if context.return_value is not None:
                break
    elif isinstance(node, FunctionDef):
        func = Function(node.params, node.body)
        context.define_function(node.name, func)
    elif isinstance(node, FString):
        # regex expression finder (within curly thingys)
        pattern = r'\{([^}]+)\}'
        parts = re.split(pattern, node.value)
        result = ''
        for i, part in enumerate(parts):
            if i % 2 == 0:
                result += part
            else:
                expr = parser.parse(part, lexer=lexer)
                result += str(execute(expr, context))
        return result

    elif isinstance(node, FunctionCall):
        try:
            func = context.get_function(node.name)
        except NameError:
            suggestions = difflib.get_close_matches(node.name, context.functions.keys(), n=1, cutoff=0.8)
            if suggestions:
                print(f"Undefined function '{node.name}'. Did you mean '{suggestions[0]}'?")
            else:
                print(f"Undefined function '{node.name}'")
            return
        args = [execute(arg, context) for arg in node.args]
        if isinstance(func, BuiltInFunction):
            result = func.func(*args)
            return result
        elif isinstance(func, Function):
            if len(func.params) != len(args):
                raise TypeError(f"Function '{node.name}' expected {len(func.params)} arguments, got {len(args)}")
            func_context = ExecutionContext(parent=context)
            for param, arg in zip(func.params, args):
                func_context.set_variable(param, arg)
            try:
                execute(func.body, func_context)
            except ReturnException as e:
                return e.value
            return func_context.return_value
        else:
            raise TypeError(f"'{node.name}' is not a function")
    elif isinstance(node, Return):
        value = execute(node.value, context)
        raise ReturnException(value)
    elif isinstance(node, MethodCall):
        obj = execute(node.obj, context)
        args = [execute(arg, context) for arg in node.args]
        # ----------------------------------------------------------------------------------------------------------------------
        if isinstance(obj, str):
            if node.method_name == 'lower':
                return obj.lower()
            elif node.method_name == 'upper':
                return obj.upper()
            elif node.method_name == 'strip':
                return obj.strip()
            # add more str methods here later 
            else:
                raise AttributeError(f"'str' object has no attribute '{node.method_name}'")
        else:
            raise TypeError(f"Unsupported object type '{type(obj).__name__}' for method calls")
    elif isinstance(node, BinaryOp):
        left = execute(node.left, context)
        right = execute(node.right, context)
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '%':
            return left % right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == 'and':
            return left and right
        elif node.op == 'or':
            return left or right
        else:
            raise ValueError(f"Unknown operator '{node.op}'")
    elif isinstance(node, UnaryOp):
        operand = execute(node.operand, context)
        if node.op == 'increment':
            result = operand + 1
            # Assuming node.operand is a variable node
            context.set_variable(node.operand.name, result)
            return result
        elif node.op == 'decrement':
            result = operand - 1
            context.set_variable(node.operand.name, result)
            return result
        elif node.op == 'not':
            return not operand
        elif node.op == '-':
            return -operand
        else:
            raise ValueError(f"Unknown operator '{node.op}'")
    elif isinstance(node, CompoundAssignment):
        value = execute(Variable(node.name), context)
        right = execute(node.value, context)
        if node.op == '+':
            result = value + right
        elif node.op == '-':
            result = value - right
        context.set_variable(node.name, result)
        return result
    elif isinstance(node, ForLoop):
        iterable = execute(node.iterable, context)
        if not hasattr(iterable, '__iter__'):
            raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
        for item in iterable:
            loop_context = ExecutionContext(parent=context)
            loop_context.set_variable(node.var_name, item)
            execute(node.body, loop_context)
            if loop_context.return_value is not None:
                break

    elif isinstance(node, RangeExpression):
        start = execute(node.start, context)
        end = execute(node.end, context)
        return range(start, end)

    else:
        raise TypeError(f"Unknown node type '{type(node).__name__}'")

source_code = '''

'''

if __name__ == '__main__':
    parser_arg = argparse.ArgumentParser(description='UniLang Interpreter')
    parser_arg.add_argument('script', help='Path to the UniLang script file')
    parser_arg.add_argument('--fo', action='store_true', help='Fail open on syntax errors')
    parser_arg.add_argument('--fc', action='store_true', help='Fail close on syntax errors')
    args = parser_arg.parse_args()

    # Read source code from the specified file
    with open(args.script, 'r') as f:
        source_code = f.read()

    # Parse the source code
    try:
        ast = parser.parse(source_code)
    except SyntaxError as e:
        print(e)
        if args.fc:
            exit(1)
        elif args.fo:
            pass  # Continue execution despite syntax errors

# Create the GE context and define built-in functions from Python that i stole
global_context = ExecutionContext()
global_context.define_function('str', BuiltInFunction(str))
global_context.define_function('int', BuiltInFunction(int))
global_context.define_function('input', BuiltInFunction(lambda prompt='': input(str(prompt))))
global_context.define_function('randomint', BuiltInFunction(lambda min_val, max_val: random.randint(int(min_val), int(max_val))))
global_context.define_function('length', BuiltInFunction(lambda s: len(str(s))))
global_context.define_function('substring', BuiltInFunction(lambda s, start, end: str(s)[int(start):int(end)]))
global_context.define_function('find', BuiltInFunction(lambda s, sub: str(s).find(str(sub))))
    
# Execute the parsed AST
try:
    execute(ast, global_context)
except Exception as e:
    print(e)