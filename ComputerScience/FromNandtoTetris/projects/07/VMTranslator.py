# VM(Virtual Machine) translator to assemble code 
# This program will take an input file and output a translated hack machine language file.

# Stage 1: Handling Stack Arithmetic

# Stage 2: Hanlding memory access commands

import sys
import os

## Global Constant
C_ARITHMETIC  = "C_ARITHMETIC"
C_PUSH        = "C_PUSH" 
C_POP         = "C_POP" 
C_LABEL       = "C_LABEL" 
C_GOTO        = "C_GOTO" 
C_IF          = "C_IF"
C_FUNCTION    = "C_FUNCTION"
C_RETURN      = "C_RETURN"
C_CALL        = "C_CALL"

## Memory Segment
M_LCL       = 1
M_ARG       = 2
M_THIS      = 3
M_THAT      = 4
M_STATIC    = 16
M_TEMP      = 5   # Store as Value
M_POINTER_0 = M_THIS
M_POINTER_1 = M_THAT


class Parser:
  def __init__(self, input):
    self.file = open(input, 'r') # open file
    self.current_line = self.file.readline() 
    self.words = None
    self._command_type = None
    self._arg1 = None
    self._arg2 = None
    # self.file = open(input, 'r')

  def has_more_commands(self):
    """
    check if the input has more commands to be processed
    Current assume no empty line

    @return boolean
    """
    def _parse_command(content):
      """
      parse command

      @return True
      """
      words = content.split() 
      arithmetic_cmds = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
      try:
        cmd = words[0].lower()
        if cmd in arithmetic_cmds:
          self._command_type = C_ARITHMETIC
        elif cmd == "push":
          self._command_type = C_PUSH
        elif cmd == "pop":
          self._command_type = C_POP
        else:
          self._command_type = "UNKNOWN"

      except ValueError:
        print("There is no command here") 

      # fill up arg1 and arg2
      try:
        if self._command_type == C_ARITHMETIC:
          self._arg1 = cmd
        else:
          self._arg1 = words[1].lower()
          self._arg2 = words[2].lower()
      except ValueError:
        print("something wrong in arguments")
      
      return True

    while self.current_line != '':
      content = self.current_line.strip()

      if content == '' or content.startswith("//"):  # skip empty line or comment
        self.current_line = self.file.readline()
        continue
      else: # process content
        return _parse_command(content)

    return False

  def advance(self):
    """
    read the next command from the input 

    @return null
    """
    self.current_line = self.file.readline()

  def command_type(self):
    """
    return current command's type

    @return CommandType
    """
    return self._command_type

  def arg1(self):
    """
    return the first argument

    @return string
    """
    return self._arg1

  def arg2(self):
    """
    return the second argument

    @return int
    """
    return int(self._arg2)

  def close(self):
    """
    close open file
    """
    self.file.close()

