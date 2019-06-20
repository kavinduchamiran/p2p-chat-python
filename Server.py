import socket
import threading
import sys
import time
from random import randint
import ctypes

from functions import sendMsg, recvMsg


alice = ctypes.cdll.LoadLibrary('./ObliviousTransfer/ot.so')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 10000))     # binding to local network card, port 10000
sock.listen(1)

# wait for connection from bob
c, a = sock.accept()

# overwrite default return type to char
alice.GetPublicParams.restype = ctypes.c_char_p
alice.GetBlinedKey.restype = ctypes.c_char_p
alice.GetSharedTuple.restype = ctypes.c_char_p
alice.GetBValue.restype = ctypes.c_char_p
alice.GetEValue.restype = ctypes.c_char_p
alice.GetAValue.restype = ctypes.c_char_p
alice.GetBlinedR.restype = ctypes.c_char_p

alice.InitOT(0)

securityParam = alice.GetSecurityParam()

# Get the security params from initiater(Alice)
p = alice.GetPublicParams(0)
g0 = alice.GetPublicParams(1)
g1 = alice.GetPublicParams(2)
g2 = alice.GetPublicParams(3)

# send values to bob
sendMsg(c, p, g0, g1, g2)

# aliceBKey = alice.GetBlinedKey()
# print(1)
# sendMsg(c, aliceBKey)
#
# # receive bobs key
# bobBkey = recvMsg(c)
# print(bobBkey)
#
# # send to bob
#
#
# alice.SetSharedKey(bobBkey)
