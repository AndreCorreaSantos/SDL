import sys
import re
from tokenizer import *
from vectors import Vec2, Vec3, Vec4
import numpy as np
import matplotlib.pyplot as plt
from helpers import *
import copy
import concurrent.futures

reserved_words = ["print", "if", "while"]


class SymbolTable:
    def __init__(self):
        self.variables = {}

    def get(self, key):
        return self.variables[key]

    def set(self, key, value):
        if key not in self.variables.keys():
            raise RuntimeError("Variable not declared")
        self.variables[key] = value

    def create(self, key, value):
        if key in self.variables.keys():
            raise RuntimeError("Variable already declared")
        if key in reserved_words:
            raise RuntimeError("Variable name is reserved")
        self.variables[key] = value

    def clean(self):
        self.variables = {}


class FuncTable:
    def __init__(self):
        self.functions = {}

    def get(self, key):
        return self.functions[key]

    def set(self, key, value):
        if key in self.functions.keys():
            raise RuntimeError("Function already declared")
        self.functions[key] = value





class PrePro:
    @staticmethod
    def filter(source):
        return re.sub(r"--.*?\n", "\n", source)


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = (
            children if children is not None else []
        )  # lista vazia de nodes caso children seja None

    def Evaluate(self, table):
        pass


class BinOp(Node):
    def Evaluate(self, table):
        child1, type1 = self.children[0].Evaluate(table)
        child2, type2 = self.children[1].Evaluate(table)

        def check_vector_and_scalar(op_type1, op_type2):
            if "vec" in op_type1 and ("int" in op_type2 or "float" in op_type2):
                return True
            elif "vec" in op_type2 and ("int" in op_type1 or "float" in op_type1):
                return True
            return False

        if type1 != type2 and not check_vector_and_scalar(type1, type2) and self.value not in ("..", "==","^"):
            print(child1, child2)
            raise RuntimeError(f"Unsupported operation between {type1} and {type2}")

        def result_type():
            if "vec" in type1 or "vec" in type2:
                if type1 == type2 or check_vector_and_scalar(type1, type2):
                    return type1 if "vec" in type1 else type2
                else:
                    raise RuntimeError("Vector operations require vectors of the same type or a scalar")
            elif "float" in (type1, type2):
                return "float"
            return "int"

        if self.value == "+":
            result = (child1 + child2, result_type())
        elif self.value == "-":
            result = (child1 - child2, result_type())
        elif self.value == "*":
            result = (child1 * child2, result_type())
        elif self.value == "/":
            if type1 == "float" or type2 == "float":
                result = (child1 / child2, "float")  # Floating point division
            else:
                result = (child1 // child2, "int")  # Integer division
        elif self.value == "or":
            result = (child1 or child2, result_type())
        elif self.value == "==":
            result = (child1 == child2, "int")
        elif self.value == "<":
            result = (child1 < child2, "int")
        elif self.value == ">":
            result = (child1 > child2, "int")
        elif self.value == "and":
            result = (child1 and child2, result_type())
        elif self.value == "..":
            result = (str(child1) + str(child2), "str")
        elif self.value == "^":
            if "vec" in (type1, type2):
                raise RuntimeError("Exponentiation not defined for vectors")
            result = (pow(child1, child2), "float" if "float" in (type1, type2) else "int")
        else:
            raise RuntimeError("Unknown operation")

        return result



class UnOp(Node):
    def Evaluate(self, table):
        child1, type = self.children.Evaluate(table)  # CONSERTAR TIPOS AQUI
        if self.value == "+":
            result = (child1, type)
        elif self.value == "-":
            result = (-child1, type)
        elif self.value == "not":
            result = (not child1, type)
        else:
            raise SyntaxError("ta estranho")  # nao é para chegar aqui

        return result


class IntVal(Node):
    def Evaluate(self, table):
        return (int(self.value), "int")

class FloatVal(Node):
    def Evaluate(self, table):
        return (float(self.value), "float")

    
class Vec2Val(Node):
    def __init__(self, x, y):
        super().__init__(None, [])
        self.x = x
        self.y = y

    def Evaluate(self, table):
        self.x = self.x.Evaluate(table)
        self.y = self.y.Evaluate(table)
        return (Vec2(float(self.x[0]), float(self.y[0])), 'vec2')

class Vec3Val(Node):
    def __init__(self, x, y, z):
        super().__init__(None, [])
        self.x = x
        self.y = y
        self.z = z

    def Evaluate(self, table):

        self.x = self.x.Evaluate(table)
        self.y = self.y.Evaluate(table)
        self.z = self.z.Evaluate(table)
        return (Vec3(float(self.x[0]), float(self.y[0]), float(self.z[0])), 'vec3')

class Vec4Val(Node):
    def __init__(self, x, y, z, w):
        super().__init__(None, [])
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def Evaluate(self, table):
        self.x = self.x.Evaluate(table)
        self.y = self.y.Evaluate(table)
        self.z = self.z.Evaluate(table) 
        self.w = self.w.Evaluate(table)
        return (Vec4(float(self.x[0]), float(self.y[0]), float(self.z[0]), float(self.w[0])), 'vec4')



class StrVal(Node):
    def Evaluate(self, table):
        return (self.value, "str")


class Identifier(Node):
    def Evaluate(self, table):
        if self.children: # Vector property access
            vector = table.get(self.value)
            property_name = self.children[0].value
            if hasattr(vector, property_name):
                return getattr(vector, property_name), type(vector).__name__
            else:
                raise AttributeError("Property not found in vector")
        else:
            return table.get(self.value)
        
class PropertyAccess(Node):
    def __init__(self, identifier, property_name):
        super().__init__(None, [])
        self.identifier = identifier
        self.property_name = property_name

    def Evaluate(self, table):
        vector = self.identifier.Evaluate(table)[0]
        if hasattr(vector, self.property_name):
            return getattr(vector, self.property_name), type(vector).__name__
        else:
            raise AttributeError(f"Property {self.property_name} not found on vector")



class Block(Node):
    def Evaluate(self, table):
        for children in self.children:
            if isinstance(children, Return):
                return children.Evaluate(table)
                
            children.Evaluate(table)


class Assign(Node):
    def Evaluate(self, table):
        if isinstance(self.children[0], PropertyAccess):
            vector, _ = self.children[0].identifier.Evaluate(table)
            value, _ = self.children[1].Evaluate(table)
            setattr(vector, self.children[0].property_name, value)
            table.set(self.children[0].identifier.value, vector)
        else:
            value, _ = self.children[1].Evaluate(table)
            table.set(self.value, value)



class Read(Node):
    def Evaluate(self, table):
        return (int(input()), "int")


class Print(Node):
    def Evaluate(self, table):
        value = self.children.Evaluate(table)
        print(value[0])


class While(Node):

    def Evaluate(self, table):
        while self.children[0].Evaluate(table)[0]:
            for child in self.children[1]:
                child.Evaluate(table)


class If(Node):
    def Evaluate(self, table):
        bool_res, type = self.children[0].Evaluate(table)

        if len(self.children) > 2:
            if bool_res:
                return self.children[1].Evaluate(table)
            else:
                return self.children[2].Evaluate(table)
        else:
            if bool_res:
                return self.children[1].Evaluate(table)


class VarDec(Node):
    def Evaluate(self, table):
        bool_res = None
        if len(self.children) > 0:
            bool_res = self.children[0].Evaluate(table)
        table.create(self.value, bool_res)
        return self.value


class NoOp(Node):
    def Evaluate(self, table):
        pass


class Return(Node):
    def Evaluate(self, table):
        return self.children.Evaluate(table)


class FuncDec(Node):
    def Evaluate(self, table):
        funcTable.set(self.value, self)  # nome da função vem no valor do node


class FuncCall(Node):
    def Evaluate(self, table):
        func = funcTable.get(self.value)  # identificador da funcao vem no valor do node

        func_args, block = (
            func.children[0:-1],
            func.children[-1],
        )  # argumentos da funcao e bloco da funcao

        call_args = self.children  # argumentos da chamada de funcao

        if len(func_args) != len(call_args):
            raise RuntimeError("Invalid number of arguments")

        internal_table = SymbolTable()
        for i in range(len(func_args)):
            key = func_args[i].Evaluate(internal_table)
            internal_table.set(key, call_args[i].Evaluate(table))  # ISSO AQUI TA CERTO

        return block.Evaluate(internal_table)


class Parser:
    def __init__(self):
        self.tokenizer = None

    #### BOOLEANS

    def bool_expression(self):
        result = self.bool_term()
        while self.tokenizer.next.type == OR:
            val = self.tokenizer.next.value
            self.tokenizer.select_next()
            result = BinOp(val, [result, self.bool_term()])

        return result

    def bool_term(self):
        result = self.rel_exp()
        while self.tokenizer.next.type == AND:
            val = self.tokenizer.next.value
            self.tokenizer.select_next()
            result = BinOp(val, [result, self.rel_exp()])

        return result

    def rel_exp(self):
        result = self.parse_expression()
        while self.tokenizer.next.type in [EQUALS, BIGGER, LESSER]:
            val = self.tokenizer.next.value
            self.tokenizer.select_next()
            result = BinOp(val, [result, self.parse_expression()])

        return result

    ####-------------------------------
    def factor(self):
        next = self.tokenizer.next
        if next.type == IDENTIFIER:
            # Handle vector initialization 
            if next.value.startswith("vec"):
                vector_size = int(next.value[3:])  # Extracts the '2', '3', or '4' from vec2, vec3, vec4
                self.tokenizer.select_next()
                if self.tokenizer.next.type != OPEN_PAR:
                    raise SyntaxError("Expecting '(' after vector type")
                self.tokenizer.select_next()
                elements = []
                if self.tokenizer.next.type != CLOSE_PAR:
                    elements.append(self.parse_expression())
                    while self.tokenizer.next.type == COMMA:
                        self.tokenizer.select_next()
                        elements.append(self.parse_expression())

                if len(elements) != vector_size:
                    raise SyntaxError(f"Expected {vector_size} elements for {next.value}")
                if self.tokenizer.next.type != CLOSE_PAR:
                    raise SyntaxError("Expecting ')' after vector elements")
                self.tokenizer.select_next()
                if vector_size == 2:
                    return Vec2Val(elements[0], elements[1])
                elif vector_size == 3:
                    return Vec3Val(elements[0], elements[1], elements[2])
                elif vector_size == 4:
                    return Vec4Val(elements[0], elements[1], elements[2], elements[3])

            self.tokenizer.select_next()
            if self.tokenizer.next.type == DOT:
                self.tokenizer.select_next()
                if self.tokenizer.next.type == IDENTIFIER:
                    property_name = self.tokenizer.next.value
                    self.tokenizer.select_next()
                    return PropertyAccess(Identifier(next.value, None), property_name)
            elif self.tokenizer.next.type == OPEN_PAR:  # CHAMADA DE FUNCAO COM RETORNO DE VALOR
                args = []  # primeiro filho vai ser o identificador da funcao
                self.tokenizer.select_next()
                if self.tokenizer.next.type != CLOSE_PAR:
                    args.append(self.parse_expression())
                    while self.tokenizer.next.type == COMMA:
                        self.tokenizer.select_next()
                        args.append(self.parse_expression())
                if self.tokenizer.next.type != CLOSE_PAR:
                    raise SyntaxError("Expecting closing parenthesis after function arguments")
                self.tokenizer.select_next()
                return FuncCall(next.value, args)
            else:
                return Identifier(next.value, None)

        if next.type == STR:
            val = next.value
            self.tokenizer.select_next()
            return StrVal(val, None)
        if next.type == NUM:
            val = next.value
            self.tokenizer.select_next()
            return IntVal(val, None)
        if next.type == FLOAT:
            val = next.value
            self.tokenizer.select_next()
            return FloatVal(val, None)
        if next.type == PLUS:
            self.tokenizer.select_next()
            return UnOp("+", self.factor())
        if next.type == MINUS:
            self.tokenizer.select_next()
            return UnOp("-", self.factor())
        if next.type == NOT:
            self.tokenizer.select_next()
            return UnOp("not", self.factor())
        elif next.type == OPEN_PAR:
            self.tokenizer.select_next()
            result = self.parse_expression()
            if self.tokenizer.next.type != CLOSE_PAR:
                raise SyntaxError("No closing parenthesis")
            self.tokenizer.select_next()
            return result
        else:
            raise SyntaxError("Unexpected token")

    def power(self):
        node = self.factor()
        while self.tokenizer.next.type == POW:
            self.tokenizer.select_next()
            right = self.factor()
            node = BinOp('^', [node, right])
        return node

    def term(self):
        node = self.power()  # Instead of self.factor(), it should now start with self.power()
        while self.tokenizer.next.type in [MUL, DIV]:
            if self.tokenizer.next.type == MUL:
                self.tokenizer.select_next()
                node = BinOp('*', [node, self.power()])
            elif self.tokenizer.next.type == DIV:
                self.tokenizer.select_next()
                node = BinOp('/', [node, self.power()])
        return node

    def parse_expression(self):
        result = self.term()
        while self.tokenizer.next.type in [PLUS, MINUS, CONCAT]:
            if self.tokenizer.next.type == PLUS:
                self.tokenizer.select_next()
                result = BinOp("+", [result, self.term()])
            elif self.tokenizer.next.type == MINUS:
                self.tokenizer.select_next()
                result = BinOp("-", [result, self.term()])
            elif self.tokenizer.next.type == CONCAT:
                self.tokenizer.select_next()
                result = BinOp("..", [result, self.factor()])
            else:
                raise SyntaxError(" Invalid expression")

        return result

    def call_if(self):  # LEMBRAR DE CONSERTAR IF PARA CASO O IF ESTEJA VAZIO, PUXAR DA VERSAO FINAL
        self.tokenizer.select_next()
        bool_result = self.bool_expression()  #  expressao booleana
        if self.tokenizer.next.value != "then":
            raise SyntaxError("Expected then after 'if' condition")
        self.tokenizer.select_next()
        if self.tokenizer.next.type != NEWLINE:
            raise SyntaxError("Expected newline after 'if' condition")

        self.tokenizer.select_next()  # pulando \n

        statement1 = self.parse_statement()  # bloco true
        childs = [bool_result, statement1]

        if self.tokenizer.next.type != NEWLINE:
            raise SyntaxError("Expected newline after statement")
        self.tokenizer.select_next()

        if self.tokenizer.next.value == "else":
            self.tokenizer.select_next()  # pulando else
            if self.tokenizer.next.type != NEWLINE:
                raise SyntaxError("Expected newline after statement")
            self.tokenizer.select_next()  # pulando newline
            statement2 = self.parse_statement()
            childs.append(statement2)
            self.tokenizer.select_next()

        if self.tokenizer.next.value != "end":
            raise SyntaxError("Expected 'end' after 'if'")
        self.tokenizer.select_next()

        return If(None, childs)  # Retornando node

    def call_while(self):

        self.tokenizer.select_next()
        bool_exp = self.bool_expression()

        if self.tokenizer.next.value == "do":
            self.tokenizer.select_next()
        else:
            raise SyntaxError("""No "do" after while expression""")

        if self.tokenizer.next.type == NEWLINE:
            self.tokenizer.select_next()
        else:
            raise SyntaxError("No newline after do")

        childs = []
        while self.tokenizer.next.value != "end":
            childs.append(self.parse_statement())
            self.tokenizer.select_next()

        return While(None, [bool_exp, childs])

    def call_print(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type == OPEN_PAR:
            self.tokenizer.select_next()
            expression = self.bool_expression()

            if self.tokenizer.next.type == CLOSE_PAR:
                self.tokenizer.select_next()
                if self.tokenizer.next.value == "\n":
                    return Print(None, expression)
                else:
                    raise SyntaxError("Sem \\n no final")
            else:
                raise SyntaxError("Sintaxe errada de print2")
        else:
            raise SyntaxError("Sintaxe errada de print1")

    def call_funcDec(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type != IDENTIFIER:
            raise SyntaxError("Expecting identifier after function declaration")

        children = []
        ident = self.tokenizer.next.value  # NOME DA FUNCAO
        self.tokenizer.select_next()

        if self.tokenizer.next.type != OPEN_PAR:
            raise SyntaxError("Expecting opening parenthesis after function identifier")
        self.tokenizer.select_next()

        # processando argumentos
        if self.tokenizer.next.type != CLOSE_PAR:
            children.append(
                VarDec(self.tokenizer.next.value, None)
            )  # primeiro argumento da funcao
            self.tokenizer.select_next()
            while self.tokenizer.next.type == COMMA:
                self.tokenizer.select_next()
                if self.tokenizer.next.type != IDENTIFIER:
                    raise SyntaxError("Expecting identifier after comma")
                children.append(VarDec(self.tokenizer.next.value, None))
                self.tokenizer.select_next()

        if self.tokenizer.next.type != CLOSE_PAR:
            raise SyntaxError("Expecting closing parenthesis after function arguments")

        # processando bloco
        self.tokenizer.select_next()
        if self.tokenizer.next.type != NEWLINE:
            raise SyntaxError("Expecting newline after function arguments")
        self.tokenizer.select_next()
        block_childs = []
        while self.tokenizer.next.value != "end":
            block_childs.append(self.parse_statement())
            self.tokenizer.select_next()

        children.append(Block(None, block_childs))

        return FuncDec(ident, children)

    def call_return(self):
        self.tokenizer.select_next()
        expression = self.bool_expression()
        if self.tokenizer.next.type != NEWLINE:
            raise SyntaxError("Sem \\n no final")
        return Return(None, expression)
    

    def parse_directive(self):
        if self.tokenizer.next.type != IDENTIFIER:
            raise SyntaxError("Expecting identifier after directive")
    
        if self.tokenizer.next.value == "in":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != IDENTIFIER:
                raise SyntaxError("Expecting identifier after 'in'")
            if self.tokenizer.next.value != "vec3":
                raise SyntaxError("All programs must receive a vec3 input")
            
            self.tokenizer.select_next()

            global in_variable_name
            in_variable_name = self.tokenizer.next.value
            
        elif self.tokenizer.next.value == "out":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != IDENTIFIER:
                raise SyntaxError("Expecting identifier after 'out'")
            
            if self.tokenizer.next.value == "vec3":
                self.tokenizer.select_next()
                global out_color_name
                out_color_name = self.tokenizer.next.value
            elif self.tokenizer.next.value == "float":
                self.tokenizer.select_next()
                global out_distance_name
                out_distance_name = self.tokenizer.next.value
            else:
                raise SyntaxError("Output must be of type vec3 or float")
        
        elif self.tokenizer.next.value == "opt":
            self.tokenizer.select_next()
            if self.tokenizer.next.value == "width":
                self.tokenizer.select_next()
                if self.tokenizer.next.type != NUM:
                    raise SyntaxError("Expecting number after 'opt_width'")
                global opt_width
                opt_width = int(self.tokenizer.next.value)

            elif self.tokenizer.next.value == "height":
                self.tokenizer.select_next()
                if self.tokenizer.next.type != NUM:
                    raise SyntaxError("Expecting number after 'height'")
                global opt_height
                opt_height = int(self.tokenizer.next.value)
            
            elif self.tokenizer.next.value == "steps":
                self.tokenizer.select_next()
                if self.tokenizer.next.type != NUM:
                    raise SyntaxError("Expecting number after 'steps'")
                
                global opt_steps
                opt_steps = int(self.tokenizer.next.value)
            
            else:
                raise SyntaxError("Invalid option")
            
        
        else:
            print(self.tokenizer.next.value)
            raise SyntaxError("Invalid directive")

    def parse_statement(self):
        if self.tokenizer.next.value == "\n":
            return NoOp(None, None)
        elif self.tokenizer.next.type == DIRECTIVE: # compiler directive statements
            self.tokenizer.select_next()
            self.parse_directive()
            self.tokenizer.select_next()
            while self.tokenizer.next.type == COMMA:
                self.tokenizer.select_next()
                self.parse_directive()
                self.tokenizer.select_next()

            if self.tokenizer.next.type != NEWLINE:
                raise SyntaxError("Expecting newline after directive")
            

        elif self.tokenizer.next.type == IDENTIFIER:
            ident = self.tokenizer.next.value
            if ident == "print":  # checando se print
                return self.call_print()
            elif ident == "while":
                return self.call_while()
            elif ident == "if":
                return self.call_if()
            elif ident == "function":  # DECLARACAO DE FUNCAO
                return self.call_funcDec()
            elif ident == "return":
                return self.call_return()
            elif (
                ident == "local"
            ):  # se local, proximo ident tem que ser um nome de variavel
                self.tokenizer.select_next()
                ident = self.tokenizer.next.value

                if self.tokenizer.next.type != IDENTIFIER:
                    raise SyntaxError("Expecting identifier after local")

                self.tokenizer.select_next()
                child = []

                if self.tokenizer.next.type == ASSIGN:

                    self.tokenizer.select_next()
                    expression = self.bool_expression()

                    child.append(expression)

                if self.tokenizer.next.type != NEWLINE:
                    raise SyntaxError("Expecting newline after statement")

                return VarDec(ident, child)

            else:  # se nenhum dos anteriores, entao é assign
                ident = self.tokenizer.next.value
                self.tokenizer.select_next()
                if (
                    self.tokenizer.next.type == OPEN_PAR
                ):  # CHAMADA DE FUNCAO SEM RETORNO DE VALOR
                    # parsing args
                    args = []
                    self.tokenizer.select_next()
                    if self.tokenizer.next.type != CLOSE_PAR:
                        args.append(self.bool_expression())
                        while self.tokenizer.next.type == COMMA:
                            self.tokenizer.select_next()
                            args.append(self.bool_expression())
                        # NAO SEI SE PRECISO DAR SELF.TOKENIZER .SELECT_NEXT() AQUI

                    if self.tokenizer.next.type != CLOSE_PAR:
                        raise SyntaxError(
                            "Expecting closing parenthesis after function arguments"
                        )
                    self.tokenizer.select_next()
                    if self.tokenizer.next.type != NEWLINE:
                        raise SyntaxError("Expecting newline after statement")

                    return FuncCall(ident, args)  # RETORNANDO NODE DE CHAMADA DE FUNCAO

                elif self.tokenizer.next.type == ASSIGN:
                    self.tokenizer.select_next()
                    expression = self.parse_expression()
                    if self.tokenizer.next.type == NEWLINE:
                        return Assign(ident, expression)
                    else:
                        raise SyntaxError("Sem \\n no final")
                else:
                    raise SyntaxError("Sintaxe errada de assignment")
        else:
            raise SyntaxError("No statement")

    def parse_block(self):
        children = []
        while self.tokenizer.next.type != EOF:
            statement = self.parse_statement()
            self.tokenizer.select_next()
            if statement != None:
                children.append(statement)
        return Block(None, children)

    def run(self, source, fileName):
        count = 0
        
        # Parsing the block
        self.tokenizer = Tokenizer(source)
        self.tokenizer.select_next()
        original_block = self.parse_block()
        
        if ("in_variable_name" not in globals()) or "out_color_name" not in globals() or "out_distance_name" not in globals():
            raise RuntimeError("Input and output variables not defined")
        
        if "opt_steps" not in globals():
            opt_steps = 10
        else:
            opt_steps = globals()["opt_steps"]
        
        if "opt_width" not in globals():
            opt_width = 100
        else:
            opt_width = globals()["opt_width"]
        
        if "opt_height" not in globals():
            opt_height = 100
        else:
            opt_height = globals()["opt_height"]

        print(f"Rendering image with {opt_width}x{opt_height} pixels and {opt_steps} steps")

        aspect_ratio = opt_width / opt_height
        fov = np.pi / 3 
        camera_pos = np.array([0.0, 0.0, -5.0])
        image_data = np.zeros((opt_height, opt_width, 3), dtype=np.float32)
        total_pixels = opt_width * opt_height

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for x in range(opt_width):
                for y in range(opt_height):
                    futures.append(executor.submit(self.march, x, y, camera_pos, fov, original_block, aspect_ratio))

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                x, y, color = result
                image_data[x][y] = color
                # Update progress bar
                progress_bar(count, total_pixels, prefix='Progress:', suffix='Complete', length=50)
                count += 1

        # Save the image to a PNG file
        plt.imsave(fileName + ".png", image_data)

    def march(self, x, y, camera_pos, fov, original_block, aspect_ratio):
        
        px = (2 * (x + 0.5) / float(opt_width) - 1) * np.tan(fov / 2) * aspect_ratio
        py = (1 - 2 * (y + 0.5) / float(opt_height)) * np.tan(fov / 2)
        ray_dir = np.array([px, py, 1])
        ray_dir /= np.linalg.norm(ray_dir)  # Normalize the vector

        march_pos = np.copy(camera_pos)
        color = [0,0,0]
        for step in range(opt_steps):
            block = copy.deepcopy(original_block)
            point = march_pos + ray_dir * step
            
            global funcTable
            funcTable = FuncTable()
            table = SymbolTable()

            table.create(in_variable_name, (Vec3(*point),'vec3'))  
            block.Evaluate(table)
            
            dist = table.get(out_distance_name)[0]
            if dist < 0.01:  
                color = table.get(out_color_name)[0]
                color = [color.x, color.y, color.z]
                return x, y, color
            
            # Update march position along the ray
            march_pos += ray_dir * dist
        
        return x, y, color



if __name__ == "__main__":
    text = ""
    with open(sys.argv[1], "r") as file:
        text = file.read()
    source = PrePro.filter(text)
    parser = Parser()
    filename = sys.argv[1].split(".")[0]
    parser.run(source,filename)
