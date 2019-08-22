/*
 *  The scanner definition for COOL.
 */

/*
 *  Stuff enclosed in %{ %} in the first section is copied verbatim to the
 *  output, so headers and global definitions are placed here to be visible
 * to the code in the file.  Don't remove anything that was here initially
 */
%{
#include <cool-parse.h>
#include <stringtab.h>
#include <utilities.h>

/* The compiler assumes these identifiers. */
#define yylval cool_yylval
#define yylex  cool_yylex

/* Max size of string constants */
#define MAX_STR_CONST 1025
#define YY_NO_UNPUT   /* keep g++ happy */

extern FILE *fin; /* we read from this file */

/* define YY_INPUT so we read from the FILE fin:
 * This change makes it possible to use this scanner in
 * the Cool compiler.
 */
#undef YY_INPUT
#define YY_INPUT(buf,result,max_size) \
	if ( (result = fread( (char*)buf, sizeof(char), max_size, fin)) < 0) \
		YY_FATAL_ERROR( "read() in flex scanner failed");

char string_buf[MAX_STR_CONST]; /* to assemble string constants */
char *string_buf_ptr;

extern int curr_lineno;
extern int verbose_flag;

extern YYSTYPE cool_yylval;

/*
 *  Add Your own definitions here
 */
int nested_comment;
bool escaped;

%}

/*
 * Define names for regular expressions here.
 */

/*
 * FORMAT:
 * Regex_name      regular_expression pattern
 *
 * For flex pattern, refer to: http://flex.sourceforge.net/manual/Patterns.html#Patterns
*/

/*
 *   KEYWORDS : all keywords are case insensitive except for true and false
 */
CLASS           (?i:class)
ELSE            (?i:else)
FI              (?i:fi)
IF              (?i:if)
IN              (?i:in)
INHERITS        (?i:inherits)
ISVOID          (?i:isvoid)
LET             (?i:let)
LOOP            (?i:loop)
POOL            (?i:pool)
THEN            (?i:then)
WHILE           (?i:while)
CASE            (?i:case)
ESAC            (?i:esac)
NEW             (?i:new)
OF              (?i:of)
NOT             (?i:not)

/*
 * KEYWORDS: true and false, first letter must be lowercase, the trailing letters may be upper or lower
 */
TRUE            t(?i:rue)
FALSE           f(?i:alse)

/*
 *  Integer, Identifier, and special Notattion
 */
DIGIT           [0-9]
INTEGER         {DIGIT}+
ALPHANUMERIC    [a-zA-Z0-9_]
TYPE_ID         [A-Z][a-zA-Z0-9_]*
OBJECT_ID       [a-z][a-zA-Z0-9_]*

WHITE_SPACE     [ \f\r\t\v]
NEWLINE         [\n]
NOT_NEWLINE     [^\n]*

DARROW          =>
LE              <=
SINGLESYMB      [(){}.@~*/+-;<=]
ASSIGN          <-
SINGLE_COMMENT  --
COMMENT_START   "(*"
COMMENT_END     "*)"
QUOTE           \"


/*
 *  Start condition, exclusive start
 */
%x SINGLE_COM COMMENT STRING STRING_ERROR 

%%
 /*
  *     TOKEN declearation in: ./include/PA2/cool-parser.h
  */
{WHITE_SPACE}   ;

{SINGLE_COMMENT}    {   BEGIN(SINGLE_COM); }
<SINGLE_COM>{
    {NOT_NEWLINE}   ;
    {NEWLINE}       {
                        curr_lineno = curr_lineno + 1;
                        BEGIN(INITIAL);
                    }
    <<EOF>>         {   yyterminate(); }
}


 /*
  *  Integer
  */
{INTEGER}       {
                    cool_yylval.symbol = inttable.add_string(yytext); /* record the value in the global variable cool_yylval */
                    return INT_CONST; /* return the token code */
                }

 /*
  *  Nested comments
  */
{COMMENT_START} {
                    nested_comment = 1;
                    BEGIN(COMMENT);
                }
{COMMENT_END}   {
                    cool_yylval.error_msg = "Unmatched *)";
                    return ERROR;
                }

