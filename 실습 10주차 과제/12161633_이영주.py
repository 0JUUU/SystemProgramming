import sys

def checkArgv():
    if len(sys.argv) == 1:
        print('Please set asm filename')
        exit()
    elif len(sys.argv) >= 3:
        print('Please only set 1 argument for asm filename')
        exit()

def readAsmFile(filepath):
    f = open(filepath, 'rb')
    lines = f.readlines()
    f.close()
    return lines

def readAsmLine(line):
    line_split = line.split()
    line_label = ''
    line_opcode = ''
    line_operand = ''
    if len(line_split) == 2:
        line_opcode, line_operand = line_split
    elif len(line_split) == 3:
        line_label, line_opcode, line_operand = line_split
    return line_label, line_opcode, line_operand

def main():
    checkArgv()  # check is only 1 argument for asm filename
    #  ---------- Pass 1 ----------
    LOCCTR = 0  # current address
    lines = readAsmFile(sys.argv[1])
    for line in lines:
        line_label, line_opcode, line_operand = readAsmLine(line)
        if line_opcode == b'START':
            start_addr = int(line_operand)  # save # [OPERAND] as starting address
            LOCCTR = start_addr	# initialize LOCCTR to starting address
            print('Start address is {:d}'.format(LOCCTR))

main()