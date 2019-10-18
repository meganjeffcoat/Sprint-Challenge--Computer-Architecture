"""CPU functionality."""
#functionality, classes, constructor

import sys



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.operations = {
            "LDI": 0b10000010,
            "HLT": 0b00000001,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "ADD": 0b10100000,
            "PUSH": 0b01000101, 
            "POP": 0b01000110,
            "CALL": 0b01010000,
            "RET": 0b00010001,
            "CMP": 0b10100111,
            "JMP": 0b01010100,
            "JEQ": 0b01010101,
            "JNE": 0b01010110,
        }
        self.sp = 7 # stack pointer is register R7, since starting from 0
        self.reg[7] = 0xf4
        self.flag = 0b00000000


    # should accept the address to read and return the value stored there
    def ram_read(self, MAR): # MAR contains the address being read or written to
        return self.ram[MAR]


    # should accept a value to write, and the address to write it to
    def ram_write(self,MAR, MDR): # MDR contains the data that WAS read or the data to write
        self.ram[MAR] = MDR


    def load(self):
        """Load a program into memory."""
        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    try:
                        val =int(num, 2)
                    except ValueError:
                        continue

                    self.ram[address] = val
                    address +=1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.operations["ADD"]:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == self.operations["MUL"]:
            mul = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = mul

        elif op == self.operations["CMP"]:
            # FL bits: 00000LGE
            value_1 = self.reg[reg_a]
            value_2 = self.reg[reg_b]
            # If they are equal, set the Equal E flag to 1, otherwise set it to 0
            if value_1 == value_2:
                self.flag = 0b00000001
            # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0
            if value_1 < value_2:
                self.flag = 0b00000100
            # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0
            if value_1 > value_2:
                self.flag = 0b00000010

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

    def run(self):
        """Run the CPU."""
        # needs to read memory address that's stored in register PC
        # need to store that result in IR
        # self.trace() #trace program execution
        # LDI = 0b10000010 # LDI R0,8 (register immediate, set the value of a register to an integer)
        # PRN = 0b01000111 # PRN R0 (pseudo-instruction, print numeric value stored in the given register)
        # HLT = 0b00000001 # HLT (halt the CPU, and exit the emulator)

        #print(self.ram)

        running = True
        while running:
            IR = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            #self.trace()
            if IR == self.operations["LDI"]:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == self.operations["PRN"]:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.operations["HLT"]:
                running = False
                break
            elif IR == self.operations["MUL"]:
                self.alu(self.operations["MUL"], operand_a, operand_b)
                self.pc += 3
            elif IR == self.operations["PUSH"]:
                # push the value in the given register on the stack
                # Decrement self.sp
                self.sp = (self.sp - 1) & 0xFF
                #copy the value in the given register to the address pointed to by self.sp
                self.ram[self.sp] = self.reg[operand_a]
                self.pc +=2
            elif IR == self.operations["POP"]:
                # pop the value at the top of the stack into the given register
                # copy the value from the address pointed to by self.sp to the given register
                self.reg[operand_a] = self.ram[self.sp]
                # increment self.sp
                self.sp = (self.sp + 1) & 0xFF
                self.pc += 2

            elif IR == self.operations["CALL"]:
                #self.reg[self.sp] -= 1
                # self.sp = (self.sp - 1) & 0xFF
                # self.ram[self.reg[self.sp]] = self.sp + 2

                # self.pc = self.reg[operand_a]
                self.reg[self.sp] -= 1
                self.ram[self.sp] = self.pc +2
                self.pc = self.reg[operand_a]

            elif IR == self.operations["RET"]:
                # self.reg[1] = self.ram[self.reg[self.sp]]
                # #self.reg[self.sp] += 1
                # self.sp = (self.sp + 1) & 0xFF
                # self.pc = self.reg[1]
                self.pc = self.ram[self.sp]
                self.reg[self.sp] += 1

            elif IR == self.operations["ADD"]:
                self.alu(self.operations["ADD"], operand_a, operand_b)
                self.pc += 3
        ########## SC Code ########################################################
            elif IR == self.operations["CMP"]:
                self.alu(self.operations["CMP"], operand_a, operand_b)
                self.pc +=3

            elif IR == self.operations["JMP"]:
                # Jump to the address stored in the given register
                address = self.reg[operand_a]
                # Set the PC to the address stored in the given register
                self.pc = address

            else:
                print(f"Unknown instruction: {self.ram[self.pc]}")
                break
