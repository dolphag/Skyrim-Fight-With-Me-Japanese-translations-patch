import sys, struct, pefile, re
from capstone import *
dll='x/SKSE/Plugins/FightWithMe.dll'
pe=pefile.PE(dll); data=open(dll,'rb').read()
base=pe.OPTIONAL_HEADER.ImageBase
def rva2off(r): return pe.get_offset_from_rva(r)
text=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
tb=data[text.PointerToRawData:text.PointerToRawData+text.SizeOfRawData]; tva=text.VirtualAddress
def xrefs(s):
    b=s.encode()+b'\0'
    out=[]
    for m in re.finditer(re.escape(b),data):
        off=m.start()
        # rva
        for sec in pe.sections:
            if sec.PointerToRawData<=off<sec.PointerToRawData+sec.SizeOfRawData:
                rva=off-sec.PointerToRawData+sec.VirtualAddress
        # scan lea rip
        for i in range(len(tb)-7):
            if tb[i+1]==0x8d and tb[i] in (0x48,0x4c) and (tb[i+2]&0xc7)==0x05:
                d=struct.unpack('<i',tb[i+3:i+7])[0]
                if tva+i+7+d==rva: out.append(tva+i)
    return out
for s in sys.argv[1:]:
    print(s,[hex(x) for x in xrefs(s)])
