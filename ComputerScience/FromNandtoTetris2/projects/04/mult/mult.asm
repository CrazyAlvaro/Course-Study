// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Pseudo Code
// if R1 < 0;
// R1 = - R1, R0 = -R0
// 
// sum = 0
// for i = 0; i < R1; i++
//    sum = sum + R0
// R2 = sum
// End Pseudo Code

// Multiple RAM[1] and RAM[0]
    @R1
    D=M
    @CHANGE_SIGN
    D; JLT // Jump to CHANGE_SIGN if R1 < 0 

    @i
    M=0

    @R2
    M=0

(LOOP)
    @i
    D=M
    @R1
    D=D-M; 
    @END
    D; JEQ // End Loop if i - RAM[1]  == 0

    @R2
    D=M
    @R0
    D=D+M
    @R2
    M=D

    @i
    M = M+1
    @LOOP
    0; JMP 

(CHANGE_SIGN)
    @R1
    D=-M
    M=D

    @R0
    D=-M
    M=D
    @LOOP
    0; JMP

(END)
    @END
    0; JMP 