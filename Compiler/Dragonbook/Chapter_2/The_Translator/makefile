CC=cc
SOURCES=lexer.c parser.c emitter.c symbol.c init.c error.c main.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=infix_postfix


all: $(SOURCES) $(EXECUTABLE) 

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@

clean:
	rm -rf *.o infix_postfix
