sdl: src/sdl.lex src/sdl.y
	bison -d src/sdl.y -o src/sdl.tab.c
	lex -o src/lex.yy.c src/sdl.lex
	gcc -o $@ src/sdl.tab.c src/lex.yy.c -lfl

clean:
	rm -f sdl
	rm -f src/lex.yy.c
	rm -f src/sdl.tab.c
	rm -f src/sdl.tab.h
