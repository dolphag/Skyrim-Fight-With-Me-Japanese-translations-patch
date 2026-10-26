import sys
sys.argv=['x','x/SKSE/Plugins/FightWithMe.dll']
exec(open('xr.py').read().split("if __name__")[0])
sys.path.insert(0,'tools')
import fwm_cfg as C
from fwm_trans1 import T1; from fwm_trans2 import T2; from fwm_trans3 import T3; from fwm_trans4 import T4; from fwm_trans5 import T5; from fwm_trans6 import T6
T={**T1,**T2,**T3,**T4,**T5,**T6}
raw2=open('out/t8.dll','rb').read()
def regname(r): return md.reg_name(r)
res=[]
for en,ja in T.items():
    L=len(en.encode()); JL=len(ja.encode())
    if L==JL: continue
    for va in find_str(en):
        for k in refs(va):
            i0=ins[k]
            if i0.mnemonic!='lea': continue
            # look for a store of a register as length in next 8 instructions: mov [mem], reg
            for j in range(k+1,min(len(ins),k+10)):
                x=ins[j]
                if x.mnemonic in('call','ret','jmp'): break
                if x.mnemonic=='mov' and len(x.operands)==2 and x.operands[0].type==X86_OP_MEM and x.operands[1].type==X86_OP_REG and x.operands[0].size==8:
                    reg=x.operands[1].reg
                    if reg==i0.operands[0].reg: continue
                    # back-search for mov reg,imm==L
                    for m in range(j-1,max(0,j-150),-1):
                        y=ins[m]
                        if y.mnemonic in('ret',) : break
                        if y.mnemonic=='mov' and y.operands[0].type==X86_OP_REG and y.operands[1].type==X86_OP_IMM and md.reg_name(y.operands[0].reg) in (regname(reg),regname(reg).replace('r','e')) and y.operands[1].imm==L:
                            o2=tx.PointerToRawData+y.address-IB-tx.VirtualAddress
                            y2=next(md.disasm(raw2[o2:o2+15],y.address))
                            if y2.operands[1].imm==L: res.append((en[:30],ja[:10],hex(i0.address-IB),hex(y.address-IB),y.mnemonic+' '+y.op_str,'store@'+hex(x.address-IB)))
                            break
                        if y.mnemonic in ('mov','xor','lea','movzx') and y.operands[0].type==X86_OP_REG and y.operands[0].reg==reg: break
                    break
print(len(res))
for r in sorted(set(res)): print(r)
