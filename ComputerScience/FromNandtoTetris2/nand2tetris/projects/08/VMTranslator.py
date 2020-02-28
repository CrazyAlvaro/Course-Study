# VM(Virtual Machine) translator to assemble code 
# This program will take an input file/directory 
# and output a translated assembly code file.


import sys
import os

BASE_SP = 256

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
C_UNKNOWN     = "C_UNKOWN"
C_EMPTY       = "C_EMPTY"

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
    self._file = open(input, 'r') # open file
    self._current_line = self._file.readline().strip()
    self._command_type = None
    self._arg1 = None
    self._arg2 = None
    # self._file = open(input, 'r')

  def has_more_commands(self):
    """
    check if the input has more commands to be processed

    @return boolean
    """
    def _parse_command(content):
      """
      parse command

      @return True
      """
      content = content.strip()
      if content == '':
        self._command_type = C_EMPTY
        return True # empty line

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
        elif cmd == "label":
          self._command_type = C_LABEL
        elif cmd == "goto":
          self._command_type = C_GOTO
        elif cmd == "if-goto":
          self._command_type = C_IF
        elif cmd == "function":
          self._command_type = C_FUNCTION
        elif cmd == "call":
          self._command_type = C_CALL
        elif cmd == "return":
          self._command_type = C_RETURN
        else:
          self._command_type = C_UNKNOWN

      except ValueError:
        print("There is no command here") 

      # fill up arg1 and arg2
      try:
        if self._command_type == C_ARITHMETIC:
          self._arg1 = cmd
        elif (self._command_type == C_LABEL or 
              self._command_type == C_GOTO or 
              self._command_type == C_IF):
          self._arg1 = words[1]
        elif (self._command_type == C_PUSH or 
              self._command_type == C_POP or
              self._command_type == C_CALL or 
              self._command_type == C_FUNCTION):
          self._arg1 = words[1]
          self._arg2 = words[2]
        elif self._command_type == C_UNKNOWN:
          self._arg1 = content
        else:
          pass
      except ValueError:
        print("something wrong in arguments")
      
      return True

    # Start hasMoreCommand function loop
    while self._current_line != '':
      """
      if content == '' or content.startswith("//"):  # skip empty line or comment
        self._current_line = self._file.readline()
        continue
      else: # process content
      """
      return _parse_command(self._current_line)

    return False

  def advance(self):
    """
    read the next command from the input 

    @return null
    """
    self._current_line = self._file.readline()

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

  def current_line(self):
    """
    return current line, for debugging purpose 
    """
    return self._current_line

  def close(self):
    """
    close open file
    """
    self._file.close()

