# SIGNED DISTANCE LANGUAGE

## Goal

The goal of this language is to abstract away the need for ray casting or ray marching in glsl implementations of renderers which use signed distance functions to render three dimensional scenes.

The language simplifies the process by requiring the user to define two main functions within the code: the **Signed Distance Function** and the  **Color Function** .

### Signed Distance Function

Each signed distance function should take a point in space (vec3) as input and return a single float representing the distance from the given point to the nearest surface in the scene.

Distances to surfaces are defined as positive values, representing the Euclidean distance from points outside the surface to the surface itself. For points lying within the surface, the distance is 0, and for points inside solid objects, the distance is represented as -1.

The backend renderer will employ the user-defined signed distance function within its volumetric integrator (also known as a ray marcher) to determine whether a specific pixel should be rendered onto the screen.

### Color Function

The color function should take a point in space (vec3) as input and return a vec4 representing the color that the point would have if rendered (with RGB values and alpha within the [0,1] interval).

For each pixel rendered on the screen, the renderer will consult the user-defined color function to determine the color that the pixel should have based on the position of the point being rendered as that pixel.

### The EBNF for SDL is as follows:

```ebnf
program = "#",PROGRAM_ARGUMENTS,BLOCK;
PROGRAM_ARGUMENTS = ARG,{',',ARG};
ARG = ('out' | 'in'), TYPE, IDENTIFIER , | 'opt', OPTION, INT;
OPTION = 'width'|'height'|'steps';
BLOCK = { STATEMENT };
TYPE = float | int | bool | vec2 | vec3 | vec4;
STATEMENT = ( |ASSIGNMENT |DECLARATION|WHILE | IF | FUNC_DEF | RETURN ), "\n" ;
FUNC_DEF ="function", IDENTIFIER, "(", ( | IDENTIFIER, { ( "," ), IDENTIFIER } ), ")", "\n", { ( STATEMENT ) }, "end";
FUNC_CALL = IDENTIFIER, "(", , ( | BOOL_EXP, { ( "," ), BOOL_EXP } ),")";
WHILE = "while", BOOL_EXP, "do", "\n", { ( STATEMENT )}, "end";
IF = "if", BOOL_EXP, "then", "\n", { ( STATEMENT )}, (  | ( "else", "\n",  { ( STATEMENT )})), "end" ;
ASSIGNMENT = IDENTIFIER, '=', BOOL_EXP;
DECLARATION = 'local', IDENTIFIER,('=', BOOL_EXP | );
RETURN = "return", BOOL_EXP;
BOOL_EXP = BOOL_TERM, { ("or"), BOOL_TERM } ;
BOOL_TERM = REL_EXP, { ("and"), REL_EXP } ;
REL_EXP = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION = TERM, {("+" | "-" | "**"), TERM};
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = INT | IDENTIFIER | FLOAT | vec2 | vec3 | vec4 | (("+" | "-" | "not"), FACTOR ) | "(", BOOL_EXP, ")"| FUNCTION_CALL | TRIG_FUNCS ;
vec2 = 'vec2','(',FLOAT,',',FLOAT,')';
vec3 = 'vec3','(',FLOAT,',',FLOAT,',',FLOAT,')';vec4 = 'vec4','(',FLOAT,',',FLOAT,',',FLOAT,')';
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" }, (PROPERTY_ACCESS |);
PROPERTY_ACCESS = '.', ('x'|'y'|'z'|'w');
INT =  DIGIT, { DIGIT };
FLOAT = INT,'.',INT;
LETTER = ( "a" | "..." | "z" | "A" | "..." | "Z" );
FUNCTION_CALL = IDENTIFIER,'(',{IDENTIFIER,','},')';
TRIG_FUNCS = ("sin" | "cos" | "tan"), "(", BOOL_EXP, ")"; 
```

and its diagram can be seen here:

![1717983465837](image/readme/1717983465837.png)

### Flex Bison

to run the flex bison simply make the executable running:

```bash
make
```
and then run the executable with the input file as argument:

```bash
./sdl input.sdl
```
If the input file is correct there should be no output, if there is a syntax error it will be printed to the console.

### Examples

example codes can be seen in the code_examples folder, and their respective outputs can be seen as the .png files in the same folder.


### Presentation

The presentation can be found in the "apresentacao" folder:

[apresentacao.pdf](https://github.com/AndreCorreaSantos/SDL/blob/main/apresentacao/apresentacao.pdf)