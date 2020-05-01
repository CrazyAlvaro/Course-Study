    //  // This file is part of www.nand2tetris.org    //  // and the book "The Elements of Computing Systems"
    //  // by Nisan and Schocken, MIT Press.
    //  // File name: projects/08/ProgramFlow/BasicLoop/BasicLoop.vm
    //  // Computes the sum 1 + 2 + ... + argument[0] and pushes the 
    //  // result onto the stack. Argument[0] is initialized by the test 
    //  // script before this code starts running.
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 0    
    @1
    D=M
    @0
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop local 0         // initializes sum = 0
(BasicLoop.$LOOP_START)
    //  label LOOP_START
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
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M+D
    @SP
    M=M+1
    //  add
    @1
    D=M
    @0
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop local 0	        // sum = sum + counter
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
    @1
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 1
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
    D=M
    @0
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop argument 0      // counter--
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
    @BasicLoop.$LOOP_START
    D, JNE
    //  if-goto LOOP_START  // If counter > 0, goto LOOP_START
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
(END)
    @END
    0, JMP
