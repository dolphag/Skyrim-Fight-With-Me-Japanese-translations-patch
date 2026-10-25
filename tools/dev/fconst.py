import sys,struct
sys.argv=['x',sys.argv[1] if len(sys.argv)>1 else 'x/SKSE/Plugins/FightWithMe.dll']+sys.argv[2:]
exec(open('xr.py').read().split("if __name__")[0])
def fval(i):
    for op in i.operands:
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
            va=i.address+i.size+op.mem.disp-IB
            for s in pe.sections:
                if s.VirtualAddress<=va<s.VirtualAddress+s.Misc_VirtualSize and i.mnemonic in('mulss','movss','addss','subss','divss','comiss','maxss','minss'):
                    o=s.PointerToRawData+va-s.VirtualAddress; return struct.unpack('<f',raw[o:o+4])[0]
