listx = list()
for x in range(1, 51):
    listx.append(int(x))

print(listx)
nums = [10, 20, 30, 40, 50]
listx1 = listx

for x in listx:
    if x in nums:
        listx.remove(x)

print(listx)

for x in listx:
    iff
