#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This thread has state management as following. \n
#          1. Start Timer
#          2. Send Request Command to device.
#          3. Receive Ack Command from device.
#          4. Receive Response Command from device.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import threading
from Encode_TLV import Encode_TLV_Req
from Encode_ComHdr import Encode_ComHdr
from Decode_TLV import Decode_TLV
from seq_num import GetSeqNum
from Debug import Debug_GetObj
from CLS_Define import COM_DEF
import time


##
# @brief start timer thread when timeout happen.
# @param QSndRcv    queue class used by this thread and
#                   receive interface thread (class object)
# @retval None
def TimerThread(QSndRcv):

    # Get logger info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

    Dbg.log(COM_DEF.TRACE, "[S] TimerThread")

    Dbg.log(COM_DEF.ERROR, "TIMEOUT !!")
    l_rply_cmd = []
    l_rply_cmd.append([COM_DEF.i_RET_ABNORMAL_TIMEOUT,
                       0, 0, 0, 0, 0, 0, 0, "TIMEOUT"])

    QSndRcv.put(l_rply_cmd)

    Dbg.log(COM_DEF.TRACE, "[E] TimerThread")


##
# @brief Check whether to change dst id from 0x1x to 0x10 \n
#        example ResetDUT command is node unit.
# @param i_dst_id    destination id
# @param i_cmd_id    command id
# @retval None
def CheckDeviceCmd(i_dst_id, i_cmd_id):

    if COM_DEF.i_CMD_ResetDUT <= i_cmd_id <= COM_DEF.i_CMD_GetCountryCode:
        i_dst_id &= COM_DEF.i_DSTID_MASK
    elif COM_DEF.i_CMD_StartDhcpd <= i_cmd_id <= COM_DEF.i_CMD_StopCaptureLog:
        i_dst_id &= COM_DEF.i_DSTID_MASK
    else:
        pass

    return i_dst_id


##
# @brief Check common header parameter.
# @param i_result    the result of decode common header
# @param i_cp_dst_id    destination id in request command
# @param i_dst_id    destination id in ack or response command
# @param i_cp_src_id    source id in request command
# @param i_src_id    source id in ack or response command
# @param i_action    action id in ack or response command
# @param i_cp_seq_num    sequence number in request command
# @param i_ack_num    sequence number in request command
# @retval i_ret_result    value of the result \n
#                           - Success : COM_DEF.i_RET_SUCCESS \n
#                           - Failure : COM_DEF.i_RET_COMHDR_ABNORMAL
def ChkRcvCmd(i_result, i_cp_dst_id, i_dst_id, i_cp_src_id,
              i_src_id, i_action, i_cp_seq_num, i_ack_num):

    # Get logger info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

    Dbg.log(COM_DEF.TRACE, "[S] ChkRcvCmd")

    i_Ret = COM_DEF.i_RET_SUCCESS

    Dbg.log(COM_DEF.TRACE,
            "RESULT  : " + str(i_result))
    Dbg.log(COM_DEF.TRACE,
            "[Notified] DST ID : 0x%04x" % (i_dst_id) +
            " [Expected] SRC ID : 0x%04x" % (i_cp_src_id))
    Dbg.log(COM_DEF.TRACE,
            "[Notified] SRC ID : 0x%04x" % (i_src_id) +
            " [Expected] DST ID : 0x%04x" % (i_cp_dst_id))
    Dbg.log(COM_DEF.TRACE,
            "ACTION  : 0x%02x" % (i_action))
    Dbg.log(COM_DEF.TRACE,
            "SEQ NO  : %d" % (i_cp_seq_num))
    Dbg.log(COM_DEF.TRACE,
            "ACK NO  : %d" % (i_ack_num))

    # check results of cksum and length in common header
    if i_result != COM_DEF.i_RET_SUCCESS:
        Dbg.log(COM_DEF.ERROR,
                "SRC ID : 0x%04x" % (i_cp_src_id) +
                " : cksum or length error [ret:%d]" %
                (i_result))
        i_Ret = COM_DEF.i_RET_COMHDR_ABNORMAL
    # check device instance id
    elif (i_cp_dst_id & COM_DEF.i_INSTANCEID_MASK) != 0 and \
            i_src_id != i_cp_dst_id:
        Dbg.log(COM_DEF.ERROR,
                "SRC ID unmatch : [Notified] 0x%04x" %
                (i_src_id) +
                " [Expected] 0x%04x" % (i_cp_dst_id))
        i_Ret = COM_DEF.i_RET_COMHDR_ABNORMAL
    # check CP thread id
    elif i_dst_id != i_cp_src_id:
        Dbg.log(COM_DEF.ERROR,
                "DST ID unmatch : [Notified] 0x%04x" %
                (i_dst_id) +
                " [Expected] 0x%04x" % (i_cp_src_id))
        i_Ret = COM_DEF.i_RET_COMHDR_ABNORMAL
    # check acknowledge number
    elif i_ack_num != i_cp_seq_num:
        Dbg.log(COM_DEF.ERROR,
                "SEQ No unmatch : [Notified] %d" %
                (i_ack_num) +
                " [Expected] %d" % (i_cp_seq_num))
        i_Ret = COM_DEF.i_RET_COMHDR_ABNORMAL
    else:
        pass

    Dbg.log(COM_DEF.TRACE, "[E] ChkRcvCmd")

    return i_Ret


