# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.5 (default, Sep 10 2020, 16:47:10) 
# [GCC 8.3.0]
# Embedded file name: emulator.py
from io import TextIOWrapper
from sys import stdout, stdin, exit
from math import ceil
from time import sleep
from copy import deepcopy
from enum import Enum, auto
from dataclasses import dataclass
from multiprocessing.dummy import Process
from typing import Dict, Tuple

class ISA(Enum):
    IMM = auto()
    ADD = auto()
    ADDI = auto()
    SUB = auto()
    SUBI = auto()
    PUSH = auto()
    MULT = auto()
    POP = auto()
    STM = auto()
    LDM = auto()
    CMP = auto()
    JMP = auto()
    JMPN = auto()
    SYS = auto()
    NOP = auto()
    XOR = auto()


@dataclass
class REGISTERS:
    SP: int
    IP: int
    A: int
    B: int
    C: int
    D: int
    F: int


@dataclass
class FILE:
    name: str
    fp_obj: TextIOWrapper
    fp_num: int


roundup = lambda x: int(ceil(x / 1024.0)) * 1024
VMCODE = {'🈳':ISA.NOP, 
 '➕':ISA.ADD, 
 '😖':ISA.ADDI, 
 '➖':ISA.SUB, 
 '✨':ISA.SUBI, 
 '❌':ISA.MULT, 
 '⏬':ISA.PUSH, 
 '🔝':ISA.POP, 
 '😄':ISA.LDM, 
 '😭':ISA.STM, 
 '💯':ISA.CMP, 
 '🚀':ISA.JMP, 
 '🌮':ISA.JMPN, 
 '💀':ISA.SYS, 
 '👻':ISA.IMM, 
 '🥑':ISA.XOR}
VMDATA = {
  '🤖': 0,
  '😍': 1,
  '💢': 2,
  '🤙': 3,
  '😩': 4,
  '👾': 5,
  '🤢': 6,
  '😿': 7,
  '💙': 8,
  '🙉': 9,
  '🙈': 10}
REGS = {
  '🤡': 'SP',
  '🦷': 'IP',
  '😡': 'A',
  '😓': 'B',
  '😷': 'C',
  '🤥': 'D',
  '😿': 'F'}
REGS_INV = {v: k for k, v in REGS.items()}
MEM_OFFSET = 1024

