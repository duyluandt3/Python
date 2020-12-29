#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief NETWORKTOOL main function.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import sys
import threading
from Debug import Debug_GetObj
from CLS_Define import COM_DEF
from tx_snd import snd_rsp_cmd


##
# @brief Identify the command ID and call the method of
#        the NETWORKTOOL_FUNC class.
# @param cls_endpoint_func    NETWORKTOOL function class (class object)
# @param l_com_hdr_info    command header parameter
# @param d_tlv_param    tlv parameter
# @retval d_endpoint_rply    response data \n
#                              ["Result"] value of the result \n
#                                - Success : COM_DEF.i_RET_SUCCESS \n
#                                - Failure : Value other than \n
#                                            COM_DEF.i_RET_SUCCESS
def call_endpointfunc(cls_endpoint_func, l_com_hdr_info, d_tlv_param):

    d_endpoint_rply = {}

    # Get debug info
    debug = Debug_GetObj(COM_DEF.i_MODULE_NETWORKTOOL)

    debug.log(COM_DEF.TRACE, "[S] call_endpointfunc")

    # get command id
    i_cmd_id = l_com_hdr_info[0][2]

    debug.log(COM_DEF.DEBUG,
              "[0x%04x] COMMAND : 0x%04x"
              % (l_com_hdr_info[0][1], i_cmd_id))

    if COM_DEF.i_CMD_Attach == i_cmd_id:
        d_endpoint_rply = cls_endpoint_func.attach(l_com_hdr_info,
                                                   d_tlv_param)
    elif COM_DEF.i_CMD_Detach == i_cmd_id:
        d_endpoint_rply = cls_endpoint_func.detach(l_com_hdr_info,
                                                   d_tlv_param)
    elif COM_DEF.i_CMD_SetCurrentTime == i_cmd_id:
        d_endpoint_rply = cls_endpoint_func.date(l_com_hdr_info,
                                                 d_tlv_param)
    elif COM_DEF.i_CMD_StartPing == i_cmd_id:
        d_endpoint_rply = cls_endpoint_func.ping_start(l_com_hdr_info,
                                                       d_tlv_param)
    elif COM_DEF.i_CMD_StartIperf == i_cmd_id:
        d_endpoint_rply = cls_endpoint_func.iperf_start(l_com_hdr_info,
                                                        d_tlv_param)
    elif COM_DEF.i_CMD_FinishIperfServerProcess == i_cmd_id:
        d_endpoint_rply = cls_endpoint_func.iperf_end(l_com_hdr_info,
                                                      d_tlv_param)
    elif COM_DEF.i_CMD_TestReady == i_cmd_id:
        d_endpoint_rply = cls_endpoint_func.test_ready(l_com_hdr_info,
                                                       d_tlv_param)
    else:
        debug.log(COM_DEF.ERROR,
                  "[0x%04x] command 0x%04x not supported"
                  % (l_com_hdr_info[0][1], i_cmd_id))
        d_endpoint_rply["Result"] = COM_DEF.i_RET_COMHDR_ABNORMAL

    debug.log(COM_DEF.TRACE, "[E] call_endpointfunc")

    return d_endpoint_rply


##
# @brief It receives the queue notification from the common reception thread
#        and calls the NETWORKTOOL_FUNC class method. \n
#        Receive the result and send the response.
# @param que_main    queue used by this module and main_ctrl_thread
#                     (queue class object)
# @param cls_soc    socket used for sending response command to MC
#                    (clas object)
# @param s_device_type    device type
# @param s_host     MC IP Address
# @retval None
def endpoint_ctrl_thread(que_main, cls_soc, s_device_type, s_host):

    d_endpoint_rply = {}

    # Get debug info
    debug = Debug_GetObj(COM_DEF.i_MODULE_NETWORKTOOL)

    debug.log(COM_DEF.TRACE, "[S] endpoint_ctrl_thread")

    # read environment file
    sys.path.append("./device/NETWORKTOOL/sub/")
    from Control import NETWORKTOOL_FUNC

    # Get API function
    cls_endpoint_func = NETWORKTOOL_FUNC(cls_soc, s_host)

    while(1):
        debug.log(COM_DEF.INFO, "wait queue...")

        # wait to queue
        l_decode_data = que_main.get()

        debug.log(COM_DEF.TRACE, "queue get data")

        # get comhdr param
        l_com_hdr_info = l_decode_data[0][0]
        # get tlv param
        d_tlv_param = l_decode_data[0][1]

        d_endpoint_rply = call_endpointfunc(cls_endpoint_func, l_com_hdr_info,
                                            d_tlv_param)

        # send response command
        snd_rsp_cmd(l_com_hdr_info, d_endpoint_rply, cls_soc,
                    COM_DEF.i_MODULE_NETWORKTOOL, s_device_type)

    # while end

    debug.log(COM_DEF.TRACE, "[E] endpoint_ctrl_thread")


##
# @brief It receives the queue notification from the common reception thread
#        and calls the NETWORKTOOL_FUNC class method. \n
#        Receive the result and send the response.
# @param que_main    queue used by this module and main_ctrl_thread
#                     (queue class object)
# @param cls_soc    socket used for sending response command to MC
#                    (clas object)
# @param s_device_type    device type
# @param d_DevConfigInfo     device configuration info
# @retval None
def module_start(que_main, cls_soc, s_device_type, d_DevConfigInfo):

    s_host = d_DevConfigInfo["ExHost"]
    endpoint_th = threading.Thread(target=endpoint_ctrl_thread,
                                   args=(que_main, cls_soc,
                                         s_device_type, s_host,),
                                   name="NETWORKTOOL_main")
    endpoint_th.setDaemon(True)
    endpoint_th.start()
