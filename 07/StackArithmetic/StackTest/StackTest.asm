
//push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq


//push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 16

@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq


//push constant 16

@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq


//push constant 892

@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt


//push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 892

@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt


//push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt


//push constant 32767

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt


//push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32767

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt


//push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt


//push constant 57

@57
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 31

@31
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 53

@53
D=A
@SP
A=M
M=D
@SP
M=M+1

//add

@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=D+A
@SP
A=M
M=D
@SP
M=M+1

//push constant 112

@112
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub

@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=A-D
@SP
A=M
M=D
@SP
M=M+1

//neg

@SP
M=M-1
@SP
A=M
D=M
D=-D
@SP
A=M
M=D
@SP
M=M+1

//and

@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=D&A
@SP
A=M
M=D
@SP
M=M+1

//push constant 82

@82
D=A
@SP
A=M
M=D
@SP
M=M+1

//or

@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=D|A
@SP
A=M
M=D
@SP
M=M+1

//not

@SP
M=M-1
@SP
A=M
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1
