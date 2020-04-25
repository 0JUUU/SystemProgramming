import sys

def checkArgv():
    if len(sys.argv) == 1:
        print("Please set asm filename")
        exit()
    elif len(sys.argv) >= 3:
        print("Please only set 1 gargument for as filename")
        exit()

    print("Successfully loaded")

def readAsmFile(filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readAsmLine(line):
    if line[0] == '.': # this is comment line
        return ['.', '.', '.']
    line_split = line.split()
    line_label = ''
    line_opcode = ''
    line_operand = ''

    if len(line_split) == 2:
        line_opcode, line_operand = line_split
        line_opcode = line_split[0]
        line_operand = line_split[1]
    elif len(line_split) == 3:
        line_label, line_opcode, line_operand = line_split
    elif len(line_split) == 1:
        line_opcode = line_split[0]

    return [line_label, line_opcode, line_operand]

def main():
    checkArgv() # check is only 1 argument for asm filename

    # initialization
    intermediate_file = []
    # Dictionary of defined symbols and their values
    SYMTAB = {}
    # OP Table
    OPTAB = {'START':'', 'LDA':0x00, 'STA':0x0C, 'ADD':0x18, 'RSUB':0x4C}

    # ----- PASS 1 ----
    LOCCTR = 0  # current address # initialize LOCCTR to 0
    lines = readAsmFile(sys.argv[1])
    for line in lines:
        line_label, line_opcode, line_operand = readAsmLine(line)

        if line_opcode == 'START':
            start_addr = int(line_operand) # save # [OPERAND] as starting address
            LOCCTR = start_addr # initialization LOCCTR to starting address
            print('Start address is {:d}'.format(start_addr))
            intermediate_file.append(['', line_label, line_opcode, line_operand]) # write line to intermediate file
        elif line_opcode != 'END':
            if not line_label == '.': # this is not a comment line
                if not line_label == '': # there is a symbol in the LABEL filed
                    if line_label in SYMTAB: # search SYMTAB for LABEL, if found then set error flag
                        print('EROR : duplicated symbol')
                        exit()
                    else:
                        SYMTAB[line_label] = LOCCTR # insert (LABEL, LOCCTR) into SYMTAB
                # write line to intermediate file
                intermediate_file.append([LOCCTR, line_label, line_opcode, line_operand])
            if line_opcode in OPTAB: # search OPTAB for OPCODE
                LOCCTR += 3 # {instruction length} to LOCCTR
            elif line_opcode == 'WORD':
                LOCCTR += 3 # add to LOCCTR
            elif line_opcode == 'RESW':
                LOCCTR += 3*int(line_operand) # add 3 *  #[OPERAND] to LOCCTR
            elif line_opcode == 'BYTE':
                # 문자 또는 16진수 상수를 생성, 상수를 표현하는데 필요한 만큼의 바이트를 지정
                print('implement later')
            elif line_opcode == '.':
                print('')
            else:
                print('ERROR : invalid operation code') # set error flag (invalid operation code)
                exit()
    program_length = LOCCTR - start_addr # save (LOCCTR - starting address) as program length
    print('program length is {:d}'.format(program_length))
    print(SYMTAB.items())
    for line in intermediate_file:
        print(line)
main()