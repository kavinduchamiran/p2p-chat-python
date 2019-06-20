import socket
import threading
import sys
import time
from random import randint
import ctypes

from functions import sendMsg, recvMsg

bob = ctypes.cdll.LoadLibrary('./ObliviousTransfer/ot.so')

address = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.connect((address, 10000))
print('connected')

bob.GetPublicParams.restype = ctypes.c_char_p
bob.GetBlinedKey.restype = ctypes.c_char_p
bob.GetSharedTuple.restype = ctypes.c_char_p
bob.GetBValue.restype = ctypes.c_char_p
bob.GetEValue.restype = ctypes.c_char_p
bob.GetAValue.restype = ctypes.c_char_p
bob.GetBlinedR.restype = ctypes.c_char_p

bob.InitOT(1)

securityParam = bob.GetSecurityParam()

# bob receiving from alice
p, g0, g1, g2 = recvMsg(sock)
bob.SetPublicParams(p, g0, g1, g2)
print(p, g0, g1, g2)

# bobBKey = bob.GetBlinedKey()
# # send to alice
# sendMsg(sock, bobBKey)
#
# # receive alices key
# aliceBKey = recvMsg(sock)
# print(aliceBKey)
#
# bob.SetSharedKey(aliceBKey)



