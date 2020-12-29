#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This is sub-function to check the packet capture log
# @author E2N3
# @date 2018.11.08

# -*- coding: utf-8 -*-

# library of Pcap
import pcapy
import json
import subprocess
import sys
import os
import glob
import shutil
# import time as TIME
# from datetime import datetime
from CLS_Define import COM_DEF
from collections import OrderedDict
from tx_snd import snd_req_cmd


# @cond
def debug_level():
    s_dbg_inf_file = "../../Common/debug/json/DebugInfo_AIRCAP.json"

    try:
        with open(s_dbg_inf_file, "r", encoding='utf-8-sig') as fr_data:
            d_debugInfo = json.load(fr_data)
    except Exception as err_info:
        print(err_info)
        print("can't open debug file")
        return 0

    return d_debugInfo["DebugLevel"]
# @endcond


##
#  @brief execute command
#  @param l_com_hdr_info    command header parameter
#  @param soc               socket number
#  @param s_cmd_str         command to be executed
#  @param logger            logger parameter for debug
#  @retval d_rply_tlv     reply TLV data to Control PC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def exec_command(l_com_hdr_info, soc, s_cmd_str, logger):
    logger.debug("[PKT CHK] exec_command")
    i_ret = COM_DEF.i_RET_SUCCESS

    snd_req_cmd(l_com_hdr_info, str(s_cmd_str), soc,
                COM_DEF.i_MODULE_AIRCAP)
    logger.debug(s_cmd_str)

    i_ret = subprocess.call(s_cmd_str)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        s_err_str = "[PKT CHK] " + str(s_cmd_str) + " fail"
        logger.error(s_err_str)
    else:
        pass

    return i_ret


