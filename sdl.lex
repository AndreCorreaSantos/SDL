%{
#include "sdl.tab.h"
%}

WS     [ \t\n]+
TYPE   ("float"|"bool"|"vec4"|"vec3"|"vec2"|"func")
BOOL   ("true"|"false")
IDENT  [a-zA-Z_][a-zA-Z0-9_]*
NUMBER [0-9]+(\.[0-9]+)?
PROPERTY \.[a-zA-Z_][a-zA-Z0-9_]*


%%

{WS}                     ;
"#"                      { return PROGRAM_START; }
"in"                     { return IN; }
"out"                    { return OUT; }
"def"                   { return FUNC; }
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
"{"                      { return LBRACE; }
"}"                      { return RBRACE; }
"("                      { return LPAREN; }
")"                      { return RPAREN; }
","                      { return COMMA; }
{TYPE}                   { return TYPE; }
{BOOL}                   { return BOOL; }
{IDENT}                  { return IDENTIFIER; }
{NUMBER}                 { return FLOAT; }
{PROPERTY}               { return PROPERTY; }
"\\n"                    { return NEWLINE; }

%%
