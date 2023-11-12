
p = 0.04
q = 0.38
delta = 0.71
alpha = 0.3
M = 800
ro = 0.08
r = 0.01
E = [0]
F = [0]
for i in range(100):
    new_E = E[i] + pow(800,2)*p*pow(delta,i) + 0.08*E[i]
    E.append(new_E)
    # if new_E > 120000:
    #     print(f"{i}: {new_E}")
    #     break

#print(new_E)

for i in range(100):
    new_F = F[i] + q*pow(delta,i)*alpha*M
    F.append(new_F)

# apparently the answer to #4 is 3 and I can't be bothered to figure out
# what to do for that one again because my code was bad
#print(new_F)
re_from_fwd = r*(F[59]-F[58])*M

print(re_from_fwd)

N = [800]
for i in range(100):
    new_N = N[i] + (E[i+1] - E[i]) + (F[i+1] - F[i]) + r*(F[i]-F[i-1])*M
    N.append(new_N)
    #if new_N > 1400000:
    #    print(i+1)
    #    break