/********   global.h  ******************************************/

#include <stdio.h>          /* load i/o routines */
#include <ctype.h>          /* load character test routine */

#define BSIZE   128         /* buffer size */
#define NONE    -1
#define EOS     '\0' 

#define NUM     256
#define DIV     257
#define MOD     258
#define ID      259
#define DONE    260

int tokenval;   /* value of token attribute */
int lineno;

/* form of symbol table entry */
struct entry {  
    char *lexptr;
    int  token;
};

struct entry symtable[];    /* symbol table */

