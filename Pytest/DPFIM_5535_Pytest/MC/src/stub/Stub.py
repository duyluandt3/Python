# --------------------------------------------------------------------
# AutoEva - Automatic Evaluation System for Wi-Fi
#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# CP_Stub function.
##

# -*- coding: utf-8 -*-
import queue
import time
import threading
import binascii
import json

from Debug import *
from Encode_TLV import Encode_TLV_Ack
from Encode_TLV import Encode_TLV_Rsp
from Encode_ComHdr import Encode_ComHdr
from Decode_TLV import Decode_TLV
from Decode_ComHdr import Decode_ComHdr


LOCK = threading.Semaphore()

QUE_RCV_LIST = {}
with open("config/DeviceInfo.json", "r", encoding='utf-8-sig') \
                                                        as f_deviceInfo:
    d_deviceInfo = json.load(f_deviceInfo)
    for s_ifname in  list(d_deviceInfo):
        if "SOCKET" == d_deviceInfo[s_ifname]:
            s_key_param = d_deviceInfo[s_ifname]["SOCKET"]["PORT"]
        else:
            s_key_param = d_deviceInfo[s_ifname]["SERIAL"]["COMPORT"]

        QUE_RCV_LIST[s_key_param] = queue.Queue()

QUE_SND_LIST = {}
BASE_TIME = 0
i_REQ_SEQNUM = 0


def STUB_GetSeqNum():
    global LOCK
    global i_REQ_SEQNUM

    LOCK.acquire()
    i_ret_seq_num = i_REQ_SEQNUM
    if i_REQ_SEQNUM < 255:
        i_REQ_SEQNUM += 1
    else:
        i_REQ_SEQNUM = 0
    LOCK.release()

    return i_ret_seq_num


def STUB_Create_Log_Command(i_dst_id, i_src_id, s_log_data, i_MODULE_STUB):
    global BASE_TIME

    i_TYPE_OffsetTime_len = 4

    # create OffsetTime tlv
    s_tlv_value = hex(i_TYPE_OffsetTime)[2:].zfill(4)
    i_tlv_all_len = 2

    s_tlv_value += hex(i_TYPE_OffsetTime_len)[2:].zfill(4)
    i_tlv_all_len += 2

    if 0 != BASE_TIME:
        f_currenttime = time.time()
#        print("[STUB][DBG] current time -> " + str(f_currenttime))
        f_offsettime = f_currenttime - BASE_TIME
#        print("[STUB][DBG] diff time -> " + str(f_offsettime))
        # register by usec unit
        i_offsettime = int(f_offsettime * 1000000)
#        print("[STUB][DBG] offset time -> " + str(i_offsettime))
        s_tlv_value += hex(i_offsettime)[2:].zfill(8)
    else:
        s_tlv_value += hex(0)[2:].zfill(8)
    i_tlv_all_len += 4

    # create LogData tlv
    s_tlv_value += hex(i_TYPE_LogData)[2:].zfill(4)
    i_tlv_all_len += 2

    i_tlv_len = len(s_log_data)
    s_tlv_value += hex(i_tlv_len)[2:].zfill(4)
    i_tlv_all_len += 2

    # set data to list by separating byte unit
    for s_char in s_log_data:
        s_tlv_value += hex(ord(s_char))[2:]
    i_tlv_all_len += i_tlv_len

    # swap src id and dsc id
    tmp = i_dst_id
    i_dst_id = i_src_id
    i_src_id = tmp

    # create common header
    i_ack_num = 0
    i_cmd_id = i_CMD_NotifyCaptureLog
    i_action = 0x11
    i_seq_num = STUB_GetSeqNum()
    s_comhdr = Encode_ComHdr(i_dst_id, \
                                i_src_id, \
                                i_cmd_id, \
                                i_action, \
                                i_seq_num, \
                                i_ack_num, \
                                i_tlv_all_len, \
                                s_tlv_value, \
                                i_MODULE_STUB)
    return s_comhdr + s_tlv_value


