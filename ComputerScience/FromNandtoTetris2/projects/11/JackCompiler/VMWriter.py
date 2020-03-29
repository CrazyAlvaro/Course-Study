import os
import JackTokenizer

class VMWriter:
  def __init__(self, output_file):
    try:
      os.remove(output_file)
    except OSError:
      pass

    self._output_path = output_file

  def _do_write_line(self, content):
    with open(self._output_path, "a") as f:
      f.write("{}\n".format(content))

  def write_push(self, segment, index):
    if segment == JackTokenizer.K_FIELD:
      segment = "this"
    self._do_write_line("push {} {}".format(segment, index))

  def write_pop(self, segment, index):
    if segment == JackTokenizer.K_FIELD:
      segment = "this"
    self._do_write_line("pop {} {}".format(segment, index))

  def write_arithmetic(self, command):
    if command == "*":
      self._do_write_line("call Math.multiply 2")
    elif command == "/":
      self._do_write_line("call Math.divide 2")
    elif command == "+":
      self._do_write_line("add")
    elif command == "-":
      self._do_write_line("sub")
    elif command == "&":
      self._do_write_line("and")
    elif command == "|":
      self._do_write_line("or")
    elif command == ">":
      self._do_write_line("gt")
    elif command == "<":
      self._do_write_line("lt")
    elif command == "=":
      self._do_write_line("eq")
    else:
      self._do_write_line(command)

  def write_label(self, label):
    self._do_write_line("label {}".format(label))

  def write_goto(self, label):
    self._do_write_line("goto {}".format(label))

  def write_if(self, label):
    self._do_write_line("if-goto {}".format(label))

  def write_call(self, name, n_args):
    self._do_write_line("call {} {}".format(name, n_args))

  def write_function(self, name, n_locals):
    self._do_write_line("function {} {}".format(name, n_locals))

  def write_return(self):
    self._do_write_line("return")