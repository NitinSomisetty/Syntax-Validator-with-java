#!/usr/bin/env python3
"""
Single-file Java Syntax Validator (lexer + parser + CLI)
"""
import sys
import ply.lex as lex
import ply.yacc as yacc

# ----------------------
# Lexer (tokens + rules)
# ----------------------

# the list of token and its names we need
tokens = (
    'ID',
    'NUMBER',

    # keywords
    'INT',
    'FLOAT',
    'DOUBLE',
    'CHAR',
    'BOOLEAN',
    'STRING',
    'VOID',
    'IF',
    'ELSE',
    'WHILE',
    'NEW',

    # operators
    'ASSIGN',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQ',
    'NE',
    'LT',
    'GT',
    'LE',
    'GE',
    'AND',
    'OR',
    'INCREMENT',
    'DECREMENT',

    # delimiters
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COMMA',
)

reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'char': 'CHAR',
    'boolean': 'BOOLEAN',
    'String': 'STRING',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'new': 'NEW',
}

# token regexes
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'

# delimiters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ignore whitespace and single-line comments
t_ignore = ' \t'
t_ignore_COMMENT = r'//.*'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# build lexer
lexer = lex.lex()

# ----------------------
# Parser (grammar rules)
# ----------------------

parsing_errors = []

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])
    print("Yes, Program syntax is valid")

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration
                | array_declaration
                | if_statement
                | while_statement
                | function_declaration
                | assignment_statement
                | increment_statement
                | decrement_statement'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : type ID SEMICOLON'''
    p[0] = ('declaration', p[1], p[2])
    print(f"Yes, Valid simple data-type declaration: {p[1]} {p[2]};")

def p_declaration_with_assignment(p):
    '''declaration : type ID ASSIGN expression SEMICOLON'''
    p[0] = ('declaration_assign', p[1], p[2], p[4])
    print(f"Yes, Valid declaration with assignment: {p[1]} {p[2]} = ...;")

def p_type(p):
    '''type : INT
           | FLOAT
           | DOUBLE
           | CHAR
           | BOOLEAN
           | STRING
           | VOID'''
    p[0] = p[1]

def p_array_declaration(p):
    '''array_declaration : type LBRACKET RBRACKET ID SEMICOLON
                        | type ID LBRACKET RBRACKET SEMICOLON'''
    if p[2] == '[':
        name = p[4]
    else:
        name = p[2]
    p[0] = ('array_declaration', p[1], name)
    print(f"Yes, Valid array declaration: {p[1]}[] {name};")

def p_array_declaration_with_init(p):
    '''array_declaration : type LBRACKET RBRACKET ID ASSIGN NEW type LBRACKET NUMBER RBRACKET SEMICOLON'''
    p[0] = ('array_init', p[1], p[4], p[9])
    print(f"Yes, Valid array declaration with initialization: {p[1]}[] {p[4]} = new {p[7]}[{p[9]}];")

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN block'''
    p[0] = ('if', p[3], p[5])
    print("Yes, Valid if statement")

def p_if_else_statement(p):
    '''if_statement : IF LPAREN condition RPAREN block ELSE block'''
    p[0] = ('if_else', p[3], p[5], p[7])
    print("Yes, Valid if-else statement")

def p_condition(p):
    '''condition : expression relational_op expression
                | expression'''
    if len(p) == 4:
        p[0] = ('condition', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_relational_op(p):
    '''relational_op : LT
                    | GT
                    | LE
                    | GE
                    | EQ
                    | NE
                    | AND
                    | OR'''
    p[0] = p[1]

def p_block(p):
    '''block : LBRACE statement_list RBRACE
            | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = ('block', p[2])
    else:
        p[0] = ('block', [])

def p_while_statement(p):
    '''while_statement : WHILE LPAREN condition RPAREN block'''
    p[0] = ('while', p[3], p[5])
    print("Yes, Valid while loop")

def p_function_declaration(p):
    '''function_declaration : type ID LPAREN parameter_list RPAREN block'''
    p[0] = ('function', p[1], p[2], p[4], p[6])
    print(f"Yes, Valid function declaration: {p[1]} {p[2]}(...)")

def p_parameter_list(p):
    '''parameter_list : parameter
                     | parameter_list COMMA parameter
                     | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    '''parameter : type ID'''
    p[0] = ('param', p[1], p[2])

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_increment_statement(p):
    '''increment_statement : ID INCREMENT SEMICOLON'''
    p[0] = ('increment', p[1])

def p_decrement_statement(p):
    '''decrement_statement : ID DECREMENT SEMICOLON'''
    p[0] = ('decrement', p[1])

def p_expression(p):
    '''expression : ID
                  | NUMBER
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | ID INCREMENT
                  | ID DECREMENT
                  | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[2], p[1])
    elif len(p) == 4:
        if p[1] == '(': 
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        error_msg = f"unexpected token -> {p.value}"
        parsing_errors.append(error_msg)
        print("Error:", error_msg)
    else:
        error_msg = "unexpected end of input"
        parsing_errors.append(error_msg)
        print("Error:", error_msg)

# build parser
parser = yacc.yacc()

def parse_code(code):
    global parsing_errors
    parsing_errors = []
    print("----- Starting Syntax Check -----")
    result = parser.parse(code, lexer=lexer)
    print("----- Parsing Complete -----")

    if parsing_errors:
        print("Syntax errors found:")
        for err in parsing_errors:
            print("-", err)
    else:
        print("No syntax errors detected. Code is valid.")

    return result, parsing_errors

def validate_file(filename):
    try:
        with open(filename, 'r') as f:
            code = f.read()
        print(f"\nValidating {filename}...\n")
        result, errors = parse_code(code)
        print("\nValidation complete.")
        return len(errors) == 0
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python java_syntax_validator.py <java_file>")
        sys.exit(1)
    filename = sys.argv[1]
    success = validate_file(filename)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
