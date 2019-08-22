#include <stdio.h>
#include <ctype.h>

#define NUM 256

int lineno = 1;
int tokenval = NULL;

int lexan()
{
    int t;
    while(1) {
        t = getchar();
        if (t == ' ' || t == '\t')  /* white space or tab */
            ;   /* strip out blanks and tabs */
        else if ( t == '\n')
            lineno += 1;
        else if (isdigit(t)) {
            tokenval = t - '0';
            t = getchar();
            while (isdigit(t)) {
                tokenval = tokenval*10 + ( t - '0' );
                t = getchar();
            }
            ungetc(t, stdin);   /* t is not a digit, put it back to stdin */
            return NUM;
        }
        else {
            tokenval = NULL;
            return t;
        }
    }
}

