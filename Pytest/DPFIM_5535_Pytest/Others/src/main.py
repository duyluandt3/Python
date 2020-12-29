#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief Common main function about AP/AIRCAP/NETWORKTOOL.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import datetime
import json
import sys
import queue
import threading
import signal
from CLS_Define import COM_DEF
from tx_snd import snd_ack_cmd
from Debug import Debug_Init
from Debug import Debug_GetObj
from Decode_TLV import Decode_TLV
from Decode_ComHdr import Decode_ComHdr
from CLS_Socket import COM_SOCKET
from collections import OrderedDict


##
# @brief Device control thread. this thread treats common procedure.
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @param s_device_type    device type
# @param que_end    queue between main thread and common receive thread
#                     (class object)
# @param s_DevConfigName  device config info
# @retval None
def main_ctrl_thread(i_module_type, s_device_type, que_end, d_DevConfigInfo):

    que_main = queue.Queue()
    s_read_command = ""
    i_while_loop = 1

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    if COM_DEF.i_MODULE_AP == i_module_type:
        s_device_type = 'AP'
    elif COM_DEF.i_MODULE_AIRCAP == i_module_type:
        s_device_type = 'AIRCAP'
    else:
        s_device_type = 'NETWORKTOOL'

    Dbg.log(COM_DEF.TRACE,
            "[S] %s main_ctrl_thread" % (s_device_type))

    i_dst_node_id = 0x00
    i_dst_instance_id = 0x01

    s_host = d_DevConfigInfo["ExHost"]
    i_port = d_DevConfigInfo["ExPort"]
    i_backlog = d_DevConfigInfo["ExBacklog"]
    i_bufsize = d_DevConfigInfo["ExBufsize"]

    # connect control pc
    cls_soc = COM_SOCKET(i_port, i_bufsize, i_module_type)
    cls_soc.bind(s_host, i_port)
    cls_soc.listen(i_backlog)

    # get device function
    module_start(que_main, cls_soc, s_device_type, d_DevConfigInfo)

    Dbg.log(COM_DEF.TRACE,
            "[%s] wait connect..."
            % (s_device_type))
    cls_soc.accept()

    # wait to receive command
    while(i_while_loop):

        Dbg.log(COM_DEF.TRACE,
                "[%s] wait command..."
                % (s_device_type))
        try:
            s_read_data = cls_soc.read()
        except Exception as err_info:
            Dbg.log(COM_DEF.ERROR,
                    "[%s] failed to read socket"
                    % (s_device_type))
            Dbg.log(COM_DEF.ERROR,
                    err_info)
            break

        # FIN receive
        if not s_read_data:
            Dbg.log(COM_DEF.INFO,
                    "[%s] FIN receive"
                    % (s_device_type))
            break
        else:
            pass

        if isinstance(s_read_data, str):
            s_read_command += s_read_data

            while "" != s_read_command:

                Dbg.log(COM_DEF.DEBUG,
                        "[%s] rcv cmd : %s"
                        % (s_device_type, s_read_command))

                # get common header
                i_result, i_dst_id, i_src_id, i_cmd_id, i_action, \
                    i_seq_num, i_ack_num, i_tlv_len, s_tlv_data = \
                    Decode_ComHdr(s_read_command, i_module_type)

                if (COM_DEF.i_RET_COMHDR_LENGTH == i_result or
                        COM_DEF.i_RET_WAIT_NEXT_CMD == i_result):
                    Dbg.log(COM_DEF.TRACE,
                            "[%s] wait next command..."
                            % (s_device_type))
                    break
                else:

                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] DST ID   : 0x%04x" %
                            (s_device_type, i_dst_id))
                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] SRC ID   : 0x%04x" %
                            (s_device_type, i_src_id))
                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] COMMAND  : 0x%04x" %
                            (s_device_type, i_cmd_id))
                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] ACTION   : 0x%02x" %
                            (s_device_type, i_action))
                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] SEQ NO   : %d" %
                            (s_device_type, i_seq_num))
                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] ACK NO  : %d" %
                            (s_device_type, i_ack_num))
                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] TLV LEN : %d" %
                            (s_device_type, i_tlv_len))
                    Dbg.log(COM_DEF.DEBUG,
                            "[%s] TLV     : %s" %
                            (s_device_type, s_tlv_data))

                    if COM_DEF.i_RET_SUCCESS == i_result:
                        if (i_action & COM_DEF.i_ACTION_UPPERMASK) == \
                                COM_DEF.i_ACTION_REQ:

                            # First initialization command
                            if COM_DEF.i_CMD_TestReady != i_cmd_id \
                                    and 0x00 == \
                                    (i_dst_id & COM_DEF.i_INSTANCEID_MASK):

                                i_dst_node_id = \
                                    i_dst_id & COM_DEF.i_NODEID_MASK

                                # Instance ID setting
                                i_dst_id = \
                                    i_dst_node_id + i_dst_instance_id
                                Dbg.log(COM_DEF.DEBUG,
                                        "[%s] SRC ID  : 0x%04x" %
                                        (s_device_type, i_dst_id))
                            else:
                                pass

                            # parse and check tlv data
                            i_ret, d_tlv_param = Decode_TLV(i_dst_id,
                                                            i_src_id,
                                                            i_cmd_id,
                                                            i_action,
                                                            i_tlv_len,
                                                            s_tlv_data,
                                                            i_module_type,
                                                            s_device_type)

                            # common header
                            l_com_hdr_info = []
                            l_com_hdr_info.append([i_dst_id,
                                                   i_src_id,
                                                   i_cmd_id,
                                                   i_action,
                                                   i_seq_num,
                                                   i_ack_num])

                            #  encoded information
                            l_decode_data = []
                            l_decode_data.append([l_com_hdr_info,
                                                  d_tlv_param])

                            # send ack command (either success or abnormal)
                            snd_ack_cmd(i_result,
                                        l_com_hdr_info,
                                        cls_soc,
                                        i_module_type)

                            if COM_DEF.i_RET_SUCCESS == i_result:

                                Dbg.log(COM_DEF.TRACE,
                                        "[%s] put queue data" %
                                        s_device_type)
                                # call device function
                                que_main.put(l_decode_data)
                            else:
                                pass

                        else:
                            # discard command (this root is abnormal)
                            s_read_command = ""

                    else:
                        Dbg.log(COM_DEF.ERROR,
                                "[%s] Decode_ComHdr error [ret:%d]" %
                                (s_device_type, i_result))

                        l_com_hdr_info = []
                        l_com_hdr_info.append([i_dst_id,
                                              i_src_id,
                                              i_cmd_id,
                                              i_action,
                                              i_seq_num,
                                              i_ack_num])

                        # fail to decode common header
                        snd_ack_cmd(i_result,
                                    l_com_hdr_info,
                                    cls_soc,
                                    i_module_type)

                    # extract next command from the received string
                    if COM_DEF.i_COMHDR_LENGTH + i_tlv_len < \
                            len(s_read_command):
                        i_pos = (COM_DEF.i_COMHDR_LENGTH * 2 + i_tlv_len * 2)
                        s_read_command = s_read_command[i_pos:]
                    else:
                        pass

                    if s_read_command:
                        Dbg.log(COM_DEF.DEBUG,
                                "[%s] remain : %s" %
                                (s_device_type, s_read_command))
                    else:
                        pass
            # while end
        else:
            pass

    # while end
    que_end.put(1)

    Dbg.log(COM_DEF.TRACE,
            "[E] %s main_ctrl_thread" % (s_device_type))