class Processor:
    _CODE = None
    FILES = {}
    FILES: Dict[(int, FILE)]
    _MEM = bytearray()
    _REGISTERS = None

    def __init__(self):
        self.order = [
         0, 1, 2]

    def print_regs(self):
        regs = f"\n======\nSP: {self._REGISTERS.SP}\nIP: {(self._REGISTERS.IP - 2048) / 3}\n======\nA: {self._REGISTERS.A}\nB: {self._REGISTERS.B}\nC: {self._REGISTERS.C}\nD: {self._REGISTERS.D}\n======\nF: {self._REGISTERS.F}\n======\nSTACK (first 10 values from SP):\n{self._MEM[max(0, self._REGISTERS.SP - 10 + 1):self._REGISTERS.SP + 1]}\n======\n        "
        print(regs)

    def load_code(self, exec_code):
        """
        MEM:
        code
        stack
        data_stored
        """
        code = deepcopy(exec_code)
        MAX_SIZE = roundup(len(code) + 2048)
        self._MEM = [
         ''] * MAX_SIZE
        for i in range(len(code)):
            self._MEM[i + 2048] = code[i]
        else:
            stats = f"\n        CODE LENGTH: {len(code)}\n        MEM  LENGTH: {len(self._MEM)}\n        "
            print(stats)

    def init_registers(self) -> 0:
        if self._REGISTERS is not None:
            print('Overriding a current state!')
            s = input('Continue? [yY/nN]')
            if 'n' in s.lower():
                return -1
        self._REGISTERS = REGISTERS(0, 2048, 0, 0, 0, 0, 0)
        return 0

    def execvm(self):
        self.init_registers()
        self._REGISTERS.IP = 2048
        while self._REGISTERS.IP >= 2048:
            while self._REGISTERS.IP <= len(self._MEM):
                try:
                    instr = self._MEM[self._REGISTERS.IP:self._REGISTERS.IP + 3]
                    self.interp_instr(instr=instr)
                    # NEW
                    if self._REGISTERS.IP > 5856 and self._MEM[self._REGISTERS.IP] == '💯':#'🥑':#'💯':
                        pass
                        #print(self._REGISTERS.IP)
                        #print(self._MEM[:2048])
                    #self.print_regs()
                except KeyboardInterrupt:
                    self.print_regs()
                    #print(self._MEM)
                    input()
                
                self._REGISTERS.IP += 3

    def parse_instr(self, instr) -> Tuple[(bytes, bytes, bytes)]:
        opcode = instr[self.order[0]]
        arg1 = instr[self.order[1]]
        arg2 = instr[self.order[2]]
        return (
         opcode, arg1, arg2)

    def get_register_value(self, reg) -> Tuple[(str, int)]:
        try:
            emoji = REGS_INV[reg]
        except:
            emoji = reg

        if emoji == '🤡':
            return ('SP', self._REGISTERS.SP)
        if emoji == '🦷':
            return ('IP', self._REGISTERS.IP)
        if emoji == '😡':
            return ('A', self._REGISTERS.A)
        if emoji == '😓':
            return ('B', self._REGISTERS.B)
        if emoji == '😷':
            return ('C', self._REGISTERS.C)
        if emoji == '🤥':
            return ('D', self._REGISTERS.D)
        if emoji == '😿':
            return ('F', self._REGISTERS.F)

    def set_register_value(self, reg, val):
        try:
            emoji = REGS_INV[reg]
        except:
            emoji = reg
        else:
            if type(val) == str:
                val = ord(val)
        if emoji == '🤡':
            self._REGISTERS.SP = val
        else:
            if emoji == '🦷':
                self._REGISTERS.IP = val
            else:
                if emoji == '😡':
                    self._REGISTERS.A = val
                else:
                    if emoji == '😓':
                        self._REGISTERS.B = val
                    else:
                        if emoji == '😷':
                            self._REGISTERS.C = val
                        else:
                            if emoji == '🤥':
                                self._REGISTERS.D = val
                            else:
                                if emoji == '😿':
                                    self._REGISTERS.F = val

    def get_memory_value(self, offset) -> int:
        return self._MEM[MEM_OFFSET + offset]

    def set_memory_value(self, offset, value):
        self._MEM[MEM_OFFSET + offset] = value

    def interp_instr(self, instr):
        opcode, arg1, arg2 = self.parse_instr(instr)
        op = VMCODE[opcode]
        if op == ISA.NOP:
            temp = 3
            temp2 = 2 + temp
            temp3 = temp + temp2
            del temp3
            del temp2
            return
        if op == ISA.ADD:
            r1name, reg1val = self.get_register_value(arg1)
            _, reg2val = self.get_register_value(arg2)
            val = reg1val + reg2val
            calculated = val
            self.set_register_value(r1name, calculated)
            return
        if op == ISA.ADDI:
            r1name, reg1val = self.get_register_value(arg1)
            imm = VMDATA[arg2]
            val = reg1val + imm
            calculated = val
            self.set_register_value(r1name, calculated)
            return
        if op == ISA.SUB:
            r1name, reg1val = self.get_register_value(arg1)
            _, reg2val = self.get_register_value(arg2)
            val = reg1val - reg2val
            calculated = val
            self.set_register_value(r1name, calculated)
            return
        if op == ISA.SUBI:
            r1name, reg1val = self.get_register_value(arg1)
            imm = VMDATA[arg2]
            val = reg1val - imm
            calculated = val
            self.set_register_value(r1name, calculated)
            return
        if op == ISA.MULT:
            r1name, reg1val = self.get_register_value(arg1)
            _, reg2val = self.get_register_value(arg2)
            val = reg1val * reg2val
            calculated = val
            self.set_register_value(r1name, calculated)
            return
        if op == ISA.PUSH:
            self._REGISTERS.SP += 1
            r1name, reg1val = self.get_register_value(arg1)
            self._MEM[self._REGISTERS.SP] = reg1val
            return
        if op == ISA.POP:
            stk_val = self._MEM[self._REGISTERS.SP]
            r1name, reg1val = self.get_register_value(arg1)
            self.set_register_value(r1name, stk_val)
            self._REGISTERS.SP -= 1
            self._REGISTERS.SP = 0 if self._REGISTERS.SP < 0 else self._REGISTERS.SP
            return
        if op == ISA.LDM:
            reg1_name, _ = self.get_register_value(arg1)
            _, reg2_val = self.get_register_value(arg2)
            mem_val = self.get_memory_value(reg2_val)
            if type(mem_val) == str:
                if mem_val == '':
                    mem_val = 0
                else:
                    mem_val = ord(mem_val)
            self.set_register_value(reg1_name, mem_val)
            return
        if op == ISA.STM:
            _, reg1_val = self.get_register_value(arg1)
            _, reg2_val = self.get_register_value(arg2)
            self.set_memory_value(reg2_val, reg1_val)
            return
        if op == ISA.CMP:
            _, reg1val = self.get_register_value(arg1)
            _, reg2val = self.get_register_value(arg2)
            # NEW
            #print(f"[DEBUG] {reg1val} == {reg2val}")
            self._REGISTERS.F = 0
            if reg1val == reg2val:
                self._REGISTERS.F |= 1
            if reg1val > reg2val:
                self._REGISTERS.F |= 2
            if reg1val < reg2val:
                self._REGISTERS.F |= 4
            if reg1val != reg2val:
                self._REGISTERS.F |= 8
            return
        if op == ISA.JMP:
            INSTRS_COUNT = (len(self._MEM) - 2048) / 3
            cond = VMDATA[arg1]
            _, instr_num = self.get_register_value(arg2)
            instr_num = (instr_num - 1) * 3 + 2048
            flag_register = self._REGISTERS.F
            if cond & flag_register:
                self._REGISTERS.IP = instr_num
            else:
                if cond == 0:
                    self._REGISTERS.IP = instr_num
                else:
                    self._REGISTERS.F = 0
            return
        if op == ISA.JMPN:
            direction = VMDATA[arg1]
            _, num_to_jump = self.get_register_value(arg2)
            _, cond = self.get_register_value('C')
            _, flag_register = self.get_register_value('F')
            if direction == 0:
                instr_to_jump = (num_to_jump + 1) * 3
            else:
                instr_to_jump = (num_to_jump - 1) * 3
            if cond & flag_register:
                if direction == 0:
                    self._REGISTERS.IP = self._REGISTERS.IP - instr_to_jump
                else:
                    if direction == 1:
                        self._REGISTERS.IP = self._REGISTERS.IP + instr_to_jump
            else:
                if cond == 0:
                    if direction == 0:
                        self._REGISTERS.IP = self._REGISTERS.IP - instr_to_jump
                    else:
                        if direction == 1:
                            self._REGISTERS.IP = self._REGISTERS.IP + instr_to_jump
                else:
                    self._REGISTERS.F = 0
            return
        if op == ISA.SYS:
            _, syscall = self.get_register_value(arg1)
            return_reg_name, _ = self.get_register_value(arg2)
            retval = 0
            if syscall == 16:
                retval = self.read_user()
            else:
                if syscall == 32:
                    retval = self.write_user()
                else:
                    if syscall == 48:
                        retval = self.read_file()
                    else:
                        if syscall == 64:
                            retval = self.write_file()
                        else:
                            if syscall == 80:
                                retval = self.open_file()
                            else:
                                if syscall == 96:
                                    retval = self.sleep()
                                else:
                                    if syscall == 112:
                                        retval = self._exit()
                                    else:
                                        if syscall == 128:
                                            pass
            self.set_register_value(return_reg_name, retval)
            return
        if op == ISA.IMM:
            reg = REGS[arg1]
            val = VMDATA[arg2]
            self.set_register_value(reg, val)
        else:
            if op == ISA.XOR:
                r1name, reg1val = self.get_register_value(arg1)
                _, reg2val = self.get_register_value(arg2)
                if type(reg1val) == str:
                    reg1val = int(reg1val)
                if type(reg2val):
                    reg2val = int(reg2val)
                val = reg1val ^ reg2val
                # NEW
                #print(f"[DEBUG]: {r1name} <-- {val} = {reg1val} ^ {reg2val}")
                calculated = val
                self.set_register_value(r1name, calculated)
                return

    def get_string(self, idx):
        name = bytearray()
        iddx = idx
        while True:
            if self.get_memory_value(iddx) != '\x00':
                name.append(self.get_memory_value(iddx))
                iddx += 1

        return name

    def read_user(self):
        stdin.buffer.flush()
        stdout.buffer.flush()
        idx = self._REGISTERS.A
        num_bytes = self._REGISTERS.B
        userin = ''
        length_read = 0
        for _ in range(num_bytes):
            userin += stdin.read(1)
            if userin[-1] in ('\n', '\x05'):
                break
            else:
                length_read += 1
        else:
            userin = userin.encode().ljust(num_bytes, b'\x00')
            iddx = idx
            for b in range(num_bytes):
                self.set_memory_value(iddx, userin[b])
                iddx += 1
            else:
                self.set_memory_value(iddx, 0)
                iddx += 1
                return length_read

    def write_user(self):
        stdin.buffer.flush()
        stdout.buffer.flush()
        idx = self._REGISTERS.A
        num_bytes = self._REGISTERS.B
        data = bytearray()
        for i in range(idx, idx + num_bytes):
            data.append(self.get_memory_value(i))
        else:
            stdout.buffer.write(bytes(data))
            return len(data)

    def read_file(self):
        """
        read(fp, index, number of bytes)
        read(regA, regB, regC)
        """
        fp = self._REGISTERS.A
        idx = self._REGISTERS.B
        num_bytes = self._REGISTERS.C
        file = self.FILES[fp]
        bytes_read = 0
        for i in range(num_bytes):
            self.set_memory_value(idx + i, file.fp_obj.read(1))
            bytes_read += 1
        else:
            return bytes_read

    def open_file(self):
        """
        open(file_str_idx)
        open(regA)
        """
        idx = self._REGISTERS.A
        mode = self._REGISTERS.B
        fname = self.get_string(idx)
        if mode == 49:
            fp = open(fname.decode(), 'rb')
        else:
            if mode == 50:
                fp = open(fname.decode(), 'wb')
        fp_int = 3
        max_num = fp_int
        for fpnum, _ in self.FILES.items():
            if fpnum > max_num:
                max_num = fpnum
        else:
            fpnum = max_num + 1
            new_file = FILE(fname, fp, fpnum)
            self.FILES[fpnum] = new_file
            return fpnum

    def write_file(self):
        """
        write(fp, index, number of bytes)
        write(regA, regB, regC)
        """
        fp = self._REGISTERS.A
        idx = self._REGISTERS.B
        num_bytes = self._REGISTERS.C
        file = self.FILES[fp]
        bytes_written = 0
        for i in range(num_bytes):
            file.write(self.get_memory_value(idx + i))
            bytes_written += 1
        else:
            return bytes_written

    def sleep(self):
        """
        sleep(time)
        sleep(regA)
        """
        sleep_time = self._REGISTERS.A
        sleep(int(sleep_time))

    def _exit(self):
        exit()


p = Processor()
with open('./emojis.out') as fp:
    data = fp.read()
p.load_code(data)
try:
    p.execvm()
except KeyError as e:
    try:
        print('Wrong!')
    finally:
        e = None
        del e

except IndexError as e:
    try:
        print('Ran out of instructions...oops!')
    finally:
        e = None
        del e
# okay decompiling emulator.pyc
