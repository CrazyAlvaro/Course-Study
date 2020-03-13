KIND_STATIC = "static"
KIND_FIELD = "field"
KIND_ARG = "argument"
KIND_LCL = "local"

################################################################################
## class: SymbolTable
##   class that maintain the symbol table when parsing Jack program
##
##   variables
##     name: identifier's name
##     type: identifier's type
##     kind: (class): field, static; (subroutine): argument, local
##     count/index: number of current kind of identifiers within the scope
##
##   each symbol represent by an object { _name, _type, _kind, _index }
##
################################################################################
class SymbolTable:
  def __init__(self):
    """
    start processing a class
    """
    self._fld_count = 0 # field
    self._stc_count = 0 # static
    self._arg_count = 0 # argument
    self._lcl_count = 0 # local

    self._clss_table = {}   # class level identifier symbol table
    self._sbrt_table = {}   # subroutine level identifier symbol table

  def start_subroutine(self):
    """
    """
    self._arg_count = 0
    self._lcl_count = 0
    self._sbrt_table = {}   # reset subroutine level identifier symbol table

  def define(self, name, typ, kind):
    """
    class level: field, static
    subroutine level: argument, local
    """
    smbl_obj = dict(_name=name, _type=typ, _kind=kind)

    if kind == KIND_FIELD:
      smbl_obj["_index"] = self._fld_count
      self._fld_count += 1
      self._clss_table[name] = smbl_obj
    elif kind == KIND_STATIC:
      smbl_obj["_index"] = self._stc_count
      self._stc_count += 1
      self._clss_table[name] = smbl_obj
    elif kind == KIND_ARG:
      smbl_obj["_index"] = self._arg_count
      self._arg_count += 1
      self._sbrt_table[name] = smbl_obj
    elif kind == KIND_LCL:
      smbl_obj["_index"] = self._lcl_count
      self._lcl_count += 1
      self._sbrt_table[name] = smbl_obj
    else:
      raise ValueError("SymbolTable:define Unrecoganized kind: {}".format(kind))

  def var_count(self, kind):
    """
    return different kind variable's current count
    """
    if kind == KIND_FIELD:
      return self._fld_count
    elif kind == KIND_STATIC:
      return self._stc_count
    elif kind == KIND_ARG:
      return self._arg_count
    elif kind == KIND_LCL:
      return self._lcl_count
    else:
      raise ValueError("Unrecoganized kind: {}".format(kind))

  def kind_of(self, name):
    """
    find identifer's kind by name
    """
    if name in self._sbrt_table:
      return self._sbrt_table[name]["_kind"]
    elif name in self._clss_table:
      return self._clss_table[name]["_kind"]
    else:
      return None

  def type_of(self, name):
    """
    find identifer's type by name
    """
    if name in self._sbrt_table:
      return self._sbrt_table[name]["_type"]
    elif name in self._clss_table:
      return self._clss_table[name]["_type"]
    else:
      return None

  def index_of(self, name):
    """
    find identifer's index by name
    """
    if name in self._sbrt_table:
      return self._sbrt_table[name]["_index"]
    elif name in self._clss_table:
      return self._clss_table[name]["_index"]
    else:
      return None

  def __str__(self):
    """
    print out symbol table:
    "
    class level:
      name  type  kind   #
      x     int   field  0
      count int   static 0

    subroutine level:
      name  type  kind     #
      this  Point argument 0
      x     int   local    0
    "
    """
    return "{}\n{}\n{}\n{}".format("class level:", self._clss_table, "subroutine level:", self._sbrt_table)

