
from utility import ecc_width
from math import ceil
from module import Module

def get_int_param(param, params_map):
    if isinstance(param, int):
        return param
    elif isinstance(param, str):
        return params_map.get(param)
    else:
        raise Exception('Invalid param[{0}]'.format(param))


class Field:
    def __init__(self, name, width=1, description='', default=0):
        self.name = name
        self.wid = width
        self.description = description
        self.default = default

    def width(self, params_map={}):
        return get_int_param(self.wid, params_map)
      
    def __repr__(self):
        r = ''
        r += '{0: <20} {1:>8} {2:>8} {3}\n'.format(self.name, self.width, self.default, self.summary)
        return r
      

class Table:
    def __init__(self, name='', summary='', fields=[], depth=1, **args):
        self.name = ''
        self.summary = summary
        self.fields = fields
        self.access = []
        self.args = args
        self.dep = depth

    def append_field(self, *field):
        for f in field:
            self.fields.append(f)
        return self
        
    def append_access(self, *access):
        for a in access:
            self.access.append(a)
        return self

    def width(self, params_map={}):
        """Width with wrap but check code"""
        return sum( *map( lambda f: f.width(params_map), self.fields ) ) * self.get('wrap', 1)

    def depth(self, params_map={}):
        """Depth considering wrap"""
        return ceil(get_int_param(self.dep, params_map) / self.args.get('wrap', 1))

    def logic_width(self, params_map={}):
        """Width with wrap and check code"""
        max_width = self.width(params_map)
        
        chk_typ = self.args.get('chk', None)
        if chk_typ == None: chk_width = 0
        elif chk_typ == 'ecc': chk_width = ecc_width(max_width)
        elif chk_typ == 'parity': chk_width = 1
        else: raise Exception('Invalid parameter chk[{0}] in args. It must be inside of None, ecc and parity'.format(chk_typ))

        return max_width + chk_width

    def read_rate(self, speed_up=1):
        acc = filter(lambda a: isinstance(a, [Read, ReadModifyWrite]), self.access)
        return sum( *map( lambda a: a.rate, acc ) ) * speed_up

    def write_rate(self, speed_up=1):
        acc = filter(lambda a: isinstance(a, [Write, ReadModifyWrite]), self.access)
        return sum( *map( lambda a: a.rate, acc ) ) * speed_up

    def __repr__(self):
        r = '================================================\n'
        r += 'Name: {0}        | Num: {1}\n'.format(self.name, self.num)
        r += '{0}\n'.format(self.summary)
        for f in self.fields:
            r += f.__repr__()
        return r


class Access:
    def __init__(self, typ, summary='', rate=1):
        self.summary = summary
        self.rate = rate


class Write(Access):
    def __init__(self, summary='', rate=1):
        super().__init__(summary, rate)


class Read(Access):
    def __init__(self, summary='', rate=1):
        super().__init__(summary, rate)


class ReadModifyWrite(Access):
    def __init__(self, summary='', rate=1):
        super().__init__(summary, rate)


class Data(Module):
    """
    # Arguement:
        chk {None|'ecc'|'parity'}
    """
    def __init__(self, name, summary='', depth=1, num=1, **args):
        self.name = name
        self.summary = summary
        self.dep = depth
        self.num = num
        self.args = args
        
        self.tbls = [Table(depth=depth, **args)]

    def append_table(self, *table, name='', summary='', depth=None):
        if len(table) > 0:
            for t in table:
                self.tbls.append(t)
            return self
        else:
            depth = depth if depth else self.dep
            self.tbls.append(Table(name, summary=summary, depth=depth, **self.args))
            return self

    def append_field(self, *field, name='', width=0, description='', default=0, tbl=0):
        if len(field) > 0:
            for f in field:
                self.tbls[tbl].append_field(f)
            return self
        else:
            self.tbls[tbl].append_field(Field(name,width,description,default))
        
    def append_access(self, *access, tbl=0):
        for a in access:
            self.access[tbl].append_access(a)
        return self


    def width(self, params_map={}):
        max_width = max(* map(lambda s: s.width(params_map), self.scenarios))
        
        chk_typ = self.args.get('chk', None)
        if chk_typ == None: chk_width = 0
        elif chk_typ == 'ecc': chk_width = ecc_width(max_width)
        elif chk_typ == 'parity': chk_width = 1
        else: raise Exception('Invalid parameter chk[{0}] in args. It must be inside of None, ecc and parity'.format(chk_typ))

        return max_width + chk_width

    def depth(self, params_map={}):
        if isinstance(self.dep, int):
            return self.dep
        elif isinstance(self.dep, str):
            return self.args.get(self.dep, 1)

    def number(self, params_map={}):
        if isinstance(self.num, int):
            return self.num
        elif isinstance(self.num, str):
            return self.args.get(self.num, 1)

    def bits(self, params_map={}):
        return self.width(params_map) * self.depth(params_map)

    def summary(self, params_map={}):
        r = ''
        r += '{0:<30} {1:<3} {2:<4} '.format(self.name, self.typ, self.access_bandwidth())
        r += '{0:>8} {1:>3}'.format(self.depth(params_map), self.number(params_map))
        return r

    def __repr__(self):
        r = '================================================\n'
        r += 'Name: {0}        | Num: {1}\n'.format(self.name, self.num)
        r += '{0}\n'.format(self.summary)
        return r
        

class REG(Data):
    def __init__(self, name, summary='', depth=1, **args):
        super().__init__(name, summary, depth, **args)


class SP(Data):
    def __init__(self, name, summary='', depth=1, **args):
        super().__init__(name, summary, depth, **args)


class TP(Data):
    def __init__(self, name, summary='', depth=1, **args):
        super().__init__(name, summary, depth, **args)


class DP(Data):
    def __init__(self, name, summary='', depth=1, **args):
        super().__init__(name, summary, depth, **args)



__all__ = [
    'Field',
    'Table',
    'Write',
    'Read',
    'ReadModifyWrite',
    'REG',
    'SP',
    'TP',
    'DP',
]