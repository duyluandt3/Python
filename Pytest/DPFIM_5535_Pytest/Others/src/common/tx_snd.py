#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief Send tx command to control pc.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import threading
import time
from Encode_TLV import Encode_TLV_Ack
from Encode_TLV import Encode_TLV_Rsp
from Encode_ComHdr import Encode_ComHdr
from Debug import Debug_GetObj
from CLS_Define import COM_DEF

##
# @brief LOCK    Semaphore variables
LOCK = threading.Semaphore()

##
# @brief d_SEQ_NUM_LIST    Sequence number list variable
d_SEQ_NUM_LIST = {}

##
# @brief CLS_BASE_TIME    Reference time variable
CLS_BASE_TIME = 0


##
# @brief A reference time for adding Offset from the reference time
#        set by the date command to the log is stored.
# @param time    Current time (time class object)
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval None
def set_base_time(time, i_module_type):

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] set_base_time")

    global CLS_BASE_TIME
    s_device_type = ("AP" if COM_DEF.i_MODULE_AP == i_module_type
                     else "AIRCAP" if COM_DEF.i_MODULE_AIRCAP == i_module_type
                     else "NETWORKTOOL")
    s_cmd_str = "{} base time = {:.6f}"
    Dbg.log(COM_DEF.INFO, s_cmd_str.format(s_device_type, time))

    CLS_BASE_TIME = time

    Dbg.log(COM_DEF.TRACE,
            "[E] set_base_time")


##
# @brief The sequence number transmitted from each device side is managed,
#        and the sequence number used for transmission is returned.
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret_seq_num    the sequence number
def get_seq_num(i_module_type):

    global LOCK
    global d_SEQ_NUM_LIST

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] get_seq_num")

    LOCK.acquire()
    i_ret_seq_num = d_SEQ_NUM_LIST[i_module_type]
    if d_SEQ_NUM_LIST[i_module_type] < 255:
        d_SEQ_NUM_LIST[i_module_type] += 1
    else:
        d_SEQ_NUM_LIST[i_module_type] = 0
    LOCK.release()

    Dbg.log(COM_DEF.TRACE,
            "[%s] sequence number : %d" %
            ("AP" if COM_DEF.i_MODULE_AP == i_module_type
             else "AIRCAP" if COM_DEF.i_MODULE_AIRCAP == i_module_type
             else "NETWORKTOOL", d_SEQ_NUM_LIST[i_module_type]))
    Dbg.log(COM_DEF.TRACE,
            "[E] get_seq_num")

    return i_ret_seq_num


##
# @brief Create and initialize a sequence number list.
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval None
def cre_seq_list(i_module_type):

    global d_SEQ_NUM_LIST

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] cre_seq_list")

    if i_module_type not in d_SEQ_NUM_LIST:
        d_SEQ_NUM_LIST[i_module_type] = 0
    else:
        pass

    Dbg.log(COM_DEF.TRACE,
            "[E] cre_seq_list")