##
#  @brief set monitor mode to the external wlan device
#  @param self      instance of AIRCAP_FUNC class
#  @param l_com_hdr_info    command header parameter
#  @param s_wlan_ifname     name of the external wlan device
#  @retval d_rply_tlv     reply TLV data to Control PC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def set_external_wlan_dev(self, l_com_hdr_info, s_wlan_ifname):
    self.logger.debug("[PKT CHK] set_external_wlan_dev")
    i_ret = COM_DEF.i_RET_SUCCESS

    # ifcheck
    s_cmd_str = "iw dev " + self.wlan_ifname + " info"
    snd_req_cmd(l_com_hdr_info, s_cmd_str, self.soc, COM_DEF.i_MODULE_AIRCAP)
    self.logger.debug(s_cmd_str)

    try:
        s_return_data = subprocess.getoutput(s_cmd_str)
    except Exception as err_info:
        self.logger.error(err_info)
        s_err_str = "[PKT CHK] " + str(s_cmd_str) + " fail"
        self.logger.error(s_err_str)
        return COM_DEF.i_RET_SYSTEM_ERROR

    snd_req_cmd(l_com_hdr_info, s_return_data, self.soc,
                COM_DEF.i_MODULE_AIRCAP)

    if "No such device" in s_return_data:
        self.logger.error("No such device")
        return COM_DEF.i_RET_TLV_ABNORMAL
    else:
        pass

    # ifdown
    s_cmd_str = ["ip", "link", "set", s_wlan_ifname, "down"]
    i_ret = exec_command(l_com_hdr_info, self.soc, s_cmd_str, self.logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # set monitor mode
    s_cmd_str = ["iw", "dev", s_wlan_ifname, "set", "monitor", "none"]
    i_ret = exec_command(l_com_hdr_info, self.soc, s_cmd_str, self.logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifup
    s_cmd_str = ["ip", "link", "set", s_wlan_ifname, "up"]
    i_ret = exec_command(l_com_hdr_info, self.soc, s_cmd_str, self.logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    return i_ret


##
#  @brief set monitor mode to the internal wlan device
#  @param self      instance of AIRCAP_FUNC class
#  @param l_com_hdr_info    command header parameter
#  @param s_wlan_ifname     name of the internal wlan device
#  @retval d_rply_tlv     reply TLV data to Control PC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def set_internal_wlan_dev(self, l_com_hdr_info, s_wlan_ifname):
    self.logger.debug("[PKT CHK] set_internal_wlan_dev")

    # ifcheck
    s_cmd_str = "iw dev wmon0 info"
    snd_req_cmd(l_com_hdr_info, s_cmd_str, self.soc,
                COM_DEF.i_MODULE_AIRCAP)
    self.logger.debug(s_cmd_str)

    try:
        s_return_data = subprocess.getoutput(s_cmd_str)
    except Exception as err_info:
        self.logger.error(err_info)
        s_err_str = "[PKT CHK] " + str(s_cmd_str) + " fail"
        self.logger.error(s_err_str)
        return COM_DEF.i_RET_SYSTEM_ERROR

    snd_req_cmd(l_com_hdr_info, s_return_data, self.soc,
                COM_DEF.i_MODULE_AIRCAP)

    if "No such device" in s_return_data:
        # check no "wmon0" device
        pass
    else:
        self.logger.info("[PKT CHK] already wmon0 add")
        return COM_DEF.i_RET_SUCCESS

    # ifdown
    s_cmd_str = ["ip", "link", "set", s_wlan_ifname, "down"]
    i_ret = exec_command(l_com_hdr_info, self.soc, s_cmd_str, self.logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifadd
    s_cmd_str = ["iw", "dev", s_wlan_ifname, "interface", "add",
                 "wmon0", "type", "monitor"]
    i_ret = exec_command(l_com_hdr_info, self.soc, s_cmd_str, self.logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifup
    s_cmd_str = ["ip", "link", "set", "wmon0", "up"]
    i_ret = exec_command(l_com_hdr_info, self.soc, s_cmd_str, self.logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifdel
    s_cmd_str = ["iw", "dev", s_wlan_ifname, "del"]
    i_ret = exec_command(l_com_hdr_info, self.soc, s_cmd_str, self.logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    return COM_DEF.i_RET_SUCCESS


##
#  @brief set the wlan interface
#  @param self      instance of AIRCAP_FUNC class
#  @param l_com_hdr_info    command header parameter
#  @param d_tlv_param     received TLV parameter from Control PC
#  @retval d_rply_tlv     reply TLV data to Control PC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def set_wlan_if(self, l_com_hdr_info, d_tlv_param):
    self.logger.debug("[PKT CHK] set_wlan_if")

    # option parameter
    if "AircapIfId" in d_tlv_param:
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
        s_wlan_ifname = self.wlan_ifname

    if "wlp" in s_wlan_ifname:
        i_ret = set_internal_wlan_dev(self, l_com_hdr_info, s_wlan_ifname)
    else:
        i_ret = set_external_wlan_dev(self, l_com_hdr_info, s_wlan_ifname)

    return i_ret


##
#  @brief transfer the file with scp command
#  @param s_src_file    source file (or directory path)
#  @param s_dst_file    destination file (or directory path)
#  @param s_passwd      password for the user account on the remote host
#  @param logger        logger parameter for debug
#  @retval i_ret        int value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def transfer_file(s_src_file, s_dst_file, s_passwd, logger):
    logger.debug("[PKT CHK] transfer file")
    i_ret = COM_DEF.i_RET_SUCCESS

    s_cmd_str = ["sshpass", "-p", s_passwd, "scp", "-o",
                 "StrictHostKeyCHecking=no",
                 "-r", s_src_file, s_dst_file]
    try:
        s_res = subprocess.check_output(s_cmd_str)
    except:
        logger.error("[PKT CHK] (transfer_file) Unexpected error:",
                     sys.exc_info()[0])
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR

    return i_ret


##
#  @brief make zip file from several capture file
#  @param self          instance of AIRCAP_FUNC class \n
#      **self.cap_file_path**   directory path for the capture file (str)
#  @param d_tlv_param           TLV parameter \n
#      **["AircapIfId"]**       id of the air capture interface (int) \n
#      **["CaptureFileName"]**  capture file name without both
#                               the file path and file extension (str)
#  @retval i_ret        the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL \n
#      - i_RET_SYSTEM_ERROR
#      .
#  @retval s_zip_file           the zip file name with the directory path
def make_zip_file(self, d_tlv_param, logger):
    logger.debug("[PKT CHK] zip capture file")

    i_ret = COM_DEF.i_RET_SUCCESS
    s_zip_file = ""
    l_cap_file_list = []

    # option parameter
    if "AircapIfId" in d_tlv_param:
        i_aircap_if_id = d_tlv_param["AircapIfId"]
    else:
        i_aircap_if_id = 1

    if "CaptureFileName" in d_tlv_param:
        s_zip_file_path = self.cap_file_path
        s_zip_file_path += d_tlv_param["CaptureFileName"]
        s_zip_file_path += "_AIRCAP"
        s_zip_file_path += str(i_aircap_if_id)

        s_cap_file = self.cap_file_path
        s_cap_file += d_tlv_param["CaptureFileName"]
        s_cap_file += "*.*"
        l_cap_file_list = glob.glob(s_cap_file)
    else:
        logger.error("[PKT CHK] capture file name is not specified !!")
        i_ret = COM_DEF.i_RET_TLV_ABNORMAL
        return i_ret, s_zip_file

    if len(l_cap_file_list) == 0:
        logger.error("[PKT CHK] capture file does not exists!!")
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR
        return i_ret, s_zip_file
    else:
        pass

    # make work directory
    if not os.path.exists(s_zip_file_path):
        os.makedirs(s_zip_file_path)
    else:
        pass

    # move capture file to work directory
    for cap_file in l_cap_file_list:
        shutil.move(cap_file, s_zip_file_path)

    # execute zip to work directory
    shutil.make_archive(s_zip_file_path, "zip", root_dir=s_zip_file_path)
    s_zip_file = s_zip_file_path + ".zip"
    if not os.path.exists(s_zip_file):
        logger.error("[PKT CHK] zip file is not created !!")
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR
        return i_ret, s_zip_file
    else:
        # delete work directory
        shutil.rmtree(s_zip_file_path)

    return i_ret, s_zip_file


##
#  @brief set capture file name from the TLV parameter
#  @param self          instance of AIRCAP_FUNC class \n
#      **self.cap_file_path**  the directory path for the capture file (str) \n
#      **self.filename_extension**  file extension of the capture file (str) \n
#      **self.s_filename**  capture file name which has already been stored
#                           to the instance of AIRCAP_FUNC class. (str)
#  @param d_tlv_param       TLV parameter \n
#      **["AircapIfId"]**   id of the air capture interface (int) \n
#      **["CaptureFileName"]**  capture file name without both
#                               the file path and file extension (str)
#  @retval i_ret        the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
#  @retval s_capturefilename    the capture file name with the
#                               directory path (str)
def set_capture_file_name(self, d_tlv_param, logger):
    logger.debug("[PKT CHK] set capture file name")

    i_ret = COM_DEF.i_RET_SUCCESS
    s_capturefilename = ""

    # option parameter
    if "AircapIfId" in d_tlv_param:
        i_aircap_if_id = d_tlv_param["AircapIfId"]
    else:
        i_aircap_if_id = 1

    # option parameter
    '''
    if "CaptureFileName" in d_tlv_param:
        s_cap_file = self.cap_file_path
        s_cap_file += d_tlv_param["CaptureFileName"]
        s_cap_file += "_AIRCAP"
        s_cap_file += str(i_aircap_if_id)
        # wild card
        s_cap_file += "*.*"
        l_cap_file_list = glob.glob(s_cap_file)
        if len(l_cap_file_list) != 0:
            s_capturefilename = l_cap_file_list[-1]
        else:
            pass

    # @cond
    '''
    if self.s_filename == "":
        # @endcond
            if "CaptureFileName" in d_tlv_param:
                s_cap_file = self.cap_file_path
                s_cap_file += d_tlv_param["CaptureFileName"]
                s_cap_file += "_AIRCAP"
                s_cap_file += str(i_aircap_if_id)
                # wild card
                s_cap_file += "*.*"
                l_cap_file_list = glob.glob(s_cap_file)
                if len(l_cap_file_list) != 0:
                    s_capturefilename = l_cap_file_list[-1]
                else:
                    logger.error("[PKT CHK] capture file name does not exists!!")
                    i_ret = COM_DEF.i_RET_TLV_ABNORMAL
    else:
        s_capturefilename = self.s_filename

    if not os.path.exists(s_capturefilename):
        logger.error("[PKT CHK] capture file name does not exists!!")
        i_ret = COM_DEF.i_RET_TLV_ABNORMAL
    else:
        pass

    logger.debug(s_capturefilename)
    return i_ret, s_capturefilename


##
#  @brief calculate the control frequency and the center frequency \n
#  @brief from the channel number and the bandwidth
#  @param i_channel         the channel number
#  @param s_bandwidth       the bandwidth
#  @param logger            logger parameter for debug
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
#  @retval d_ch_info        dict data for the channel infomation \n
#      **["ControlFreq"]**    the control frequency (int) \n
#      **["CenterFreq"]**     the center frequency (int) \n
#      **["CenterFreq2"]**    the 2nd center frequency (int) \n
#      **["BandWidth"]**      the bandwidth (str) \n
def calculate_freq(i_channel, s_bandwidth, logger):
    logger.debug("[PKT CHK] start calculate_freq")
    s_ch_bw_str = ["i_channel", str(i_channel), "s_bandwidth", s_bandwidth]
    logger.debug(s_ch_bw_str)

    i_2g_base_freq = 2412
    i_5g_base_freq = 5000

    l_w52 = [36, 40, 44, 48]
    l_w53 = [52, 56, 60, 64]
    l_w56 = [100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144]
    l_w58 = [149, 153, 157, 161, 165, 169]
    l_5g_ch = l_w52 + l_w53 + l_w56

    i_ch_bandwidth = 20
    i_controlfreq = 0
    i_centerfreq = 0

    d_ch_info = OrderedDict()
    i_ret = COM_DEF.i_RET_SUCCESS

    # set int value of the bandwidth
    if "80+80" in s_bandwidth:
        i_bandwidth = 80
    else:
        i_bandwidth = int(s_bandwidth)

    # calculate the control frequency and the center frequency
    if 1 <= i_channel <= 14 and s_bandwidth in ["20", "40"]:
        # 2.4GHz
        i_controlfreq = i_2g_base_freq + (i_channel - 1) * 5
        if i_channel == 14 and s_bandwidth in ["20"]:
            # ch14 : 2.4GHz/HT20 (802.11b only)
            i_controlfreq = 2484
            i_centerfreq = 2484
        elif 1 <= i_channel <= 9:
            # ch1 - ch9   : 2.4GHz/HT40+
            i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10)
        else:
            # ch10 - ch13 : 2.4GHz/HT40-
            i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10) * -1
    elif i_channel in l_w58:
        # 5GHz - W58
        if i_channel in [165, 169] and s_bandwidth in ["40", "80"]:
            logger.error("[PKT CHK] bandwidth parameter is abnormal !!")
            i_ret = COM_DEF.i_RET_TLV_ABNORMAL
            return i_ret, d_ch_info
        else:
            pass

        i_controlfreq = i_5g_base_freq + i_channel * 5
        i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10) - (
            i_ch_bandwidth * (((i_channel - 1) // 4 - 9) %
                              (i_bandwidth // i_ch_bandwidth)))
    elif i_channel in l_5g_ch:
        # 5GHz - W52/W53/W56
        i_controlfreq = i_5g_base_freq + i_channel * 5
        i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10) - (
            i_ch_bandwidth * ((i_channel // 4 - 9) %
                              (i_bandwidth // i_ch_bandwidth)))
    else:
        # ERROR
        logger.error("[PKT CHK] channel parameter is abnormal !!")
        i_ret = COM_DEF.i_RET_TLV_ABNORMAL

    # set the channel infomation for the result
    d_ch_info["ControlFreq"] = i_controlfreq
    d_ch_info["BandWidth"] = s_bandwidth
    d_ch_info["CenterFreq"] = i_centerfreq
    if "80+80" in s_bandwidth:
        d_ch_info["CenterFreq2"] = i_centerfreq + 80
    else:
        d_ch_info["CenterFreq2"] = 0

    logger.debug(d_ch_info)
    logger.debug("[PKT CHK] calculate_freq complete")

    return i_ret, d_ch_info


##
#  @brief set channel parameter to the wlan device interface
#  @param l_com_hdr_info    com header info
#  @param soc               socket number
#  @param d_tlv_param       TLV parameter \n
#      **["Channel"]**      the channel number (int) \n
#      **["Bandwidth"]**    string of the bandwidth (str) \n
#  @param logger            logger parameter for debug
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
def set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, logger):
    logger.debug("[PKT CHK] set channel")

    i_ret = COM_DEF.i_RET_SUCCESS

    # mandatory parameter
    i_channel = d_tlv_param["Channel"]

    # mandatory parameter
    i_chanwidth = d_tlv_param["Bandwidth"]
    if COM_DEF.i_Bandwidth_20MHz == i_chanwidth:
        s_bandwidth = "20"
    elif COM_DEF.i_Bandwidth_40MHz == i_chanwidth:
        s_bandwidth = "40"
    elif COM_DEF.i_Bandwidth_80MHz == i_chanwidth:
        s_bandwidth = "80"
    elif COM_DEF.i_Bandwidth_80_80MHz == i_chanwidth:
        s_bandwidth = "80+80"
    elif COM_DEF.i_Bandwidth_160MHz == i_chanwidth:
        s_bandwidth = "160"
    else:
        logger.error("[PKT CHK] bandwidth parameter is abnormal !!")
        return COM_DEF.i_RET_TLV_ABNORMAL

    # calculate channel freq
    i_ret, d_ch_info = calculate_freq(i_channel, s_bandwidth, logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # set band
    if 0 != d_ch_info["ControlFreq"] and 0 != d_ch_info["CenterFreq"]:
        # create iw dev command
        s_cmd_str = ["iw", "dev", s_wlan_ifname, "set", "freq",
                     str(d_ch_info["ControlFreq"]),
                     d_ch_info["BandWidth"],
                     str(d_ch_info["CenterFreq"])]

        if "80+80" in d_ch_info["BandWidth"]:
            s_cmd_str += [str(d_ch_info["CenterFreq2"])]
        else:
            pass

        # execute iw dev command
        i_ret = exec_command(l_com_hdr_info, soc, s_cmd_str, logger)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            return i_ret
        else:
            pass
    else:
        pass

    return i_ret


##
#  @brief convert "pcap" file to "json" file
#  @param s_cap_file    the "pcap" file name
#  @param logger        logger parameter for debug
#  @retval i_ret        the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
#  @return **s_json_file**    "json" file name
def pcap2json(s_cap_file, logger):
    logger.debug("[PKT CHK] cnv pcap to json")

    i_ret = COM_DEF.i_RET_SUCCESS
    s_json_file = s_cap_file.replace(".pcap", ".json")
    s_cmd_str = ["tshark", "-r", s_cap_file, "-T", "json"]
    logger.debug(s_cmd_str)

    try:
        json_data = subprocess.check_output(s_cmd_str).decode("utf-8")
        json_data = json_data.replace("  {", "[\n  {")
        json_data = json_data.replace("  }\n\n", "  }\n]")
        json_data = json_data.replace("  ,", ",")
        json_data = json_data.replace("]]", "]\n]")
        # print(json_data)

        with open(s_json_file, "w") as fw_json:
            fw_json.write(json_data)
    except Exception as err_info:
        logger.error(err_info)
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR

    return i_ret


##
#  @brief count the number of the packets in the "pcap" file
#  @param s_cap_file    the "pcap" file name
#  @param logger        logger parameter for debug
#  @retval i_num_of_pkt the number of the packets
#  @retval i_ret        the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def count_packet(s_cap_file, logger):
    logger.debug("[PKT CHK] count num of packet")

    i_num_of_pkt = 0
    i_ret = COM_DEF.i_RET_SUCCESS
    s_cmd_str = ["tshark", "-r", s_cap_file,
                 "-T", "fields", "-e", "frame.time_epoch"]
    logger.debug(s_cmd_str)

    try:
        s_cmd_result = subprocess.check_output(s_cmd_str).decode("utf-8")
        l_cmd_result = s_cmd_result.split("\n")
        l_cmd_result.remove("")

        i_num_of_pkt = len(l_cmd_result)
    except Exception as err_info:
        logger.error(err_info)
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR

    logger.debug("[PKT CHK] num_of_pkt: " + str(i_num_of_pkt))
    return i_num_of_pkt, i_ret


##
#  @brief set the packet filter for thark's option
#  @param i_analyzemsg    AnalyzeMsg type which is defined
#                         in "CLS_Define.py" file
#  @param logger          logger parameter for debug
#  @retval s_filter       the packet filter for thark's option
def set_pkt_filter(i_analyzemsg, logger):
    logger.debug("[PKT CHK] create packet filter")

    # read packet filter file
    s_filter_file = "./device/AIRCAP/sub/filter.json"

    try:
        with open(s_filter_file, "r") as fr_filter:
            # set dict data for the packet filter
            d_pkt_filter = json.load(fr_filter, object_pairs_hook=OrderedDict)
    except Exception as err_info:
        logger.error(err_info)
        return ""

    s_filter = [v for v in d_pkt_filter[str(i_analyzemsg)].values()][0]
    logger.debug(s_filter)
    return s_filter


##
#  @brief create the filter string of sevral address for thark's option
#  @param d_tlv_param       TLV parameter \n
#      **["NumOfLink"]**    the number of the link between the DUT and
#                           the remote device (int) \n
#      **["SourceAddr"]**   the source address to be filtered (str) \n
#      **["DestAddr"]**     the destination address to be filtered (str) \n
#      **["TransAddr"]**    the tranmitter address to be filtered (str)
#  @param i_analyzemsg      AnalyzeMsg type which is defined in
#                           "CLS_Define.py" file, to be selected (int)
#  @param logger            logger parameter for debug
#  @retval s_filter         the address filter set for thark's option
def create_addr_filter(d_tlv_param, i_analyzemsg, logger):
    logger.debug("[PKT CHK] create address filter")

    s_filter = ""

    # option parameter
    if "NumOfLink" in d_tlv_param:
        i_num_of_link = d_tlv_param["NumOfLink"]
    else:
        i_num_of_link = 1

    for num in range(i_num_of_link):
        if "" != s_filter:
            s_filter += " or "
        else:
            pass

        if i_num_of_link != 1:
            d_tmp_dict = OrderedDict()
            #for i in range(len(d_tlv_param["DataList"])):
            d_tmp_dict.update(d_tlv_param["DataList"][num])
        else:
            d_tmp_dict = d_tlv_param

        # create address filter
        if "SourceAddr" in d_tmp_dict and "DestAddr" in d_tmp_dict:
            s_filter += "((wlan src " + d_tmp_dict["SourceAddr"]
            if i_analyzemsg != COM_DEF.i_AnalyzeMsg_ProbeReq:
                s_filter += " and wlan dst " + d_tmp_dict["DestAddr"]
            else:
                pass

            s_filter += ") or "
            s_filter += "(wlan src " + d_tmp_dict["DestAddr"]
            if i_analyzemsg != COM_DEF.i_AnalyzeMsg_Beacon:
                s_filter += " and wlan dst " + d_tmp_dict["SourceAddr"]
            else:
                pass

            s_filter += "))"
        elif "SourceAddr" in d_tmp_dict:
            s_filter += "(wlan src " + d_tmp_dict["SourceAddr"]
            s_filter += " or wlan dst " + d_tmp_dict["SourceAddr"]
            s_filter += ")"
        elif "DestAddr" in d_tmp_dict:
            s_filter += "(wlan src " + d_tmp_dict["DestAddr"]
            s_filter += " or wlan dst " + d_tmp_dict["DestAddr"]
            s_filter += ")"
        else:
            pass

        # option parameter
        if "TransAddr" in d_tmp_dict:
            if "" != s_filter:
                s_filter += " or wlan host " + d_tmp_dict["TransAddr"]
            else:
                s_filter += "wlan host " + d_tmp_dict["TransAddr"]
        else:
            pass

    return s_filter


##
#  @brief create the filter string of both of the address filter and
#         the packet filter for thark's option
#  @param d_tlv_param   TLV parameter
#  @param i_analyzemsg  AnalyzeMsg type which is defined in
#                       "CLS_Define.py" file, to be selected
#  @param logger        logger parameter for debug
#  @retval s_filter   filter set string of both the address filter and
#                     the packet filter for thark's option
def create_filter(d_tlv_param, i_analyzemsg, logger):
    logger.debug("[PKT CHK] create filter")

    s_filter = ""
    s_filter += create_addr_filter(d_tlv_param, i_analyzemsg, logger)

    if "" != s_filter:
        s_filter += " and "
    else:
        pass

    s_filter += set_pkt_filter(i_analyzemsg, logger)

    return s_filter


##
#  @brief search the packet of AnalyzeMsg which is specified at the filter,
#  and create the filtered "pcap" file.
#  @param s_capturefilename     the capture file name with the directory path
#  @param s_filter            the filter for thark's option
#  @param logger              logger parameter for debug
#  @retval i_ret              the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
#  @retval s_filtered_file    the name of the filtered "pcap" file
#                             with the directory path
def create_filtered_file(s_capturefilename, s_filter, logger):
    logger.debug("[PKT CHK] start create_filtered_file")

    i_base_length = 0
    s_filtered_file = ""
    i_ret = COM_DEF.i_RET_SUCCESS

    try:
        # open capture file
        pcap = pcapy.open_offline(s_capturefilename)
        s_filtered_file = s_capturefilename.replace(".pcap", "-f.pcap")
        dumper = pcap.dump_open(s_filtered_file)
    except Exception as err_info:
        logger.error(err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, s_filtered_file

    # set filter
    logger.info("[PKT CHK3] filter : " + s_filter + " || filename : " +
                s_filtered_file)

    pcap.setfilter(s_filter)
    try:
        # read packet one by one
        (header, payload) = pcap.next()
        dumper.dump(header, payload)
    except Exception as err_info:
        logger.error(err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, s_filtered_file

    # check whether target packet is or not
    if header is not None:
        logger.error("[PKT CHK] target packet is none !!")
    else:
        pass

    while header:
        # skip to check same packet
        if i_base_length == header.getlen():
            try:
                (header, payload) = pcap.next()
                #dumper.dump(header, payload)
            except Exception as err_info:
                logger.error(err_info)
                break
            continue
        else:
            i_base_length = header.getlen()

        try:
            (header, payload) = pcap.next()
            dumper.dump(header, payload)
        except Exception as e:
            logger.error(e)
            pass

    # close s_filtered_file
    del dumper

    logger.debug("[PKT CHK] create_filtered_file complete")
    return i_ret, s_filtered_file


##
#  @brief get the number of the packets in the "pcap" file
#  @param s_capturefilename the capture file name
#  @param i_analyzemsg      AnalyzeMsg type which is defined
#                           in "CLS_Define.py" file, to be counted
#  @param d_tlv_param       TLV parameter
#  @param logger            logger parameter for debug
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
#  @retval s_filtered_file  the name of the filtered "pcap" file
#                           with the directory path
#  @retval i_num_of_pkt     the number of the packets of
#                           AnalyzeMsg type
def get_pkt_num(s_capturefilename, i_analyzemsg, d_tlv_param, logger):
    logger.debug("[PKT CHK] start count_pkt")

    s_filter = ""
    s_filtered_file = ""
    i_num_of_pkt = 0
    i_ret = COM_DEF.i_RET_SUCCESS

    # create filter
    s_filter = create_filter(d_tlv_param, i_analyzemsg, logger)
    if "" == s_filter:
        logger.error("[PKT CHK] TLV is wrong !!")
        return COM_DEF.i_RET_TLV_ABNORMAL, s_filtered_file, i_num_of_pkt

    # search capture file
    i_ret, s_filtered_file_name = create_filtered_file(
        s_capturefilename, s_filter, logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        # rename the filtered file for the each AnalyzeMsg
        s_suffix = "-f-" + str(i_analyzemsg) + ".pcap"
        s_filtered_file = s_filtered_file_name.replace("-f.pcap", s_suffix)
        os.rename(s_filtered_file_name, s_filtered_file)

    # count num of packet
    i_num_of_pkt, i_ret = count_packet(s_filtered_file, logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        pass

    logger.debug("[PKT CHK] get_pkt_num complete")
    return i_ret, s_filtered_file, i_num_of_pkt


##
#  @brief search the packet of AnalyzeMsg in the "pcap" file,
#         and return the filtered "pcap" file.
#  @param s_cap_file        the "pcap" file name
#  @param i_analyzemsg      AnalyzeMsg type which is defined
#                           in "CLS_Define.py" file, to be selected
#  @param d_tlv_param       TLV parameter
#  @param logger            logger parameter for debug
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
#  @retval s_filtered_file  the name of the filtered "pcap" file
#                           with the directory path
#  @retval i_num_of_pkt     the number of the packets of AnalyzeMsg type
def search(s_capturefilename, i_analyzemsg, d_tlv_param, logger):
    logger.debug("[PKT CHK] start select")

    s_filter = ""
    s_filtered_file = ""
    i_num_of_pkt = 0
    i_ret = COM_DEF.i_RET_SUCCESS

    # create filter
    s_filter = create_filter(d_tlv_param, i_analyzemsg, logger)
    if "" == s_filter:
        logger.error("[PKT CHK] TLV is wrong !!")
        return COM_DEF.i_RET_TLV_ABNORMAL, s_filtered_file, i_num_of_pkt

    # search capture file
    i_ret, s_filtered_file_name = create_filtered_file(
        s_capturefilename, s_filter, logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        # rename the filtered file for the each AnalyzeMsg
        s_suffix = "-f-" + str(i_analyzemsg) + ".pcap"
        s_filtered_file = s_filtered_file_name.replace("-f.pcap", s_suffix)
        os.rename(s_filtered_file_name, s_filtered_file)

    # cnv pcap to json
    if debug_level() > 0:
        i_ret = pcap2json(s_filtered_file, logger)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            logger.error("[PKT CHK] json convert fail !!")
            return i_ret, s_filtered_file, i_num_of_pkt
        else:
            pass

    # count num of packet
    i_num_of_pkt, i_ret = count_packet(s_filtered_file, logger)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        pass

    logger.debug("[PKT CHK] select complete")
    return i_ret, s_filtered_file, i_num_of_pkt


##
#  @brief compare the IE value between the capture data and the reference data
#  @param i_analyzemsg      AnalyzeMsg type which is defined
#                           in "CLS_Define.py" file, to be analyzed
#  @param l_ie_name_list    list of the IE name which will be compared
#  @param d_ref_data        dict data of IE values of the reference data
#  @param d_cap_ie          dict data of IE values of the capture data
#  @param d_rply_tlv        input data of reply TLV
#  @param i_cnt             input value of the counter of NG ie
#  @param logger            logger parameter for debug
#  @retval i_cnt            output value of the counter of NG ie
#  @retval d_rply_tlv       output data of reply TLV data to Control PC \n
#      **["Result"]**    the value of the result (int) \n
#      - i_RET_SUCCESS\n
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
def compare_ie_val(i_analyzemsg, l_ie_name_list, d_ref_data, d_cap_ie,
                   d_rply_tlv, i_cnt, logger):
    l_tlv_list = []
    i_in_cnt = 0
    logger.debug("[PKT CHK] start compare_ie_val")
    logger.debug(d_cap_ie)

    # set result value as default

    # compare cap_ie_val with ref_ie_value
    for s_ie_name in l_ie_name_list:
        s_ref_ie_val = d_ref_data.get(s_ie_name)
        s_cap_ie_val = d_cap_ie.get(s_ie_name)

        l_ref_ie_val = s_ref_ie_val.split(",")
        l_cap_ie_val = s_cap_ie_val.split(",")

        i_lst_idx = 0
        l_cap_ie_val_result = []
        for ie_val in l_ref_ie_val:
            if ie_val in l_cap_ie_val[i_lst_idx:]:
                l_cap_ie_val_result.append(ie_val)
                i_lst_idx = l_cap_ie_val.index(ie_val)

        if s_ref_ie_val == "":
            logger.debug("IE check result : OK\n  " + s_ie_name +
                         "\n  " + "ref_ie:" + s_ref_ie_val +
                         " cap_ie:" + s_cap_ie_val)
            continue
        # check l_ref_ie_val which is included in s_cap_ie_val
        elif l_ref_ie_val == l_cap_ie_val_result:
            logger.debug("IE check result : OK\n  " + s_ie_name +
                         "\n  " + "ref_ie:" + s_ref_ie_val +
                         " cap_ie:" + s_cap_ie_val)
            continue
        else:
            # set NG result & reason
            logger.error("IE check result : NG\n  " + s_ie_name +
                         "\n  " + "ref_ie:" + s_ref_ie_val +
                         " cap_ie:" + s_cap_ie_val)

            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
            d_rply_tlv["NgReason"] = COM_DEF.i_IeNotMatch

            d_list_tlv = OrderedDict()
            d_list_tlv["AnalyzeMsg"] = i_analyzemsg
            d_list_tlv["NgIeName"] = s_ie_name
            d_list_tlv["NgIeValueLen"] = len(s_cap_ie_val)
            d_list_tlv["NgIeValue"] = s_cap_ie_val
            l_tlv_list.append(d_list_tlv)

            i_in_cnt += 1

    if i_in_cnt:
        d_rply_tlv["DataList"].extend(l_tlv_list)
        d_rply_tlv["NumOfNg"] = i_in_cnt + i_cnt
        logger.info("DataList:   " +  str(d_rply_tlv["DataList"]))        
        logger.info("AAAAA___Count:  " +  str(d_rply_tlv["NumOfNg"]))
    else:
        pass

    return i_in_cnt + i_cnt, d_rply_tlv
