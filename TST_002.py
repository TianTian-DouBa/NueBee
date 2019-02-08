from ctypes import *
nb = cdll.LoadLibrary('./activiation32.so')
print("c dll loaded")
# nb.WriteActiveFile.restype = c_bool
# result = not nb.WriteActiveFile()
# print("Write file success? ", result)
nb.ValidKey.restype = c_bool
result = nb.ValidKey()
print("License Active:", result)
