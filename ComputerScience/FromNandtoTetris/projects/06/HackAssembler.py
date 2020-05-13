import sys, re, os, collections

A_COMMAND=0
C_COMMAND=1
L_COMMAND=2

class Parser:
  def __init__(self, asm_file):
    self._origin_file = asm_file
    self._file = open(asm_file, 'r')
    self._curr_line = self._file.readline()
    self._curr_cmd = None
    self._symbol = None

  def reset(self):
    self.__init__(self._origin_file)

  def has_more_commands(self):
    """
    @return boolean
    """
    while self._curr_line != "":
      line = self._curr_line.strip()
      line = re.sub(r"//.*", "", line)  # // commend
      line = re.sub(r"\s+", "", line)       # whitespace
      if line == "":
        self.advance()
      else:
        self._parse_command(line)
        return True

    return False

  def _parse_command(self, cmd):
    # clear command parts
    self._dst = ""
    self._cmp = ""
    self._jmp = ""

    if cmd[0] == '@':
      self._curr_cmd = A_COMMAND
      self._symbol = cmd[1:]
    elif cmd[0] == '(':
      self._curr_cmd = L_COMMAND
      self._symbol = cmd[1:-1]
    else:
      self._curr_cmd = C_COMMAND
      # ?(dest=) (comp) ?(;jump)
      dst_pattern = r"^(\w+)="
      dst_match = re.search(dst_pattern , cmd)
      if dst_match:
        self._dst = dst_match.group(0)[:-1]
        cmd = re.sub(dst_pattern, "", cmd)

      jmp_pattern = r";(\w+)$"
      jmp_match = re.search(jmp_pattern, cmd)
      if jmp_match:
        self._jmp = jmp_match.group(0)[1:]
        cmd = re.sub(jmp_pattern, "", cmd)

      self._cmp = cmd

  def advance(self):
    self._curr_line = self._file.readline()

  def command_type(self):
    """
    @return A_COMMAND, C_COMMAND, L_COMMAND
    """
    return self._curr_cmd

  def symbol(self):
    """
    return the current symbol, should be called only when
    curr_cmd is A_COMMAND or L_COMMAND

    @return string
    """
    if self._curr_cmd != A_COMMAND and self._curr_cmd != L_COMMAND:
      raise ValueError("symbol method should only be called within A or L Command")

    return self._symbol

  def dest(self):
    """
    @return string
    """
    return self._dst

  def comp(self):
    """
    @return string
    """
    return self._cmp

  def jump(self):
    """
    @return string
    """
    return self._jmp

class SymbolTable:
  def __init__(self):
    """
    initialize Symbol Table with build-in predefined symbols
    """
    self._symbol_table = collections.defaultdict()

    # Initializing
    self.add_entry("SP", 0)
    self.add_entry("LCL", 1)
    self.add_entry("ARG", 2)
    self.add_entry("THIS", 3)
    self.add_entry("THAT", 4)
    self.add_entry("SCREEN", 16384)
    self.add_entry("KBD", 24576)
    for idx in range(16):
      register = "R{}".format(idx)
      self.add_entry(register, idx)

  def add_entry(self, symbol, address):
    """
    Add symbol to the SymbolTable with address
    @args: symbol string
           address int
    """
    if symbol not in self._symbol_table:
      self._symbol_table[symbol] = address

  def contains(self, symbol):
    """
    @args: symbol string
    @return boolean
    """
    return symbol in self._symbol_table

  def get_address(self, symbol):
    """
    @args: symbol string
    @return int
    """
    return self._symbol_table[symbol]

