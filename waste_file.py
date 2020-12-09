from memory_profiler import profile
import time
strt = time.time()
myset = {value for value in range(99999)}
end = time.time()
gd = end - strt
str1 = time.time()
mylis = [value for value in range(99999)]
end1 = time.time()
gd1 = end1 - str1

print("lis",gd1)
print(gd)
ele = ["asdasdasdasd", "adasdsadasasdsa"," qqadasdas"]
res  = ', '.join(ele)
print(res)