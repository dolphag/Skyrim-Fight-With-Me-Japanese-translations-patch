import pefile,json,bisect,sys
from capstone import *
orig,patched=sys.argv[1],sys.argv[2]
pe=pefile.PE(orig); IB=pe.OPTIONAL_HEADER.ImageBase
pe.parse_data_directories([pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXCEPTION']])
fn=sorted((r.struct.BeginAddress,r.struct.EndAddress) for r in pe.DIRECTORY_ENTRY_EXCEPTION)
starts=[a for a,b in fn]
def func(a):
    i=bisect.bisect_right(starts,a)-1
    return fn[i] if i>=0 and fn[i][0]<=a<fn[i][1] else None
img=bytes(pe.get_memory_mapped_image())
pp=bytes(pefile.PE(patched).get_memory_mapped_image())
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True; md.skipdata=True
# 変更された mov r32,imm32 を全探索(原版と差があるもの)
flag={'edi':'dil','esi':'sil','ebx':'bl','r12d':'r12b','r13d':'r13b','r14d':'r14b','r15d':'r15b','ebp':'bpl','eax':'al','ecx':'cl','edx':'dl','r8d':'r8b','r9d':'r9b','r10d':'r10b','r11d':'r11b'}
txt=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
a0=txt.VirtualAddress; n=0
for i in md.disasm(img[a0:a0+txt.Misc_VirtualSize],IB+a0):
    a=i.address-IB
    if i.mnemonic=='mov' and len(i.operands)==2 and i.operands[0].type==1 and i.operands[1].type==2 and i.size in(5,6) and pp[a:a+i.size]!=img[a:a+i.size]:
        reg=i.reg_name(i.operands[0].reg)
        if reg not in flag: continue
        f=func(a)
        if not f: continue
        old=i.operands[1].imm; new=int.from_bytes(pp[a+i.size-4:a+i.size],'little')
        hits=[]
        for k in md.disasm(img[a+i.size:f[1]],IB+a+i.size):
            s=k.op_str
            if k.mnemonic in('test','and','or','bt') and len(k.operands)==2 and k.operands[1].type==2 and (s.startswith(flag[reg]+',') or s.startswith(reg+',')):
                hits.append((hex(k.address-IB),k.mnemonic,s))
        n+=1
        if hits: print('FLAG?',hex(a),reg,old,'->',new,hits[:3])
print('checked mov-imm edits:',n)
