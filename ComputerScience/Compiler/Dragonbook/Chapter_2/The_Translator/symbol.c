/******    symbol.c   ********************************************/

#include "global.h"

#define STRMAX 999  /* size of lexemes array */
#define SYMMAX 100  /* size of symtable */

char    lexemes[STRMAX];
int     lastchar = -1;      /* last used position in lexemes */
struct  entry symtable[SYMMAX];
int     lastentry = 0;      /* last used position in symtable */ 

int     lookup(s)           /* returns position of entry for s */
    char s[];
{
    int p;
    for (p = lastentry; p > 0; p = p -1 )
        if (strcmp(symtable[p].lexptr, s) == 0)
            return p;
    
    return 0;
}

int insert(s, tok)          /* returns position of entry for s */
    char s[];
    int  tok;
{
    int len;
    len = strlen(s);    
    if(lastentry + 1 >= SYMMAX)
        error("symbol table full");
    if(lastchar + len >= STRMAX)
        error("lexemes array full");

    lastentry = lastentry + 1;
    symtable[lastentry].token = tok;
    symtable[lastentry].lexptr = &lexemes[lastchar + 1];
    lastchar = lastchar + len + 1;
    strcpy( symtable[lastentry].lexptr, s);
    return lastentry;
}