class CodeWriter:
  def __init__(self, output, vm_file, sys_init=False):
    # delete this file if already existed
    try:
      os.remove(output)
    except OSError:
      pass
    self._vm_filename        = vm_file     # current vm_file name, change each vm file being parsed
    self._output_filename    = vm_file     # output file name, not change
    self._output              = output      # output assembly file path
    self._arithmetic_counter  = 0           # used for arithmetic labeling
    self._return_counter      = 0           # function return counter for return address labeling
    self._current_function    = ""          # initially no function

    # only init if explicit specified
    if sys_init:
      bootstrap = "    @{}\n".format(BASE_SP) +\
                  "    D=A\n" +\
                  "    @SP\n" +\
                  "    M=D\n"
      self._append_output(bootstrap)
      self.write_call("Sys.init", 0)  # Call Sys.init function

  def _append_output(self, code_piece):
    with open(self._output, 'a+') as file:
      file.write(code_piece)

  #################### 
  ## label functions

  def _get_function_label(self, function_name):
    """
    function should be see from the whole assembly program scope, being called across different vm program.
    so use single output filename as label 
    """
    return "{}.{}".format(self._output_filename, function_name)

  def _get_return_label(self):
    """
    use vm_filename, function_name and counter to label call's return
    """
    self._return_counter += 1
    return "{}.{}$ret.{}".format(self._vm_filename, self._current_function, self._return_counter)

  def _get_static_label(self, index):
    """
    static variable expose to all functions inside a vm program(vm file), 
    so no function_name used
    """
    return "{}.{}".format(self._vm_filename, index)

  def _get_translated_label(self, origin_label):
    """
    vm_file function specific label
    label should be "{vm_filename}.{function_name}${label}"
    @return string
    """
    return "{}.{}${}".format(self._vm_filename, self._current_function, origin_label)
  
  ## end label functions
  #################### 

  def set_filename(self, vm_file):
    """
    starting a new vm_file code_writer part, 
    """
    # reset translated label dictionary
    self._vm_filename = vm_file
  
  def write_init(self):
    """
    write the assembly instruction that initialize the bootstrap code
    """
    pass

  def write_label(self, label):
    target_label = self._get_translated_label(label)
    self._append_output("("+target_label+")\n")

  def write_goto(self, label):
    target_label = self._get_translated_label(label)
    asm_code = "    @" + target_label +  "\n" + \
               "    0, JMP\n"
    self._append_output(asm_code)

  def write_if(self, label):
    """
    """
    target_label = self._get_translated_label(label)
    asm_code = "    @SP\n" + \
               "    AM=M-1\n" + \
               "    D=M\n" + \
               "    @" + target_label + "\n" + \
               "    D, JNE\n" 
    self._append_output(asm_code)

  def write_function(self, function_name, num_vars):
    """
    """
    self._current_function = function_name  # used for label creation "file_name.function_name$label"
    self._return_counter = 0 # reset function return counter
    self._append_output("({})\n".format(self._get_function_label(function_name)))

    # push num_vars 0s as local variables by simulating "push local i"
    for _ in range(num_vars):
      self.write_push_pop(C_PUSH, "constant", 0)

  def write_call(self, function_name, num_args):
    """
    1 save return_address, lcl, arg, this, that
    2 reposition LCL and ARG
    3 goto function
    """
    return_label = self._get_return_label()
    call_function_label = self._get_function_label(function_name)

    asm_code = "    @{}\n".format(return_label) +\
               "    D=A\n" +\
               "    @SP\n" +\
               "    A=M\n" +\
               "    M=D // store return address\n" +\
               "    @SP\n" +\
               "    M=M+1\n" +\
               "    @{}\n".format(M_LCL) +\
               "    D=M\n" +\
               "    @SP\n" +\
               "    A=M\n" +\
               "    M=D // store local \n" +\
               "    @SP\n" +\
               "    M=M+1\n" +\
               "    @{}\n".format(M_ARG) +\
               "    D=M\n" +\
               "    @SP\n" +\
               "    A=M\n" +\
               "    M=D // store arg \n" +\
               "    @SP\n" +\
               "    M=M+1\n" +\
               "    @{}\n".format(M_THIS) +\
               "    D=M\n" +\
               "    @SP\n" +\
               "    A=M\n" +\
               "    M=D // store this \n" +\
               "    @SP\n" +\
               "    M=M+1\n" +\
               "    @{}\n".format(M_THAT) +\
               "    D=M\n" +\
               "    @SP\n" +\
               "    A=M\n" +\
               "    M=D // store that \n" +\
               "    @SP\n" +\
               "    M=M+1\n"

    # reposition LCL, ARG
    asm_code+= "    @SP\n" +\
               "    D=M\n" +\
               "    @{}\n".format(M_LCL) +\
               "    M=D // reposition LCL\n" +\
               "    @SP\n" +\
               "    D=M\n" +\
               "    @{}\n".format(num_args+5) +\
               "    D=D-A\n" +\
               "    @{}\n".format(M_ARG) +\
               "    M=D // reposition ARG\n" +\
               "    @{}\n".format(call_function_label) +\
               "    0, JMP\n" +\
               "({})\n".format(return_label)

    self._append_output(asm_code)
  
  def write_return(self):
    """
    return to the original caller:
    0 store caller's SP(ARG + 1) on R13
      store return address on R14
    1 copy the return value onto argument 0
    2 restore the segment pointers of the caller: 

      | (ARG 0  )       |
      | (ARG ...)       |
      | return address  |
      | saved LCL       |
      | saved ARG       |
      | saved THIS      |
      | saved THAT      |
      | (LCL    )       |
      | (LCL ...)       |
      | return value    |
      | (SP)            |
    3 clear the stack
    4 set SP for the caller
    5 jump to the return address within the caller's code
    """
    asm_code = "    @{}\n".format(M_ARG) +\
               "    A=M\n" +\
               "    D=A+1\n" +\
               "    @R13\n" +\
               "    M=D // R13 stores caller's SP\n" +\
               "    @{}\n".format(M_LCL) +\
               "    D=M\n" +\
               "    @5\n" +\
               "    A=D-A\n" +\
               "    D=M\n" +\
               "    @R14\n" +\
               "    M=D // R14 store return address\n"

    # 1 Copy return value to argument 0 
    asm_code += "    @SP\n" +\
                "    AM=M-1\n" +\
                "    D=M\n" +\
                "    @{}\n".format(M_ARG) +\
                "    A=M\n" +\
                "    M=D // caller's ARG store return value\n"

    # 2 restore segment pointers, THAT, THIS, ARG, LCL
    asm_code += "    @{}\n".format(M_LCL) +\
                "    A=M-1\n" +\
                "    D=M\n" +\
                "    @{}\n".format(M_THAT) +\
                "    M=D // THAT\n" +\
                "    @{}\n".format(M_LCL) +\
                "    D=M\n" +\
                "    @2\n" +\
                "    A=D-A\n" + \
                "    D=M\n" + \
                "    @{}\n".format(M_THIS) +\
                "    M=D // THIS\n" +\
                "    @{}\n".format(M_LCL) +\
                "    D=M\n" +\
                "    @3\n" +\
                "    A=D-A\n" + \
                "    D=M\n" +\
                "    @{}\n".format(M_ARG) +\
                "    M=D // ARG\n" +\
                "    @{}\n".format(M_LCL) +\
                "    D=M\n" +\
                "    @4\n" +\
                "    A=D-A\n" + \
                "    D=M\n" +\
                "    @{}\n".format(M_LCL) +\
                "    M=D // LCL\n" 
    
    # 3 skip cleaning

    # 4 restore SP
    asm_code += "    @R13\n" +\
                "    D=M\n" +\
                "    @SP\n" +\
                "    M=D // restore SP\n"

    # 5 jump to return address
    asm_code += "    @R14\n" +\
                "    A=M\n" +\
                "    0, JMP\n"

    self._append_output(asm_code) 

  def write_comment(self, content):
    """
    just write conent as comment to target file
    """
    self._append_output("    //  " + content)

  def write_arithmetic(self, command):
    """
    @command string
    """
    _counter_used = False

    if command == "add":
      """
      add x + y
      """
      hack = "    @SP\n" +\
             "    AM=M-1\n" +\
             "    D=M\n" +\
             "    @SP\n" +\
             "    AM=M-1\n" +\
             "    M=M+D\n" +\
             "    @SP\n" +\
             "    M=M+1\n"
    elif command == "sub":
      """
      sub x - y
      """
      hack = "    @SP\n" + \
             "    AM=M-1\n" + \
             "    D=M\n" + \
             "    @SP\n" + \
             "    AM=M-1\n" + \
             "    M=M-D\n" + \
             "    @SP\n" + \
             "    M=M+1\n" 
    elif command == "eq":
      """
      x == y
      """
      _counter_used = True

      hack = "    @SP\n" + \
             "    AM=M-1\n" + \
             "    D=M \n" + \
             "    @SP\n" + \
             "    AM=M-1  \n" + \
             "    D=M-D\n" + \
             "    @EQUAL_TRUE" + str(self._arithmetic_counter) + "\n" + \
             "    D, JEQ\n" + \
             "" + \
             "    @SP\n" + \
             "    A=M\n" + \
             "    M=0\n" + \
             "    @SP\n" + \
             "    M=M+1\n" + \
             "    @EQUAL_END" + str(self._arithmetic_counter) + "\n" + \
             "    0, JMP\n" + \
             "(EQUAL_TRUE" + str(self._arithmetic_counter) + ")\n" + \
             "    @SP\n" + \
             "    A=M\n" + \
             "    M=-1\n" + \
             "    @SP\n" + \
             "    M=M+1\n" + \
             "(EQUAL_END" + str(self._arithmetic_counter) + ")\n"
             
    elif command == "gt":
      # x > y
      _counter_used = True

      hack = "    @SP\n" +\
             "    AM=M-1  \n" +\
             "    D=M \n" +\
             "    @SP\n" +\
             "    AM=M-1  \n" +\
             "    D=M-D\n" +\
             "    @GT_FALSE" + str(self._arithmetic_counter) + "\n" +\
             "    D, JLE\n" +\
             "" + \
             "    @SP\n" + \
             "    A=M\n" + \
             "    M=-1\n" +\
             "    @SP\n" +\
             "    M=M+1\n" +\
             "    @GT_END" + str(self._arithmetic_counter) + "\n" + \
             "    0, JMP\n" +\
             "(GT_FALSE" + str(self._arithmetic_counter) + ")\n" +\
             "    @SP\n" + \
             "    A=M\n" + \
             "    M=0\n" +\
             "    @SP\n" +\
             "    M=M+1\n" +\
             "(GT_END" + str(self._arithmetic_counter) + ")\n"
    elif command == "lt":
      # x < y
      _counter_used = True

      hack = "    @SP\n" + \
             "    AM=M-1\n" + \
             "    D=M \n" + \
             "    @SP\n" + \
             "    AM=M-1  \n" + \
             "    D=M-D\n" + \
             "    @LT_TRUE" + str(self._arithmetic_counter) + "\n" +\
             "    D, JLT\n" + \
             "    @SP\n" + \
             "    A=M\n" + \
             "    M=0\n" + \
             "    @SP\n" + \
             "    M=M+1\n" + \
             "    @LT_END" + str(self._arithmetic_counter) + "\n" + \
             "    0, JMP\n" + \
             "(LT_TRUE" + str(self._arithmetic_counter) + ")\n" +\
             "    @SP\n" + \
             "    A=M\n" + \
             "    M=-1\n" + \
             "    @SP\n" + \
             "    M=M+1\n" + \
             "(LT_END" + str(self._arithmetic_counter) + ")\n"
    elif command == "and":
      # x and y
      hack = "    @SP\n" +\
             "    AM=M-1  \n" +\
             "    D=M \n" +\
             "    @SP\n" +\
             "    AM=M-1  \n" +\
             "    D=M&D\n" +\
             "    M=D\n" +\
             "    @SP\n" + \
             "    M=M+1\n"
    elif command == "or":
      # x or y
      hack ="    @SP\n" +\
            "    AM=M-1\n" +\
            "    D=M\n" +\
            "    @SP\n" +\
            "    AM=M-1\n" +\
            "    D=M|D\n" +\
            "    M=D\n" +\
            "    @SP\n" + \
            "    M=M+1\n"
    elif command == "neg":
      # - y
      hack = "    @SP\n" + \
             "    A=M-1\n" + \
             "    M=-M\n"
    elif command == "not":
      # not y
      hack = "    @SP\n" + \
             "    A=M-1\n" + \
             "    M=!M\n"
    else:
      # unknown command
      return 

    if _counter_used:    
      self._arithmetic_counter += 1

    self._append_output(hack)

  def write_push_pop(self, command, segment, index):
    """
    @command: push/pop
    """
    def _get_segment_addr(segment):
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
        value_hack = "    @{}\n".format(self._get_static_label(index)) + \
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
        target_addr = _get_segment_addr(segment) 
        value_hack = "    @" + str(target_addr) + "\n" +\
                     "    D=M\n" +\
                     "    @" + str(index) + "\n" + \
                     "    A=D+A\n" +\
                     "    D=M\n"

      push_hack = value_hack + "    @SP\n" +\
                               "    A=M\n" +\
                               "    M=D\n" +\
                               "    @SP\n" +\
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
        addr_hack = "    @{}\n".format(self._get_static_label(index)) + \
                    "    D=A\n"
      elif segment == "temp":
        # temp store from 5 as value
        target_addr = _get_segment_addr(segment) + index
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
        target_addr = _get_segment_addr(segment) 
        addr_hack = "    @" + str(target_addr) + "\n" +\
                    "    D=M\n" +\
                    "    @" + str(index) + "\n" + \
                    "    D=D+A\n"

      pop_hack = addr_hack +\
                 "    @SP\n" +\
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

    self._append_output(hack_asm)

  def close(self):
    """
    Add END
    """
    end_hack = "(END)\n" +\
               "    @END\n" +\
               "    0, JMP\n"

    self._append_output(end_hack)

