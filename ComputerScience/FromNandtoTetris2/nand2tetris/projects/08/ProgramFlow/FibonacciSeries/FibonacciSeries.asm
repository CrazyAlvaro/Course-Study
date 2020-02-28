    //  // This file is part of www.nand2tetris.org    //  // and the book "The Elements of Computing Systems"
    //  // by Nisan and Schocken, MIT Press.
    //  // File name: projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm
    //  // Puts the first argument[0] elements of the Fibonacci series
    //  // in the memory, starting in the address given in argument[1].
    //  // Argument[0] and argument[1] are initialized by the test script 
    //  // before this code starts running.
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
    @4
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 1           // that = argument[1]
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 0
    @4
    D=M
    @0
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop that 0              // first element in the series = 0
    @1
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 1
    @4
    D=M
    @1
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop that 1              // second element in the series = 1
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
    @2
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 2
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
    //  pop argument 0          // num_of_elements -= 2 (first 2 elements are set)
(FibonacciSeries.$MAIN_LOOP_START)
    //  label MAIN_LOOP_START
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
    @FibonacciSeries.$COMPUTE_ELEMENT
    D, JNE
    //  if-goto COMPUTE_ELEMENT // if num_of_elements > 0, goto COMPUTE_ELEMENT
    @FibonacciSeries.$END_PROGRAM
    0, JMP
    //  goto END_PROGRAM        // otherwise, goto END_PROGRAM
(FibonacciSeries.$COMPUTE_ELEMENT)
    //  label COMPUTE_ELEMENT
    @4
    D=M
    @0
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push that 0
    @4
    D=M
    @1
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push that 1
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M+D
    @SP
    M=M+1
    //  add
    @4
    D=M
    @2
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop that 2              // that[2] = that[0] + that[1]
    @4
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push pointer 1
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
    M=M+D
    @SP
    M=M+1
    //  add
    @4
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 1           // that += 1
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
    //  pop argument 0          // num_of_elements--
    @FibonacciSeries.$MAIN_LOOP_START
    0, JMP
    //  goto MAIN_LOOP_START
(FibonacciSeries.$END_PROGRAM)
    //  label END_PROGRAM
(END)
    @END
    0, JMP
