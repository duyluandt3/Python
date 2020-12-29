#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This funcion is done when received request command from peer device.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import json
from Decode_TLV import Decode_TLV
# from Decode_TLV import Decode_Log_Info
from CLS_Define import COM_DEF
from Debug import Debug_GetObj
from threading import Semaphore

##
# @brief LOG_SND_LOCK    semaphore lock variable
LOG_SND_LOCK = Semaphore()


##
# @brief This function send ack command to device.
# @param SocLog    use to send log data (class object)
# @param i_result    the result of decode common header
# @param i_dst_id    destination id
# @param i_src_id    source id
# @param i_cmd_id    command id
# @param i_action    action id in ack or response command
# @param i_ack_num    sequence number in request command
# @param i_tlv_len    TLV length
# @param s_tlv_data    TLV data
# @param QSndRcv    queue class used by this thread and
#                   receive interface thread (class object)
# @param SndCtrl    this class object (class object)
# @param s_DeviceType    command data
# @retval None
def Decode_RequestData(SocLog, i_result, i_dst_id, i_src_id,
                       i_cmd_id, i_action, i_ack_num, i_tlv_len, s_tlv_data,
                       QSndRcv, SndCtrl, s_DeviceType):

    # Get logger info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

    Dbg.log(COM_DEF.TRACE,
            "[S] Decode_RequestData")

    # initialize tlv parameter
    d_tlv_param = {}

    if COM_DEF.i_RET_SUCCESS == i_result:

        d_log_info = {}

        # received request from device
        i_result, d_tlv_param = Decode_TLV(i_dst_id, i_src_id, i_cmd_id,
                                           i_action, i_tlv_len, s_tlv_data,
                                           COM_DEF.i_MODULE_MC, s_DeviceType)
        if COM_DEF.i_RET_SUCCESS != i_result:
            Dbg.log(COM_DEF.ERROR,
                    "Decode_TLV error [ret:%d]" %
                    (i_result))
            return
        else:
            pass

        if d_tlv_param["Command"] == "NotifyCaptureLog" and \
                (i_action & COM_DEF.i_ACTION_UPPERMASK) == \
                COM_DEF.i_ACTION_REQ:

            # get log data
            d_log_info["Log"] = d_tlv_param["LogData"]

        elif d_tlv_param["Command"] == "NotifyEvent" and \
                (i_action & COM_DEF.i_ACTION_UPPERMASK) == \
                COM_DEF.i_ACTION_REQ:

            # get event number
            d_log_info["Log"] = "[EVT] received number : " + \
                                str(d_tlv_param["EventNum"])

            b_wait_flg = \
                SndCtrl.Get_EventStatus(d_tlv_param["EventNum"])
            if b_wait_flg:
                QSndRcv.put(d_tlv_param["EventNum"])
            else:
                pass
        else:
            pass

        d_log_info["DstId"] = i_dst_id
        d_log_info["SrcId"] = i_src_id
        d_log_info["Time"] = hex(d_tlv_param["OffsetTime"])[2:]
        send_str = json.dumps(d_log_info)

        Dbg.log(COM_DEF.TRACE,
                "start to write log : %s" %
                (d_log_info["Log"]))

        LOG_SND_LOCK.acquire()
        SocLog.sock.send(send_str.encode('utf-8'))
        rcv_str = SocLog.sock.recv(4096)
        LOG_SND_LOCK.release()

        Dbg.log(COM_DEF.TRACE,
                "the log write is finished : %s" %
                (rcv_str.decode('utf-8')))
    else:
        pass

    Dbg.log(COM_DEF.TRACE,
            "[E] Decode_RequestData")

    return
