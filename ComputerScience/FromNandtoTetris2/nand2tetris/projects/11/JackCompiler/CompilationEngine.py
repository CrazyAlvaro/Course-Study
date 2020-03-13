# CompilationEngine.py
import JackTokenizer
import VMWriter
import SymbolTable
import os

class CompilationEngine:
  _op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
  _unary_op = ['-', '~']

  def __init__(self, input_file, output_file, xml=False, vm=True, verbose=False):
    self._xml = xml
    self._vm = vm
    try:
      if self._xml:
        self._xml_output = output_file + ".parser.xml"
        os.remove(self._xml_output)
    except OSError:
      pass

    self._tknz = JackTokenizer.JackTokenizer(input_file)
    self._vm_write = VMWriter.VMWriter(output_file+".vm")
    self._indention = ""
    self._symbol_table = SymbolTable.SymbolTable()
    self._class_name = ""
    self._verbose=verbose
    self._label_count = 0
    self._sbrt_name  = ""

    # start parsing
    self._compile_log("#######################")
    self._compile_log("## Start Compilation ##")
    self._compile_log("")
    self.compile_class()
    self._compile_log(self._symbol_table._clss_table)

  def _compile_log(self, log):
    if self._verbose: print("{}".format(log))

  def _control_label(self):
    label = "{}.{}#{}".format(self._class_name, self._sbrt_name, self._label_count)
    self._label_count += 1
    return label.upper()

  def _append_output(self, content):
    if self._xml == False: return

    with open(self._xml_output, 'a+') as f:
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
    return token
    """
    tk_typ = self._tknz.token_type()
    if tk_typ == JackTokenizer.T_STRING_CONST:
      tk = self._tknz.string_val()
    elif tk_typ == JackTokenizer.T_SYMBOL:
      tk = self._tknz.symbol()
    else:
      tk = self._tknz.token()
    self._append_output("<{}> {} </{}>\n".format(tk_typ, tk, tk_typ))
    return tk

  def _write_forward_until(self, end_token):
    """
    token_list record all token with its type
    """
    token_list = []
    try:
      while self._tknz.token() != end_token:
        token_list.append((self._tknz.token(), self._tknz.token_type()))
        self._write_token_and_type()
        self._tknz.advance()

      # write end_token
      self._write_token_and_type()
      self._tknz.advance()
    except ValueError:
      print("## ERROR _write_forward_until parsing error at token: {} token_type: {}".format(self._tknz.token(), self._tknz.token_type()))

    return token_list

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
      first_tk = self._tknz.token()
      # first_tk_typ = self._tknz.token_type()
      kind = self._symbol_table.kind_of(first_tk)
      index = self._symbol_table.index_of(first_tk)

      # identifier
      self._write_token_and_type()
      self._tknz.advance()
      tk = self._tknz.token()

      if tk == '[':
        # case 2: array access
        self._vm_write.write_push(kind, index)
        self._write_forward_until('[')
        self.compile_expression()
        self._write_forward_until(']')
        self._vm_write.write_arithmetic("+")
        self._vm_write.write_pop("pointer", 1)  # assignment address
        self._vm_write.write_push("that", 0)    # get value
      elif tk == '.':
        # case 3, 4
        tk_list = self._write_forward_until('(')
        arg_num = self.compile_expression_list()
        self._write_forward_until(')')

        if kind != None:
          # case 3
          class_name = self._symbol_table.type_of(first_tk)
          self._vm_write.write_push(kind, index)              # push object
          self._vm_write.write_call("{}.{}".format(class_name, tk_list[1][0]), arg_num + 1)
        else:
          # case 4
          class_name = first_tk
          self._vm_write.write_call("{}.{}".format(class_name, tk_list[1][0]), arg_num)
      elif tk == '(':
        # case 5
        arg_num = self.compile_expression_list()
        self._write_forward_until(')')
        self._vm_write.write_call(first_tk, arg_num)
      else:
        # case 1
        self._vm_write.write_push(kind, index)

    except ValueError:
      print("## ERROR _compile_identifier_ll2 parsing error at token: {} token_type: {}".format(self._tknz.token(), self._tknz.token_type()))

  def _add_var_dec(self, token_list):
    """
    from token_list [(token1, type), (token2, type)] add to symbol table
    """
    var_kind = token_list[0][0]
    var_type = token_list[1][0]
    names = []

    for token, token_type in token_list[2:]:
      if token_type == JackTokenizer.T_IDENTIFIER:
        names.append(token)

    if var_kind in [JackTokenizer.K_FIELD, JackTokenizer.K_STATIC]:
      for name in names:
        self._symbol_table.define(name, var_type, var_kind)
    elif var_kind== JackTokenizer.K_VAR:
      for name in names:
        self._symbol_table.define(name, var_type, "local")
    else:
      raise ValueError("ERROR: Unrecoganized var type")

  def compile_class(self):
    """
    class Name { ... }
    """
    try:
      while self._tknz.token() != JackTokenizer.K_CLASS:
          self._tknz.advance()

      class_tag = "class"

      self._start_marking(class_tag)
      token_list = self._write_forward_until('{')
      self._class_name = token_list[1][0]

      ####################################################################################################
      ## NOTE: inside class body, assume static/field var declaration ahead of function/method/constructor
      ##       otherwise the var count would be wrong. Two-pass needed to get it right
      ####################################################################################################
      while self._tknz.token() in [JackTokenizer.K_STATIC, JackTokenizer.K_FIELD]:
        self.compile_class_var_dec(self._tknz.token())

      while self._tknz.token() in [JackTokenizer.K_CONSTRUCTOR, JackTokenizer.K_FUNCTION, JackTokenizer.K_METHOD]:
        self.compile_subroutine_dec(self._tknz.token())
        self._compile_log(self._symbol_table._sbrt_table)

      # }
      if self._tknz.token() != '}':
        raise ValueError()
      self._write_token_and_type()
      self._end_marking(class_tag)
    except ValueError:
      print("## ERROR compile_class parsing error at token: {} token_type: {}".format(self._tknz.token(), self._tknz.token_type()))


  def compile_class_var_dec(self, var_type):
    """
    (static | field) type varName(, varName)* ;
    """
    class_var_dec_tag = "classVarDec"
    self._start_marking(class_var_dec_tag)
    self._add_var_dec(self._write_forward_until(';'))
    self._end_marking(class_var_dec_tag)

  def compile_subroutine_dec(self, sbrt_type):
    """
    routineType type name( parameterList ) subroutineBody
    """
    sbrt_dec_tag = "subroutineDec"
    self._start_marking(sbrt_dec_tag)
    self._symbol_table.start_subroutine()     # symbol_table start_subroutine
    tk_list = self._write_forward_until('(')  # routineType type name (

    self._label_count = 0                     # reset label counter
    self._sbrt_name = tk_list[2][0]

    # Method's first argument is this, object oritented
    if sbrt_type == JackTokenizer.K_METHOD:
      self._symbol_table.define("this", self._class_name, "argument")
    self.compile_parameter_list()   # add arguments to symbol table
    self._write_forward_until(')')

    ##################################################
    ## Compile subroutine body
    ##################################################
    self.compile_subroutine_body(sbrt_type)

    self._end_marking(sbrt_dec_tag)

  def compile_parameter_list(self):
    """
    (type varName (, type varName)*)?
    """
    param_list_tag = "parameterList"
    self._start_marking(param_list_tag)
    if self._tknz.token() != ')':
      # type
      arg_type = self._write_token_and_type()
      self._tknz.advance()
      # varName
      arg_name = self._write_token_and_type()
      self._tknz.advance()
      self._symbol_table.define(arg_name, arg_type, "argument")

    while self._tknz.token() == ',':
      # ,
      self._write_token_and_type()
      self._tknz.advance()
      # type
      arg_type = self._write_token_and_type()
      self._tknz.advance()
      # varName
      arg_name = self._write_token_and_type()
      self._tknz.advance()
      self._symbol_table.define(arg_name, arg_type, "argument")

    self._end_marking(param_list_tag)

  def compile_subroutine_body(self, sbrt_type):
    """
    { varDec* | statements }
    """
    sbrt_bdy_tag = "subroutineBody"
    self._start_marking(sbrt_bdy_tag)
    self._write_forward_until('{')

    ####################################################################################################
    ## NOTE: inside subroutine body, we assume var declaration on top,
    ##       otherwise the var count would be wrong.
    ####################################################################################################
    while self._tknz.token() == JackTokenizer.K_VAR:
        # add var to symbol table
        self.compile_var_dec()

    # Write Function Declartion and initialize local variables
    lcl_num = self._symbol_table.var_count(SymbolTable.KIND_LCL)
    self._vm_write.write_function("{}.{}".format(self._class_name, self._sbrt_name), lcl_num)
    if sbrt_type == JackTokenizer.K_CONSTRUCTOR:
      # alloc memory for fields variables if its constructor
      field_num = self._symbol_table.var_count(SymbolTable.KIND_FIELD)
      self._vm_write.write_push("constant", field_num)
      self._vm_write.write_call("Memory.alloc", 1)
      self._vm_write.write_pop("pointer", 0)
    elif sbrt_type == JackTokenizer.K_METHOD:
      self._vm_write.write_push("argument", 0)
      self._vm_write.write_pop("pointer", 0)

    while self._tknz.token() != '}':
        self.compile_statements()

    self._write_forward_until('}')
    self._end_marking(sbrt_bdy_tag)

  def compile_var_dec(self):
    """
    var type varName (, varName)* ;
    """
    var_dec_tag = "varDec"
    self._start_marking(var_dec_tag)
    self._add_var_dec(self._write_forward_until(';'))
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
    let varName([ expression_1 ])? = expression_2 ;
    """
    let_tag = "letStatement"
    self._start_marking(let_tag)

    # let
    self._write_token_and_type()
    self._tknz.advance()

    # identifier
    tk = self._tknz.token()
    kind = self._symbol_table.kind_of(tk)
    index = self._symbol_table.index_of(tk)
    self._write_token_and_type()
    self._tknz.advance()

    if self._tknz.token() == '[':
      """
      Array assignment:

      push varName
      push expression_1
      +
      push expression_2
      pop temp 0
      pop pointer 1     # addr to that
      push temp 0       # get value back
      pop that 0        # to array
      """
      self._vm_write.write_push(kind, index)
      self._write_forward_until('[')
      self.compile_expression()               # expression_1
      self._write_forward_until(']')
      self._vm_write.write_arithmetic("+")    # calculate target array address

      self._write_forward_until('=')
      self.compile_expression()               # expression_2
      self._write_forward_until(';')
      self._vm_write.write_pop("temp", 0)     # value to temp 0

      self._vm_write.write_pop("pointer", 1)  # address to "that"
      self._vm_write.write_push("temp", 0)
      self._vm_write.write_pop("that", 0)     # assignhment value to array position
    else:
      self._write_forward_until('=')
      self.compile_expression()
      self._write_forward_until(';')
      self._vm_write.write_pop(kind, index)

    self._end_marking(let_tag)

  def compile_if(self):
    """
    if (expression) { statements_1 } ( else { statements_2 } )?

      expression
      not
      if-goto L1
      statements_1
      goto L2
    label L1
      statements_2
    label L2
    """
    if_tag = "ifStatement"
    self._start_marking(if_tag)

    label_1 = self._control_label()
    label_2 = self._control_label()

    # if (
    self._write_forward_until('(')
    self.compile_expression()
    self._vm_write.write_arithmetic("not")
    self._vm_write.write_if(label_1)
    # ) {
    self._write_forward_until('{')
    self.compile_statements()
    self._write_forward_until('}')
    self._vm_write.write_goto(label_2)
    self._vm_write.write_label(label_1)
    if self._tknz.token() == JackTokenizer.K_ELSE:
      # else {
      self._write_forward_until('{')
      self.compile_statements()
      self._write_forward_until('}')

    self._vm_write.write_label(label_2)
    self._end_marking(if_tag)

  def compile_while(self):
    """
    while (expression) { statements }

    label L1
      expression
      not
      if-goto L2
      statements
      goto L1
    label L2
    """
    while_tag = "whileStatement"
    self._start_marking(while_tag)
    label_1 = self._control_label()
    label_2 = self._control_label()

    # while (
    self._vm_write.write_label(label_1)
    self._write_forward_until('(')
    self.compile_expression()
    self._vm_write.write_arithmetic("not")
    self._vm_write.write_if(label_2)
    # ) {
    self._write_forward_until('{')
    self.compile_statements()
    self._write_forward_until('}')
    self._vm_write.write_goto(label_1)
    self._vm_write.write_label(label_2)

    self._end_marking(while_tag)

  def compile_do(self):
    """
    do subroutineCall ;
    """
    do_tag = "doStatement"
    self._start_marking(do_tag)
    # do (identifier.)? subroutine(
    tk_list = self._write_forward_until('(')

    if len(tk_list) == 2:
      """
      do foo(x, y)
      """
      routine_call = "{}.{}".format(self._class_name, tk_list[1][0])
      self._vm_write.write_push("pointer", 0)  # push 'this' as first argument
      self._vm_write.write_call(routine_call, self.compile_expression_list() + 1)
    elif len(tk_list) == 4:
      """
      do boo(Boo).foo(a, b)
      """
      tk, routine = tk_list[1][0], tk_list[3][0]
      symbol_type = self._symbol_table.type_of(tk)

      if symbol_type != None:
        """
        boo is an identifier in symbol_table
        """
        tk_kind = self._symbol_table.kind_of(tk)
        tk_index = self._symbol_table.index_of(tk)
        self._vm_write.write_push(tk_kind,tk_index)
        self._vm_write.write_call("{}.{}".format(symbol_type, routine), self.compile_expression_list() + 1)
      else:
        """
        Boo is not in symbol_table, it's a class name
        """
        self._vm_write.write_call("{}.{}".format(tk, routine), self.compile_expression_list())
    else:
      raise ValueError("## ERROR CompliationEngine#compile_do: unrecoganized token_list")

    self._write_forward_until(';')
    self._end_marking(do_tag)
    self._vm_write.write_pop("temp", 0) # pop dummy return

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
    else:
      self._vm_write.write_push("constant", 0)

    self._write_forward_until(';')
    self._end_marking(return_tag)
    self._vm_write.write_return()

  def compile_expression(self):
    """
    term (op term)*
    """
    expression_tag = "expression"
    self._start_marking(expression_tag)

    self.compile_term()
    while self._tknz.token() in CompilationEngine._op:
      # op
      operator = self._tknz.token()
      self._write_token_and_type()
      self._tknz.advance()
      # term
      self.compile_term()
      self._vm_write.write_arithmetic(operator)

    self._end_marking(expression_tag)

  def compile_term(self):
    """
    1 intConstant |
    2 stringConstant |
    3 keywordConstant |
    4 varName |
    5 varName[expression] |
    6 subroutineCall |
    7 (expression) |
    8 unaryOp term
    """
    term_tag = "term"
    self._start_marking(term_tag)

    tk = self._tknz.token()
    tk_typ = self._tknz.token_type()
    if tk_typ == JackTokenizer.T_INT_CONST:
      # case 1
      self._vm_write.write_push("constant", tk)
      self._write_token_and_type()
      self._tknz.advance()
    elif tk_typ == JackTokenizer.T_STRING_CONST:
      # case 2
      tk = tk[1:-1]       # remove '""
      str_len = len(tk)
      self._vm_write.write_push("constant", str_len)
      self._vm_write.write_call("String.new", 1)
      for char in tk:
        self._vm_write.write_push("constant", ord(char))
        self._vm_write.write_call("String.appendChar", 2)

      self._write_token_and_type()
      self._tknz.advance()
    elif tk_typ == JackTokenizer.T_KEYWORD:
      # case 3
      if tk in ["null", "false"]:
        self._vm_write.write_push("constant", 0)
      elif tk == "true":
        self._vm_write.write_push("constant", 1)
        self._vm_write.write_arithmetic("neg")
      elif tk == "this":
        self._vm_write.write_push("pointer", 0)
      else:
        raise("## ERROR compile_term unrecganized keyword term")
      self._write_token_and_type()
      self._tknz.advance()
    elif tk == '(':
      # case 7
      self._write_forward_until("(")
      self.compile_expression()
      self._write_forward_until(")")
    elif tk in CompilationEngine._unary_op:
      # case 8
      self._write_token_and_type()
      self._tknz.advance()
      self.compile_term()
      if tk == "-":
        self._vm_write.write_arithmetic("neg")
      else:
        #tk == "~":
        self._vm_write.write_arithmetic("not")
    else:
      # case 4,5,6
      self._compile_var_name_ll2()

    self._end_marking(term_tag)

  def compile_expression_list(self):
    """
    (expression (, expression)*)?
    @return: number of expression
    """
    exp_num = 0
    exp_list_tag = "expressionList"
    self._start_marking(exp_list_tag)

    if self._tknz.token() == ')':
      self._end_marking(exp_list_tag)
      return exp_num

    # expression
    exp_num += 1
    self.compile_expression()

    while self._tknz.token() == ',':
      # ,
      exp_num += 1
      self._write_token_and_type()
      self._tknz.advance()
      self.compile_expression()

    self._end_marking(exp_list_tag)
    return exp_num