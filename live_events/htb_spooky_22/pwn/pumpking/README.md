# Writeup Notes

Some light reversing shows us that we just need a hardcoded password, and then whatever we pass into the second input gets hit with a `CALL` instruction. Looking at the `setup()` function, we see some seccomp filters put into place.

```shell
$ seccomp-tools dump ./pumpking
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
 0005: 0x15 0x04 0x00 0x00000000  if (A == read) goto 0010
 0006: 0x15 0x03 0x00 0x00000001  if (A == write) goto 0010
 0007: 0x15 0x02 0x00 0x0000000f  if (A == rt_sigreturn) goto 0010
 0008: 0x15 0x01 0x00 0x0000003c  if (A == exit) goto 0010
 0009: 0x15 0x00 0x01 0x00000101  if (A != openat) goto 0011
 0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0011: 0x06 0x00 0x00 0x00000000  return KILL
```

Seccomp filters prevent what system calls, which are like operating-system level functions, that you can and cannot make. Here, we only have access to `read`, `write`, `openat`, and `rt_sigreturn`. Pwntools' shellcraft tool allows us to generate shellcode where we open the `flag.txt` file, read it into the `rax` register, and then write that out to STDOUT.