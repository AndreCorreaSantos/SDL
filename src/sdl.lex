%{
#include "sdl.tab.h"
%}

WS     [ \t\n]+
INT    [0-9]+
VEC_TYPE  ("vec2"|"vec3"|"vec4")
TYPE   ("float"|"bool")
BOOL   ("true"|"false")
IDENT  [a-zA-Z_][a-zA-Z0-9_]*
NUMBER [0-9]+(\.[0-9]+)?
PROPERTY \.[a-zA-Z_][a-zA-Z0-9_]*


%%

{WS}                     ;
"\n"                     { return NEWLINE; }
"#"                      { return PROGRAM_START; }
"in"                     { return IN; }
"out"                    { return OUT; }
"opt"                    { return OPT; }
"width"                  { return WIDTH; }
"height"                 { return HEIGHT; }
"steps"                  { return STEPS; }
"function"                   { return FUNC; }
"local"                  { return LOCAL; }
"while"                  { return WHILE; }
"if"                     { return IF; }
"then"                   { return THEN; }
"else"                   { return ELSE; }
"end"                    { return END; }
"and"                    { return AND; }
"or"                     { return OR; }
"not"                    { return NOT; }
"do"                     { return DO; }
"return"                 { return RETURN; }
"+"                      { return PLUS; }
"-"                      { return MINUS; }
"*"                      { return MULTIPLY; }
"**"                     { return POWER; }
"/"                      { return DIVIDE; }
"="                      { return ASSIGN; }
"=="                     { return EQUALS; }
">"                      { return GREATER; }
"<"                      { return LESS; }
"("                      { return LPAREN; }
")"                      { return RPAREN; }
","                      { return COMMA; }
{INT}                    { return INT; }
{VEC_TYPE}              { return VEC_TYPE; }
{TYPE}                   { return TYPE; }
{BOOL}                   { return BOOL; }
{IDENT}                  { return IDENTIFIER; }
{NUMBER}                 { return FLOAT; }
{PROPERTY}               { return PROPERTY; }

%%
