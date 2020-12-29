#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief AP main function.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import json
import sys
import threading
from Debug import Debug_GetObj
from CLS_Define import COM_DEF
from tx_snd import snd_rsp_cmd


##
# @brief Identify the command ID and call the method of the AP_FUNC class.
# @param cls_ap_func    AP function class (class object)
# @param l_com_hdr_info    command header parameter
# @param d_tlv_param    tlv parameter \n
#                         ["SecurityType"] Security type
# @retval d_ap_rply    response data \n
#                        ["Result"] value of the result \n
#                          - Success : COM_DEF.i_RET_SUCCESS \n
#                          - Failure : Value other than COM_DEF.i_RET_SUCCESS
def call_apfunc(cls_ap_func, l_com_hdr_info, d_tlv_param):

    d_ap_rply = {}

    # Get debug info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_AP)

    Dbg.log(COM_DEF.TRACE, "[S] call_apfunc")

    # get command id
    i_cmd_id = l_com_hdr_info[0][2]

    Dbg.log(COM_DEF.DEBUG,
            "[0x%04x] COMMAND : 0x%04x"
            % (l_com_hdr_info[0][1], i_cmd_id))

    if COM_DEF.i_CMD_Attach == i_cmd_id:
        d_ap_rply = cls_ap_func.attach(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetCurrentTime == i_cmd_id:
        d_ap_rply = cls_ap_func.date(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetSsid == i_cmd_id:
        d_ap_rply = cls_ap_func.ssid(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetSecurity == i_cmd_id:
        if "SecurityType" in d_tlv_param:
            if COM_DEF.i_SecurityType_Open == d_tlv_param["SecurityType"]:
                d_ap_rply = cls_ap_func.open(l_com_hdr_info, d_tlv_param)
            elif COM_DEF.i_SecurityType_Wep == d_tlv_param["SecurityType"]:
                d_ap_rply = cls_ap_func.wep(l_com_hdr_info, d_tlv_param)
            elif COM_DEF.i_SecurityType_Wpa == d_tlv_param["SecurityType"]:
                d_ap_rply = cls_ap_func.wpa(l_com_hdr_info, d_tlv_param)
            else:
                Dbg.log(COM_DEF.ERROR,
                        "Security Type Err !! : " +
                        str(d_tlv_param["SecurityType"]))
                d_ap_rply["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
        else:
            Dbg.log(COM_DEF.ERROR,
                    "Security Type parameter is nothing !! ")
            d_ap_rply["Result"] = COM_DEF.i_RET_TLV_ABNORMAL

    elif COM_DEF.i_CMD_SetChannel == i_cmd_id:
        d_ap_rply = cls_ap_func.channel(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetCountryCode == i_cmd_id:
        d_ap_rply = cls_ap_func.country(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetStealthMode == i_cmd_id:
        d_ap_rply = cls_ap_func.stealth(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetRadioOutput == i_cmd_id:
        d_ap_rply = cls_ap_func.controlbss(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_GetStaList == i_cmd_id:
        d_ap_rply = cls_ap_func.stalist(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetConnectionLimit == i_cmd_id:
        d_ap_rply = cls_ap_func.limit(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_Set11n == i_cmd_id:
        d_ap_rply = cls_ap_func.control11n(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_Detach == i_cmd_id:
        d_ap_rply = cls_ap_func.detach(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_TestReady == i_cmd_id:
        d_ap_rply = cls_ap_func.test_ready(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_StartDhcpd == i_cmd_id:
        d_ap_rply = cls_ap_func.dhcpd(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_SetIpInfo == i_cmd_id:
        d_ap_rply = cls_ap_func.setipinfo(l_com_hdr_info, d_tlv_param)
    elif COM_DEF.i_CMD_GetIpInfo == i_cmd_id:
        d_ap_rply = cls_ap_func.getipinfo(l_com_hdr_info, d_tlv_param)
    else:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] command 0x%04x not supported"
                % (l_com_hdr_info[0][1], i_cmd_id))
        d_ap_rply["Result"] = COM_DEF.i_RET_COMHDR_ABNORMAL

    Dbg.log(COM_DEF.TRACE, "[E] call_apfunc")

    return d_ap_rply


##
# @brief It receives the queue notification from the common reception thread
#        and calls the AP_FUNC class method. \n
#        Receive the result and send the response.
# @param que_main    queue used by this module and main_ctrl_thread
#                      (queue class object)
# @param cls_soc    socket used for sending response command to MC
#                     (clas object)
# @param s_device_type    device type
# @param s_host     MC IP Address
# @param s_model_name   AP model name. (AP folder name)
# @retval None
def ap_ctrl_thread(que_main, cls_soc, s_device_type, s_host, s_model_name):

    d_ap_rply = {}

    # Get debug info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_AP)

    Dbg.log(COM_DEF.TRACE, "[S] ap_ctrl_thread")

    # read environment file
    s_env_file = "./device/AP/env.json"
    fp = open(s_env_file, 'r')
    d_env_data = json.load(fp)
    s_ap_name = d_env_data["DeviceName"]
    fp.close()

    Dbg.log(COM_DEF.INFO, "Device Name : " + s_ap_name)

    sys.path.append("./device/AP/" + s_ap_name + "/")
    from Control import AP_FUNC

    # Get API function
    cls_ap_func = AP_FUNC(cls_soc, s_host, s_model_name)

    while(1):
        Dbg.log(COM_DEF.INFO, "wait queue...")

        # wait to queue
        l_decode_data = que_main.get()

        Dbg.log(COM_DEF.TRACE, "queue get data")

        # get comhdr param
        l_com_hdr_info = l_decode_data[0][0]
        # get tlv param
        d_tlv_param = l_decode_data[0][1]

        d_ap_rply = call_apfunc(cls_ap_func, l_com_hdr_info, d_tlv_param)

        # send response command
        snd_rsp_cmd(l_com_hdr_info, d_ap_rply, cls_soc,
                    COM_DEF.i_MODULE_AP, s_device_type)

    # while end

    Dbg.log(COM_DEF.TRACE, "[E] ap_ctrl_thread")


##
# @brief Start module main process.
# @param que_main    queue used by this module and main_ctrl_thread
#                      (queue class object)
# @param cls_soc    socket used for sending response command to MC
#                     (clas object)
# @param s_device_type    device type
# @param d_DevConfigInfo     device configuration info
# @retval None
def module_start(que_main, cls_soc, s_device_type, d_DevConfigInfo):

    s_host = d_DevConfigInfo["ExHost"]
    s_model_name = d_DevConfigInfo["ModelName"]
    ap_th = threading.Thread(target=ap_ctrl_thread,
                             args=(que_main, cls_soc, s_device_type,
                                   s_host, s_model_name, ),
                             name="AP_main")
    ap_th.setDaemon(True)
    ap_th.start()
