#include <ctype.h>  /* loads file with predicate isdigit */

int lookahead;      /* global variable */

main()
{
    lookahead = getchar();
    expr();
    putchar('\n'); /* adds trailing newline character */
}

expr()
{
    term();
    while(1)
        if (lookahead == '+') {
            match('+'); term(); putchar('+');
        }
        else if (lookahead == '-') {
            match('-'); term(); putchar('-');
        }
        else break;
}

term()
{
    if (isdigit(lookahead)) {
        putchar(lookahead);
        match(lookahead);
    }
    else error();
}

match(int t)
{
    if (lookahead == t)
        lookahead = getchar();
    else
        error();
}

error()
{
    printf("syntax error\n");   /* print error message */
    exit(1);                    /* then halt */
}