def translate_driver(vm_path, verbose=False):
  """
  The driver of the vm translator
  """
  def _handle_single_vm(code_writer, vm_file_path):
    """
    """
    parser = Parser(vm_file_path)
  
    while parser.has_more_commands():
      cmd = parser.command_type()
      if cmd ==  C_ARITHMETIC:
        arg1 = parser.arg1()
        code_writer.write_arithmetic(arg1)
      elif cmd == C_LABEL:
        arg1 = parser.arg1()
        code_writer.write_label(arg1)
      elif cmd == C_GOTO:
        arg1 = parser.arg1()
        code_writer.write_goto(arg1)
      elif cmd == C_IF:
        arg1 = parser.arg1()
        code_writer.write_if(arg1)
      elif cmd == C_PUSH or cmd == C_POP:
        arg1 = parser.arg1()
        arg2 = parser.arg2()
        code_writer.write_push_pop(cmd, arg1, arg2)
      elif cmd == C_FUNCTION:
        arg1 = parser.arg1()
        arg2 = parser.arg2()
        code_writer.write_function(arg1, arg2)
      elif cmd == C_CALL:
        arg1 = parser.arg1()
        arg2 = parser.arg2()
        code_writer.write_call(arg1, arg2)
      elif cmd == C_RETURN:
        code_writer.write_return()
      else:
        # Unrecoganized
        pass
      
      if verbose == True and cmd != C_EMPTY:
        code_writer.write_comment(parser.current_line())
        
      # advance line
      parser.advance()
    parser.close()
  ### END _handle_single_vm FUNCTION

  if os.path.isdir(vm_path):  # directory
    files = list(filter(lambda file: file.endswith(".vm"), os.listdir(vm_path)))

    if len(files) == 0:
      print("No vm file found under directory")
      return 

    sys_init = False
    if "Sys.vm" in files:
      sys_init = True

    vm_abs_path = os.path.abspath(vm_path)
    output_file = os.path.join(vm_abs_path,os.path.basename(vm_abs_path) + ".asm")
    file_name   = os.path.basename(output_file)[:-4]
    # print(file_name)
    code_writer = CodeWriter(output_file, file_name, sys_init)

    for curr_file in files:
      code_writer.set_filename(curr_file[:-3]) # without ".vm"
      _handle_single_vm(code_writer, os.path.join(vm_abs_path, curr_file))
  elif os.path.isfile(vm_path):     # file
    output_file = vm_path[:-3]+".asm"
    file_name   = os.path.basename(output_file)[:-4]
    # print(file_name)
    code_writer = CodeWriter(output_file, file_name)
    _handle_single_vm(code_writer, vm_path)
  else:
    print("ERROR: Not a file or dir\n") 
    return


  code_writer.close()
  # Close output file
  
if __name__ == "__main__":
  translate_driver(sys.argv[1], True)