def STUB_Create_Rsp_TLV(i_cmd_id, i_action):
    d_tlv_param = {}

    # ResetDUT
    if 1 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # GetStateDUT
    elif 2 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0, "DeviceStatus": 1}
    # SetCurrentTime
    elif 3 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # InitWLAN
    elif 4 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetInstance
    elif 5 == i_cmd_id:
        #reserved
        pass
    # TerminateWLAN
    elif 6 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetCountryCode or GetCountryCode
    elif 7 == i_cmd_id:
        # default
        if i_action & 0xf0:
            d_tlv_param = {"Result": 0, "CountryCode": "US"}
        else:
            d_tlv_param = {"Result": 0}
    # GetRssi
    elif 8 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0, "Rssi": -40}
    # GetMacAddr
    elif 9 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0, "Bssid": "02:11:22:33:44:55"}
    # SetIpInfo or GetIpInfo
    elif 10 == i_cmd_id:
        # default
        if 0 == i_action & 0xf0:
            d_tlv_param = {"Result": 0, \
                            "IpAddress": "192.168.0.99", \
                            "NetMask": "255.255.255.0", \
                            "GateWay": "192.168.0.1"}
        else:
            d_tlv_param = {"Result": 0}
    # StartPing
    elif 11 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # StartIperf
    elif 12 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # FinishIperfServerProcess
    elif 13 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0, \
        "IperfCmdString": "[  4]  0.0-90.0 sec   297 MBytes  27.7 Mbits/sec"}
    # SetDhcpIpInfo
    elif 14 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0, \
                        "IpAddress": "192.168.0.99", \
                        "NetMask": "255.255.255.255.0", \
                        "GateWay": "192.168.0.1"}
    # StartDhcpd
    elif 15 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # GetCaptureLog
    elif 16 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # StartCaptureLog
    elif 17 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # StopCaptureLog
    elif 18 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # Scan or GetScanList
    elif 32 == i_cmd_id:
        # default
        if i_action & 0xf0:
            d_tlv_param = {"Result": 0}
        else:
            d_tlv_param = {"Result": 0, "NumOfAp" : 0}
    # ConnectAp or GetApInfo
    elif 33 == i_cmd_id:
        # default
        if i_action & 0xf0:
            d_tlv_param = {"Result": 0}
        else:
            d_tlv_param = {"Result": 0}
    # DisconnectAp
    elif 34 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetPowersaveMode
    elif 35 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetSsid
    elif 64 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetOpenSecurity
    elif 65 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetWepSecurity
    elif 66 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetWpaSecurity
    elif 67 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetChannel
    elif 68 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetStealthMode
    elif 69 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetRadioOutput
    elif 70 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # GetStaList
    elif 71 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # SetConnectionLimit
    elif 72 == i_cmd_id:
        # default
        d_tlv_param = {"Result": 0}
    # unexpected cmd id
    else:
        pass

    return d_tlv_param


def Stub_Readline(s_portNo):
    global QUE_RCV_LIST

    que_rcv = QUE_RCV_LIST[s_portNo]
    # DEBUG
#    print("[STB] wait ack/rsp command !!")
    s_command = que_rcv.get()
    try:
        b_rply_command = binascii.unhexlify(s_command)
        print("[STB] rply command -> " + str(b_rply_command) + " len : " + str(len(b_rply_command)))
    except:
        print("[STB] " + s_command)

    return b_rply_command


def Stub_Write(b_command):
    global QUE_SND_LIST

    print("[STB] snd command -> " + str(b_command) + " len : " + str(len(b_command)))
    s_command = binascii.hexlify(b_command).decode('utf-8')

    i_result, \
    i_dst_id, \
    i_src_id, \
    i_cmd_id, \
    i_action, \
    i_seq_num, \
    i_ack_num, \
    i_tlv_len, s_tlv_data = Decode_ComHdr(s_command, i_MODULE_STUB)

    if 0x70 == i_cmd_id:
