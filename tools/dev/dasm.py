import sys,pefile
from capstone import *
import sys
p=sys.argv[3] if len(sys.argv)>3 else 'x/SKSE/Plugins/FightWithMe.dll'; pe=pefile.PE(p); raw=open(p,'rb').read(); IB=pe.OPTIONAL_HEADER.ImageBase
t=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
def dis(a,b):
    md=Cs(CS_ARCH_X86,CS_MODE_64)
    o=t.PointerToRawData+a-t.VirtualAddress
    for i in md.disasm(raw[o:o+(b-a)],IB+a): print('%x  %-28s %s %s'%(i.address-IB,i.bytes.hex(),i.mnemonic,i.op_str))
a,b=int(sys.argv[1],16),int(sys.argv[2],16); dis(a,b)
