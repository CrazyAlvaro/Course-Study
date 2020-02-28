    @256
    D=A
    @SP
    M=D
    @NestedCall.$ret.1
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
    @NestedCall.Sys.init
    0, JMP
(NestedCall.$ret.1)
    //  // Sys.vm for NestedCall test.    //  // Sys.init()
    //  //
    //  // Calls Sys.main() and stores return value in temp 1.
    //  // Does not return.  (Enters infinite loop.)
(NestedCall.Sys.init)
    //  function Sys.init 0
    @4000
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 4000	// test THIS and THAT context save
    @3
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 0
    @5000
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 5000
    @4
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 1
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
    @5
    D=D-A
    @2
    M=D // reposition ARG
    @NestedCall.Sys.main
    0, JMP
(Sys.Sys.init$ret.1)
    //  call Sys.main 0
    @6
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop temp 1
(Sys.Sys.init$LOOP)
    //  label LOOP
    @Sys.Sys.init$LOOP
    0, JMP
    //  goto LOOP
    //  // Sys.main()
    //  //
    //  // Sets locals 1, 2 and 3, leaving locals 0 and 4 unchanged to test
    //  // default local initialization to 0.  (RAM set to -1 by test setup.)
    //  // Calls Sys.add12(123) and stores return value (135) in temp 0.
    //  // Returns local 0 + local 1 + local 2 + local 3 + local 4 (456) to confirm
    //  // that locals were not mangled by function call.
(NestedCall.Sys.main)
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
    @0
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  function Sys.main 5
    @4001
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 4001
    @3
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 0
    @5001
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 5001
    @4
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 1
    @200
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 200
    @1
    D=M
    @1
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop local 1
    @40
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 40
    @1
    D=M
    @2
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop local 2
    @6
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 6
    @1
    D=M
    @3
    D=D+A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop local 3
    @123
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 123
    @Sys.Sys.main$ret.1
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
    @NestedCall.Sys.add12
    0, JMP
(Sys.Sys.main$ret.1)
    //  call Sys.add12 1
    @5
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop temp 0
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
    @1
    D=M
    @2
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push local 2
    @1
    D=M
    @3
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push local 3
    @1
    D=M
    @4
    A=D+A
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push local 4
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
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M+D
    @SP
    M=M+1
    //  add
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
    AM=M-1
    D=M
    @SP
    AM=M-1
    M=M+D
    @SP
    M=M+1
    //  add
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
    //  // Sys.add12(int n)
    //  //
    //  // Returns n+12.
(NestedCall.Sys.add12)
    //  function Sys.add12 0
    @4002
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 4002
    @3
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 0
    @5002
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 5002
    @4
    D=A
    @SP
    AM=M-1
    D=D+M
    A=D-M
    D=D-A
    M=D
    //  pop pointer 1
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
    @12
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
    //  push constant 12
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