##
# @brief This function send request command to device. \n
#        start wait-timer and state management as following. \n
#          - wait ack command \n
#          - wait response command
# @param IfCtrl    socket or serial class
# @param i_cp_dst_id    destination id
# @param i_cp_src_id    source id
# @param s_cmd_name    command name
# @param d_testParam    user-defined parameter
# @param QSndRcv    queue class used by this thread and
#                   receive interface thread (class object)
# @param s_DeviceType    sequence number in request command
# @retval i_result    value of the result \n
#                       - Success : COM_DEF.i_RET_SUCCESS \n
#                       - Failure : Value other than COM_DEF.i_RET_SUCCESS
# @retval d_tlv_param    decoding result of TLV data
def ctrl_snd_cmd(IfCtrl, i_cp_dst_id, i_cp_src_id, s_cmd_name,
                 d_testParam, QSndRcv, s_DeviceType):

    # Get logger info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

    Dbg.log(COM_DEF.TRACE, "[S] ctrl_snd_cmd")

    i_retryCounter = 0
    i_ack_num = 0
    d_tlv_param = {"Result": COM_DEF.i_RET_SYSTEM_ERROR}

    # -------------------------------------------------------------
    #  state
    # -------------------------------------------------------------
    i_STATE_WAIT_ACK = 1
    i_STATE_WAIT_RSP = 2
    i_STATE_WAIT_DONE = 3

    # create test command (only TLV data)
    i_result, i_cmd_id_req, i_action, s_tlv_data, i_tlv_len, i_maxRetryCount, \
        i_waitRspTimer = Encode_TLV_Req(s_DeviceType, i_cp_src_id, s_cmd_name,
                                        d_testParam, COM_DEF.i_MODULE_MC)

    if COM_DEF.i_RET_SUCCESS != i_result:
        return i_result, {}
    else:
        pass

    while i_retryCounter < i_maxRetryCount:

        i_state = i_STATE_WAIT_ACK

        # get sequence number
        i_cp_seq_num = GetSeqNum(s_DeviceType)
        Dbg.log(COM_DEF.DEBUG,
                "SEQ NO : " + str(i_cp_seq_num))

        # create common header
        s_comhdr = Encode_ComHdr(i_cp_dst_id, i_cp_src_id, i_cmd_id_req,
                                 i_action, i_cp_seq_num, i_ack_num, i_tlv_len,
                                 s_tlv_data, COM_DEF.i_MODULE_MC)

        # add comhdr to tlv data
        s_snd_cmd = s_comhdr + s_tlv_data

        Dbg.log(COM_DEF.DEBUG,
                "ENCODE DATA : %s" % s_snd_cmd)

        th_tim = threading.Timer(i_waitRspTimer, TimerThread,
                                 args=(QSndRcv,),)
        # start timer
        th_tim.setDaemon(True)
        th_tim.start()

        # send command
        Dbg.log(COM_DEF.INFO,
                "[REQ] %s (SRC ID : 0x%04x)" %
                (s_cmd_name, i_cp_src_id))
        # socket or serial is used
        i_result = IfCtrl.write(s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_result:
            th_tim.cancel()
            del th_tim
            d_tlv_param['Result'] = i_result
            Dbg.log(COM_DEF.ERROR,
                    "write error [ret:%d]" %
                    (i_result))
            return i_result, d_tlv_param, i_cp_src_id
        else:
            pass

        while i_STATE_WAIT_DONE != i_state:

            Dbg.log(COM_DEF.TRACE, "wait to put queue...")

            l_rply_cmd = QSndRcv.get()

            i_result = l_rply_cmd[0][0]
            i_dev_dst_id = l_rply_cmd[0][1]
            i_dev_src_id = l_rply_cmd[0][2]
            i_cmd_id_res = l_rply_cmd[0][3]
            i_action_res = l_rply_cmd[0][4]
            i_seq_num = l_rply_cmd[0][5]
            i_ack_num = l_rply_cmd[0][6]
            i_tlv_len_res = l_rply_cmd[0][7]
            s_tlv_data_res = l_rply_cmd[0][8]
            Dbg.log(COM_DEF.TRACE, "RESULT  : " + str(i_result))
            Dbg.log(COM_DEF.TRACE, "DST ID  : 0x%04x" % i_dev_dst_id)
            Dbg.log(COM_DEF.TRACE, "SRC ID  : 0x%04x" % i_dev_src_id)
            Dbg.log(COM_DEF.TRACE, "COMMAND : 0x%04x" % i_cmd_id_res)
            Dbg.log(COM_DEF.TRACE, "ACTION  : " + hex(i_action_res))
            Dbg.log(COM_DEF.TRACE, "SEQ NO  : " + str(i_seq_num))
            Dbg.log(COM_DEF.TRACE, "ACK NO  : " + str(i_ack_num))
            Dbg.log(COM_DEF.TRACE, "TLV LEN : " + str(i_tlv_len_res))
            Dbg.log(COM_DEF.TRACE, "TLV     : " + s_tlv_data_res)

            # test is finished when timeout occurred.
            if COM_DEF.i_RET_ABNORMAL_TIMEOUT == i_result:
                Dbg.log(COM_DEF.ERROR, "detect timeout !!")
                del th_tim
                # return i_result, {}
                d_tlv_param['Result'] = i_result
                return i_result, d_tlv_param, i_dev_src_id
            else:
                pass

            if i_cmd_id_req != i_cmd_id_res:
                # discard ack commoand received after response command
                pass
            else:
                i_result = ChkRcvCmd(i_result, i_cp_dst_id, i_dev_dst_id,
                                     i_cp_src_id, i_dev_src_id, i_action_res,
                                     i_cp_seq_num, i_ack_num)

                if COM_DEF.i_RET_SUCCESS != i_result:
                    Dbg.log(COM_DEF.DEBUG,
                            "ChkRcvCmd error [ret:%d]" %
                            (i_result))
                    th_tim.cancel()
                    del th_tim
                    d_tlv_param['Result'] = i_result
                    return i_result, d_tlv_param, i_dev_src_id
                else:
                    pass

                # check tlv data
                if (i_action_res & COM_DEF.i_ACTION_UPPERMASK) == \
                        COM_DEF.i_ACTION_ACK:

                    i_state = i_STATE_WAIT_RSP

                    Dbg.log(COM_DEF.INFO,
                            "[ACK] %s (SRC ID : 0x%04x)...ok" %
                            (s_cmd_name, i_cp_src_id))

                    if COM_DEF.i_RET_SUCCESS != i_result:
                        pass
                    else:
                        i_result, d_tlv_param = Decode_TLV(i_dev_src_id,
                                                           i_dev_dst_id,
                                                           i_cmd_id_res,
                                                           i_action_res,
                                                           i_tlv_len_res,
                                                           s_tlv_data_res,
                                                           COM_DEF.i_MODULE_MC,
                                                           s_DeviceType)
                        if "Result" in d_tlv_param and \
                                COM_DEF.i_RET_SUCCESS != d_tlv_param["Result"]:
                                    Dbg.log(COM_DEF.ERROR,
                                            "Decode_TLV error [ret:%d]" %
                                            (d_tlv_param["Result"]))
                                    i_result = d_tlv_param["Result"]
                                    th_tim.cancel()
                                    del th_tim
                                    return i_result, d_tlv_param, i_dev_src_id
                        else:
                            pass

                    if COM_DEF.i_RET_SUCCESS == i_result:
                        # wait response command
                        Dbg.log(COM_DEF.DEBUG,
                                "wait response....(SRC ID : 0x%04x)"
                                % i_cp_src_id)
                        pass
                    else:
                        # retry
                        i_retryCounter += 1
                        th_tim.cancel()
                        del th_tim
                        break

                elif (i_action_res & COM_DEF.i_ACTION_UPPERMASK) == \
                        COM_DEF.i_ACTION_RSP:

                    th_tim.cancel()
                    del th_tim
                    i_state = i_STATE_WAIT_DONE

                    if COM_DEF.i_RET_SUCCESS != i_result:
                        return i_result, {}, i_dev_src_id
                    else:
                        i_result, d_tlv_param = Decode_TLV(i_dev_src_id,
                                                           i_dev_dst_id,
                                                           i_cmd_id_res,
                                                           i_action_res,
                                                           i_tlv_len_res,
                                                           s_tlv_data_res,
                                                           COM_DEF.i_MODULE_MC,
                                                           s_DeviceType)

                        if "Result" in d_tlv_param and \
                                COM_DEF.i_RET_BUSY == d_tlv_param["Result"]:
                            Dbg.log(COM_DEF.INFO,
                                    "peer device busy...(SRC ID : 0x%04x)"
                                    % i_cp_src_id)
                            time.sleep(1)
                            i_retryCounter += 1
                        else:

                            if COM_DEF.i_RET_SUCCESS != i_result:
                                Dbg.log(COM_DEF.ERROR,
                                        "Decode_TLV error [ret:%d]" %
                                        (i_result))
                                d_tlv_param['Result'] = i_result
                                return i_result, d_tlv_param, i_dev_dst_id
                            else:

                                Dbg.log(COM_DEF.INFO,
                                        "[RSP] %s (SRC ID : 0x%04x)...ok" %
                                        (s_cmd_name, i_cp_src_id))

                                Dbg.log(COM_DEF.TRACE,
                                        "[E] ctrl_snd_cmd")

                                return i_result, d_tlv_param, i_dev_src_id
                else:
                    # discard
                    pass
        # while loop end

    # while loop end
    else:
        Dbg.log(COM_DEF.ERROR,
                "%s retry over !!" % s_cmd_name)

    Dbg.log(COM_DEF.TRACE, "[E] ctrl_snd_cmd")

    return i_result, d_tlv_param, i_dev_src_id
