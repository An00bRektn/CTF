import gdb

# corctf{s331ng_thru_my_0p4qu3_pr3d1c4t35}

gdb.execute("break *0x0041687c")

known_prefix = "corctf"
flag_len = 128
i = 0
while len(known_prefix) < flag_len:
    if '}' in known_prefix:
        print(known_prefix)
        break
    
    for char in range(0x21, 0x7e + 1):
        test_prefix = known_prefix + chr(char)
        test_prefix += "x" * (128 - len(test_prefix)) + "\n"

        with open("attempt.txt", "w") as fd:
            fd.write(test_prefix)

        #print(chr(char), test_prefix)
        gdb.execute("set args")
        gdb.execute("run < attempt.txt >/dev/null")
        
        frame = gdb.selected_frame()
        rdi = hex(frame.read_register("rdi"))
        rsi = hex(frame.read_register("rsi"))

        # guess one, rdi
        guess = gdb.execute(f"x/1bx ({rdi} + {hex(len(known_prefix))})", to_string=True)
        # good one, rsi
        good = gdb.execute(f"x/1bx ({rsi} + {hex(len(known_prefix))})", to_string=True)

        guess_hex = guess.split(':')[1].strip()
        good_hex = good.split(':')[1].strip()
        print(chr(char), test_prefix, good_hex, guess_hex)

        if guess_hex == good_hex:
            known_prefix += chr(char)
            break
    else:
        print("womp womp")
        raise Exception
        
