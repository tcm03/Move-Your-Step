def add(L, x):
    L = L.copy()
    L.append(x)
    return L

myL = [1, 2, 3]
newL = add(myL, 4)
print(myL)
print(newL)