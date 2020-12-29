#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This class control a function regarding the air capture
# @author E2N3
# @date 2018.11.08

# -*- coding: utf-8 -*-

import os
import time
import json
import subprocess
import shlex
import Chk_packet as packet
from CLS_Define import COM_DEF
from tx_snd import cre_seq_list
from tx_snd import snd_req_cmd
from tx_snd import set_base_time
from Debug import Logger_GetObj
from collections import OrderedDict


##
# @brief Define AIRCAP related processing.
class AIRCAP_FUNC():
    ##
    #  @brief Run when instantiating the AIRCAP_FUNC class.
    #  @param self      instance of AIRCAP_FUNC class
    #  @param cls_soc   socket used for sending response command to Control PC
    def __init__(self, cls_soc):
        # read environment file
        try:
            env_file = "./device/AIRCAP/sub/env.json"
            fr = open(str(env_file), 'r')
            d_aircap_data = json.load(fr)
            fr.close()
        except Exception as err_info:
            print(err_info)

        # @cond
        # Get logger info
        self.logger = Logger_GetObj(COM_DEF.i_MODULE_AIRCAP)
        self.i_module_type = COM_DEF.i_MODULE_AIRCAP
        self.tshark_proc = False
        self.cap_file_path = d_aircap_data["CaptureFilePath"]
        self.filename_extension = d_aircap_data["FilenameExtension"]
        self.ref_data_path = d_aircap_data["RefDataPath"]
        self.ref_file_extension = d_aircap_data["RefFileExtension"]
        self.d_cp_info = {}
        self.d_cp_info["host"] = d_aircap_data["CpHost"]
        self.d_cp_info["id"] = d_aircap_data["CpID"]
        self.d_cp_info["passwd"] = d_aircap_data["CpPWD"]
        self.d_cp_info["path"] = d_aircap_data["CpRefDtPath"]
        self.d_cp_info["LogPath"] = d_aircap_data["CpLogPath"]

        self.wlan_ifname = d_aircap_data["WlanIf"]

        # check 2nd wlan interface
        if "WlanIf2" in d_aircap_data:
            self.wlan_ifname2 = d_aircap_data["WlanIf2"]
        else:
            self.wlan_ifname2 = ""

        # check 3rd wlan interface
        if "WlanIf3" in d_aircap_data:
            self.wlan_ifname3 = d_aircap_data["WlanIf3"]
        else:
            self.wlan_ifname3 = ""

        # check 4th wlan interface
        if "WlanIf4" in d_aircap_data:
            self.wlan_ifname4 = d_aircap_data["WlanIf4"]
        else:
            self.wlan_ifname4 = ""

        self.soc = cls_soc
        self.time_list = []
        self.radiotap_list = []
        self.ie_list = []

        # check file path
        if not os.path.exists(self.cap_file_path):
            os.makedirs(self.cap_file_path)
        else:
            pass

        if not os.path.exists(self.ref_data_path):
            os.makedirs(self.ref_data_path)
        else:
            pass
        # @endcond

        cre_seq_list(COM_DEF.i_MODULE_AIRCAP)

    ##
    #  @brief Perform initial setting of AIRCAP and change wireless I/F to
    #        Monitor Mode setting.
    #  @param self    instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info  command header parameter
    #  @param d_tlv_param     received TLV parameter from Control PC
    #  @retval d_rply_tlv     reply TLV data to Control PC \n
    #      **["Result"]**     the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_SYSTEM_ERROR
    #      .
    def attach(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] attach command start"
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        s_return_data = ""

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

        # set wlan interface
        d_rply_tlv["Result"] = packet.set_wlan_if(self, l_com_hdr_info,
                                                  d_tlv_param)

        return d_rply_tlv

    ##
    #  @brief Performs termination processing of AIRCAP.
    #  @param self      instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param   received TLV paameter from Control PC
    #  @retval d_rply_tlv   reply TLV data to Control PC \n
    #      **["Result"]**    value of the result (int) \n
    #      - i_RET_SUCCESS
    #      .
    def detach(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] detach command start"
        d_rply_tlv = {}

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        return d_rply_tlv

    ##
    #  @brief set current date & time which is received from the control PC
    #  @param self      instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param   received TLV paameter from Control PC \n
    #      **["Date"]**   year, month, day \n
    #      **["Time"]**   hours, minutes, and seconds
    #  @retval d_rply_tlv   reply TLV data to Control PC \n
    #      **["Result"]**   the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_SYSTEM_ERROR\n
    #      -
    def date(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] date command start"
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

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
        s_cmd_str = ["date", "-s", s_date + " " + s_time]
        snd_req_cmd(l_com_hdr_info, str(s_cmd_str), self.soc,
                    COM_DEF.i_MODULE_AIRCAP)
        self.logger.debug(s_cmd_str)

        i_ret = subprocess.call(s_cmd_str, shell=True)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            self.logger.error("[AIRCAP CTRL] date command fail")
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        set_base_time(time.time(), COM_DEF.i_MODULE_AIRCAP)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        return d_rply_tlv

    ##
    #  @brief start to get the air capture log
    #  @param self      instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param   received TLV paameter from Control PC
    #  @retval d_rply_tlv   reply TLV data to Control PC \n
    #      **["Result"]**   the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_SYSTEM_ERROR
    #      .
    def start_aircap(self, l_com_hdr_info, d_tlv_param):
        # @cond
        s_func_str = "[AIRCAP FUNC] start capture"
        i_analyzemsg = 0
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

        # check date
        s_cmd_str = ["date", "+%Y%m%d%H%M%S"]
        self.logger.debug(s_cmd_str)
        try:
            s_date_time = subprocess.check_output(s_cmd_str).decode("utf-8")
            s_date_time = s_date_time.replace("\n", "")
        except Exception as err_info:
            self.logger.error(err_info)
            self.logger.error("[AIRCAP CTRL] date command fail")
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv

        # option parameter
        if "AircapIfId" in d_tlv_param:
            i_aircap_if_id = d_tlv_param["AircapIfId"]
            if d_tlv_param["AircapIfId"] == COM_DEF.i_IfId_Aircap1:
                s_wlan_ifname = self.wlan_ifname
            elif d_tlv_param["AircapIfId"] == COM_DEF.i_IfId_Aircap2 \
                    and self.wlan_ifname2 != "":
                s_wlan_ifname = self.wlan_ifname2
            elif d_tlv_param["AircapIfId"] == COM_DEF.i_IfId_Aircap3 \
                    and self.wlan_ifname3 != "":
                s_wlan_ifname = self.wlan_ifname3
            elif d_tlv_param["AircapIfId"] == COM_DEF.i_IfId_Aircap4 \
                    and self.wlan_ifname4 != "":
                s_wlan_ifname = self.wlan_ifname4
            else:
                s_wlan_ifname = self.wlan_ifname
        else:
            i_aircap_if_id = 0
            s_wlan_ifname = self.wlan_ifname

        if "wlp" in s_wlan_ifname:
            s_wlan_ifname = "wmon0"
        else:
            pass

        # create address filter
        s_captureaddr = packet.create_addr_filter(d_tlv_param, i_analyzemsg,
                                                  self.logger)

        # set chennel
        i_ret = packet.set_channel(
            l_com_hdr_info, self.soc, d_tlv_param, s_wlan_ifname, self.logger)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = i_ret
            return d_rply_tlv
        else:
            pass

        # mandatory parameter
        s_capturename = d_tlv_param["CaptureFileName"]
        i_channel = d_tlv_param["Channel"]

        # check file path
        if not os.path.exists(self.cap_file_path):
            os.makedirs(self.cap_file_path)
        else:
            pass

        # create filename
        self.s_filename = self.cap_file_path
        self.s_filename += s_capturename
        self.s_filename += "_AIRCAP"
        self.s_filename += str(i_aircap_if_id + 1)
        self.s_filename += "_ch"
        self.s_filename += str(i_channel)
        self.s_filename += "_"
        self.s_filename += s_date_time
        self.s_filename += self.filename_extension

        # check whether tshark is started or not ?
        # if tshark is started, terminate process.
        if True is self.tshark_proc:
            self.logger.debug("[AIRCAP CTRL] already tshark \
                              proc start -> proc stop")
            self.tshark_proc.terminate()
            self.tshark_proc = False
        else:
            pass

        # create tshark command
        s_cmd_str = ["tshark", "-i",  s_wlan_ifname, "-F", "libpcap", "-w",
                     self.s_filename]
        if s_captureaddr:
            s_cmd_str.append("-f")
            s_captureaddr = "\'" + s_captureaddr + "\'"
            s_cmd_str.extend(shlex.split(s_captureaddr))
        else:
            pass

        snd_req_cmd(l_com_hdr_info, str(s_cmd_str), self.soc,
                    COM_DEF.i_MODULE_AIRCAP)
        self.logger.debug(s_cmd_str)

        # execute tshark command
        try:
            self.tshark_proc = subprocess.Popen(s_cmd_str)
        except Exception as err_info:
            self.logger.error(err_info)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv

        self.logger.debug("[AIRCAP CTRL] tshark proc stop -> proc start")

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        return d_rply_tlv
        # @endcond

    ##
    #  @brief stop to get the air capture log
    #  @param self      instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param   received TLV paameter from Control PC
    #  @retval d_rply_tlv   reply TLV data to Control PC \n
    #      **["Result"]**   the value of the result (int) \n
    #      - i_RET_SUCCESS
    #      .
    def stop_aircap(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] stop capture"
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

        # @cond
        # get date command paramter
        if False is self.tshark_proc:
            self.logger.debug("[AIRCAP CTRL] tshark already stop")
        else:
            self.logger.debug("[AIRCAP CTRL] tshark proc start -> proc stop")
            self.tshark_proc.terminate()
            self.tshark_proc = False

        # @endcond

        d_rply_tlv["Result"] = i_ret

        return d_rply_tlv

    ##
    #  @brief decrypt the air capture log which is encrypted with WPA2, WPA,
    #         or WEP
    #  @param self      instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param   received TLV paameter from Control PC
    #  @retval d_rply_tlv   reply TLV data to Control PC \n
    #      **["Result"]**   the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_TLV_ABNORMAL \n
    #      - i_RET_SYSTEM_ERROR
    #      .
    #  @return "pcap" file which is decrypted with "airdecap-ng" command
    def decrypt(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] decrypt capture"
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        i_wpa_hex_len = 64
        s_cmd_str = ""

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

        # set capture file name
        i_ret, s_capturefilename = packet.set_capture_file_name(
            self, d_tlv_param, self.logger)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = i_ret
            return d_rply_tlv
        else:
            pass

        # option parameter
        s_ssid = ""
        if "Ssid" in d_tlv_param:
            s_ssid = d_tlv_param["Ssid"]
        else:
            pass

        # option parameter
        if "WepKey" in d_tlv_param:
            s_key = d_tlv_param["WepKey"]
            i_key_len = len(s_key)
            s_filter = "-w" + s_key
            s_cmd_str = ["airdecap-ng", s_filter, s_capturefilename]
        else:
            pass

        # option parameter
        if "WpaPassphrase" in d_tlv_param:
            s_key = d_tlv_param["WpaPassphrase"]
            i_key_len = len(s_key)
            if i_wpa_hex_len > i_key_len:
                if "" == s_ssid:
                    self.logger.error("[AIRCAP CTRL] ssid does not exists!!")
                    d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                    return d_rply_tlv
                else:
                    s_filter = ["-e", s_ssid, "-p", s_key]
            elif i_wpa_hex_len == i_key_len:
                s_filter = ["-k", s_key]
            else:
                self.logger.error("[AIRCAP CTRL] WPA passphrase is wrong!!")
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
            s_cmd_str = ["airdecap-ng"] + s_filter + [s_capturefilename]
        else:
            pass

        if "" != s_cmd_str:
            snd_req_cmd(l_com_hdr_info, str(s_cmd_str), self.soc,
                        COM_DEF.i_MODULE_AIRCAP)
            i_ret = subprocess.call(s_cmd_str)
            self.logger.debug(s_cmd_str)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                self.logger.error("[AIRCAP CTRL] airdecap-ng command fail !!")
                d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                return d_rply_tlv
            else:
                pass
        else:
            self.logger.error("[AIRCAP CTRL] decrypt parameter is nothing!!")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        return d_rply_tlv

    ##
    #  @brief check the air capture log
    #  @param self  instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param   received TLV parameter from Control PC
    #  @retval d_rply_tlv   reply TLV data to Control PC \n
    #      **["Result"]**   the value of the result (int) \n
    #      - i_RET_SUCCESS\n
    #      - i_RET_TLV_ABNORMAL \n
    #      - i_RET_SYSTEM_ERROR \n
    #      .
    #      **["ChkResult"]** the result of having checked the packet (int) \n
    #      - i_PktChkOk \n
    #      - i_PktChkNg \n
    #      .
    #      **["NgReason"]**  the reason, if the check result is NG. (int)\n
    #      **["NumOfNg"]**  the number of NG ie value (int) \n
    #      **["DataList"][index]["AnalyzeMsg"]**
    #        the specified AnalyzeMsg which will be set,
    #        if the check result is NG. (int) \n
    #      **["DataList"][index]["NgIeName"]**
    #        IE Name which will be set, if the check result is NG. (str) \n
    #      **["DataList"][index]["NgIeValueLen"]**
    #        the length of the following "NgIeValue" parameter
    #        which will be set, if the check result is NG. (int) \n
    #      **["DataList"][index]["NgIeValue"]**
    #        IE value which will be set, if the check result is NG. (str)
    def check(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] check capture"
        d_rply_tlv = {}
        i_cnt = 0
        i_ret = COM_DEF.i_RET_SUCCESS

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str,
                    self.soc, COM_DEF.i_MODULE_AIRCAP)

        # set capture file name
        i_ret, s_capturefilename = packet.set_capture_file_name(
            self, d_tlv_param, self.logger)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = i_ret
            d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
            return d_rply_tlv
        else:
            pass

        # option parameter
        if "NumOfMsg" in d_tlv_param:
            i_num_of_msg = d_tlv_param["NumOfMsg"]
        else:
            i_num_of_msg = 1

        if i_num_of_msg == 0:
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
            return d_rply_tlv
        else:
            pass

        for num in range(i_num_of_msg):
            # read mandatory parameter
            if i_num_of_msg == 1:
                d_tmp_dict = d_tlv_param
            else:
                d_tmp_dict = OrderedDict()
                for i in range(len(d_tlv_param["DataList"][num])):
                    d_tmp_dict.update(d_tlv_param["DataList"][num][i])

            # mandatory parameter
            i_analyzemsg = d_tmp_dict["AnalyzeMsg"]
            s_reference_data = d_tmp_dict["ReferenceData"]

            # check the reference data file
            s_ref_data_name = self.ref_data_path + \
                s_reference_data + self.ref_file_extension
            if not os.path.exists(s_ref_data_name):
                self.logger.debug("no reference data")
                rmt_ref_file = self.d_cp_info["path"] + \
                    s_reference_data + self.ref_file_extension

                # get the reference data file from control PC to AIRCAP PC
                s_src_file = "%s@%s:%s" % (self.d_cp_info["id"],
                                           self.d_cp_info["host"],
                                           rmt_ref_file)
                i_ret = packet.transfer_file(s_src_file, self.ref_data_path,
                                             self.d_cp_info["passwd"],
                                             self.logger)
                if COM_DEF.i_RET_SUCCESS != i_ret:
                    d_rply_tlv["Result"] = i_ret
                    d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
                    return d_rply_tlv
                else:
                    pass
            else:
                pass

            # set dict data from the reference data file
            try:
                with open(s_ref_data_name, "r") as fr:
                    d_ref_data = json.load(fr, object_pairs_hook=OrderedDict)
            except Exception as err_info:
                self.logger.error(err_info)
                d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
                return d_rply_tlv

            # set ie name to be checked to l_ie_name_list
            l_ie_name_list = [d_ref_data]

            # set result value as default
            d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS
            d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkOk
            d_rply_tlv["DataList"] = {}

            # create the filtered "pcap" file from the capture file
            i_ret, s_filtered_file, i_num_of_pkt = \
                packet.search(s_capturefilename, i_analyzemsg,
                              d_tlv_param, self.logger)
            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = i_ret
                d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
                return d_rply_tlv
            else:
                pass

            # create tshark command
            s_cmd_str = ["tshark", "-r", s_filtered_file, "-T", "fields"]
            for ie_name in l_ie_name_list:
                s_cmd_str += ["-e", ie_name]

            self.logger.debug(s_cmd_str)

            # execute tshark to get the ie value from the filtered cap file
            try:
                cap_ie_val = subprocess.check_output(s_cmd_str).decode("utf-8")
                cap_ie_val = cap_ie_val.split("\n")
                cap_ie_val.remove("")

                l_cap_ie_val = [ie_val.split("\t") for ie_val in cap_ie_val]
                self.logger.debug(l_cap_ie_val)
            except Exception as err_info:
                self.logger.error(err_info)
                d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
                return d_rply_tlv
            else:
                pass

            for pkt_num in range(i_num_of_pkt):
                d_cap_ie = OrderedDict()
                d_cap_ie = dict(zip(l_ie_name_list, l_cap_ie_val[pkt_num]))
                # self.logger.debug(d_cap_ie)

                # compare cap_ie_val with ref_ie_value
                i_cnt, d_rply_tlv = packet.compare_ie_val(i_analyzemsg,
                                                          l_ie_name_list,
                                                          d_ref_data, d_cap_ie,
                                                          d_rply_tlv, i_cnt,
                                                          self.logger)

        # remove empty "DataList"
        if d_rply_tlv["DataList"] == {}:
            del d_rply_tlv["DataList"]

        return d_rply_tlv

    ##
    #  @brief check the number of the specified message in the air capture log
    #  @param self      instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param    received TLV paameter from Control PC
    #  @retval d_rply_tlv    reply TLV data to Control PC \n
    #      **["Result"]**    the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_TLV_ABNORMAL \n
    #      - i_RET_SYSTEM_ERROR \n
    #      .
    #      **["NumOfMsg"]**  the number of the AnalyzeMsg type (int) \n
    #      **["DataList"][index]["AnalyzeMsg"]**
    #        the value of the specified AnalyzeMsg (int) \n
    #      **["DataList"][index]["NumOfPkt"]**
    #        the number of the packet of the specified AnalyzeMsg (int)
    def check_msg_num(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] check message number"
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        i_analyzemsg = 0
        i_num_of_pkt = 0

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str,
                    self.soc, COM_DEF.i_MODULE_AIRCAP)

        # set capture file name
        i_ret, s_capturefilename = packet.set_capture_file_name(
            self, d_tlv_param, self.logger)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = i_ret
            d_rply_tlv["AnalyzeMsg"] = i_analyzemsg
            d_rply_tlv["NumOfPkt"] = i_num_of_pkt
            return d_rply_tlv
        else:
            pass

        # option parameter
        if "NumOfMsg" in d_tlv_param:
            i_num_of_msg = d_tlv_param["NumOfMsg"]
            d_rply_tlv["NumOfMsg"] = i_num_of_msg
        else:
            i_num_of_msg = 1

        i_cnt = 0
        d_list_tlv = OrderedDict()

        # set result value as default
        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        for num in range(i_num_of_msg):
            if i_num_of_msg == 1:
                # mandatory parameter
                d_tmp_dict = d_tlv_param
            else:
                d_tmp_dict = OrderedDict()
                for i in range(len(d_tlv_param["DataList"][num])):
                    d_tmp_dict.update(d_tlv_param["DataList"][num][i])

            # mandatory parameter
            i_analyzemsg = d_tmp_dict["AnalyzeMsg"]

            # get the number of the packet
            i_ret, s_filtered_file, i_num_of_pkt = \
                packet.get_pkt_num(s_capturefilename, i_analyzemsg,
                                   d_tlv_param, self.logger)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = i_ret
                d_rply_tlv["AnalyzeMsg"] = i_analyzemsg
                d_rply_tlv["NumOfPkt"] = i_num_of_pkt
                return d_rply_tlv
            else:
                pass

            if i_num_of_msg == 1:
                d_rply_tlv["AnalyzeMsg"] = i_analyzemsg
                d_rply_tlv["NumOfPkt"] = i_num_of_pkt
            else:
                d_list_tlv[str(i_cnt)] = OrderedDict()
                d_list_tlv[str(i_cnt)]["AnalyzeMsg"] = i_analyzemsg
                d_list_tlv[str(i_cnt)]["NumOfPkt"] = i_num_of_pkt
                d_rply_tlv["DataList"] = d_list_tlv

            i_cnt += 1

        return d_rply_tlv

    ##
    #  @brief get the air capture log from AIRCAP PC
    #  @param self      instance of AIRCAP_FUNC class
    #  @param l_com_hdr_info    command header parameter
    #  @param d_tlv_param    received TLV paameter from Control PC
    #  @retval d_rply_tlv    reply TLV data to Control PC \n
    #      **["Result"]**    the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_TLV_ABNORMAL \n
    #      - i_RET_SYSTEM_ERROR \n
    #      .
    def get_airlog(self, l_com_hdr_info, d_tlv_param):
        s_func_str = "[AIRCAP FUNC] get capture log file"
        d_rply_tlv = {}

        i_ret = COM_DEF.i_RET_SUCCESS

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

        # set capture file name
        i_ret, s_capturefilename = packet.make_zip_file(
            self, d_tlv_param, self.logger)
        # i_ret, s_capturefilename = packet.set_capture_file_name(
        #    self, d_tlv_param, self.logger)  # for debug
        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = i_ret
            return d_rply_tlv
        else:
            pass

        # put capture file name to control PC
        s_dst_file = "%s@%s:%s" % (self.d_cp_info["id"],
                                   self.d_cp_info["host"],
                                   self.d_cp_info["LogPath"])
        i_ret = packet.transfer_file(s_capturefilename, s_dst_file,
                                     self.d_cp_info["passwd"],
                                     self.logger)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = i_ret
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = i_ret
        return d_rply_tlv

    ##
    # @brief Node ID check as to whether the opposite device connected
    #        from the Control PC side is the same as the actually
    #        connected device, and performs time synchronization with
    #        the Control PC side.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def confirm_stat(self, l_com_hdr_info, d_tlv_param):

        s_func_str = "[AIRCAP FUNC] confirm_stat command start"
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        s_return_data = ""

        self.logger.debug(s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AIRCAP)

        # get node id
        i_dst_id = l_com_hdr_info[0][0]
        i_dst_id_upper = (i_dst_id & COM_DEF.i_NODEID_MASK) >> 8
        self.logger.debug("i_dst_id_upper : " + str(i_dst_id_upper))

        # node id check
        if i_dst_id_upper < COM_DEF.i_NODE_AIRCAP_START or \
                COM_DEF.i_NODE_AIRCAP_END < i_dst_id_upper:
            self.logger.error("node id check error !!! [i_dst_id:" +
                              str(i_dst_id) + "]")
            d_rply_tlv["Result"] = COM_DEF.i_RET_NODE_CHK_ERROR
        else:
            # date command
            d_rply_tlv = self.date(l_com_hdr_info, d_tlv_param)

        return d_rply_tlv
