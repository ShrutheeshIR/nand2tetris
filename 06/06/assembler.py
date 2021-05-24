jump_table = {  'JGT' : '001',
                'JEQ' : '010',
                'JGE' : '011',
                'JLT' : '100',
                'JNE' : '101',
                'JLE' : '110',
                'JMP' : '111'}

dest_table = {  'M' : '001',
                'D' : '010',
                'MD' : '011',
                'A' : '100',
                'AM' : '101',
                'AD' : '110',
                'AMD' : '111'}

compute_table = {'0': '101010', 
                 '1': '111111', 
                 '-1': '111010', 
                 'D': '001100', 
                 'X': '110000', 
                 '!D': '001101', 
                 '!X': '110001', 
                 '-D': '001111', 
                 '-X': '110011', 
                 'D+1': '011111', 
                 'X+1': '110111', 
                 'D-1': '001110', 
                 'X-1': '110010', 
                 'D+X': '000010', 
                 'D-X': '010011', 
                 'X-D': '000111', 
                 'D&X': '000000', 
                 'D|X': '010101'}

def val2binary(decimal_number):
    # print("DEC2BIN, ", decimal_number, type)
    if decimal_number == 0:
        return 0
    else:
        return (decimal_number % 2 + 10 * (val2binary(decimal_number // 2)))


class SymbolTable:
    def __init__(self):
        self.symboltable = {'SP' : '0', 'LCL' : '1', 'ARG' : '2', 'THIS' : '3', 'THAT' : '4', 'SCREEN' : '16384', 'KBD' : '24576',
                            'R0' : '0',
                            'R1' : '1',
                            'R2' : '2',
                            'R3' : '3',
                            'R4' : '4',
                            'R5' : '5',
                            'R6' : '6',
                            'R7' : '7',
                            'R8' : '8',
                            'R9' : '9',
                            'R10' : '10',
                            'R11' : '11',
                            'R12' : '12',
                            'R13' : '13',
                            'R14' : '14',
                            'R15' : '15',
                            }
        self.variables_added = 0
    
    def add_label(self, label, mem_loc):
        self.symboltable[label] = mem_loc
    
    def incoming_symbol(self, symb):
        if symb not in self.symboltable:
            self.symboltable[symb] = str(16 + self.variables_added)
            self.variables_added += 1
        

        return self.symboltable[symb]

    def display(self):
        for symbol, value in self.symboltable.items():
            print(symbol, value)

class Instruction:
    def __init__(self, code_line, line_no = -1):
        self.code_line = code_line
        self.line_no = line_no
        self.machine_instruction = '0' * 16 
    
    def parse_code_line_firstpass(self):
        code_line = self.code_line
        is_valid = True
        is_not_label = True
        cleaned_assembly_code = code_line[:]

        code_split_comment = code_line.split('//')
        if code_split_comment[0]:
            code_line = code_split_comment[0]
        else:
            is_valid = False
            return is_valid, is_not_label, code_line
        

        code_line = code_line.replace(' ', '')
        if len(code_line) == 0:
            is_valid = False
        else:
            if '(' in code_line:
                is_not_label = False
                code_line = code_line.split('(')[1].split(')')[0]

        return is_valid, is_not_label, code_line

    def parser_second_pass(self):
        if self.code_line[0] == '@':
            self.translate_a_instruction()
        else:
            self.translate_c_instruction()
    
    def translate_a_instruction(self):
        code_line = self.code_line
        # print(code_line)
        if self.code_line[1:].isnumeric():
            binary_comm = val2binary(int(code_line[1:]))
            machine_code = '0' + "%015d"%binary_comm
            self.machine_instruction = machine_code

    def translate_c_instruction(self):

        code_line = self.code_line
        dest_code = '000'
        jump_code = '000'
        mem_code =  '0'
        compute_code = '000000'

        code_line_dest_split = code_line.split('=')
        if len(code_line_dest_split) > 1:
            dest_part = code_line_dest_split[0]
            code_line_wo_dest = code_line_dest_split[1]
            dest_code = dest_table[dest_part]
        
        else:
            code_line_wo_dest = code_line
        
        code_line_jump_split = code_line_wo_dest.split(';')
        if len(code_line_jump_split) > 1:
            jump = code_line_jump_split[1]
            jump_code = jump_table[jump]
        code_line_wo_dest_jump = code_line_jump_split[0]


        compute = code_line_wo_dest_jump
        if 'A' in compute:
            mem_code = '0'
            compute = compute.replace('A', 'X')
        elif 'M' in compute:
            mem_code = '1'
            compute = compute.replace('M', 'X')


        compute_code = compute_table[compute]
        self.machine_instruction = '111' + mem_code + compute_code + dest_code + jump_code
    
    def display(self):
        print(self.code_line, self.machine_instruction)


class Assembler:
    def __init__(self, filename, outfilename):
        self.symbol_table = SymbolTable()

        self.total_lines = -1
        self.cleaned_assembly_code = {}
        self.machine_instructions = {}

        self.filename = filename
        self.out_filename = outfilename
    
    def read_file(self):
        with open(self.filename, 'r') as f:
            self.assembly_code_lines = f.read().split('\n')
        
    def first_pass(self):
        for instruction in self.assembly_code_lines:
            my_ins = Instruction(instruction)
            is_valid, is_not_label, code_line = my_ins.parse_code_line_firstpass()
            if is_valid and is_not_label:
                self.total_lines += 1
                self.cleaned_assembly_code[self.total_lines] = code_line
            elif is_valid and is_not_label == False:
                self.symbol_table.add_label(code_line, self.total_lines+1)

    def second_pass(self):
        for ins_line, instruction in self.cleaned_assembly_code.items():
            if instruction[0] == '@' and instruction[1:].isnumeric() == False:
                symbol2val = self.symbol_table.incoming_symbol(instruction[1:])
                myinstruction = Instruction(instruction[0] + str(symbol2val))
            else:
                myinstruction = Instruction(instruction)
            
            myinstruction.parser_second_pass()
            myinstruction.display()
            self.machine_instructions[ins_line] = myinstruction.machine_instruction

    def write_file(self):
        with open(self.out_filename, 'w') as f:
            for ins_line, instruction in self.machine_instructions.items():
                f.write(instruction)
                f.write('\n')
    
    def runner(self):
        self.read_file()
        self.first_pass()
        self.symbol_table.display()
        print(self.cleaned_assembly_code)
        self.second_pass()
        self.write_file()

    
if __name__ == '__main__':
    infilename = '/home/olorin/Desktop/OS/NAND2TETRIS/nand2tetris/projects/06/add/Add.asm'
    outfilename = '/home/olorin/Desktop/OS/NAND2TETRIS/nand2tetris/projects/06/add/Add.hack'

    assembler = Assembler(infilename, outfilename)
    assembler.runner()








# def first_pass(contlines):
#     for (line_no, code_line) in enumerate(contlines):
#         machine_ins, flag = parser(code_line.strip("\n").strip())
#         if flag == True:
#             overall_machine_ins += machine_ins + '\n'



# def second_pass(contlines):
#     overall_machine_ins = ''
#     for (line_no, code_line) in enumerate(contlines):
#         machine_ins, flag = parser(code_line.strip("\n").strip())
#         if flag == True:
#             overall_machine_ins += machine_ins + '\n'


# def runner(filename):
#     with open(filename, 'r') as f:
#         contlines = f.readlines()

#     my_symbol_table = SymbolTable()
#     changed_machine_ins = first_pass(contlines, my_symbol_table)
#     overall_machine_ins = second_pass(changed_machine_ins)

#     print(overall_machine_ins)


# def parser(code_line):
#     code_split_comment = code_line.split('//')
#     if code_split_comment[0]:
#         code_line = code_split_comment[0]
#     else:
#         return '-1', False
    
#     code_line = code_line.replace(' ', '')

#     if len(code_line) == 0:
#         return '-1', False
#     else:
#         is_a_ins = False
#         if code_line[0] == '@':
#             is_a_ins = True
#         machine_ins = translate(code_line, is_a_ins)
#         return machine_ins, True



# def translate(code_line, is_a_ins):

#     # print("TRANSLATE : ", code_line, is_a_ins)
#     if is_a_ins == True:
#         # print(code_line)
#         if code_line[1:].isnumeric():
#             binary_comm = val2binary(int(code_line[1:]))
#             machine_code = '0' + "%015d"%binary_comm
#     else:

#         dest_code = '000'
#         jump_code = '000'
#         mem_code =  '0'
#         compute_code = '000000'

#         code_line_dest_split = code_line.split('=')
#         if len(code_line_dest_split) > 1:
#             dest_part = code_line_dest_split[0]
#             code_line_wo_dest = code_line_dest_split[1]
#             dest_code = dest_table[dest_part]
        
#         else:
#             code_line_wo_dest = code_line

        
        

#         code_line_jump_split = code_line_wo_dest.split(';')
#         if len(code_line_jump_split) > 1:
#             jump = code_line_jump_split[1]
#             jump_code = jump_table[jump]
#         code_line_wo_dest_jump = code_line_jump_split[0]


#         compute = code_line_wo_dest_jump
#         if 'A' in compute:
#             mem_code = '0'
#             compute = compute.replace('A', 'X')
#         elif 'M' in compute:
#             mem_code = '1'
#             compute = compute.replace('M', 'X')


#         compute_code = compute_table[compute]
#         machine_code = '111' + mem_code + compute_code + dest_code + jump_code
    
#     return machine_code


# if __name__ == '__main__':
#     filename = '/home/olorin/Desktop/OS/NAND2TETRIS/nand2tetris/projects/06/add/add.asm'
    # runner(filename)



# print(dest_table)
# print(translate('D=D+M;JMP', False))


    

# print(type(val2binary(10)))