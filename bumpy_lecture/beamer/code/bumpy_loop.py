t = x / v                       # time corresponding to x
data = [x, t]
for i in range(h_data.shape[0]):
    h = h_data[i, :]
    a = acceleration(h, x, v)
    F = -m * a
    u, t = solver(I=0, V=0, m=m, b=b, s=s, F=F, t=t,
                  damping='linear')
    data.append([h, F, u])
