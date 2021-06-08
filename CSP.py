#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC->T->CSP
This codes is to simulate the CSP in the RSOPM-AKA scheme
including chameleon hash function, zero knowledge proof for authentication, and key agreement

2021/5/14
Jerry
"""

import sslcrypto
import random
import pickle
import socket
import hashlib
import time
from Cyptology import ChameleonHash_ECC, key_type_transform
from sslcrypto.fallback._util import  bytes_to_int, int_to_bytes
from Cryptodome.PublicKey import ECC

print('-----------------------------------------CSP registration phase-----------------------------------------------')
ChameleonHash = ChameleonHash_ECC.ChameleonHash()  # 实例化对象，这一步注意不可少！！！
KeyTrans = key_type_transform.KeyTrans()
order = ChameleonHash.order()

ID_j = b'223456789abcdef'
m_j = random.randint(1, order - 1)
r_j = random.randint(1, order - 1)   # here is to simulate R=PUF(C)
CH_j = ChameleonHash.Compute_CH(m_j, r_j)
print("The chameleon hash computed by CSP is ", CH_j.CH())
reg_message = {'ID_j': ID_j, 'CH_j': CH_j.CH()}
b_reg_message = pickle.dumps(reg_message)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 12341))
s.sendto(b_reg_message, ('127.0.0.1', 12345))
data, addr = s.recvfrom(4096)
reg_comfirm = pickle.loads(data)
TXID_rj = reg_comfirm['TXID_rj']
print("The transaction ID received by CSP is", TXID_rj)
print("-------------------------------------------CSP registration finished！------------------------------------------")

print('-------------------------------------------AKA phase of CSP-----------------------------------------------')
data_M_1, addr_M_1 = s.recvfrom(4096)
M_1 = pickle.loads(data_M_1)
print("CSP received M1 is ", M_1)

# Blockchain query
C_i = reg_comfirm['C_i']
CH_i = reg_comfirm['CH_i']
print("The chameleon hash CH_i queried from blockchain by CSP is ", CH_i)
# data_bloque, addr_bloque = s.recvfrom(4096)
# bloque = pickle.loads(data_bloque)
# print("bloque: ", bloque)
# CH_i = bloque['CH_i']

H2 = [C_i, M_1['PID_i'], M_1['A_i'], M_1['TS_i']]
print("Received H2 by CSP is ", H2)
b_H2 = pickle.dumps(H2)
h = hashlib.sha3_256()
h.update(b_H2)

z_i = bytes_to_int(bytes(h.hexdigest(), encoding='utf-8'))
m_i = M_1['m_i']

A_i_xy = M_1['A_i']
x = A_i_xy[0]
y = A_i_xy[1]
A_i = ECC.EccPoint(x, y)
P = ECC._curves['P-256'].G
print("m_i: ", m_i)
print("z_i: ", z_i)
CH_i_CSP = P.__mul__(m_i) + A_i.__mul__(z_i)
print("The chameleon hash CH_i_CSP computed by CSP is", CH_i_CSP.xy)
print("CSP_j authenticate T_i") if CH_i_CSP.xy == CH_i else print("T_i is illegal!!!")

rho = random.randint(1, order - 1)  # 随机选择一个随机数ρ
ID_j = b'543216789abcdef'
TS_j = time.process_time()
H0 = [ID_j, TS_j]
b_H0 = pickle.dumps(H0)
k = hashlib.sha3_256()
k.update(b_H0)
PID_j = bytes_to_int(bytes(k.hexdigest(), encoding='utf-8'))
Y_j = ChameleonHash.get_Y()
B_j = Y_j.pointQ.__mul__(rho)
x_j = ChameleonHash.get_x()
H3 = [M_1['PID_i'], PID_j, M_1['TS_i'], TS_j, A_i.__mul__(x_j * rho).xy]
b_H3 = pickle.dumps(H3)
sk = hashlib.sha3_256()
sk.update(b_H3)
SK_ij = bytes_to_int(bytes(sk.hexdigest(), encoding='utf-8'))
H2_j = [SK_ij, PID_j, B_j.xy, TS_j]
b_H2_j = pickle.dumps(H2_j)
z = hashlib.sha3_256()
z.update(b_H2_j)
z_j = bytes_to_int(bytes(z.hexdigest(), encoding='utf-8'))
r_j = rho * z_j

k_j = CH_j.trapdoor()[0]
x_j = CH_j.trapdoor()[1]

m_j = (k_j - r_j * x_j + order) % order

M2 = {'PID_j': PID_j, 'm_j': m_j, 'B_j': B_j.xy, 'TS_j': TS_j, 'TXID_rj': TXID_rj}
b_M2 = pickle.dumps(M2)
s.sendto(b_M2, ('127.0.0.1', 9999))
print('CSP gernerate M_2 is ', M2)
print("-------------------------------------------CSP AKA phase finished！------------------------------------------")