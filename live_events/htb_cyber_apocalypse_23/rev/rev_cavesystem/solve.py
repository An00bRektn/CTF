#!/usr/bin/env python3

import angr
import claripy

success_addr = 0x401ab3
failure_addr = 0x401ac1

flag_len = 15

project = angr.Project("./cave")
initial_state = project.factory.entry_state()
simulation = project.factory.simgr(initial_state)

simulation.explore(find=success_addr , avoid=failure_addr )

if simulation.found:
    solution_state = simulation.found[0]
    print(solution_state.posix.dumps(0))
else:
    print("[!] Failed :(")