class Code:
  def __init__(self):
    pass

  def dest(self, dst):
    """
    @args: dst string
    return 3 bits, binary code of the 'dest' mnemonic
    """
    if dst == "":
      dst_code = "000"
    elif dst == "M":
      dst_code = "001"
    elif dst == "D":
      dst_code = "010"
    elif dst == "MD" or dst == "DM":
      dst_code = "011"
    elif dst == "A":
      dst_code = "100"
    elif dst == "AM" or dst == "MA":
      dst_code = "101"
    elif dst == "AD" or dst == "DA":
      dst_code = "110"
    elif dst == "AMD" or dst == "ADM" or dst == "DAM" or dst == "DMA" or dst == "MAD" or dst == "MDA":
      dst_code = "111"
    else:
      raise ValueError("Unrecognized dest {}".format(dst))

    return dst_code

  def comp(self, cmp):
    """
    @args: cmp string
    return the binary code of the 'comp' mnemonic
    """
    if cmp == "0":              # a = 0
      cmp_code = "0101010"
    elif cmp == "1":
      cmp_code = "0111111"
    elif cmp == "-1":
      cmp_code = "0111010"
    elif cmp == "D":
      cmp_code = "0001100"
    elif cmp == "A":
      cmp_code = "0110000"
    elif cmp == "!D":
      cmp_code = "0001101"
    elif cmp == "!A":
      cmp_code = "0110001"
    elif cmp == "-D":
      cmp_code = "0001111"
    elif cmp == "-A":
      cmp_code = "0110011"
    elif cmp == "D+1":
      cmp_code = "0011111"
    elif cmp == "A+1":
      cmp_code = "0110111"
    elif cmp == "D-1":
      cmp_code = "0001110"
    elif cmp == "A-1":
      cmp_code = "0110010"
    elif cmp == "D+A":
      cmp_code = "0000010"
    elif cmp == "D-A":
      cmp_code = "0010011"
    elif cmp == "A-D":
      cmp_code = "0000111"
    elif cmp == "D&A":
      cmp_code = "0000000"
    elif cmp == "D|A":
      cmp_code = "0010101"
    elif cmp == "M":            # a = 1
      cmp_code = "1110000"
    elif cmp == "!M":
      cmp_code = "1110001"
    elif cmp == "-M":
      cmp_code = "1110011"
    elif cmp == "M+1":
      cmp_code = "1110111"
    elif cmp == "M-1":
      cmp_code = "1110010"
    elif cmp == "D+M":
      cmp_code = "1000010"
    elif cmp == "D-M":
      cmp_code = "1010011"
    elif cmp == "M-D":
      cmp_code = "1000111"
    elif cmp == "D&M":
      cmp_code = "1000000"
    elif cmp == "D|M":
      cmp_code = "1010101"
    else:
      raise ValueError("Unrecognized comp {}".format(cmp))

    return cmp_code

  def jump(self, jmp):
    """
    @args: jmp string
    return the binary code of the 'jump' mnemonic
    """
    if jmp == "":
      jmp_code = "000"
    elif jmp == "JGT":
      jmp_code = "001"
    elif jmp == "JEQ":
      jmp_code = "020"
    elif jmp == "JGE":
      jmp_code = "011"
    elif jmp == "JLT":
      jmp_code = "100"
    elif jmp == "JNE":
      jmp_code = "101"
    elif jmp == "JLE":
      jmp_code = "110"
    elif jmp == "JMP":
      jmp_code = "111"
    else:
      raise ValueError("Unrecognized jump")


    return jmp_code

def assembly_drive(asm_file, ml_file):
  """
  asm_f: assembly file to process
  """
  # 1 Initializing
  parser = Parser(asm_file)
  symbol_table = SymbolTable()
  code = Code()

  # 2 First Parse, symbol table
  line_num = 0
  # var_count = 16
  while parser.has_more_commands():
    cmd_type = parser.command_type()
    if cmd_type == L_COMMAND:
      symbol = parser.symbol()
      symbol_table.add_entry(symbol, line_num)

      parser.advance()
    else:
      line_num += 1
      parser.advance()

  # print(symbol_table._symbol_table)
  # 3 Second Parse: read and output
  parser.reset()
  line_num = 0
  var_count = 16
  while parser.has_more_commands():
    # print(line_num)
    line_num += 1
    cmd_type = parser.command_type()
    if cmd_type == C_COMMAND:
      instruction = "111{}{}{}\n".format(code.comp(parser.comp()), code.dest(parser.dest()), code.jump(parser.jump()))
      parser.advance()
    elif cmd_type == A_COMMAND:
      symbol = parser.symbol()
      if symbol_table.contains(symbol):
        addr = symbol_table.get_address(symbol)
      elif symbol[0].isnumeric():
        addr = int(symbol)
      else:
        symbol_table.add_entry(symbol, var_count)
        addr = var_count
        var_count += 1
      instruction = "0{0:015b}\n".format(int(addr))
      parser.advance()
    else:
      # pass L_COMMAND
      parser.advance()
      continue

    with open(ml_file, "a+") as file:
      # print(instruction)
      file.write(instruction)

if __name__ == "__main__":
  asm_file = sys.argv[1]
  ml_file  = asm_file[:-4] + ".hack"

  # delete this file if already existed
  try:
    os.remove(ml_file)
  except OSError:
    pass

  assembly_drive(asm_file, ml_file)