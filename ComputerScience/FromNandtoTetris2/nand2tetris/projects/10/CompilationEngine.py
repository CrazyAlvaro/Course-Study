# CompilationEngine.py
import JackTokenizer
import os

class CompilationEngine:
  _op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
  _unary_op = ['-', '~']

  def __init__(self, input_file, output_file):
    try:
      os.remove(output_file)
    except OSError:
      pass

    self._tknz = JackTokenizer.JackTokenizer(input_file)
    self._output = output_file
    self._indention = ""

    # start parsing
    self.compile_class()

  def _append_output(self, content):
    with open(self._output, 'a+') as f:
      f.write(self._indention + content)


  def _start_marking(self, tag):
    self._append_output("<{}>\n".format(tag))
    self._indention += "  "

  def _end_marking(self, tag):
    self._indention = self._indention[:-2]
    self._append_output("</{}>\n".format(tag))

  def _write_token_and_type(self):
    """
    The underlying function that write the xml file
    """
    tk_typ = self._tknz.token_type()
    if tk_typ == JackTokenizer.T_STRING_CONST:
      tk = self._tknz.string_val()
    elif tk_typ == JackTokenizer.T_SYMBOL:
      tk = self._tknz.symbol()
    else:
      tk = self._tknz.token()
    self._append_output("<{}> {} </{}>\n".format(tk_typ, tk, tk_typ))

  def _write_forward_until(self, end_token):
    try:
      while self._tknz.token() != end_token:
        self._write_token_and_type()
        self._tknz.advance()

      # write end_token
      self._write_token_and_type()
      self._tknz.advance()
    except ValueError:
      print("## ERROR _write_forward_until parsing error at token: {} token_type: {}".format(self._tknz.token(), self._tknz.token_type()))

  def _compile_var_name_ll2(self):
    """
    five cases:
      1 foo
      2 foo[expression]
      3 foo.bar(expression_list)
      4 Foo.bar(expression_list)
      5 bar(expression_list)
    """
    try:
      # prev_tk = self._tknz.token()
      # prev_tk_typ = self._tknz.token_type()

      # identifier
      self._write_token_and_type()
      self._tknz.advance()
      tk = self._tknz.token()

      if tk == '[':
        # case 2
        self._write_forward_until('[')
        self.compile_expression()
        self._write_forward_until(']')
      elif tk == '.' or tk == '(':
        # case: 3,4,5
        self._write_forward_until('(')
        self.compile_expression_list()
        self._write_forward_until(')')
      else:
        # case 1, do nothing
        pass

    except ValueError:
      print("## ERROR _compile_identifier_ll2 parsing error at token: {} token_type: {}".format(self._tknz.token(), self._tknz.token_type()))


  def compile_class(self):
    """
    class Name { ... }
    """
    try:
      while self._tknz.token() != JackTokenizer.K_CLASS:
          self._tknz.advance()

      class_tag = "class"


      self._start_marking(class_tag)
      self._write_forward_until('{')

      while self._tknz.token() != '}':
        if self._tknz.token() in [JackTokenizer.K_STATIC, JackTokenizer.K_FIELD]:
          self.compile_class_var_dec()
        elif self._tknz.token() in [JackTokenizer.K_CONSTRUCTOR, JackTokenizer.K_FUNCTION, JackTokenizer.K_METHOD]:
          self.compile_subroutine_dec()
        else:
          raise ValueError()

      # }
      self._write_token_and_type()
      self._end_marking(class_tag)
    except ValueError:
      print("## ERROR compile_class parsing error at token: {} token_type: {}".format(self._tknz.token(), self._tknz.token_type()))


  def compile_class_var_dec(self):
    """
    (static | field) type varName(, varName)* ;
    """
    class_var_dec_tag = "classVarDec"
    self._start_marking(class_var_dec_tag)
    self._write_forward_until(';')
    self._end_marking(class_var_dec_tag)

  def compile_subroutine_dec(self):
    """
    routineType type name( parameterList ) subroutineBody
    """
    sbrt_dec_tag = "subroutineDec"
    self._start_marking(sbrt_dec_tag)

    # routineType type name (
    self._write_forward_until('(')
    self.compile_parameter_list()
    self._write_forward_until(')')

    self.compile_subroutine_body()
    self._end_marking(sbrt_dec_tag)

  def compile_parameter_list(self):
    """
    (type varName (, type varName)*)?
    """
    param_list_tag = "parameterList"
    self._start_marking(param_list_tag)
    if self._tknz.token() != ')':
      # type
      self._write_token_and_type()
      self._tknz.advance()
      # varName
      self._write_token_and_type()
      self._tknz.advance()

    while self._tknz.token() == ',':
      # ,
      self._write_token_and_type()
      self._tknz.advance()
      # type
      self._write_token_and_type()
      self._tknz.advance()
      # varName
      self._write_token_and_type()
      self._tknz.advance()

    self._end_marking(param_list_tag)

  def compile_subroutine_body(self):
    """
    { varDec* statements }
    """
    sbrt_bdy_tag = "subroutineBody"
    self._start_marking(sbrt_bdy_tag)

    self._write_forward_until('{')

    while self._tknz.token() != '}':
      if self._tknz.token() == JackTokenizer.K_VAR:
        self.compile_var_dec()
      else:
        self.compile_statements()

    self._write_forward_until('}')
    self._end_marking(sbrt_bdy_tag)

  def compile_var_dec(self):
    """
    var type varName (, varName)* ;
    """
    var_dec_tag = "varDec"
    self._start_marking(var_dec_tag)
    self._write_forward_until(';')
    self._end_marking(var_dec_tag)

  def compile_statements(self):
    """
    statement *
    """
    statements_tag = "statements"
    self._start_marking(statements_tag)

    try:
      while self._tknz.token() != '}':
        if self._tknz.token()   == JackTokenizer.K_LET:
          self.compile_let()
        elif self._tknz.token() == JackTokenizer.K_IF:
          self.compile_if()
        elif self._tknz.token() == JackTokenizer.K_WHILE:
          self.compile_while()
        elif self._tknz.token() == JackTokenizer.K_DO:
          self.compile_do()
        elif self._tknz.token() == JackTokenizer.K_RETURN:
          self.compile_return()
        else:
          raise ValueError()
    except ValueError:
      print("## ERROR compile_statements parsing error at cursor: {} token: {} token_type: {}".format(self._tknz._cursor, self._tknz.token(), self._tknz.token_type()))

    self._end_marking(statements_tag)

  def compile_let(self):
    """
    let varName([ expression ])? = expression ;
    """
    let_tag = "letStatement"
    self._start_marking(let_tag)

    # let
    self._write_token_and_type()
    self._tknz.advance()

    # identifier
    self._write_token_and_type()
    self._tknz.advance()

    # expression
    if self._tknz.token() == '[':
      # [
      self._write_token_and_type()
      self._tknz.advance()

      self.compile_expression()

      # ]
      self._write_token_and_type()
      self._tknz.advance()

    # =
    self._write_token_and_type()
    self._tknz.advance()

    self.compile_expression()

    # ;
    self._write_token_and_type()
    self._tknz.advance()
    self._end_marking(let_tag)

  def compile_if(self):
    """
    if (expression) { statements } ( else { statements } )?
    """
    if_tag = "ifStatement"
    self._start_marking(if_tag)

    # if (
    self._write_forward_until('(')
    self.compile_expression()
    # ) {
    self._write_forward_until('{')
    self.compile_statements()
    self._write_forward_until('}')

    if self._tknz.token() == JackTokenizer.K_ELSE:
      # else {
      self._write_forward_until('{')
      self.compile_statements()
      self._write_forward_until('}')

    self._end_marking(if_tag)

  def compile_while(self):
    """
    while (expression) { statements }
    """
    while_tag = "whileStatement"
    self._start_marking(while_tag)
    # while (
    self._write_forward_until('(')
    self.compile_expression()
    # ) {
    self._write_forward_until('{')
    self.compile_statements()
    self._write_forward_until('}')

    self._end_marking(while_tag)

  def compile_do(self):
    """
    do subroutineCall ;
    """
    do_tag = "doStatement"

    self._start_marking(do_tag)

    # do subroutine(
    self._write_forward_until('(')
    self.compile_expression_list()
    # );
    self._write_forward_until(';')

    self._end_marking(do_tag)

  def compile_return(self):
    """
    return expression? ;
    """
    return_tag = "returnStatement"
    self._start_marking(return_tag)
    # return
    self._write_token_and_type()
    self._tknz.advance()

    if self._tknz.token() != ';':
      self.compile_expression()

    self._write_forward_until(';')
    self._end_marking(return_tag)

  def compile_expression(self):
    """
    term (op term)*
    """
    expression_tag = "expression"
    self._start_marking(expression_tag)

    self.compile_term()
    while self._tknz.token() in CompilationEngine._op:
      # op
      self._write_token_and_type()
      self._tknz.advance()
      # term
      self.compile_term()

    self._end_marking(expression_tag)

  def compile_term(self):
    """
    intConstant | stringConstant | keywordConstant | varName | varName[expression] |
    subroutineCall | (expression) | unaryOp term
    """
    term_tag = "term"
    self._start_marking(term_tag)

    tk = self._tknz.token()
    tk_typ = self._tknz.token_type()
    if tk_typ in [JackTokenizer.T_STRING_CONST, JackTokenizer.T_INT_CONST, JackTokenizer.T_KEYWORD]:
      self._write_token_and_type()
      self._tknz.advance()
    elif tk in CompilationEngine._unary_op:
      self._write_token_and_type()
      self._tknz.advance()
      self.compile_term()
    elif tk == '(':
      # (
      self._write_token_and_type()
      self._tknz.advance()

      self.compile_expression()

      # )
      self._write_token_and_type()
      self._tknz.advance()
    else:
      self._compile_var_name_ll2()

    self._end_marking(term_tag)

  def compile_expression_list(self):
    """
    (expression (, expression)*)?
    """
    exp_list_tag = "expressionList"
    self._start_marking(exp_list_tag)

    if self._tknz.token() == ')':
      self._end_marking(exp_list_tag)
      return

    # expression
    self.compile_expression()
    while self._tknz.token() == ',':
      # ,
      self._write_token_and_type()
      self._tknz.advance()
      self.compile_expression()

    self._end_marking(exp_list_tag)