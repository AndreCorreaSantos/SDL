sdl: sdl.lex sdl.y
	bison -d sdl.y
	lex sdl.lex
	gcc -o $@ sdl.tab.c lex.yy.c -lfl

clean:
	rm -f sdl
	rm -f lex.yy.c
	rm -f sdl.tab.c
	rm -f sdl.tab.h
