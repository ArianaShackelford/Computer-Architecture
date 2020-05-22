"""CPU functionality."""


import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.flag = [0] * 8
        self.PC = 0
        self.sp = 7
        self.register[self.sp] = 0xF4
        self.running = False

        self.L = self.flag[5]
        self.G = self.flag[6]
        self.E = self.flag[7]
        
        
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[POP] = self.handle_POP
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE
        


    def load(self, program):
        """Load a program into memory."""

        address = 0
        try:

            with open(sys.argv[1]) as program:
                for line in program:
                    string_split = line.split('#')
                    string_value = string_split[0].strip()
                    if string_value == '':
                        continue
                    integer = int(string_value, 2)
                    self.ram[address] = integer
                    address += 1

        except FileExistsError:
            print('File not found')
            sys.exit(1)
           



    

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
        
        elif op == CMP:
            if self.register[reg_a] > self.register[reg_b]:
                self.G = 1 
            elif self.register[reg_a] < self.register[reg_b]:
                self.L = 1
            elif self.register[reg_b] == self.register[reg_a]:
                self.E = 1
            else:
                self.G, self.L, self.E = 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
       
    def handle_HLT(self, *argv):
        self.running = False
        self.PC += 1
        

    def handle_LDI(self, *argv):
        self.register[argv[0]] = argv[1]
        self.PC += 3 

    def handle_PRN(self, *argv):
        print(self.register[argv[0]])
        self.PC += 2

    def handle_MUL(self, *argv):
        self.alu(instruction, argv[0], argv[1])
        self.PC += 3

    def handle_CMP(self, *argv):
        instruction = self.ram[self.PC]
        opr_a = self.ram_read(self.PC + 1)
        opr_b = self.ram_read(self.PC + 2)

        self.alu(instruction, opr_a, opr_b)
        self.PC += 3

    def handle_PUSH(self, *argv):
        #decrememt sp
        self.register[self.sp] -= 1
        #copy the value in the given register to the address pointed to by sp
        self.ram[self.register[self.sp]] = self.register[argv[0]]
        self.PC += 2

    def handle_POP(self, *argv):
        #copy the value from the address pointed to by sp to the given register
        value = self.ram[self.register[self.sp]]
        self.register[argv[0]] = value
        #incrament sp
        self.register[self.sp] += 1
        self.PC += 2

    def handle_CALL(self, *argv):

        return_address = argv[1]
        self.register[self.sp] -= 1
        top = self.register[self.sp]
        self.ram[top] = return_address

        # self.handle_PUSH(return_address)

        reg_num = self.ram[argv[0]]
        sub_address = self.register[reg_num]

        self.PC = sub_address


    def handle_RET(self, *argv):
        
        top = self.register[self.sp]
        return_address = self.ram[top]
        self.register[self.sp] += 1

        self.PC = return_address

    def handle_JMP(self, *argv):
        self.sp = argv[0]
        self.PC = self.register[self.sp]
    
    def handle_JEQ(self, *argv):
        if self.E == 1:
            self.sp = argv[0]
            self.PC = self.register[self.sp]
        else:
            pass

    def handle_JNE(self, *argv):
        if self.E == 0:
            self.sp = argv[0]
            self.PC = self.register[self.sp]
        else:
            pass

    def run(self):
        """Run the CPU."""
        
        self.running = True
        while self.running:
            instruction = self.ram[self.PC]
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if instruction in self.branchtable:
                self.branchtable[instruction](operand_a, operand_b)  
            else: 
                print(f'unknown instruction: {instruction}')
                sys.exit(1)


        
