import sys, struct, pefile
from capstone import *
dll=sys.argv[1]; s=int(sys.argv[2],16); e=int(sys.argv[3],16)
pe=pefile.PE(dll); data=open(dll,'rb').read()
def r2o(r): return pe.get_offset_from_rva(r)
md=Cs(CS_ARCH_X86,CS_MODE_64); md.skipdata=True; md.detail=True
names={0x1236e0:'Label',0x123490:'LabelWidth',0x123cc0:'Text',0x123e00:'TextSize',0x123840:'Paragraph',0x123a00:'TextOnWorld'}
code=data[r2o(s):r2o(e)]
import re
for i in md.disasm(code,s):
    t=i.op_str
    note=''
    m=re.search(r'rip ([+-]) (0x[0-9a-f]+)',t)
    if m:
        tgt=i.address+i.size+(int(m.group(2),16)*(1 if m.group(1)=='+' else -1))
        try:
            o=r2o(tgt); 
            f=struct.unpack('<f',data[o:o+4])[0]; d=struct.unpack('<d',data[o:o+8])[0]
            raw=data[o:o+24]
            note=' ; %x f=%g str=%r'%(tgt,f,raw.split(b'\0')[0][:30])
        except Exception as ex: pass
    if i.mnemonic=='call':
        try:
            tg=int(t,16); note=' ; '+names.get(tg,hex(tg))
        except: pass
    print('%x  %-8s %s%s'%(i.address,i.mnemonic,t,note))
