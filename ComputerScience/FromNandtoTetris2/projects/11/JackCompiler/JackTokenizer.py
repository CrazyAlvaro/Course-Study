# JackTokenizer.py
import sys
import re
import string

# token type
T_KEYWORD       = "keyword"
T_SYMBOL        = "symbol"
T_IDENTIFIER    = "identifier"
T_INT_CONST     = "integerConstant"
T_STRING_CONST  = "stringConstant"

# keyword
K_CLASS       = "class"
K_METHOD      = "method"
K_FUNCTION    = "function"
K_CONSTRUCTOR = "constructor"
K_INT         = "int"
K_BOOLEAN     = "boolean"
K_CHAR        = "char"
K_VOID        = "void"
K_VAR         = "var"
K_STATIC      = "static"
K_FIELD       = "field"
K_LET         = "let"
K_DO          = "do"
K_IF          = "if"
K_ELSE        = "else"
K_WHILE       = "while"
K_RETURN      = "return"
K_TRUE        = "true"
K_FALSE       = "false"
K_NULL        = "null"
K_THIS        = "this"


class JackTokenizer:
  symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
  keyword_list = ["class", "method", "function", "constructor", "int", "boolean", \
                  "char", "void", "var", "static", "field", "let", "do", "if", \
                  "else", "while", "return", "true", "false", "null", "this"]

  def __init__(self, input_file, verbose=False):
    with open(input_file) as file:
      self._content = file.read()

    self._content = re.sub(r"//.*\n", " ", self._content)
    self._content = self._content.replace("\n", " ")        # Join into single line
    self._content = re.sub(r"/\*.*?\*/", "", self._content) # non-greedy match
    self._content = re.sub(r"\s+", " ", self._content)      # replace multi-whitespace

    # remove leading/tailing whitespace
    self._content = self._content.strip()
    self._length = len(self._content)

    # current cursor position on input string
    self._cursor = -1
    self._token = ""
    self._token_type = ""
    if verbose: print(self._content)

  def has_more_tokens(self):
    """
    check if there is more token
    @return boolean
    """
    # at least non-whitespace char exist
    return self._cursor < (self._length - 1)

  def _skip_whitespace(self):
    """
    forward cursor to skip whitespace
    """
    while self._content[self._cursor] in string.whitespace:
      self._cursor += 1

  def advance(self):
    """
    """
    def _get_word():
      """
      get whole word until if character is '_' or letters
      """
      while self._content[self._cursor] in (string.ascii_letters + '_'):
        self._token += self._content[self._cursor]
        self._cursor += 1

      self._cursor -= 1 # get back to current token

    def _get_string():
      """
      get whole string const
      """
      self._token += self._content[self._cursor]
      self._cursor += 1

      while self._content[self._cursor] != '"':
        self._token += self._content[self._cursor]
        self._cursor += 1
      self._token += self._content[self._cursor]

    def _get_digits():
      while self._content[self._cursor] in string.digits:
        self._token += self._content[self._cursor]
        self._cursor += 1

      self._cursor -= 1 # get back to current token

    # proceed only if has more tokens
    if not self.has_more_tokens():
      return

    self._cursor += 1

    # clear token
    self._token = ""
    self._skip_whitespace()
    char = self._content[self._cursor]

    # check if the token is: symbol, integer or string
    if char in JackTokenizer.symbol_list:
      self._token_type = T_SYMBOL
      self._token = char
    elif char == '"':
      _get_string()
      self._token_type = T_STRING_CONST
    elif char in string.digits:
      _get_digits()
      self._token_type = T_INT_CONST
    elif char in (string.ascii_letters + '_'):
      _get_word()
      if self._token in JackTokenizer.keyword_list:
        self._token_type = T_KEYWORD
      else:
        self._token_type = T_IDENTIFIER
    else:
      print("## Unrecoganize Token starting:{}\n".format(char))

    # skip remaining whitespace
    self._skip_whitespace()

  def token_type(self):
    """
    return the type of current token
    """
    return self._token_type

  def token(self):
    return self._token

  def key_word(self):
    return self._token

  def symbol(self):
    if self._token == '<':
      symbol = "&lt;"
    elif self._token == '>':
      symbol = "&gt;"
    elif self._token == '"':
      symbol = "&quot;"
    elif self._token == '&':
      symbol = "&amp;"
    else:
      symbol = self._token

    return symbol

  def identifier(self):
    return self._token

  def int_val(self):
    return self._token

  def string_val(self):
    return self._token[1:-1]

# Unit-Test for JackTokenizer
if __name__ == "__main__":
  input_file = sys.argv[1]
  output_file = input_file[:-4] + "xml.tmp"
  tokenizer = JackTokenizer(input_file)

  with open(output_file, 'w+') as file:
    file.writelines("<tokens>\n")
    while tokenizer.has_more_tokens():
      tokenizer.advance()
      token_type = tokenizer.token_type()

      if token_type == T_SYMBOL:
        token = tokenizer.symbol()
      elif token_type == T_STRING_CONST:
        token = tokenizer.string_val()
      else:
        token = tokenizer.token()

      xml_str = "<{}> {} </{}>\n".format(token_type, token, token_type)
      # print(xml_str)
      file.writelines(xml_str)

    file.writelines("</tokens>\n")