"""CPU functionality."""


import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.PC = 0
        self.sp = 7
        self.register[self.sp] = 0xF4
        

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
       

    def run(self):
        """Run the CPU."""
       


        running = True

        while running: 

            instruction = self.ram[self.PC] #instruction is the address of the location of the program counter in memory

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            # print(instruction)

            if instruction == HLT:
                running = False
                self.PC += 1
            
            elif instruction == LDI:
                self.register[operand_a] = operand_b
                self.PC += 3 

            elif instruction == PRN:
                print(self.register[operand_a])
                self.PC += 2

            elif instruction == MUL:
                self.alu(instruction, operand_a, operand_b)
                self.PC += 3

            elif instruction == PUSH:
                #decrememt sp
                self.register[self.sp] -= 1
                #copy the value in the given register to the address pointed to by sp
                self.ram[self.register[self.sp]] = self.register[operand_a]
                self.PC += 2

            elif instruction == POP:
                pass
                #copy the value from the address pointed to by sp to the given register
                value = self.ram[self.register[self.sp]]
                self.register[operand_a] = value
                #incrament sp
                self.register[self.sp] += 1
                self.PC += 2
            else: 
                print(f'unknown instruction: {instruction}')


        
