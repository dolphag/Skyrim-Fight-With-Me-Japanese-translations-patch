import sys; sys.argv=[sys.argv[0],'x/SKSE/Plugins/FightWithMe.dll']+sys.argv[1:]
exec(open('xr.py').read().split("if __name__")[0])
for t in sys.argv[2:]:
    for va in find_str(t):
        hits=[]
        for k,i in enumerate(ins):
            for op in i.operands:
                if op.type==X86_OP_MEM and op.mem.base!=X86_REG_RIP and op.mem.disp in range(va,va+len(t)+1,1) and op.mem.disp>=va-0 and abs(op.mem.disp-va)<=len(t): hits.append((hex(i.address-IB),i.mnemonic,i.op_str,op.mem.disp-va))
        print(repr(t[:30]),hex(va),hits[:12])
