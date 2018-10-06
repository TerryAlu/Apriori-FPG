CC=g++
CFLAGS=-c -Wno-write-strings
LDFLAGS=
SOURCES=main.cpp command.cpp dist.cpp expdev.cpp gammln.cpp gasdev.cpp gen.cpp poidev.cpp ran0.cpp ran1.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=gen

all: $(SOURCES) $(EXECUTABLE)
		
$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm $(OBJECTS) gen


