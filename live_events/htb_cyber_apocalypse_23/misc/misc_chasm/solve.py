#!/usr/bin/env python3

from pwn import *

io = remote(sys.argv[1], int(sys.argv[2]))
context.log_level = 'debug'
class Person:
    def __init__(self, ID: int, time: int) -> None:
        self.id = ID
        self.time = time

    def __repr__(self) -> str:
        return f'{{"id":{self.id}, "time": {self.time}}}'

io.sendlineafter(">", '2')
io.recvuntil('Below are the estimates of how long each of us will take to cross the bridge and the charge left for the flashlight.')
io.recvlineS()
io.recvlineS()
people = []
all_aboard = False
i = 0
while not all_aboard:
    line = io.recvlineS()
    #info(line)
    if line.startswith("Person"):
        people.append(Person(i+1, int(line.split(' ')[4])))
        i += 1
    else:
        all_aboard = True
        flash = line

total = int(flash.split(' ')[5])
for p in people:
    info(f"Person {p.id}: {p.time}")

info(f"Flashlight: {total}")

people.sort(key=lambda x: x.time)
left = people
right = []
solution = []
total_time = 0

def move_fastest_right():
    p1, p2 = left.pop(0), left.pop(0)
    right.append(p1)
    right.append(p2)
    right.sort(key=lambda x: x.time)
    #total_time += max(p1.time, p2.time)
    solution.append([p1.id, p2.id])
    info(f"Moving right: [{p1.id}, {p2.id}]")

def move_fastest_left():
    p1 = right.pop(0)
    left.append(p1)
    left.sort(key=lambda x: x.time)
    #total_time += p1.time
    solution.append([p1.id])
    info(f"Moving left: [{p1.id}]")

def move_slowest_right():
    p1, p2 = left.pop(-1), left.pop(-1)
    right.append(p1)
    right.append(p2)
    right.sort(key=lambda x: x.time)
    #total_time += max(p1.time, p2.time)
    solution.append([p1.id, p2.id])
    info(f"Moving right: [{p1.id}, {p2.id}]")

def go():
    move_fastest_right()
    if len(left) == 0:
        return
    
    move_fastest_left()
    move_slowest_right()
    if len(left) == 0:
        return

    move_fastest_left()   

while len(left) > 0:
    go()

print(solution)
msg = ""
for s in solution:
    msg += f"{s},"

io.sendlineafter(">", msg[:-1])
io.recvuntil("reads:")
io.recvline()
success(io.recvlineS())