#        print("[STB][DBG] received log command -> " + s_command)
        # check tlv data
        if 0 < i_tlv_len:
            # DEBUG
            i_result, d_tlv_param = Decode_TLV (i_dst_id, i_src_id, i_cmd_id, \
                                      i_action, i_tlv_len, s_tlv_data, i_MODULE_STUB)
#                print("[STB] decode result : request tlv data")
#                print(" - i_result   : " + str(i_result))

            if "Result" in d_tlv_param and \
                i_RET_SUCCESS != d_tlv_param["Result"]:
                print("[STB] tlv decode error !!")
            else:
                pass
        else:
            pass
    else:
        if "None" != s_command:
            que = QUE_SND_LIST[hex(i_dst_id)]
            que.put(s_command)
        else:
            pass


def STUB_FUNC(i_src_id):
    global QUE_RCV_LIST
    global QUE_SND_LIST
    global BASE_TIME

    print("[STB] start stub : " + hex(i_src_id))

    que_snd = QUE_SND_LIST[hex(i_src_id)]
    que_rcv = QUE_RCV_LIST[hex(i_src_id)]

    while(True):
        s_command = que_snd.get()

        # DEBUG
#        print("[STB] received command -> " + s_command)

#        print("[STB] Decode common header")
        # check common header. if result is ok ,
        # change from i_src_id to i_dst_id and change from i_dst_id to src_id
        i_result, \
        i_dst_id, \
        i_src_id, \
        i_cmd_id, \
        i_action, \
        i_seq_num, \
        i_ack_num, \
        i_tlv_len, s_tlv_data = Decode_ComHdr(s_command, i_MODULE_STUB)

        # notify LOG
        if (0x0f & i_action) == 0x01:
            if 0x3 == i_cmd_id:
                BASE_TIME = time.time()
                print("[STB] base time -> " + str(BASE_TIME))
            else:
                pass

#            print("[STB] start to write log !!")
            s_command = STUB_Create_Log_Command(i_dst_id, i_src_id, \
                                        "[STB] received request command -> " \
                                        + s_command, i_MODULE_STUB)
            print("[STB] send request -> " + s_command)
            que_rcv.put(s_command)
#            time.sleep(0.5)
        else:
            pass

        # DEBUG
#        print("[STB] decode result : request common header")
#        print(" - i_result   : " + str(i_result))
#        print(" - i_dst_id   : " + str(i_dst_id))
#        print(" - i_src_id   : " + str(i_src_id))
#        print(" - i_cmd_id   : " + str(i_cmd_id))
#        print(" - i_action   : " + str(i_action))
#        print(" - i_seq_num  : " + str(i_seq_num))
#        print(" - i_ack_num  : " + str(i_ack_num))
#        print(" - i_tlv_len  : " + str(i_tlv_len))
#        print(" - s_tlv_data : " + s_tlv_data)

        if 0 != i_result:
            print("[STB] common header decode error !!")
        else:
            # check tlv data
            if 0 < i_tlv_len:
                # DEBUG
                i_result, d_tlv_param = Decode_TLV (i_dst_id, i_src_id, i_cmd_id,
                                        i_action, i_tlv_len, s_tlv_data, i_MODULE_STUB)
#                print("[STB] decode result : request tlv data")
#                print(" - i_result   : " + str(i_result))

                if "Result" in d_tlv_param and \
                    i_RET_SUCCESS != d_tlv_param["Result"]:
                    print("[STB] tlv decode error !!")
                else:
                    pass
            else:
                pass

        # create ack command
        i_result, i_tlv_len , s_tlv_data= \
                Encode_TLV_Ack(i_dst_id, i_src_id, i_cmd_id, i_result, i_MODULE_STUB)

        # DEBUG