##
# @brief Sets the TLV encode and common header, and transmits an ack command.
# @param i_result    decode result
# @param l_com_hdr_info    command header parameter
# @param cls_soc    socket object class (class object)
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval None
def snd_ack_cmd(i_result, l_com_hdr_info, cls_soc, i_module_type):

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    if COM_DEF.i_MODULE_AP == i_module_type:
        s_device_type = 'AP'
    elif COM_DEF.i_MODULE_AIRCAP == i_module_type:
        s_device_type = 'AIRCAP'
    else:
        s_device_type = 'NETWORKTOOL'

    Dbg.log(COM_DEF.TRACE,
            "[S] %s snd_ack_cmd" % s_device_type)

    i_dst_id = l_com_hdr_info[0][0]
    i_src_id = l_com_hdr_info[0][1]
    i_cmd_id = l_com_hdr_info[0][2]
    i_action = l_com_hdr_info[0][3]
    i_seq_num = l_com_hdr_info[0][4]
    i_ack_num = l_com_hdr_info[0][5]

    # create ack command
    i_result, i_tlv_len, s_tlv_data = Encode_TLV_Ack(i_dst_id,
                                                     i_src_id,
                                                     i_cmd_id,
                                                     i_result,
                                                     i_module_type)

    if COM_DEF.i_RET_SUCCESS != i_result:
        Dbg.log(COM_DEF.DEBUG,
                "Encode_TLV_Ack error [ret:%d]" % (i_result))
        return
    else:
        pass

    Dbg.log(COM_DEF.TRACE,
            "[%s] TLV     : %s"
            % (s_device_type, s_tlv_data))

    # swap src id and dsc id
    tmp = i_dst_id
    i_dst_id = i_src_id
    i_src_id = tmp

    # create common header
    i_action = (i_action & COM_DEF.i_ACTION_LOWERMASK) | COM_DEF.i_ACTION_ACK
    i_ack_num = i_seq_num
    i_seq_num = get_seq_num(i_module_type)
    s_comhdr = Encode_ComHdr(i_dst_id, i_src_id, i_cmd_id, i_action,
                             i_seq_num, i_ack_num, i_tlv_len, s_tlv_data,
                             i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[%s] HEADER  : %s"
            % (s_device_type, s_comhdr))

    # add common header to tlv data
    s_command = s_comhdr + s_tlv_data

    Dbg.log(COM_DEF.INFO,
            "ENCODE DATA : %s"
            % (s_command))

    cls_soc.write(s_command)

    Dbg.log(COM_DEF.TRACE,
            "[E] %s snd_ack_cmd" % s_device_type)


##
# @brief Sets encode of TLV and common header, and transmits response command.
# @param l_com_hdr_info    command header parameter
# @param d_ap_rply    tlv data
# @param cls_soc    socket object class (class object)
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @param s_device_type    device type
# @retval None
def snd_rsp_cmd(l_com_hdr_info, d_ap_rply, cls_soc, i_module_type,
                s_device_type):

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    if COM_DEF.i_MODULE_AP == i_module_type:
        s_device_type = 'AP'
    elif COM_DEF.i_MODULE_AIRCAP == i_module_type:
        s_device_type = 'AIRCAP'
    else:
        s_device_type = 'NETWORKTOOL'

    Dbg.log(COM_DEF.TRACE,
            "[S] %s snd_rsp_cmd" % s_device_type)

    i_dst_id = l_com_hdr_info[0][0]
    i_src_id = l_com_hdr_info[0][1]
    i_cmd_id = l_com_hdr_info[0][2]
    i_action = l_com_hdr_info[0][3]
    i_seq_num = l_com_hdr_info[0][4]

    i_ack_num = i_seq_num
    i_action = (i_action & COM_DEF.i_ACTION_LOWERMASK) | COM_DEF.i_ACTION_RSP
    i_seq_num = get_seq_num(i_module_type)

    # create Encode TLV in response command
    i_result, s_tlv_data, i_tlv_len = Encode_TLV_Rsp(s_device_type, i_src_id,
                                                     i_cmd_id, i_action,
                                                     d_ap_rply, i_module_type)

    if COM_DEF.i_RET_SUCCESS != i_result:
        Dbg.log(COM_DEF.DEBUG,
                "[%s] Encode_TLV_Rsp error [ret:%d]"
                % (s_device_type, i_result))
        return
    else:
        pass

    Dbg.log(COM_DEF.TRACE,
            "[%s] TLV     : %s"
            % (s_device_type, s_tlv_data))

    # swap src id and dsc id
    tmp = i_dst_id
    i_dst_id = i_src_id
    i_src_id = tmp

    # create common header
    s_comhdr = Encode_ComHdr(i_dst_id, i_src_id, i_cmd_id, i_action, i_seq_num,
                             i_ack_num, i_tlv_len, s_tlv_data, i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[%s] HEADER  : %s"
            % (s_device_type, s_comhdr))

    # add common header to tlv data
    s_command = s_comhdr + s_tlv_data

    Dbg.log(COM_DEF.INFO,
            "ENCODE DATA : %s"
            % (s_command))

    cls_soc.write(s_command)

    Dbg.log(COM_DEF.TRACE,
            "[E] %s snd_rsp_cmd" % s_device_type)