<COMMENT>{
    <<EOF>>         {
                        cool_yylval.error_msg = "EOF in comment";
                        BEGIN(INITIAL);
                        return ERROR;
                    }
    {NEWLINE}       {   curr_lineno++;      }
    {COMMENT_START} {   nested_comment++;   }
    {COMMENT_END}   {
                        nested_comment--;
                        if( nested_comment == 0 ){
                            BEGIN(INITIAL);
                        }
                    }
    .               ;
}


 /*
  *  The multiple-character operators.
  */
{DARROW}		{ return DARROW;  }
{LE}            { return LE;      }
{NEWLINE}       { curr_lineno = curr_lineno + 1; }
{ASSIGN}        { return ASSIGN;  }

 /*
  * Keywords are case-insensitive except for the values true and false,
  * which must begin with a lower-case letter.
  */

{CLASS}         {   return CLASS;   }
{ELSE}          {   return ELSE;    }
{FI}            {   return FI;      }
{IF}            {   return IF;      }
{IN}            {   return IN;      }
{INHERITS}      {   return INHERITS;}
{ISVOID}        {   return ISVOID;  }
{LET}           {   return LET;     }
{LOOP}          {   return LOOP;    }
{POOL}          {   return POOL;    }
{THEN}          {   return THEN;    }
{WHILE}         {   return WHILE;   }
{CASE}          {   return CASE;    }
{ESAC}          {   return ESAC;    }
{NEW}           {   return NEW;     }
{OF}            {   return OF;      }
{NOT}           {   return NOT;     }

{TRUE}          {
                    cool_yylval.boolean = 1;
                    return BOOL_CONST;
                }

{FALSE}         {
                    cool_yylval.boolean = 0;
                    return BOOL_CONST;
                }


 /*
  *  String constants (C syntax)
  *  Escape sequence \c is accepted for all characters c. Except for
  *  \n \t \b \f, the result is c.
  *
  */
{QUOTE}         {
                    BEGIN(STRING);
                    string_buf_ptr = string_buf;
                }
<STRING>{
    [\\][\\]    {
                    /* escaped \ */
                    *string_buf_ptr++ = '\\';
                }
    [\\][\"]    {
                    /* excaped " */
                    *string_buf_ptr++ = '\"';
                }
    [\\][\n]    {
                    /* excaped newline */
                    curr_lineno++;
                    *string_buf_ptr++ = '\n';
                }
    [\\][n]     {
                    /* newline in string */
                    *string_buf_ptr++ = '\n';
                }
    [\\][b]     {
                    /* backspace */
                    *string_buf_ptr++ = '\b';
                }
    [\\][t]     {
                    /* tab */
                    *string_buf_ptr++ = '\t';
                }
    [\\][f]     {
                    /* formfeed */
                    *string_buf_ptr++ = '\f';
                }

    [\0]        {
                    /* A string may not contain the null (character \0) */
                    cool_yylval.error_msg = "String contains null character";
                    BEGIN(STRING_ERROR);
                }
    [\n]        {
                    /* non-escaped newline character */
                    cool_yylval.error_msg = "Unterminated string constant";
                    curr_lineno++;
                                        /* resume lexing at the beginning of the next line */
                    BEGIN(INITIAL);     /* assume forgot the close-quote */
                    return ERROR;
                }

    {QUOTE}     {
                    if(string_buf_ptr - string_buf >= MAX_STR_CONST){
                        cool_yylval.error_msg = "String constant too long";
                        BEGIN(INITIAL);
                        return ERROR;
                    }
                    *string_buf_ptr = '\0';
                    cool_yylval.symbol = stringtable.add_string(string_buf);
                    BEGIN(INITIAL);
                    return STR_CONST;
                }
    <<EOF>>     {
                    cool_yylval.error_msg = "EOF in string constant";
                    BEGIN(INITIAL);
                    return ERROR;
                }
    [\\]        {   /* single escape */
                    escaped = true;
                }
    .           {
                    *string_buf_ptr++ = yytext[0];
                    if(escaped){
                        escaped = false;
                    }
                }
}

<STRING_ERROR>{
    [^\n\"]*    ;
    \n          {
                    curr_lineno++;
                    BEGIN(INITIAL);
                    return ERROR;
                }
    \"          {
                    BEGIN(INITIAL);
                    return ERROR;
                }
}

 /*
  * Identifier: should be placed after keyword
  */

{TYPE_ID}       {
                    cool_yylval.symbol = idtable.add_string(yytext);
                    return TYPEID;
                }

{OBJECT_ID}     {
                    cool_yylval.symbol = idtable.add_string(yytext);
                    return OBJECTID;
                }

{SINGLESYMB}    {   return *yytext; }
<<EOF>>         {   yyterminate();  }

 /*
  * Other character, error
  */
.               {
                    cool_yylval.error_msg = yytext;
                    return ERROR;
                }
%%
