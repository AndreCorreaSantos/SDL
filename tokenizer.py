NUM = 2
SPACE = 3
EOF = 4
MUL = 5
DIV = 6
PLUS = 7
MINUS = 8
OPEN_PAR = 9
CLOSE_PAR = 10
CHAR = 12
ASSIGN = 13
IDENTIFIER = 14
NEWLINE = 15
ERROR = 16
NOT = 17
AND = 18
OR = 19
EQUALS = 20
BIGGER = 21
LESSER = 22
STR = 23
CONCAT = 24
COMMA = 25
FLOAT = 26
DOT = 27
POW = 28

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self):
        if self.position >= len(self.source):
            self.next = Token("", EOF)
            return

        while (self.position < len(self.source) and self.source[self.position].isspace() and self.source[self.position] != "\n"):
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("", EOF)
            return

        current_char = self.source[self.position]
        token_type = self.get_tipo(current_char)

        if token_type in [PLUS, MINUS, MUL, DIV, CLOSE_PAR, OPEN_PAR, COMMA, NEWLINE, ASSIGN, BIGGER, LESSER, POW]:
            self.next = Token(current_char, token_type)
            self.position += 1
        elif token_type == NUM:
            self.position += 1
            num_str = current_char
            while self.position < len(self.source) and (self.source[self.position].isdigit() or self.source[self.position] == '.'):
                if self.source[self.position] == '.':
                    if self.position + 1 < len(self.source) and self.source[self.position + 1].isdigit():
                        num_str += self.source[self.position]
                    else:
                        break
                else:
                    num_str += self.source[self.position]
                self.position += 1
            if '.' in num_str:
                self.next = Token(num_str, FLOAT)
            else:
                self.next = Token(num_str, NUM)
        elif token_type == STR:
            self.position += 1  # Skip initial quote
            start = self.position
            while self.position < len(self.source) and self.source[self.position] != '"':
                self.position += 1
            self.next = Token(self.source[start:self.position], STR)
            self.position += 1  # Skip closing quote
        elif token_type == CHAR:
            ident = current_char
            self.position += 1
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position] == '_' or self.source[self.position].isdigit()):
                ident += self.source[self.position]
                self.position += 1
            if ident == "not":
                self.next = Token(ident, NOT)
            elif ident == "and":
                self.next = Token(ident, AND)
            elif ident == "or":
                self.next = Token(ident, OR)
            else:
                self.next = Token(ident, IDENTIFIER)
        elif token_type == CONCAT:
            self.position += 1
            if self.position < len(self.source) and self.source[self.position] == '.':
                self.next = Token('..', CONCAT)
                self.position += 1
            else:
                self.next = Token('.', DOT)
        elif token_type == ASSIGN:
            self.position += 1
            if self.position < len(self.source) and self.source[self.position] == '=':
                self.next = Token("==", EQUALS)
                self.position += 1
            else:
                self.position -= 1
                self.next = Token(current_char, ASSIGN)
                self.position += 1
        else:
            raise SyntaxError("Unknown character encountered: " + current_char)

    def get_tipo(self, i):
        if i == "+":
            return PLUS
        if i == "-":
            return MINUS
        if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return NUM
        if i == "*":
            return MUL
        if i == "^":
            return POW
        if i == "/":
            return DIV
        if i == "(":
            return OPEN_PAR
        if i == ")":
            return CLOSE_PAR
        if i == ",":
            return COMMA
        if i.isalpha() or i == "_":
            return CHAR
        if i == ".":
            return CONCAT
        if i == "\n":
            return NEWLINE
        if i == "=":
            return ASSIGN
        if i == "<":
            return LESSER
        if i == ">":
            return BIGGER
        if i == '"':
            return STR
        else:
            return ERROR