##
# @brief Sets encode of TLV and common header, and transmits request command.
# @param l_com_hdr_info    command header parameter
# @param s_log_data    log data
# @param cls_soc    socket object class (class object)
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval None
def snd_req_cmd(l_com_hdr_info, s_log_data, cls_soc, i_module_type):

    global CLS_BASE_TIME

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    if COM_DEF.i_MODULE_AP == i_module_type:
        s_device_type = 'AP'
    elif COM_DEF.i_MODULE_AIRCAP == i_module_type:
        s_device_type = 'AIRCAP'
    else:
        s_device_type = 'NETWORKTOOL'

    Dbg.log(COM_DEF.TRACE,
            "[S] %s snd_req_cmd" % s_device_type)

    i_dst_id = l_com_hdr_info[0][0]
    i_src_id = l_com_hdr_info[0][1]
    i_cmd_id = l_com_hdr_info[0][2]

    i_TYPE_OffsetTime_len = 4

    # create OffsetTime tlv
    s_tlv_data = hex(COM_DEF.i_TYPE_OffsetTime)[2:].zfill(4)
    i_tlv_all_len = 2

    s_tlv_data += hex(i_TYPE_OffsetTime_len)[2:].zfill(4)
    i_tlv_all_len += 2

    if 0 != CLS_BASE_TIME:
        f_currenttime = time.perf_counter()
        f_offsettime = f_currenttime - CLS_BASE_TIME
        s_cmd_str = "{} offset time : {:.6f}"
        Dbg.log(COM_DEF.DEBUG,
                s_cmd_str.format(s_device_type, f_offsettime))
        i_offsettime = int(f_offsettime * 1000000)
        s_tlv_data += hex(i_offsettime)[2:].zfill(8)
    else:
        s_tlv_data += hex(0)[2:].zfill(8)
    i_tlv_all_len += 4

    # create LogData tlv
    s_tlv_data += hex(COM_DEF.i_TYPE_LogData)[2:].zfill(4)
    i_tlv_all_len += 2

    i_tlv_len = len(s_log_data)
    s_tlv_data += hex(i_tlv_len)[2:].zfill(4)
    i_tlv_all_len += 2

    # set data to list by separating byte unit
    for s_char in s_log_data:
        s_tlv_data += hex(ord(s_char))[2:].zfill(2)
    i_tlv_all_len += i_tlv_len

    Dbg.log(COM_DEF.TRACE,
            "[%s] TLV     : %s"
            % (s_device_type, s_tlv_data))

    # swap src id and dsc id
    tmp = i_dst_id
    i_dst_id = i_src_id
    i_src_id = tmp

    i_cmd_id = COM_DEF.i_CMD_NotifyCaptureLog
    i_action = (COM_DEF.i_ACTION_SET << 4) | COM_DEF.i_ACTION_REQ
    i_seq_num = get_seq_num(i_module_type)
    i_ack_num = 0

    s_comhdr = Encode_ComHdr(i_dst_id, i_src_id, i_cmd_id, i_action, i_seq_num,
                             i_ack_num, i_tlv_all_len, s_tlv_data,
                             i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[%s] HEADER  : %s"
            % (s_device_type, s_comhdr))

    # add common header to tlv data
    s_command = s_comhdr + s_tlv_data

    Dbg.log(COM_DEF.INFO,
            "ENCODE DATA : %s"
            % (s_command))

    cls_soc.write(s_command)

    Dbg.log(COM_DEF.TRACE,
            "[E] %s snd_req_cmd" % s_device_type)
