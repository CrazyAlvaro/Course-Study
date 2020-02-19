// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INITIALIZATION)
    @action_bit
    M=0     // action_bit initialize
    @set
    M=0     // Original not set

(LISTENING)
    @KBD
    D=M
    @SET
    D; JNE  // if keyboard has input, set screen
    @CLEAR
    D; JEQ  // clear if keyboard has no input
    @LISTENINGA
    0; JMP  // Keep Listening

// 256 * 512
// for i = 0; i < 256*512/16; i++
// set SCREEN[addr + i] =  action_bit
//
(SET_LOOP)
    @i
    M=0   // initialized i to 0 

(INNER_LOOP)
    @i
    D=M 
    @8192
    D=D-A
    @LISTENING
    D; JEQ    // if i == 8192; set complete, back to listening,

    @SCREEN
    D=A
    @i
    D=D+M 
    @curr_addr
    M=D

    @action_bit
    D=M
    @curr_addr
    A=M
    M=D     // set curr_addr screen to action_bit
    @i
    M=M+1   //increment i
    @INNER_LOOP
    0; JMP  // Keep looping

(SET)
    @set
    D=M
    @LISTENING
    D; JNE    // Keep Listening if already set

    @set
    M=1
    @action_bit
    M=-1
    @SET_LOOP
    0; JMP    // set screen

(CLEAR)
    @set
    D=M
    @LISTENING
    D; JEQ    // Keep Listening if already cleared

    @set
    M=0
    @action_bit
    M=0
    @SET_LOOP
    0; JMP    // clear screen