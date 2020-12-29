#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief GetSetNum function.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-#

import threading

##
# @brief LOCK    Semaphore Lock variable
LOCK = threading.Semaphore()

##
# @brief LOCK    Sequence number list
d_SEQ_NUM_LIST = {}


##
# @brief Return the sequence number.
# @param s_device_type    device type
# @retval i_ret_seq_num    the sequence number
def GetSeqNum(s_device_type):

    global LOCK
    global d_SEQ_NUM_LIST

    LOCK.acquire()
    i_ret_seq_num = d_SEQ_NUM_LIST[s_device_type]
    if d_SEQ_NUM_LIST[s_device_type] < 255:
        d_SEQ_NUM_LIST[s_device_type] += 1
    else:
        d_SEQ_NUM_LIST[s_device_type] = 0
    LOCK.release()

    return i_ret_seq_num


##
# @brief Create sequence number list.
# @param s_device_type    device type
# @retval None
def CreateSeqList(s_device_type):

    global d_SEQ_NUM_LIST

    if s_device_type not in d_SEQ_NUM_LIST:
        d_SEQ_NUM_LIST[s_device_type] = 0
    else:
        pass
