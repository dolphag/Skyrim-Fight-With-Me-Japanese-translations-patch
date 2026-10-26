import sys,re
exec(open('sigfind.py').read().split("names={")[0])
olds={'AUTO imm32':0xc048b,'Move imm32':0xaf5f2,'LEVEL imm32':0xbad8e,'you imm32':0x7dc08,'you byte':0x7dc26,'RIGHT HAND imm32':0xb6872,'TEACH imm32':0xb8335,'Adept imm32':0xcee24,'left hand byte1':0xeb256,'left hand byte2':0xeb571}
for k,v in olds.items():
    for n in (48,40,32):
        pat,mask=pattern(old,v,n)
        r=find(pat,mask)
        if len(r)<=3: break
    print(k,hex(v),'->',[hex(x) for x in r][:6],len(pat))
