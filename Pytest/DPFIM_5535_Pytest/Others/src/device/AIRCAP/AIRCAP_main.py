#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief AIRCAP main function.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import sys
import threading
from Debug import Debug_GetObj
from CLS_Define import COM_DEF
from tx_snd import snd_rsp_cmd


##
# @brief Identify the command ID and call the method of the AIRCAP_FUNC class.
# @param cls_aircap_func    AIRCAP function class (class object)
# @param l_com_hdr_info    command header parameter
# @param d_tlv_param    tlv parameter
# @retval d_aircap_rply    response data \n
#                            ["Result"] value of the result \n
#                              - Success : COM_DEF.i_RET_SUCCESS \n
#                              - Failure : Value other than \n
#                                          COM_DEF.i_RET_SUCCESS
def call_aircapfunc(cls_aircap_func, l_com_hdr_info, d_tlv_param):

    d_aircap_rply = {}

    # Get debug info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_AIRCAP)

    Dbg.log(COM_DEF.TRACE, "[S] call_aircapfunc")

    # get command id
    i_cmd_id = l_com_hdr_info[0][2]

    Dbg.log(COM_DEF.DEBUG,
            "[0x%04x] COMMAND : 0x%04x"
            % (l_com_hdr_info[0][1], i_cmd_id))

    if COM_DEF.i_CMD_Attach == i_cmd_id:
        d_aircap_rply = cls_aircap_func.attach(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_Detach == i_cmd_id:
        d_aircap_rply = cls_aircap_func.detach(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetCurrentTime == i_cmd_id:
        d_aircap_rply = cls_aircap_func.date(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_StartAirCapture == i_cmd_id:
        d_aircap_rply = cls_aircap_func.start_aircap(l_com_hdr_info,
                                                     d_tlv_param)
    elif COM_DEF.i_CMD_StopAirCapture == i_cmd_id:
        d_aircap_rply = cls_aircap_func.stop_aircap(l_com_hdr_info,
                                                    d_tlv_param)
    elif COM_DEF.i_CMD_DecryptAirLog == i_cmd_id:
        d_aircap_rply = cls_aircap_func.decrypt(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_CheckAirLog == i_cmd_id:
        d_aircap_rply = cls_aircap_func.check(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_GetAirLog == i_cmd_id:
        d_aircap_rply = cls_aircap_func.get_airlog(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_CheckMsgNum == i_cmd_id:
        d_aircap_rply = cls_aircap_func.check_msg_num(l_com_hdr_info,
                                                      d_tlv_param)
    elif COM_DEF.i_CMD_TestReady == i_cmd_id:
        d_aircap_rply = cls_aircap_func.test_ready(l_com_hdr_info,
                                                   d_tlv_param)
    else:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] command 0x%04x not supported"
                % (l_com_hdr_info[0][1], i_cmd_id))
        d_aircap_rply["Result"] = COM_DEF.i_RET_COMHDR_ABNORMAL

    Dbg.log(COM_DEF.TRACE, "[E] call_aircapfunc")

    return d_aircap_rply


##
# @brief It receives the queue notification from the common reception thread
#        and calls the AIRCAP_FUNC class method. \n
#        Receive the result and send the response.
# @param que_main    queue used by this module and main_ctrl_thread
#                     (queue class object)
# @param cls_soc    socket used for sending response command to MC
#                    (clas object)
# @param s_device_type    device type
# @param s_host     MC IP Address
# @retval None
def aircap_ctrl_thread(que_main, cls_soc, s_device_type, s_host):

    d_aircap_rply = {}

    # Get debug info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_AIRCAP)

    Dbg.log(COM_DEF.TRACE,
            "[S] aircap_ctrl_thread")

    # read environment file
    sys.path.append("./device/AIRCAP/sub/")
    from Control import AIRCAP_FUNC

    # Get API function
    cls_aircap_func = AIRCAP_FUNC(cls_soc, s_host)

    while(1):
        Dbg.log(COM_DEF.INFO, "wait queue...")

        # wait to queue
        l_decode_data = que_main.get()

        Dbg.log(COM_DEF.TRACE, "queue get data")

        # get comhdr param
        l_com_hdr_info = l_decode_data[0][0]
        # get tlv param
        d_tlv_param = l_decode_data[0][1]

        d_aircap_rply = call_aircapfunc(cls_aircap_func, l_com_hdr_info,
                                        d_tlv_param)

        # send response command
        snd_rsp_cmd(l_com_hdr_info, d_aircap_rply, cls_soc,
                    COM_DEF.i_MODULE_AIRCAP, s_device_type)

    # while end

    Dbg.log(COM_DEF.TRACE, "[E] aircap_ctrl_thread")


##
# @brief Start module main process.
# @param que_main    queue used by this module and main_ctrl_thread
#                     (queue class object)
# @param cls_soc    socket used for sending response command to MC
#                    (clas object)
# @param s_device_type    device type
# @param d_DevConfigInfo     device configuration info
# @retval None
def module_start(que_main, cls_soc, s_device_type, d_DevConfigInfo):

    s_host = d_DevConfigInfo["ExHost"]
    aircap_th = threading.Thread(target=aircap_ctrl_thread,
                                 args=(que_main, cls_soc,
                                       s_device_type, s_host,),
                                 name="AIRCAP_main")
    aircap_th.setDaemon(True)
    aircap_th.start()
