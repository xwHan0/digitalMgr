
from module import Module
from ulity import ecc_width, bit_width

class Memory(Module):
    def __init__(self, name, width=1, depth=1, **args):
        self.name = name
        self.wid = width
        self.dep = depth
        self.args = args

    def _register(self, inst_num=1):
        regs = 0
        if self.args.get('I1'):
            regs += (self.wid + )
        if self.args.get('O1'):
            regs += self.wid


__all__ = [
    'Memory',
    'Scenario',
    'Write',
    'Read',
    'ReadModifyWrite',
    'REG',
    'SP',
    'TP',
    'DP',
]