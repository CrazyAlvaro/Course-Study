    @256
    D=A
    @SP
    M=D
    @StaticsTest.$ret.1
    D=A
    @SP
    A=M
    M=D // store return address
    @SP
    M=M+1
    @1
    D=M
    @SP
    A=M
    M=D // store local 
    @SP
    M=M+1
    @2
    D=M
    @SP
    A=M
    M=D // store arg 
    @SP
    M=M+1
    @3
    D=M
    @SP
    A=M
    M=D // store this 
    @SP
    M=M+1
    @4
    D=M
    @SP
    A=M
    M=D // store that 
    @SP
    M=M+1
    @SP
    D=M
    @1
    M=D // reposition LCL
    @SP
    D=M
    @5
    D=D-A
    @2
    M=D // reposition ARG
    @StaticsTest.Sys.init
    0, JMP
(StaticsTest.$ret.1)
    //  // This file is part of www.nand2tetris.org    //  // and the book "The Elements of Computing Systems"
    //  // by Nisan and Schocken, MIT Press.
    //  // File name: projects/08/FunctionCalls/StaticsTest/Class1.vm
    //  // Stores two supplied arguments in static[0] and static[1].
(StaticsTest.Class1.set)
    //  function Class1.set 0
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
    @Class1.0
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop static 0
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
    @Class1.1
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop static 1
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 0
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
    //  // Returns static[0] - static[1].
(StaticsTest.Class1.get)
    //  function Class1.get 0
    @Class1.0
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push static 0
    @Class1.1
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push static 1
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
    //  // This file is part of www.nand2tetris.org    //  // and the book "The Elements of Computing Systems"
    //  // by Nisan and Schocken, MIT Press.
    //  // File name: projects/08/FunctionCalls/StaticsTest/Sys.vm
    //  // Tests that different functions, stored in two different 
    //  // class files, manipulate the static segment correctly. 
(StaticsTest.Sys.init)
    //  function Sys.init 0
    @6
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 6
    @8
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 8
    @Sys.Sys.init$ret.1
    D=A
    @SP
    A=M
    M=D // store return address
    @SP
    M=M+1
    @1
    D=M
    @SP
    A=M
    M=D // store local 
    @SP
    M=M+1
    @2
    D=M
    @SP
    A=M
    M=D // store arg 
    @SP
    M=M+1
    @3
    D=M
    @SP
    A=M
    M=D // store this 
    @SP
    M=M+1
    @4
    D=M
    @SP
    A=M
    M=D // store that 
    @SP
    M=M+1
    @SP
    D=M
    @1
    M=D // reposition LCL
    @SP
    D=M
    @7
    D=D-A
    @2
    M=D // reposition ARG
    @StaticsTest.Class1.set
    0, JMP
(Sys.Sys.init$ret.1)
    //  call Class1.set 2
    @5
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop temp 0 // Dumps the return value
    @23
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 23
    @15
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 15
    @Sys.Sys.init$ret.2
    D=A
    @SP
    A=M
    M=D // store return address
    @SP
    M=M+1
    @1
    D=M
    @SP
    A=M
    M=D // store local 
    @SP
    M=M+1
    @2
    D=M
    @SP
    A=M
    M=D // store arg 
    @SP
    M=M+1
    @3
    D=M
    @SP
    A=M
    M=D // store this 
    @SP
    M=M+1
    @4
    D=M
    @SP
    A=M
    M=D // store that 
    @SP
    M=M+1
    @SP
    D=M
    @1
    M=D // reposition LCL
    @SP
    D=M
    @7
    D=D-A
    @2
    M=D // reposition ARG
    @StaticsTest.Class2.set
    0, JMP
(Sys.Sys.init$ret.2)
    //  call Class2.set 2
    @5
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop temp 0 // Dumps the return value
    @Sys.Sys.init$ret.3
    D=A
    @SP
    A=M
    M=D // store return address
    @SP
    M=M+1
    @1
    D=M
    @SP
    A=M
    M=D // store local 
    @SP
    M=M+1
    @2
    D=M
    @SP
    A=M
    M=D // store arg 
    @SP
    M=M+1
    @3
    D=M
    @SP
    A=M
    M=D // store this 
    @SP
    M=M+1
    @4
    D=M
    @SP
    A=M
    M=D // store that 
    @SP
    M=M+1
    @SP
    D=M
    @1
    M=D // reposition LCL
    @SP
    D=M
    @5
    D=D-A
    @2
    M=D // reposition ARG
    @StaticsTest.Class1.get
    0, JMP
(Sys.Sys.init$ret.3)
    //  call Class1.get 0
    @Sys.Sys.init$ret.4
    D=A
    @SP
    A=M
    M=D // store return address
    @SP
    M=M+1
    @1
    D=M
    @SP
    A=M
    M=D // store local 
    @SP
    M=M+1
    @2
    D=M
    @SP
    A=M
    M=D // store arg 
    @SP
    M=M+1
    @3
    D=M
    @SP
    A=M
    M=D // store this 
    @SP
    M=M+1
    @4
    D=M
    @SP
    A=M
    M=D // store that 
    @SP
    M=M+1
    @SP
    D=M
    @1
    M=D // reposition LCL
    @SP
    D=M
    @5
    D=D-A
    @2
    M=D // reposition ARG
    @StaticsTest.Class2.get
    0, JMP
(Sys.Sys.init$ret.4)
    //  call Class2.get 0
(Sys.Sys.init$WHILE)
    //  label WHILE
    @Sys.Sys.init$WHILE
    0, JMP
    //  goto WHILE
    //  // This file is part of www.nand2tetris.org    //  // and the book "The Elements of Computing Systems"
    //  // by Nisan and Schocken, MIT Press.
    //  // File name: projects/08/FunctionCalls/StaticsTest/Class2.vm
    //  // Stores two supplied arguments in static[0] and static[1].
(StaticsTest.Class2.set)
    //  function Class2.set 0
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
    @Class2.0
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop static 0
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
    @Class2.1
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop static 1
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 0
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
    //  // Returns static[0] - static[1].
(StaticsTest.Class2.get)
    //  function Class2.get 0
    @Class2.0
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push static 0
    @Class2.1
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push static 1
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
