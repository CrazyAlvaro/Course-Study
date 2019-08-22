/******    lexer.c   ********************************************/

#include "global.h"

char lexbuf[BSIZE];
int  lineno = 1;
int  tokenvalue = NONE;

/** 
    This function is called by the parser to find tokens.A
    the routine reads the input one character at a time and returns 
    to the parser the token it found.  

    The following tokens are expected by the parser:
    + - * / DIV MOD ( ) ID NUM DONE

    =================================================================================
        Lexeme                     |     Token          |    Attribute Value
    =================================================================================
    white space                    |                    |       
    sequence of digits             |     NUM            |   numeric value of sequence 
    div                            |     DIV            |        
    mod                            |     MOD            |        
    other sequences of a letter    |                    |    
    then letters and digits        |      ID            |   index into symtable 
    end-of-file character          |     DONE           |        
    any other character            |   that character   |           NONE 
    =================================================================================

**/
int lexan()     /* lexical analyzer */
{
    int t;
    while(1) {
        t = getchar(); 
        if ( t == ' ' || t == '\t')
            ;   /* strip out white space */
        else if ( t == '\n')
            lineno += 1;
        else if (isdigit(t)) {      /* t is a digit */
            ungetc(t, stdin);
            scanf("%d", &tokenval);
            return NUM;
        }
        else if (isalpha(t)) {      /* t is a letter */
            int p, b = 0;
            while (isalnum(t)) {    /* t is alphanumeric */
                lexbuf[b] = t;
                t = getchar();
                b += 1;
                if ( b >= BSIZE )
                    error("compiler error");
            }
            lexbuf[b] = EOS;        /* end of string */
            if (t != EOF)
                ungetc(t, stdin);   /* last char is not alnum from bread of while */

            p = lookup(lexbuf);     /* symbol table routine lookup */
            if ( p == 0 )
                p = insert(lexbuf, ID);
            tokenval = p;           /* identifier's token value is index in symbol table */
            return symtable[p].token;
        }
        else if ( t == EOF )
            return DONE;
        else {
            tokenval = NONE;
            return t;
        }
    }
}
        
