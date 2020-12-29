# --------------------------------------------------------------------
# AutoEva - Automatic Evaluation System for Wi-Fi
#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#
"""
control endpoint functions
"""
# -*- coding: utf-8 -*-
import time
import subprocess
import shlex
import threading
import json
import netifaces as ni
from CLS_Define import COM_DEF
from tx_snd import cre_seq_list
from tx_snd import snd_req_cmd
from tx_snd import set_base_time
from Debug import Debug_GetObj
from netifaces import AF_INET


##
# @brief Define NETWORKTOOL related processing.
class NETWORKTOOL_FUNC():

    ##
    # @brief Run when instantiating the NETWORKTOOL_FUNC class.
    # @param cls_soc    socket used for sending response command to
    #                   MC (class object)
    # @param s_host     MC IP Address
    # @retval None
    def __init__(self, cls_soc, s_host):

        # @cond
        # Get debug info
        self.Dbg = Debug_GetObj(COM_DEF.i_MODULE_NETWORKTOOL)
        self.i_module_type = COM_DEF.i_MODULE_NETWORKTOOL
        self.soc = cls_soc
        self.iperf_result_str = ""
        self.s_MC_IpAddr = s_host
        # @endcond

        # read environment file
        try:
            env_file = "./device/NETWORKTOOL/sub/env.json"
            fr = open(str(env_file), 'r')
            d_networktool_data = json.load(fr)
            fr.close()
        except Exception as err_info:
            print(err_info)

        self.eth_ifname = d_networktool_data['EthIf']

        cre_seq_list(COM_DEF.i_MODULE_NETWORKTOOL)

    ##
    # @brief Attach processing of NETWORKTOOL control.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def attach(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}

        self.Dbg.log(COM_DEF.TRACE, "[S] attach")

        # mandatory parameter
        if "LogName" in d_tlv_param:
            self.Dbg.log(COM_DEF.INFO,
                         "related log name : %s" %
                         d_tlv_param["LogName"])
            d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "LogName parameter is not found")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL

        self.Dbg.log(COM_DEF.TRACE, "[E] attach")

        return d_rply_tlv

    ##
    # @brief Detach processing of NETWORKTOOL control.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def detach(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}

        self.Dbg.log(COM_DEF.TRACE, "[S] attach")

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] attach")

        return d_rply_tlv

    ##
    # @brief Perform time setting for NETWORKTOOL
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Date"] year, month, day \n
    #                         ["Time"] hours, minutes, and seconds
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def date(self, l_com_hdr_info, d_tlv_param):

        global CLS_BASE_TIME
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        b_date_command_skip = False

        self.Dbg.log(COM_DEF.TRACE, "[S] date")

        self.Dbg.log(COM_DEF.DEBUG,
                     "MC IP Address : %s"
                     % (self.s_MC_IpAddr))

        interface_list = ni.interfaces()
        for interface in interface_list:
            if AF_INET in ni.ifaddresses(interface):
                if self.s_MC_IpAddr == \
                        ni.ifaddresses(interface)[AF_INET][0]['addr']:
                    b_date_command_skip = True
                else:
                    pass
            else:
                pass
        # for loop

        if True is b_date_command_skip or \
                'localhost' == self.s_MC_IpAddr:
            self.Dbg.log(COM_DEF.DEBUG,
                         "skip to execute date command")
        else:
            # get date command paramter

            # mandatory parameter
            i_date = d_tlv_param["Date"]
            # mandatory parameter
            i_time = d_tlv_param["Time"]

            # change date and time format
            i_year = (i_date >> 16) & 0x0000ffff
            i_mon = (i_date >> 8) & 0x000000ff
            i_day = i_date & 0x000000ff
            s_date = str(i_year) + "/" + str(i_mon) + "/" + str(i_day)

            i_hour = (i_time >> 24) & 0x000000ff
            i_min = (i_time >> 16) & 0x000000ff
            i_sec = (i_time >> 8) & 0x000000ff
            s_time = str(i_hour) + ":" + str(i_min) + ":" + str(i_sec)

            # set date
            date_string = 'date -s "%s %s"' % (s_date, s_time)
            snd_req_cmd(l_com_hdr_info, date_string, self.soc,
                        COM_DEF.i_MODULE_AIRCAP)
            self.Dbg.log(COM_DEF.INFO, date_string)

            try:
                i_ret = subprocess.call(date_string, shell=True)
            except Exception as err_info:
                self.Dbg.log(COM_DEF.ERROR, err_info)
                d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                return d_rply_tlv

            if COM_DEF.i_RET_SUCCESS != i_ret:
                self.Dbg.log(COM_DEF.ERROR, "date command fail")
                d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                return d_rply_tlv
            else:
                pass

        set_base_time(time.perf_counter(), COM_DEF.i_MODULE_NETWORKTOOL)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] date")

        return d_rply_tlv

    ##
    # @brief Start ping from NETWORKTOOL
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["DestIpAddress"] peer ip address \n
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ping_start(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        s_ping_cmd = "ping"
        s_opt_string = ""

        self.Dbg.log(COM_DEF.TRACE, "[S] ping_start")

        # get date command paramter

        # @cond
        # mandatory parameter
        s_ipaddr = d_tlv_param["IpAddress"]
        # @endcond

        if "Interval" in d_tlv_param:
            s_opt_string = " -i " + str(d_tlv_param["Interval"])
            s_ping_cmd += s_opt_string
        else:
            pass

        if "TotalTime" in d_tlv_param:
            s_opt_string = " -w " + str(d_tlv_param["TotalTime"])
            s_ping_cmd += s_opt_string
        else:
            pass

        if "PacketNum" in d_tlv_param:
            s_opt_string = " -c " + str(d_tlv_param["PacketNum"])
            s_ping_cmd += s_opt_string
        else:
            if "-w" in s_ping_cmd:
                pass
            else:
                s_opt_string = " -c 4"

        if "PacketSize" in d_tlv_param:
            s_opt_string = " -s " + str(d_tlv_param["PacketSize"])
            s_ping_cmd += s_opt_string
        else:
            pass

        s_ping_cmd = s_ping_cmd + " " + s_ipaddr

        try:
            proc = subprocess.Popen(shlex.split(s_ping_cmd),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, error = proc.communicate()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, err_info)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv

        if out:
            snd_req_cmd(l_com_hdr_info, out.decode("utf-8"), self.soc,
                        COM_DEF.i_MODULE_NETWORKTOOL)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS
        else:
            d_rply_tlv["Result"] = COM_DEF.i_RET_NETSTACK_ERROR

        self.Dbg.log(COM_DEF.TRACE, "[E] ping_start")

        return d_rply_tlv

    ##
    # @brief Start Iperf execution thread.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["IperfCmdString"] iperf execution command \n
    #                         ["IperfModeType"] iperf startup mode \n
    #                           - 1 : server mode \n
    #                           - 2 : client mode
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def iperf_start(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] iperf_start")

        # get date command paramter

        # @cond
        # mandatory parameter
        self.i_iperfmode = d_tlv_param["IperfModeType"]
        # @endcond

        # mandatory parameter
        s_iperf_str = "iperf " + d_tlv_param["IperfCmdString"]

        # start iperf thread
        iperf_th = threading.Thread(target=self.iperf_thread,
                                    args=(l_com_hdr_info, s_iperf_str, ),
                                    name="iperf")
        iperf_th.setDaemon(True)
        iperf_th.start()

        if COM_DEF.i_IperfModeType_Server == self.i_iperfmode:
            pass
        else:
            self.Dbg.log(COM_DEF.TRACE, "wait to finish thread...")
            iperf_th.join()

        d_rply_tlv["Result"] = i_ret

        self.Dbg.log(COM_DEF.TRACE, "[E] iperf_start")

        return d_rply_tlv

    ##
    # @brief Stop Iperf execution thread.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def iperf_end(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] iperf_end")

        if COM_DEF.i_IperfModeType_Server == self.i_iperfmode:
            self.iperf_proc.terminate()
        else:
            pass

        if "" == self.iperf_result_str:
            i_ret = COM_DEF.i_RET_NETSTACK_ERROR
        else:
            pass
        d_rply_tlv["Result"] = i_ret
        d_rply_tlv["IperfCmdString"] = self.iperf_result_str

        self.Dbg.log(COM_DEF.TRACE, "[E] iperf_end")

        return d_rply_tlv

    ##
    # @brief Execute Iperf and get the execution result.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def iperf_thread(self, l_com_hdr_info, s_iperf_str):

        self.Dbg.log(COM_DEF.TRACE, "[S] iperf_thread")

        snd_req_cmd(l_com_hdr_info, s_iperf_str, self.soc,
                    COM_DEF.i_MODULE_NETWORKTOOL)
        self.Dbg.log(COM_DEF.DEBUG,
                     "command string : " + s_iperf_str)

        # @cond
        try:
            self.iperf_proc = subprocess.Popen(shlex.split(s_iperf_str),
                                               stdout=subprocess.PIPE)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "failed to start iperf")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return

        if COM_DEF.i_IperfModeType_Server == self.i_iperfmode:

            while (1):
                byte_read_data = self.iperf_proc.stdout.readline()

                if not byte_read_data:
                    break
                else:
                    s_read_data = byte_read_data.decode('Shift-JIS')
                    self.Dbg.log(COM_DEF.DEBUG, s_read_data)
                    if "0.0-" in s_read_data:
                        self.iperf_result_str = \
                            s_read_data[0:(len(s_read_data)-1)]
                    else:
                        pass
                    snd_req_cmd(l_com_hdr_info, s_read_data, self.soc,
                                COM_DEF.i_MODULE_NETWORKTOOL)
            # while loop end

            self.Dbg.log(COM_DEF.INFO,
                         "iperf result : %s" %
                         (self.iperf_result_str))

            self.iperf_proc.wait()

        else:
            l_parse_iperf = s_iperf_str.split()
            for cnt, param in enumerate(l_parse_iperf):
                if "-t" in param:
                    if 2 == len(param):
                        i_iperf_time = int(l_parse_iperf[cnt+1])
                    else:
                        i_iperf_time = int(param[2:])
                    break
                else:
                    pass
            i_iperf_time += 3  # add mergin
            self.Dbg.log(COM_DEF.INFO, "sleep %d sec" % i_iperf_time)
            time.sleep(i_iperf_time)

        # @endcond

    ##
    # @brief Node ID check as to whether the opposite device connected
    #        from the MC side is the same as the actually
    #        connected device, and performs time synchronization with
    #        the MC side.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def test_ready(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        l_kill_pid_list = []

        self.Dbg.log(COM_DEF.TRACE, "[S] test_ready")

        l_cmd_data = ['ps', '-x']
        try:
            proc = subprocess.Popen(l_cmd_data,
                                    stdout=subprocess.PIPE, shell=True)
            stdout = proc.communicate()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "failed to start subprocess.Popen")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv

        if 'iperf' in stdout[0].decode('utf-8'):

            # sdtdout is a byte type, which contains a single data.
            split_data = stdout[0].decode('utf-8').split('\n')
            for ps_data in split_data:
                if 'iperf' in ps_data:
                    pid = ps_data.split(' ')[0]
                    l_kill_pid_list.append(pid)
                else:
                    pass

            if len(l_kill_pid_list):
                l_cmd_data = ['kill', '-9']
                for pid in l_kill_pid_list:
                    l_cmd_data.append(pid)

                self.Dbg.log(COM_DEF.INFO, ' '.join(l_cmd_data))

                try:
                    proc = subprocess.Popen(l_cmd_data,
                                            stdout=subprocess.PIPE,
                                            shell=False)
                except Exception as err_info:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "failed to start subprocess.Popen")
                    self.Dbg.log(COM_DEF.ERROR, err_info)
                    d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                    return d_rply_tlv
            else:
                pass
        else:
            self.Dbg.log(COM_DEF.DEBUG, "iperf is no running process")

        # get node id
        i_dst_id = l_com_hdr_info[0][0]
        i_node_id = (i_dst_id & COM_DEF.i_NODEID_MASK) >> 8
        self.Dbg.log(COM_DEF.DEBUG, "NODE ID : 0x%02x" % (i_node_id))

        # node id check
        if i_node_id < COM_DEF.i_NODE_NETWORKTOOL_START or \
                COM_DEF.i_NODE_NETWORKTOOL_END < i_node_id:
            self.Dbg.log(COM_DEF.ERROR,
                         "node id error [0x%04x]"
                         % (i_dst_id))
            d_rply_tlv["Result"] = COM_DEF.i_RET_NODE_CHK_ERROR
        else:
            # date command
            d_rply_tlv = self.date(l_com_hdr_info, d_tlv_param)

        try:
            d_rply_tlv['IpAddress'] = \
                ni.ifaddresses(self.eth_ifname)[AF_INET][0]['addr']
            d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "can't get eth ip address...")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR

        self.Dbg.log(COM_DEF.TRACE, "[E] test_ready")

        return d_rply_tlv