##
# @brief Start a thread to receive commands from MC.
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @param s_device_type    device type
# @param s_DevConfigName  device config info
# @retval None
def start_thread(i_module_type, s_device_type, d_DevConfigInfo):

    que_end = queue.Queue()
    main_th = \
        threading.Thread(target=main_ctrl_thread,
                         args=(i_module_type,
                               s_device_type,
                               que_end,
                               d_DevConfigInfo, ),
                         name=s_device_type + "_thread")
    main_th.setDaemon(True)
    main_th.start()
    que_end.get()


##
# @brief Stop test case when thread received signal.
# @param signum    signal number
# @param frame    stack frame (frame object)
# @retval None
def Signal_Handler(signum, frame):

    print("[MAIN] Signal Received !! -> " + str(signum))
    sys.exit(0)


##
# @brief read configuration file
# @param s_DevConfigName
# @retval None
def Read_DeviceConfigFile(s_DevConfigName):
    """
    read device information file
    """

    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    try:
        with open(s_DevConfigName, "r", encoding='utf-8-sig') as fp:
            d_deviceInfo = decoder.decode(fp.read())
    except Exception as err_info:
        print(COM_DEF.ERROR, "can't read %s" % s_DevConfigName)
        print(COM_DEF.ERROR, err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, {}

    return COM_DEF.i_RET_SUCCESS, d_deviceInfo


##
# @brief when aircap stop, send log to MC .
# @param signum    s_log_name
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL \n
#      - i_RET_SYSTEM_ERROR \n
def get_log_name(s_log_name):

    i_ret = COM_DEF.i_RET_SUCCESS
    Dbg = Debug_GetObj(i_module_type)

    GetLog = AIR_LOG_COLLECT_FUNC(Dbg)
    print(s_log_name)

    i_ret = GetLog.get_log_file(s_log_name)
    if i_ret == COM_DEF.i_RET_SUCCESS:
        pass
    else:
        return i_ret

    return i_ret

    print("Get Aircap Log OK !!")


# @cond
if __name__ == '__main__':

    # read device type except DUT
    s_DeviceId = sys.argv[1]
    print("Devicd Id   : %s" % s_DeviceId)

    # read configuration file
    config_file = "./config/" + s_DeviceId + "_config.json"
    i_ret, d_DevConfigInfo = \
        Read_DeviceConfigFile(config_file)
    if i_ret:
        sys.exit(1)
    else:
        if "DeviceType" in d_DevConfigInfo:
            s_device_type = \
                d_DevConfigInfo["DeviceType"]
        else:
            pass

    sys.path.append("./device/" + s_device_type)
    print("Device Type : %s" % s_device_type)

    # initialize test parameter
    if "AP" == s_device_type:
        i_module_type = COM_DEF.i_MODULE_AP
        from AP_main import module_start
    elif "AIRCAP" == s_device_type:
        i_module_type = COM_DEF.i_MODULE_AIRCAP
        from AIRCAP_main import module_start
        sys.path.append("./device/" + s_device_type + "/sub/")
        from Getlog import AIR_LOG_COLLECT_FUNC
    elif "NETWORKTOOL" == s_device_type:
        i_module_type = COM_DEF.i_MODULE_NETWORKTOOL
        from NETWORKTOOL_main import module_start
    else:
        print("[Main] failed to initialize debug")

    # set Debug level
    s_log_filename = \
        COM_DEF.s_TOPDIR + \
        "/LOG/" + \
        s_DeviceId + \
        "_" + \
        datetime.datetime.today().strftime('%Y%m%d%H%M%S') + \
        ".txt"
    i_result = Debug_Init(i_module_type, s_log_filename)
    if COM_DEF.i_RET_SUCCESS != i_result:
        print("[Main] failed to initialize debug")
    else:
        pass

    signal.signal(signal.SIGTERM, Signal_Handler)
    signal.signal(signal.SIGINT, Signal_Handler)

    # start main thread
    start_thread(i_module_type, s_device_type, d_DevConfigInfo)

    # Get log from AirCap PC (only AIRCAP mode)
    if "AIRCAP" == s_device_type:
        print("Start send log to MC")
        get_log_name(s_log_filename)
    else:
        pass

    print("Test Finished !!")

# @endcond