class CodeWriter:
  def __init__(self, output):
    # delete this file if already existed
    try:
      os.remove(output)
    except OSError:
      pass
    
    self._output = output
    self._file_name = self._get_file_name(output)
    self._arithmetic_counter = 0  # used for labeling

  def _get_file_name(self, path):
    """
    get file name from path
    """
    # delete ".asm"
    return os.path.basename(path)[:-4] 

  def write_arithmetic(self, command):
    """
    @command string
    """
    if command == "add":
      """
      add x + y
      """
      hack = "    @R0\n" +\
             "    AM=M-1\n" +\
             "    D=M\n" +\
             "    @R0\n" +\
             "    AM=M-1\n" +\
             "    M=M+D\n" +\
             "    @R0\n" +\
             "    M=M+1\n"
    elif command == "sub":
      """
      sub x - y
      """
      hack = "    @R0\n" + \
             "    AM=M-1\n" + \
             "    D=M\n" + \
             "    @R0\n" + \
             "    AM=M-1\n" + \
             "    M=M-D\n" + \
             "    @R0\n" + \
             "    M=M+1\n" 
    elif command == "eq":
      """
      x == y
      """
      hack = "    @R0\n" + \
             "    AM=M-1\n" + \
             "    D=M \n" + \
             "    @R0\n" + \
             "    AM=M-1  \n" + \
             "    D=M-D\n" + \
             "    @EQUAL_TRUE" + str(self._arithmetic_counter) + "\n" + \
             "    D, JEQ\n" + \
             "" + \
             "    @R0\n" + \
             "    A=M\n" + \
             "    M=0\n" + \
             "    @R0\n" + \
             "    M=M+1\n" + \
             "    @EQUAL_END" + str(self._arithmetic_counter) + "\n" + \
             "    0, JMP\n" + \
             "(EQUAL_TRUE" + str(self._arithmetic_counter) + ")\n" + \
             "    @R0\n" + \
             "    A=M\n" + \
             "    M=-1\n" + \
             "    @R0\n" + \
             "    M=M+1\n" + \
             "(EQUAL_END" + str(self._arithmetic_counter) + ")\n"
             
    elif command == "gt":
      # x > y
      hack = "    @R0\n" +\
             "    AM=M-1  \n" +\
             "    D=M \n" +\
             "    @R0\n" +\
             "    AM=M-1  \n" +\
             "    D=M-D\n" +\
             "    @GT_FALSE" + str(self._arithmetic_counter) + "\n" +\
             "    D, JLE\n" +\
             "" + \
             "    @R0\n" + \
             "    A=M\n" + \
             "    M=-1\n" +\
             "    @R0\n" +\
             "    M=M+1\n" +\
             "    @GT_END" + str(self._arithmetic_counter) + "\n" + \
             "    0, JMP\n" +\
             "(GT_FALSE" + str(self._arithmetic_counter) + ")\n" +\
             "    @R0\n" + \
             "    A=M\n" + \
             "    M=0\n" +\
             "    @R0\n" +\
             "    M=M+1\n" +\
             "(GT_END" + str(self._arithmetic_counter) + ")\n"
    elif command == "lt":
      # x < y
      hack = "    @R0\n" + \
             "    AM=M-1  \n" + \
             "    D=M \n" + \
             "    @R0\n" + \
             "    AM=M-1  \n" + \
             "    D=M-D\n" + \
             "    @LT_TRUE" + str(self._arithmetic_counter) + "\n" +\
             "    D, JLT\n" + \
             "" + \
             "    @R0\n" + \
             "    A=M\n" + \
             "    M=0\n" + \
             "    @R0\n" + \
             "    M=M+1\n" + \
             "    @LT_END" + str(self._arithmetic_counter) + "\n" + \
             "    0, JMP\n" + \
             "(LT_TRUE" + str(self._arithmetic_counter) + ")\n" +\
             "    @R0\n" + \
             "    A=M\n" + \
             "    M=-1\n" + \
             "    @R0\n" + \
             "    M=M+1\n" + \
             "(LT_END" + str(self._arithmetic_counter) + ")\n"
    elif command == "and":
      # x and y
      hack = "    @R0\n" +\
             "    AM=M-1  \n" +\
             "    D=M \n" +\
             "    @R0\n" +\
             "    AM=M-1  \n" +\
             "    D=M&D\n" +\
             "    M=D\n" +\
             "    @R0\n" + \
             "    M=M+1\n"
    elif command == "or":
      # x or y
      hack ="    @R0\n" +\
            "    AM=M-1\n" +\
            "    D=M\n" +\
            "    @R0\n" +\
            "    AM=M-1\n" +\
            "    D=M|D\n" +\
            "    M=D\n" +\
            "    @R0\n" + \
            "    M=M+1\n"
    elif command == "neg":
      # - y
      hack = "    @R0\n" + \
             "    A=M-1\n" + \
             "    M=-M\n"
    elif command == "not":
      # not y
      hack = "    @R0\n" + \
             "    A=M-1\n" + \
             "    M=!M\n"
    else:
      # unknown command
      return 
    
    self._arithmetic_counter += 1
    with open(self._output, 'a+') as file:
      # file.write("arithm\n")
      file.write(hack)

  def write_push_pop(self, command, segment, index):
    """
    @command: push/pop
    """
    def _get_push_pop_addr(segment, index):
      """
      get push/pop command's memory segment's address
      """
      if segment == "local":
        sgmt_addr = M_LCL
      elif segment == "argument":
        sgmt_addr = M_ARG
      elif segment == "this":
        sgmt_addr = M_THIS
      elif segment == "that":
        sgmt_addr = M_THAT
      elif segment == "temp":
        sgmt_addr = M_TEMP
      else:
        raise ValueError("Unrecoganized 'segment' value: %s %i", segment, index)
      
      return sgmt_addr

    def _write_push(segment, index):
      """
      # push constant/memory index:
      # implementation:

      *sp = index/memory[index]   // value_hack
      sp++                        // assign_hack
      """
      if segment == "constant":
        value_hack = "    @" + str(index) + "\n" + \
                     "    D=A\n"
      elif segment == "static":
        # static store value @FileName.index
        value_hack = "    @" + str(self._file_name) + "." + str(index) + "\n" +\
                     "    D=M\n"
      elif segment == "temp":
        # temp store from 5 as value
        target_addr = M_TEMP + index
        value_hack = "    @" + str(target_addr) + "\n" +\
                     "    D=M\n"
      elif segment == "pointer":
        if index == 0:
          target_addr = M_THIS
        elif index == 1:
          target_addr = M_THAT
        else:
          raise ValueError("'index' after 'pointer' other than 0/1: %s %i", segment, index)

        value_hack = "    @" + str(target_addr) + "\n" +\
                     "    D=M\n"
      else:
        # other segment store address, need get value then add index
        target_addr = _get_push_pop_addr(segment, index) 
        value_hack = "    @" + str(target_addr) + "\n" +\
                     "    D=M\n" +\
                     "    @" + str(index) + "\n" + \
                     "    A=D+A\n" +\
                     "    D=M\n"

      push_hack = value_hack + "    @R0\n" +\
                               "    A=M\n" +\
                               "    M=D\n" +\
                               "    @R0\n" +\
                               "    M=M+1\n"

      return push_hack 

    def _write_pop(segment, index):
      """
      pop memory index

      # implementation
        addr = segment + index
        sp--
        *addr = *sp

      # Explaination on code piecez:
        AM=M-1    # A = addr
        D=D+M     # D = addr(D) + value(M)
        D=D-A     # D = D - A = value
      """
      if segment == "static":
        # static store value
        addr_hack = "    @" + str(self._file_name) + "." + str(index) + "\n" +\
                    "    D=A\n"
      elif segment == "temp":
        # temp store from 5 as value
        target_addr = _get_push_pop_addr(segment, index) + index
        addr_hack = "    @" + str(target_addr) + "\n" +\
                    "    D=A\n"
      elif segment == "pointer":
        if index == 0:
          target_addr = M_THIS
        elif index == 1:
          target_addr = M_THAT
        else:
          raise ValueError("'index' after 'pointer' other than 0/1: %s %i", segment, index)
        addr_hack = "    @" + str(target_addr) + "\n" +\
                    "    D=A\n"
      else:
        # other segment store address, need get value then add index
        target_addr = _get_push_pop_addr(segment, index) 
        addr_hack = "    @" + str(target_addr) + "\n" +\
                    "    D=M\n" +\
                    "    @" + str(index) + "\n" + \
                    "    D=D+A\n"

      pop_hack = addr_hack +\
                 "    @R0\n" +\
                 "    AM=M-1\n" +\
                 "    D=D+M\n" +\
                 "    A=D-M\n" +\
                 "    D=D-A\n" +\
                 "    M=D\n"
      return pop_hack 

    if command == C_PUSH:
      hack_asm = _write_push(segment, index)
    elif command == C_POP:
      hack_asm = _write_pop(segment, index)
    else:
      print("ERROR: Unrecoganized command, not C_PUSH or C_POP")

    with open(self._output, 'a+') as file:
      file.write(hack_asm)

  def close(self):
    """
    Add END
    """
    end_hack = "(END)\n" +\
               "    @END\n" +\
               "    0, JMP\n"
    with open(self._output, 'a+') as file:
      file.write(end_hack)


if __name__ == "__main__":
  vm_file = sys.argv[1]
  output_file = vm_file[:-3]+".asm"

  parser = Parser(vm_file)
  code_writer = CodeWriter(output_file)

  while parser.has_more_commands():
    cmd = parser.command_type()
    if cmd ==  C_ARITHMETIC:
      code_writer.write_arithmetic(cmd)
      arg1 = parser.arg1()
      code_writer.write_arithmetic(arg1)
      # print("current cmd: ", cmd)
    elif cmd == C_PUSH or cmd == C_POP:
      arg1 = parser.arg1()
      arg2 = parser.arg2()
      code_writer.write_push_pop(cmd, arg1, arg2)
      # print("current cmd: ", cmd, arg1, arg2)
    else:
      # Unrecoganized
      pass
      
    # advance line
    parser.advance()

  parser.close()
  code_writer.close()
  # Close output file


