import sys,pefile,struct
from capstone import *
from capstone.x86 import *
p,a,b=sys.argv[1],int(sys.argv[2],16),int(sys.argv[3],16)
pe=pefile.PE(p); raw=open(p,'rb').read(); IB=pe.OPTIONAL_HEADER.ImageBase
def sec(va):
    for s in pe.sections:
        if s.VirtualAddress<=va<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData): return s
def rd(va):
    s=sec(va); o=s.PointerToRawData+va-s.VirtualAddress; e=raw.index(b'\0',o); return raw[o:e].decode('utf-8','replace')
t=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
o=t.PointerToRawData+a-t.VirtualAddress
for i in md.disasm(raw[o:o+(b-a)],IB+a):
    s=''
    for op in i.operands:
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
            va=i.address+i.size+op.mem.disp-IB
            try: s=' ; "'+rd(va)[:50]+'"'
            except Exception: pass
    print('%x  %s %s%s'%(i.address-IB,i.mnemonic,i.op_str,s))
