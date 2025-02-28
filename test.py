selection = [1,2,3,2,1,2,2,7,6,8,9,10,11,90,1,1,9,8,2]
var_dict = dict()
for i in selection:
    if i not in var_dict.keys():
        var_dict[i] = 1
    else:
        var_dict[i] += 1

print(var_dict)

maxx = 0
answer = None
for key, value in var_dict.items():
    if value > maxx:
        maxx = value
        answer = key
    elif value == maxx:
        answer = list([answer, key])


import math
print(math.floor(1.3))
print(math.ceil(1.3))
