CC = gcc
CFLAGS = -fPIC -Wall
LDFLAGS = -shared
BIN = backup_generator
LIBDIR = ../lib
LIBNAME = libbackup_utils.so

all: $(BIN)

$(LIBNAME): libbackup_utils.c
	$(CC) $(CFLAGS) -o $(LIBNAME) $(LDFLAGS) libbackup_utils.c

$(BIN): backup_generator.c $(LIBNAME)
	$(CC) -o $(BIN) backup_generator.c -L$(LIBDIR) -lbackup_utils

clean:
	rm -f $(BIN) $(LIBNAME)
