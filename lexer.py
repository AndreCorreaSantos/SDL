from rply import LexerGenerator

lg = LexerGenerator()

lg.add('PROGRAM_START', r'\#')
lg.add('IN', r'in')
lg.add('OUT', r'out')
lg.add('FUNC', r'def')
lg.add('LOCAL', r'local')  # nao sei se isso esta correto, checar depois
lg.add('WHILE', r'while')
lg.add('IF', r'if')
lg.add('THEN', r'then')
lg.add('ELSE', r'else')
lg.add('END', r'end')
lg.add('TYPE', r'(float|int|vec4|vec3|vec2|bool)')
lg.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
lg.add('FLOAT', r'\d*\.\d+')
lg.add('INT', r'\d+')
lg.add('BOOL', r'(true|false)')
lg.add('AND', r'and')
lg.add('OR', r'or')
lg.add('NOT', r'not')
lg.add('EQUALS', r'==')
lg.add('GREATER', r'>')
lg.add('LESS', r'<')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MULTIPLY', r'\*')
lg.add('DIVIDE', r'/')
lg.add('POWER', r'\*\*')
lg.add('ASSIGN', r'=')
lg.add('COMMA', r',')
lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.add('PROPERTY_ACCESS', r'\.(x(y(z(w)?)?)?)?') 
lg.add('LBRACE', r'\{')
lg.add('RBRACE', r'\}')
lg.add('NEWLINE', r'\n')
lg.ignore(r'[ \t]+')  # Ignore whitespace except newlines



if __name__ == '__main__':
    lexer = lg.build()

    input_string = """
def teste(){
local x
}
"""

    tokens = lexer.lex(input_string)

    for token in tokens:
        print(token)
