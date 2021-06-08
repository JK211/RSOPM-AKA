#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC->T->CSP
This codes is to simulate the RC in the RSOPM-AKA scheme
including chameleon hash function, post registration message to blockchain

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

# ************************UDP服务器端编程*********************************
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 12345))  # 绑定端口
data_i, addr_i = s.recvfrom(4096)
i_reg_message = pickle.loads(data_i)
C_i = i_reg_message['C_i']
CH_i = i_reg_message['CH_i']
ID_i = i_reg_message['ID_i']
print("RC接收到的终端注册消息为：", i_reg_message)

data_j, addr_j = s.recvfrom(4096)
j_reg_message = pickle.loads(data_j)
CH_j = j_reg_message['CH_j']
ID_j = j_reg_message['ID_j']
print("RC接收到的CSP注册消息为：", j_reg_message)

"""
RC use Chameleon hash function to post CH_i to the blockchain with CH_ri，which we omit the blockchain programming temporarily
the transaction TXID_ST = b'8b60004928090023bef4292ed4e0e414a9f1eaa2d734d4b34beb5c6b2f33bb59'
"""
TXID_ri = b'8b60004928090023bef4292ed4e0e414a9f1eaa2d734d4b34beb5c6b2f33bb59'
i_reg_comfirm_message = {'TXID_ri': TXID_ri, 'CH_j': CH_j}
b_i_reg_comfirm_message = pickle.dumps(i_reg_comfirm_message)
s.sendto(b_i_reg_comfirm_message, ('127.0.0.1', 9999))

TXID_rj = b'8b65364928090023bef4292ed4e0e414a9f1eaa2d734d4b34beb5c6b2f56af45'
j_reg_comfirm_message = {'TXID_rj': TXID_rj, 'C_i': C_i,'CH_i': CH_i}
b_j_reg_comfirm_message = pickle.dumps(j_reg_comfirm_message)
s.sendto(b_j_reg_comfirm_message, ('127.0.0.1', 12341))

# bloque_i = {'CH_i': CH_i, }
# b_bloque_i = pickle.dumps(bloque_i)
# s.sendto(b_bloque_i, ('127.0.0.1', 12341))