    //  // This file is part of www.nand2tetris.org    //  // and the book "The Elements of Computing Systems"
    //  // by Nisan and Schocken, MIT Press.
    //  // File name: projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm
    //  // Performs a simple calculation and returns the result.
(SimpleFunction.SimpleFunction.test)
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  function SimpleFunction.test 2
    @1
    D=M
    @0
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push local 0
    @1
    D=M
    @1
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push local 1
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M+D
    @SP
    M=M+1
    //  add
    @SP
    A=M-1
    M=!M
    //  not
    @2
    D=M
    @0
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push argument 0
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M+D
    @SP
    M=M+1
    //  add
    @2
    D=M
    @1
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push argument 1
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M-D
    @SP
    M=M+1
    //  sub
    @2
    A=M
    D=A+1
    @R13
    M=D // R13 stores caller's SP
    @1
    D=M
    @5
    A=D-A
    D=M
    @R14
    M=D // R14 store return address
    @SP
    AM=M-1
    D=M
    @2
    A=M
    M=D // caller's ARG store return value
    @1
    A=M-1
    D=M
    @4
    M=D // THAT
    @1
    D=M
    @2
    A=D-A
    D=M
    @3
    M=D // THIS
    @1
    D=M
    @3
    A=D-A
    D=M
    @2
    M=D // ARG
    @1
    D=M
    @4
    A=D-A
    D=M
    @1
    M=D // LCL
    @R13
    D=M
    @SP
    M=D // restore SP
    @R14
    A=M
    0, JMP
    //  return
(END)
    @END
    0, JMP
