from VMConstants import *

class Parser:
    '''
    Reads input file, and loads every command. 
    '''
    _command_type = { 'add' : C_ALU, 'sub' : C_ALU, 'neg' : C_ALU,   #arithmetic 
                     'gt' : C_ALU, 'lt' : C_ALU, 'eq' : C_ALU,      #logical
                     'and' : C_ALU, 'or' : C_ALU, 'not' : C_ALU,     #bitwise
                     'push' : C_PUSH,
                     'pop' : C_POP
                   }
    
    _nullary_args = [C_ALU]
    _unary_args = []
    _binary_args = [C_PUSH, C_POP]

    def __init__(self):
        self.cmd_type = C_NONE
        self.arg1 = ''
        self.arg2 = ''
        self.cmd_args_no = -1
        self.cmd_name = ''

    def _set_cmd_type(id):
        self.cmd_type = self._command_type[id]


    def parse_cmd(command_tokens):
        if command_tokens[0] in self._command_type:
            self._set_cmd_type(command_tokens[0])
            self.cmd_name = command_tokens[0]
        
        if self.cmd_type in self._nullary_args:
            self.cmd_args_no = 0
        
        elif self.cmd_type in self._binary_args:
            self.cmd_args_no = 2
            self.arg1 = command_tokens[1]
            self.arg2 = command_tokens[2]


class Tokenizer:
    def __init__(self, cmdstr):
        self.cmd_str = cmdstr
    
    def parse(self):
        my_cmd = self.cmd_str
        my_cmd = my_cmd.replace(';','').tolower()
        cmd_tokens = my_cmd.split(' ')
        if len(cmd_tokens):
            return cmd_tokens
        else:
            return -1



class CodeWriter:
    '''
    Required operations: 
    SP: dec SP, inc SP, set SP
    '''

    def __init__(self, command, writer):
        self.command = command
        self.out_buf = writer
    

    def _alu_op(self, alu_operation):
        if alu_operation == 'add':
            self._binary_aluop('D+A')
        elif alu_operation == 'sub':
            self._binary_aluop('D-A')
        elif alu_operation == 'and':
            self._binary_aluop('D&A')
        elif alu_operation == 'or':
            self._binary_aluop('D|A')

        elif alu_operation == 'neg':
            self._unary_aluop('-D')
        elif alu_operation == 'not':
            self._unary_aluop('!D')


    def _binary_aluop(computation):
        self._dec_SP()        
        self._a_command('SP')
        self._c_command('A', 'M')
        self._c_command('D', 'M')

        self._dec_SP()        
        self._a_command('SP')
        self._c_command('A', 'M')
        self._c_command('A', 'M')
        
        self._c_command('D', computation)

        self._a_command('SP')
        self._c_command('A', 'M')
        self._c_command('M', 'D')

        self._inc_SP()

    def _push_operation(self, memseg, addr):
        self._get_offset_memseg(memseg, addr)
        self._c_command('D', 'M')
        self._deref_assignSP()
        self._inc_SP()

    def _pop_operation(self, tokens):
        self._get_offset_memseg(memseg, addr)

        self._a_command('R15')
        self._c_command('A', 'D')

        self._dec_SP()
        self._ref_SP()

        self._a_command('R15')
        self._c_command('A', 'M')

        self._c_command('M', 'D')


    def _get_offset_memseg(self, memseg, addr, do_indir_add=True):

        if addr!='0':
            self._a_command(addr)
            self._c_command('D', 'A')
            self._a_command(memseg)
            self._c_command('A', 'M')
            self._c_command('AD', 'A+D')
        
        else:
            self._a_command(addr)
            self._c_command('AD', 'M')


    def _deref_assignSP(self):
        self._a_command('SP')
        self._c_command('A', 'M')
        self._c_command('M', 'D')

    def _ref_SP(self):
        '''
        Store the value in memory held by stack pointer onto 'D'
        '''
        self._a_command('SP')
        self._c_command('A', 'M')
        self._c_command('D', 'M')


    def _inc_SP(self):
        self._a_command('SP')
        self._c_command('M', 'M+1')

    def _dec_SP(self):
        self._a_command('SP')
        self._c_command('M', 'M-1')

    def _a_command(self, addr):
        self.out_buf.write('@' + addr + '\n')

    def _c_command(self, dest, comp):
        my_cmd = ''
        if dest:
            my_cmd += dest + '='
        if comp:
            my_cmd += comp
        self.out_buf.write(my_cmd + '\n')

    def translate_and_write(self):
        if self.command.cmd_type == C_PUSH:
            self._push_operation(self.command.arg1, self.command.arg2)
        elif self.command.cmd_type == C_POP:
            self._pop_operation(self.command.arg1, self.command.arg2)
        elif self.command.cmd_type == C_ALU:
            self._alu_op(self.command.cmd_name)


class VMTranslate:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.inp_cmds = []
        self.out_buf = None
    
    def _open_file(self):
        with open(self.infile, 'r') as f:
            lines = f.readlines()
        self.inp_cmds = lines

    def _open_out(self):
        self.out_buf = open(self.outfile, 'w')

    def runner(self):
        self._open_file()
        self._open_out()
        for cmd in self.inp_cmds:
            cmd_tokens = Tokenizer(cmd).parse()
            cw = CodeWriter(cmd_tokens, self.out_buf)
            cw.translate_and_write()

if __name__ == '__main__':
    vmt = VMTranslate('07\MemoryAccess\BasicTest\BasicTest.vm', )
