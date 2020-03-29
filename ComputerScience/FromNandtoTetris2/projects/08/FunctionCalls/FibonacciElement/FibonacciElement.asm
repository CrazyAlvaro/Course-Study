    @256
    D=A
    @SP
    M=D
    @FibonacciElement.$ret.1
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
    @FibonacciElement.Sys.init
    0, JMP
(FibonacciElement.$ret.1)
    //  // This file is part of www.nand2tetris.org    //  // and the book "The Elements of Computing Systems"
    //  // by Nisan and Schocken, MIT Press.
    //  // File name: projects/08/FunctionCalls/FibonacciElement/Main.vm
    //  // Computes the n'th element of the Fibonacci series, recursively.
    //  // n is given in argument[0].  Called by the Sys.init function 
    //  // (part of the Sys.vm file), which also pushes the argument[0] 
    //  // parameter before this code starts running.
(FibonacciElement.Main.fibonacci)
    //  function Main.fibonacci 0
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
    D=M-D
    @LT_TRUE0
    D, JLT
    @SP
    A=M
    M=0
    @SP
    M=M+1
    @LT_END0
    0, JMP
(LT_TRUE0)
    @SP
    A=M
    M=-1
    @SP
    M=M+1
(LT_END0)
    //  lt                     // checks if n<2
    @SP
    AM=M-1
    D=M
    @Main.Main.fibonacci$IF_TRUE
    D, JNE
    //  if-goto IF_TRUE
    @Main.Main.fibonacci$IF_FALSE
    0, JMP
    //  goto IF_FALSE
(Main.Main.fibonacci$IF_TRUE)
    //  label IF_TRUE          // if n<2, return n
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
(Main.Main.fibonacci$IF_FALSE)
    //  label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1)
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
    @Main.Main.fibonacci$ret.1
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
    @6
    D=D-A
    @2
    M=D // reposition ARG
    @FibonacciElement.Main.fibonacci
    0, JMP
(Main.Main.fibonacci$ret.1)
    //  call Main.fibonacci 1  // computes fib(n-2)
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
    @Main.Main.fibonacci$ret.2
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
    @6
    D=D-A
    @2
    M=D // reposition ARG
    @FibonacciElement.Main.fibonacci
    0, JMP
(Main.Main.fibonacci$ret.2)
    //  call Main.fibonacci 1  // computes fib(n-1)
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M+D
    @SP
    M=M+1
    //  add                    // returns fib(n-1) + fib(n-2)
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
    //  // File name: projects/08/FunctionCalls/FibonacciElement/Sys.vm
    //  // Pushes a constant, say n, onto the stack, and calls the Main.fibonacii
    //  // function, which computes the n'th element of the Fibonacci series.
    //  // Note that by convention, the Sys.init function is called "automatically" 
    //  // by the bootstrap code.
(FibonacciElement.Sys.init)
    //  function Sys.init 0
    @4
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 4
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
    @6
    D=D-A
    @2
    M=D // reposition ARG
    @FibonacciElement.Main.fibonacci
    0, JMP
(Sys.Sys.init$ret.1)
    //  call Main.fibonacci 1   // computes the 4'th fibonacci element
(Sys.Sys.init$WHILE)
    //  label WHILE
    @Sys.Sys.init$WHILE
    0, JMP
    //  goto WHILE              // loops infinitely
(END)
    @END
    0, JMP
