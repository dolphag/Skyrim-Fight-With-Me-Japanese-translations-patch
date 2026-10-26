import sys,re,pefile
from capstone import *
from capstone.x86 import *
def load(p):
    pe=pefile.PE(p); raw=open(p,'rb').read(); IB=pe.OPTIONAL_HEADER.ImageBase
    S={s.Name.rstrip(b'\0').decode():s for s in pe.sections}
    return pe,raw,IB,S
old=load('../fwm020/x/SKSE/Plugins/FightWithMe.dll'); new=load('x/SKSE/Plugins/FightWithMe.dll')
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
def tx(d):
    pe,raw,IB,S=d; t=S['.text']; return raw[t.PointerToRawData:t.PointerToRawData+t.Misc_VirtualSize], t.VirtualAddress
def pattern(d,va,n=60):
    pe,raw,IB,S=d; code,base=tx(d); o=va-base
    pat=bytearray(code[o:o+n+16]); mask=bytearray(b'\xff'*len(pat)); end=0
    for ins in md.disasm(bytes(pat),IB+va):
        a=ins.address-IB-va
        rip=any(op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP for op in ins.operands)
        if rip and ins.disp_size:
            for k in range(ins.disp_size): mask[a+ins.disp_offset+k]=0
        elif ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP):
            for k in range(1,ins.size): mask[a+k]=0
        end=a+ins.size
        if end>=n: break
    return bytes(pat[:end]),bytes(mask[:end])
def find(pat,mask):
    code,base=tx(new); rx=b''.join((re.escape(bytes([p])) if m else b'.') for p,m in zip(pat,mask))
    return [base+m.start() for m in re.finditer(rx,code,re.S)]
names={'LABEL':0xd1c50,'LABELWIDTH':0xd1a00,'TEXT':0xd2230,'TEXTSIZE':0xd2370,'ALLOC':0x1d540,'STRCTOR':0x1d5b0,'PARAGRAPH':0xd1db0,'TEXTONWORLD':0xd1f70}
for k,v in names.items():
    pat,mask=pattern(old,v)
    r=find(pat,mask); print(k,hex(v),'->',[hex(x) for x in r][:5],len(pat))
