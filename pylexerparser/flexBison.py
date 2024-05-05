from rply import LexerGenerator, ParserGenerator
from lexer import lg

lexer = lg.build() # PERGUNTAS: COMO FAZER ACESSO DE PROPRIEDADE, OS TIPOS WHILE IF DO NEWLINE ETC ESTAO CORRETOS? DEVO DEFINIR TODOS ESSES TIPOS?

pg = ParserGenerator([
    'PROGRAM_START', 'IN', 'OUT', 'TYPE', 'IDENTIFIER', 'INT', 'FLOAT', 'COMMA', 'LPAREN', 'RPAREN', 'EQUALS', 
    'GREATER', 'LESS', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN', 'FUNC', 'LBRACE', 'RBRACE', 'LOCAL', 
    'WHILE', 'IF', 'THEN', 'ELSE', 'END', 'AND', 'OR', 'NOT', 'NEWLINE', 'POWER','DO', 'RETURN', 'BOOL'
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

@pg.production("func_call_args : fcall_types COMMA func_call_args | fcall_types | ")
def func_call_args(p):
    print(p)

@pg.production("fcall_types : INT | IDENTIFIER | FLOAT | BOOL ")
def fcall_types(p):
    pass


@pg.production("func_arg : TYPE IDENTIFIER")
def func_arg(p):
    print(p)

# Block definition
@pg.production("block : newlines statement block")
@pg.production("block : ")
def block(p):
    pass

# Statement types
@pg.production("statement : assignment_statement newlines | declaration_statement newlines | while_statement newlines | if_statement newlines | return_statement newlines")
def statement(p):
    pass

# Assignment statement
@pg.production("assignment_statement : IDENTIFIER ASSIGN bool_exp")
def assignment_statement(p):
    pass

# Return statement
@pg.production("return_statement : RETURN bool_exp")
def return_statement(p):
    pass
# Declaration statement
@pg.production("declaration_statement : LOCAL IDENTIFIER")
def declaration_statement(p):
    pass

# While statement
@pg.production("while_statement : WHILE bool_exp DO block END")
def while_statement(p):
    pass

# If statement
@pg.production("if_statement : IF bool_exp THEN block END | IF bool_exp THEN block ELSE block END")
def if_statement(p):
    pass

# Boolean expressions
@pg.production("bool_exp : bool_term OR bool_term | bool_term")
def bool_exp(p):
    pass

@pg.production("bool_term : rel_exp AND rel_exp | rel_exp")
def bool_term(p):
    pass

@pg.production("rel_exp : expression EQUALS expression | expression GREATER expression | expression LESS expression | expression")
def rel_exp(p):
    pass

@pg.production("expression : term PLUS term | term MINUS term | term POWER term | term")
def expression(p):
    pass

# Term structure
@pg.production("term : factor MULTIPLY factor | term DIVIDE factor | factor")
def term(p):
    pass

@pg.production("factor : INT | FLOAT | constructors | IDENTIFIER | LPAREN expression RPAREN | function_call | PLUS factor | MINUS factor | NOT factor")
def factor(p):
    pass

@pg.production("constructors : TYPE LPAREN func_call_args RPAREN")
def constructors(p):
    pass

@pg.production("function_call : IDENTIFIER LPAREN func_call_args RPAREN")
def function_call(p):
    pass


parser = pg.build()

# Example input
input_string = """
#out vec3 teste, in vec2 testando

def teste(){

while teste do
local u
u = vec3(1.0,1.0)
end

return teste
}
"""

# Parse and process tokens
tokens = lexer.lex(input_string)

# Run the parser
result = parser.parse(tokens)
