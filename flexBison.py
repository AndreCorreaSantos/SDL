from rply import LexerGenerator, ParserGenerator
from lexer import lg

lexer = lg.build()

pg = ParserGenerator([
    'PROGRAM_START', 'IN', 'OUT', 'TYPE', 'IDENTIFIER', 'INT', 'FLOAT', 'COMMA', 'LPAREN', 'RPAREN', 'EQUALS', 
    'GREATER', 'LESS', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN', 'FUNC', 'LBRACE', 'RBRACE', 'LOCAL', 
    'WHILE', 'IF', 'THEN', 'ELSE', 'END', 'AND', 'OR', 'NOT', 'NEWLINE', 'POWER'
])

# Program definition
@pg.production("program : newlines PROGRAM_START program_args functions")
def program(p):
    print(p)

@pg.production("functions : newlines functions | function functions | function | ")
def functions(p):
    print(p)

@pg.production("newlines : NEWLINE newlines | NEWLINE")
@pg.production("newlines : ")
def newlines(p):
    print(p)

# Program arguments
@pg.production("program_args : IN func_arg COMMA program_args | OUT func_arg COMMA program_args ")
@pg.production("program_args : OUT func_arg | IN func_arg")
def program_args(p):
    print(p)

# Function definition
@pg.production("function : FUNC IDENTIFIER LPAREN func_args RPAREN LBRACE block RBRACE")
def function(p):
    print(p)

@pg.production("func_args : func_arg COMMA func_args")
@pg.production("func_args : func_arg")
@pg.production("func_args : ")
def func_args(p):
    print(p)

@pg.production("func_call_args : IDENTIFIER COMMA func_call_args | IDENTIFIER | ")
def func_call_args(p):
    print(p)

@pg.production("func_arg : TYPE IDENTIFIER")
def func_arg(p):
    print(p)

# Block definition
@pg.production("block : newlines statement block")
@pg.production("block : ")
def block(p):
    pass

# Statement types
@pg.production("statement : assignment_statement newlines | declaration_statement newlines ")
# @pg.production("statement : while_statement")
# @pg.production("statement : if_statement")
def statement(p):
    pass

# Assignment statement
@pg.production("assignment_statement : IDENTIFIER ASSIGN factor")
def assignment_statement(p):
    pass

# Declaration statement
@pg.production("declaration_statement : LOCAL IDENTIFIER ASSIGN factor")
def declaration_statement(p):
    pass

# # While statement
# @pg.production("while_statement : WHILE bool_exp NEWLINE block END")
# def while_statement(p):
#     pass

# # If statement
# @pg.production("if_statement : IF bool_exp NEWLINE block THEN statement END")
# @pg.production("if_statement : IF bool_exp NEWLINE block THEN statement ELSE NEWLINE statement END")
# def if_statement(p):
#     pass

# Boolean expressions
# @pg.production("bool_exp : bool_term OR bool_term | bool_term")
# def bool_exp(p):
#     pass

# @pg.production("bool_term : rel_exp AND rel_exp | rel_exp")
# def bool_term(p):
#     pass

# @pg.production("rel_exp : expression EQUALS expression | expression GREATER expression | expression LESS expression | expression")
# def rel_exp(p):
#     pass

# @pg.production("expression : term PLUS term | term MINUS term | term POWER term | term")
# def expression(p):
#     pass

# # Term structure
# @pg.production("term : factor MULTIPLY factor | term DIVIDE factor | factor")
# def term(p):
#     pass

# @pg.production("factor : INT | FLOAT | IDENTIFIER | LPAREN expression RPAREN | function_call")
# @pg.production("factor : INT | FLOAT | IDENTIFIER | LPAREN expression RPAREN | function_call")
@pg.production("factor : INT | FLOAT | IDENTIFIER | function_call")
def factor(p):
    pass

@pg.production("function_call : IDENTIFIER LPAREN func_call_args RPAREN")
def function_call(p):
    pass

parser = pg.build()

# Example input
input_string = """
#out vec3 teste, in vec2 testando

def teste(){

testando = teste(teste1,teste2)

}
"""

# Parse and process tokens
tokens = lexer.lex(input_string)

# Run the parser
result = parser.parse(tokens)
