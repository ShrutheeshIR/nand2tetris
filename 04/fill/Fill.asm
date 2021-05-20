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

(LOOP)

    @KBD
    D=M

    @BLANKSCRN
    D;JEQ

    @R0
    M=-1
    @FILLSCREEN
    0;JMP

    (BLANKSCRN)
    @R0
    M=0
    @FILLSCREEN
    0;JMP


(FILLSCREEN)

    @8191
    D=A
    @R1
    M=D

    // Walk the screen and set the values to R0.
    (NEXT)
        @R1
        D=M
        @pos
        M=D
        @SCREEN
        D=A
        @pos
        M=M+D

        @R0
        D=M
        @pos
        A=M
        M=D


        @R1
        D=M-1
        M=D
        @NEXT
        D;JGE



@SCREEN
M=0

@LOOP
D; JMP
