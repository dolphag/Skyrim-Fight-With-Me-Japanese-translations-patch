import sys
sys.argv=['x','x/SKSE/Plugins/FightWithMe.dll']
exec(open('xr.py').read().split("if __name__")[0])
sys.path.insert(0,'tools')
import importlib, fwm_cfg as C
from fwm_trans1 import T1; from fwm_trans2 import T2; from fwm_trans3 import T3; from fwm_trans4 import T4; from fwm_trans5 import T5; from fwm_trans6 import T6
T={**T1,**T2,**T3,**T4,**T5,**T6}
# patched dll to see which immediates remain
import pefile
rep=__import__('json').load(open('out/t8.json'))
patched_addrs=set()
cand=[]
import os
W=int(os.environ.get('W','40')); MINL=int(os.environ.get('MINL','4'))
raw2=open('out/t8.dll','rb').read()
def immv(i):
    for op in i.operands:
        if op.type==X86_OP_IMM: return op.imm
for en,ja in T.items():
    L=len(en.encode()); JL=len(ja.encode())
    if L==JL or L<MINL: continue
    for va in find_str(en):
        for k in refs(va):
            lo=max(0,k-W); hi=min(len(ins),k+W)
            for j in range(lo,hi):
                i=ins[j]
                if i.mnemonic in('mov','cmp','add','sub','lea') and immv(i)==L and i.size>=3:
                    o2=tx.PointerToRawData+i.address-IB-tx.VirtualAddress
                    i2=next(md.disasm(raw2[o2:o2+15],i.address))
                    if immv(i2)==L: cand.append((en[:30],ja[:12],hex(ins[k].address-IB),hex(i.address-IB),i.mnemonic+' '+i.op_str))
print(len(cand))
import collections
for c in cand: print(c)
