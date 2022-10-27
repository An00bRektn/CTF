# Writeup Notes

Despite the fact that the binary is stripped, the ghidra decompile is very clean. If you click through the functions, you'll see a lot of bytes being declared, and a string that says "someinitialvalue". There's also a function that explicitly says AES-256-CBC, so I would hope it's obvious at this point what to do.

Pull the encrypted bytes out of the wireshark capture (view as hexdump, convert hexdump to raw bytes), take the many bytes out and reverse them to get a key "supersecretkeyusedforencryption!", and decrypt with CyberChef or Python.
