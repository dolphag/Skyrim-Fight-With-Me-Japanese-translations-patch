import sys,pefile,struct,re,collections
from capstone import *
from capstone.x86 import *
p=sys.argv[1]; pe=pefile.PE(p); raw=open(p,'rb').read(); IB=pe.OPTIONAL_HEADER.ImageBase
S={s.Name.rstrip(b'\0').decode():s for s in pe.sections}
rd=S['.rdata']; tx=S['.text']
rdraw=raw[rd.PointerToRawData:rd.PointerToRawData+rd.SizeOfRawData]
def find_str(t):
    b=t.encode(); out=[]
    for m in re.finditer(re.escape(b)+b'\0',rdraw):
        if m.start()==0 or rdraw[m.start()-1]==0: out.append(rd.VirtualAddress+m.start())
    return out
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
code=raw[tx.PointerToRawData:tx.PointerToRawData+tx.Misc_VirtualSize]
ins=[]; _o=0
while _o<len(code):
    n=0
    for i in md.disasm(code[_o:],IB+tx.VirtualAddress+_o):
        ins.append(i); n+=i.size
    _o+=n+1
idx={i.address-IB:k for k,i in enumerate(ins)}
def refs(va):
    out=[]
    for k,i in enumerate(ins):
        for op in i.operands:
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP and i.address+i.size+op.mem.disp-IB==va: out.append(k)
    return out
def calls_after(k,n=25):
    out=[]
    for j in range(k,min(k+n,len(ins))):
        i=ins[j]
        if i.mnemonic=='call' and i.operands[0].type==X86_OP_IMM: out.append((hex(i.address-IB),hex(i.operands[0].imm-IB)))
    return out
if __name__=='__main__':
    for t in sys.argv[2:]:
        for va in find_str(t):
            for k in refs(va): print(repr(t),hex(ins[k].address-IB),calls_after(k)[:4])
