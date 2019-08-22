/******    parser.c   ********************************************/

#include "global.h"

int lookahead;
void expr();
void term();

parse()     /* parsers and translates expression list */
{
    lookahead = lexan();
    while (lookahead != DONE) {
        expr(); match(';');
    }
}

/**
        expr   -> term moreterms
    moreterms  -> + term { print('+') } moreterms
                | - term { print('+') } moreterms
                | e
*/
void expr()
{
    int t;
    term();
    while(1) {
        switch(lookahead) {
        case '+': case '-':
            t = lookahead;
            match(lookahead); term(); emit(t, NONE);
            continue;   
        default:
            return;
        }
    }
}

/**
        term    -> factor morefactors
    morefactors -> *    factor { print('*')   } morefactors
                |  /    factor { print('/')   } morefactors
                | div   factor { print('DIV') } morefactors
                | mod   factor { print('MOD') } morefactors
                | e
*/
void term()
{
    int t;
    factor();
    while(1) {
        switch (lookahead) {
        case '*': case '/': case DIV: case MOD:
            t = lookahead;
            match(lookahead); factor(); emit(t, NONE);
            continue;   /* TODO why continue here*/
        default:
            return;
        }
    }
}

factor()
{
    switch(lookahead) {
    case '(':
        match('('); expr(); match(')'); break;
    case NUM:
        emit(NUM, tokenval); match(NUM); break;
    case ID:
        emit(ID, tokenval); match(ID); break;
    default:
        error("syntax error");
    }
}

match(t)
    int t;
{
    if (lookahead == t)
        lookahead = lexan();
    else
        error("syntax error");
}