#        print("[STB] encode result : ack tlv data")
#        print(" - i_result   : " + str(i_result))
#        print(" - i_tlv_len  : " + str(i_tlv_len))
#        print(" - s_tlv_data : " + s_tlv_data)

        if 0 != i_result:
            print("[STB] ack command : tlv encode error !!")
        else:
            pass

        # swap src id and dsc id
        tmp = i_dst_id
        i_dst_id = i_src_id
        i_src_id = tmp

        # create common header
        i_action = (i_action & 0xf0) | 0x02
        i_ack_num = i_seq_num
        i_seq_num = STUB_GetSeqNum()

#        print("[STB] Encode common header in ack command")
        s_comhdr = Encode_ComHdr(i_dst_id, \
                                    i_src_id, \
                                    i_cmd_id, \
                                    i_action, \
                                    i_seq_num, \
                                    i_ack_num, \
                                    i_tlv_len, \
                                    s_tlv_data, \
                                    i_MODULE_STUB)

        # DEBUG
#        print("[STB] encode result : ack common header")
#        print(" - s_comhdr   : " + s_comhdr)

        # add common header to tlv data
        s_command = ""
        s_command = s_comhdr + s_tlv_data

        # DEBUG
        print("[STB] " + hex(i_dst_id) + " send ack command -> " + s_command)

        # Ack msg reply
        que_rcv.put(s_command)

#        time.sleep(0.5)

        # swap src id and dsc id
        tmp = i_dst_id
        i_dst_id = i_src_id
        i_src_id = tmp

        # create response command
        i_action = (i_action & 0xf0) | 0x03
        i_ack_num = i_seq_num
        i_seq_num = STUB_GetSeqNum()

        d_TLV_Param = {}
        d_TLV_Param = STUB_Create_Rsp_TLV(i_cmd_id, i_action)
        print("[STB] " + hex(i_dst_id) + " user settings : "
                                                            + str(d_TLV_Param))

#        print("[STB] Encode TLV in response command")
        i_result, s_tlv_data, i_tlv_len = \
                    Encode_TLV_Rsp (
                                       i_dst_id, i_src_id, i_cmd_id,
                                       i_action, d_TLV_Param, i_MODULE_STUB
                                      )
        if 0 != i_result:
            print("[STB] response command : tlv encode error !!")
            return "NG"
        else:
            pass

        # swap src id and dsc id
        tmp = i_dst_id
        i_dst_id = i_src_id
        i_src_id = tmp

        # create common header
#        print("[STB] Encode common header in response command")
        s_comhdr = Encode_ComHdr(i_dst_id, \
                                    i_src_id, \
                                    i_cmd_id, \
                                    i_action, \
                                    i_seq_num, \
                                    i_ack_num, \
                                    i_tlv_len, \
                                    s_tlv_data, \
                                    i_MODULE_STUB)

        # add common header to tlv data
        s_command = ""
        s_command = s_comhdr + s_tlv_data

        # DEBUG
        print("[STB] " + hex(i_dst_id) + " send response command -> " \
                                                                + s_command)

        # Ack msg reply
        que_rcv.put(s_command)
        # if - else (check log command)

    # while loop end


def Stub_Init(i_src_id, s_log_name, s_key_param):
    global QUE_SND_LIST
    global QUE_RCV_LIST

    print("[STB] thread start !! : " + hex(i_src_id))
    s_stub_th_name = "STUB-" + hex(i_src_id)[2:]
    th_stub = threading.Thread(target=STUB_FUNC, \
                                name=s_stub_th_name, \
                                args=(i_src_id,))

    QUE_RCV_LIST[hex(i_src_id)] = QUE_RCV_LIST[s_key_param]
    QUE_SND_LIST[hex(i_src_id)] = queue.Queue()
    print("[STB] que send list " + str(QUE_SND_LIST[hex(i_src_id)]))
    th_stub.setDaemon(True)
    th_stub.start()
