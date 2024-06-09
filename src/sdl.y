%{
#include <stdio.h>
extern FILE *yyin;
int yylex(void);
void yyerror(char *s);
%}

%union {
    char *identifier;
    int integer;
    double number;
    int boolean;
}

%token <identifier> IDENTIFIER
%token <number> FLOAT
%token <boolean> BOOL
%token <integer> INT
%token PROGRAM_START IN OUT TYPE VEC_TYPE FUNC LOCAL WHILE IF THEN ELSE END AND OR NOT DO RETURN PROPERTY OPT WIDTH HEIGHT STEPS
%token PLUS MINUS MULTIPLY DIVIDE ASSIGN EQUALS GREATER LESS LPAREN RPAREN COMMA POWER NEWLINE

%%

program
    : PROGRAM_START program_args block
    ;


/* newlines
    : NEWLINE newlines
    | NEWLINE
    |
    ; */

all_types
    : TYPE
    | VEC_TYPE
    ;

program_args
    : IN arg COMMA program_args
    | OUT arg COMMA program_args
    | OPT option INT COMMA program_args
    | OUT arg
    | IN arg
    | OPT option INT
    ;

option
    : WIDTH
    | HEIGHT
    | STEPS
    ;

arg 
    : all_types IDENTIFIER
    ; 

block
    : statement block
    | statement
    ;

statement
    :
    | dec_assign_statement
    | while_statement
    | if_statement
    | return_statement
    | function_definition
    ;


dec_assign_statement
    : LOCAL IDENTIFIER
    | LOCAL IDENTIFIER ASSIGN bool_exp
    | IDENTIFIER ASSIGN bool_exp
    ;


function_definition
    : FUNC IDENTIFIER LPAREN func_args RPAREN block END
    ;

func_args
    : func_arg COMMA func_args
    | func_arg
    | 
    ;

func_call_args
    : bool_exp COMMA func_call_args
    | bool_exp
    | 
    ;

func_arg
    : IDENTIFIER
    ;


while_statement
    : WHILE bool_exp DO block END
    ;

if_statement
    : IF bool_exp THEN block END
    | IF bool_exp THEN block ELSE block END
    ;

return_statement
    : RETURN bool_exp
    | RETURN
    ;

bool_exp
    : bool_exp OR bool_term
    | bool_term
    ;

bool_term
    : bool_term AND rel_exp
    | rel_exp
    ;

rel_exp
    : rel_exp EQUALS expression
    | rel_exp GREATER expression
    | rel_exp LESS expression
    | expression
    ;

expression
    : expression PLUS term
    | expression MINUS term
    | expression POWER term
    | term
    ;

term
    : term MULTIPLY factor
    | term DIVIDE factor
    | factor
    ;

factor
    : FLOAT
    | BOOL
    | constructors property_access
    | IDENTIFIER property_access
    | LPAREN expression RPAREN property_access
    | function_call property_access
    | PLUS factor 
    | MINUS factor
    | NOT factor
    ;

property_access
    :  PROPERTY property_access
    | 
    ;

constructors
    : VEC_TYPE LPAREN func_call_args RPAREN
    ;

function_call
    : IDENTIFIER LPAREN func_call_args RPAREN
    ;

%%

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Expected args: %s <input_file>\n", argv[0]);
        return 1;
    }
    FILE *input_file = fopen(argv[1], "r");
    if (!input_file) {
        fprintf(stderr, "Error: could not open file %s\n", argv[1]);
        return 1;
    }
    yyin = input_file;
    yyparse();

    fclose(input_file);
    return 0;
}

void yyerror(char *s) {
    fprintf(stderr, "error: %s\n", s);
}