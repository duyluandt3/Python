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
    s_dbg_inf_file = \
        COM_DEF.s_TOPDIR + "/Common/debug/json/DebugInfo_AIRCAP.json"

    try:
        with open(s_dbg_inf_file, "r", encoding='utf-8-sig') as fr_data:
            d_debugInfo = json.load(fr_data)
    except Exception as err_info:
        print(err_info)
        print("failed to open debug file")
        return COM_DEF.i_RET_SUCCESS

    return d_debugInfo["DebugLevel"]
# @endcond


##
#  @brief execute command
#  @param l_com_hdr_info    command header parameter
#  @param soc               socket number
#  @param s_cmd_str         command array to be executed
#  @param Dbg            debug parameter for debug
#  @retval d_rply_tlv     reply TLV data to MC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def exec_command(l_com_hdr_info, soc, l_cmd_data, Dbg):

    Dbg.log(COM_DEF.TRACE,
            "[S] exec_command")

    i_ret = COM_DEF.i_RET_SUCCESS

    snd_req_cmd(l_com_hdr_info, ' '.join(l_cmd_data), soc,
                COM_DEF.i_MODULE_AIRCAP)

    Dbg.log(COM_DEF.INFO, ' '.join(l_cmd_data))

    i_ret = subprocess.call(l_cmd_data)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        Dbg.log(COM_DEF.ERROR,
                "subprocess.call error [ret:%d]" % i_ret)
    else:
        pass

    Dbg.log(COM_DEF.TRACE,
            "[E] exec_command")

    return i_ret


##
#  @brief set monitor mode to the external wlan device
#  @param self      instance of AIRCAP_FUNC class
#  @param l_com_hdr_info    command header parameter
#  @param s_wlan_ifname     name of the external wlan device
#  @retval d_rply_tlv     reply TLV data to MC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def set_external_wlan_dev(self, l_com_hdr_info, s_wlan_ifname):

    self.Dbg.log(COM_DEF.TRACE,
                 "[S] set_external_wlan_dev")

    i_ret = COM_DEF.i_RET_SUCCESS

    # ifcheck
    s_cmd_str = "iw dev " + self.wlan_ifname + " info"
    snd_req_cmd(l_com_hdr_info, s_cmd_str, self.soc, COM_DEF.i_MODULE_AIRCAP)

    self.Dbg.log(COM_DEF.INFO, s_cmd_str)

    for i in range(5):

        try:
            s_return_data = subprocess.getoutput(s_cmd_str)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.DEBUG,
                         "subprocess.getoutput error")
            self.Dbg.log(COM_DEF.DEBUG,
                         err_info)

        if s_return_data:
            break
        else:
            pass
    # for end

    if 5 <= i:
        self.Dbg.log(COM_DEF.ERROR,
                     "can't get monitor I/F info")
        return COM_DEF.i_RET_SYSTEM_ERROR
    else:
        pass

    snd_req_cmd(l_com_hdr_info, s_return_data, self.soc,
                COM_DEF.i_MODULE_AIRCAP)

    self.Dbg.log(COM_DEF.INFO, s_return_data)

    if "No such device" in s_return_data:
        self.Dbg.log(COM_DEF.ERROR, "No such device")
        return COM_DEF.i_RET_TLV_ABNORMAL
    else:
        if "channel" in s_return_data:
            self.Dbg.log(COM_DEF.DEBUG,
                         "already set monitor interface")
            self.Dbg.log(COM_DEF.TRACE,
                         "[E] set_external_wlan_dev")
            return i_ret
        else:
            pass

    # ifdown
    l_cmd_data = ["ip", "link", "set", s_wlan_ifname, "down"]
    i_ret = exec_command(l_com_hdr_info, self.soc, l_cmd_data, self.Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # set monitor mode
    l_cmd_data = ["iw", "dev", s_wlan_ifname, "set", "monitor", "none"]
    i_ret = exec_command(l_com_hdr_info, self.soc, l_cmd_data, self.Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifup
    l_cmd_data = ["ip", "link", "set", s_wlan_ifname, "up"]
    i_ret = exec_command(l_com_hdr_info, self.soc, l_cmd_data, self.Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    self.Dbg.log(COM_DEF.TRACE,
                 "[E] set_external_wlan_dev")

    return i_ret


##
#  @brief set monitor mode to the internal wlan device
#  @param self      instance of AIRCAP_FUNC class
#  @param l_com_hdr_info    command header parameter
#  @param s_wlan_ifname     name of the internal wlan device
#  @retval d_rply_tlv     reply TLV data to MC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def set_internal_wlan_dev(self, l_com_hdr_info, s_wlan_ifname):

    self.Dbg.log(COM_DEF.TRACE,
                 "[S] set_internal_wlan_dev")

    # ifcheck
    s_cmd_str = "iw dev wmon0 info"
    snd_req_cmd(l_com_hdr_info, s_cmd_str, self.soc,
                COM_DEF.i_MODULE_AIRCAP)

    self.Dbg.log(COM_DEF.INFO, s_cmd_str)

    try:
        s_return_data = subprocess.getoutput(s_cmd_str)
    except Exception as err_info:
        self.Dbg.log(COM_DEF.ERROR,
                     "subprocess.getoutput error")
        self.Dbg.log(COM_DEF.ERROR,
                     err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR

    snd_req_cmd(l_com_hdr_info, s_return_data, self.soc,
                COM_DEF.i_MODULE_AIRCAP)

    self.Dbg.log(COM_DEF.INFO, s_return_data)

    if "No such device" in s_return_data:
        # check no "wmon0" device
        pass
    else:
        self.Dbg.info("[PKT CHK] already wmon0 add")
        return COM_DEF.i_RET_SUCCESS

    # ifdown
    l_cmd_data = ["ip", "link", "set", s_wlan_ifname, "down"]
    i_ret = exec_command(l_com_hdr_info, self.soc, l_cmd_data, self.Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifadd
    l_cmd_data = ["iw", "dev", s_wlan_ifname, "interface", "add",
                  "wmon0", "type", "monitor"]
    i_ret = exec_command(l_com_hdr_info, self.soc, l_cmd_data, self.Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifup
    l_cmd_data = ["ip", "link", "set", "wmon0", "up"]
    i_ret = exec_command(l_com_hdr_info, self.soc, l_cmd_data, self.Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # ifdel
    l_cmd_data = ["iw", "dev", s_wlan_ifname, "del"]
    i_ret = exec_command(l_com_hdr_info, self.soc, l_cmd_data, self.Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    self.Dbg.log(COM_DEF.TRACE,
                 "[E] set_internal_wlan_dev")

    return COM_DEF.i_RET_SUCCESS


##
#  @brief set the wlan interface
#  @param self      instance of AIRCAP_FUNC class
#  @param l_com_hdr_info    command header parameter
#  @param d_tlv_param     received TLV parameter from MC
#  @retval d_rply_tlv     reply TLV data to MC \n
#      **["Result"]**     the value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def set_wlan_if(self, l_com_hdr_info, d_tlv_param):

    self.Dbg.log(COM_DEF.TRACE,
                 "[S] set_wlan_if")

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

    self.Dbg.log(COM_DEF.DEBUG,
                 "INTERFACE : %s" % s_wlan_ifname)

    if "wlp" in s_wlan_ifname:
        i_ret = set_internal_wlan_dev(self, l_com_hdr_info, s_wlan_ifname)
    else:
        i_ret = set_external_wlan_dev(self, l_com_hdr_info, s_wlan_ifname)

    self.Dbg.log(COM_DEF.TRACE,
                 "[E] set_wlan_if")

    return i_ret


##
#  @brief transfer the file with scp command
#  @param l_com_hdr_info    command header parameter
#  @param s_src_file        source file (or directory path)
#  @param s_dst_file        destination file (or directory path)
#  @param s_passwd          password for the user account on the remote host
#  @param Dbg               debug parameter for debug
#  @param soc               socket descriptor
#  @retval i_ret            int value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def transfer_file(l_com_hdr_info, s_src_file, s_dst_file,
                  s_passwd, Dbg, soc):

    Dbg.log(COM_DEF.TRACE, "[S] transfer_file")

    i_ret = COM_DEF.i_RET_SUCCESS

    l_cmd_data = ["sshpass", "-p", s_passwd, "scp", "-o",
                  "StrictHostKeyCHecking=no",
                  "-r", s_src_file, s_dst_file]

    snd_req_cmd(l_com_hdr_info, ' '.join(l_cmd_data), soc,
                COM_DEF.i_MODULE_AIRCAP)

    Dbg.log(COM_DEF.INFO, ' '.join(l_cmd_data))

    try:
        subprocess.check_output(l_cmd_data)
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "subprocess.check_output error")
        Dbg.log(COM_DEF.ERROR, err_info)
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR

    Dbg.log(COM_DEF.TRACE, "[E] transfer_file")

    return i_ret


##
#  @brief transfer the file with scp command
#  @param l_com_hdr_info    command header parameter
#  @param s_src_file        source file (Aircap file)
#  @param Dbg               debug parameter for debug
#  @param soc               socket descriptor
#  @retval i_ret            int value of the result (int) \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def check_file_size(self, l_com_hdr_info, s_src_file, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] check_file_size")

    i_ret = COM_DEF.i_RET_SUCCESS
    i_file_size = 0
    get_list = " "
    file_buff = []
    l_cmd_data = ["ls", "-la", s_src_file]

    snd_req_cmd(l_com_hdr_info, ' '.join(l_cmd_data), self.soc,
                COM_DEF.i_MODULE_AIRCAP)
    self.Dbg.log(COM_DEF.INFO,
                 ' '.join(l_cmd_data))

    try:
        proc = subprocess.Popen(l_cmd_data,
                                stdout=subprocess.PIPE)
        stdout = proc.communicate()

    except Exception as err_info:
        self.Dbg.log(COM_DEF.ERROR,
                     "subprocess.Popen error")
        self.Dbg.log(COM_DEF.ERROR,
                     err_info)
        d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
        return d_rply_tlv

    # Get file info and split size of file
    self.Dbg.log(COM_DEF.INFO, stdout)
    get_list = str(stdout)
    file_buff = get_list.split(' ')
    # print(file_buff[4])

    # Check size of file
    if 0 == int(file_buff[4]):
        i_ret = COM_DEF.i_RET_TLV_ABNORMAL
        return i_ret
    else:
        i_file_size = int(file_buff[4])

    Dbg.log(COM_DEF.TRACE, "[E] Get Aircap packet size")

    return i_ret, i_file_size


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
def make_zip_file(self, d_tlv_param, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] make_zip_file")

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
        Dbg.log(COM_DEF.DEBUG, "serach file : %s" % s_cap_file)
        l_cap_file_list = glob.glob(s_cap_file)
    else:
        Dbg.log(COM_DEF.ERROR,
                "capture file name is not specified !!")
        i_ret = COM_DEF.i_RET_TLV_ABNORMAL
        return i_ret, s_zip_file

    if len(l_cap_file_list) == 0:
        Dbg.log(COM_DEF.ERROR,
                "capture file does not exists!!")
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
        Dbg.log(COM_DEF.ERROR,
                "zip file is not created !!")
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR
        return i_ret, s_zip_file
    else:
        # delete work directory
        shutil.rmtree(s_zip_file_path)

    Dbg.log(COM_DEF.INFO,
            "create zip file : %s" % (s_zip_file))

    Dbg.log(COM_DEF.TRACE, "[E] make_zip_file")

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
def set_capture_file_name(self, d_tlv_param, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] set_capture_file_name")

    i_ret = COM_DEF.i_RET_SUCCESS
    s_capturefilename = ""

    # option parameter
    if "AircapIfId" in d_tlv_param:
        i_aircap_if_id = d_tlv_param["AircapIfId"]
    else:
        i_aircap_if_id = 1

    if self.s_filename == "":
        if "CaptureFileName" in d_tlv_param:
            s_cap_file = self.cap_file_path
            s_cap_file += d_tlv_param["CaptureFileName"]
            s_cap_file += "_AIRCAP"
            s_cap_file += str(i_aircap_if_id)
            # wild card
            s_cap_file += "*.*"
            l_cap_file_list = sorted(glob.glob(s_cap_file),
                                     key=os.path.getmtime)
            if len(l_cap_file_list) != 0:
                s_capturefilename = l_cap_file_list[-1]
            else:
                Dbg.log(COM_DEF.ERROR,
                        "capture file name does not exists!!")
                i_ret = COM_DEF.i_RET_TLV_ABNORMAL
        else:
            Dbg.log(COM_DEF.ERROR,
                    "capture file name does not exists!!")
            i_ret = COM_DEF.i_RET_TLV_ABNORMAL
    else:
        s_capturefilename = self.s_filename

    if not os.path.exists(s_capturefilename):
        Dbg.log(COM_DEF.ERROR,
                "capture file name does not exists!!")
        i_ret = COM_DEF.i_RET_TLV_ABNORMAL
    else:
        pass

    Dbg.log(COM_DEF.INFO,
            "capture file name : %s" % (s_capturefilename))

    Dbg.log(COM_DEF.TRACE, "[E] set_capture_file_name")

    return i_ret, s_capturefilename


##
#  @brief calculate the control frequency and the center frequency \n
#  @brief from the channel number and the bandwidth
#  @param i_channel         the channel number
#  @param s_bandwidth       the bandwidth
#  @param i_sideband        the upper or lower in 2.4GHz
#  @param Dbg            debug parameter for debug
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
#  @retval d_ch_info        dict data for the channel infomation \n
#      **["ControlFreq"]**    the control frequency (int) \n
#      **["CenterFreq"]**     the center frequency (int) \n
#      **["CenterFreq2"]**    the 2nd center frequency (int) \n
#      **["BandWidth"]**      the bandwidth (str) \n
def calculate_freq(i_channel, s_bandwidth, i_sideband, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] calculate_freq")

    Dbg.log(COM_DEF.DEBUG,
            "CHANNEL : %d  BANDWIDTH : %s"
            % (i_channel, s_bandwidth))

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
        elif 1 <= i_channel <= 4:
            # ch1 - ch9   : 2.4GHz/HT40+
            i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10)
        elif 5 <= i_channel and i_channel <= 9:
            if COM_DEF.i_Sideband_upper == i_sideband:
                i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10)
            elif COM_DEF.i_Sideband_lower == i_sideband:
                i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10) * -1
            else:
                Dbg.log(COM_DEF.INFO,
                        "can't get sideband paramter...\
                         set lower to sideband from 5ch to 9ch")
                i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10) * -1
        else:
            # ch10 - ch13 : 2.4GHz/HT40-
            i_centerfreq = i_controlfreq + (i_bandwidth // 2 - 10) * -1
    elif i_channel in l_w58:
        # 5GHz - W58
        if i_channel in [165, 169] and s_bandwidth in ["40", "80"]:
            Dbg.log(COM_DEF.ERROR,
                    "bandwidth parameter is abnormal !!")
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
        Dbg.log(COM_DEF.ERROR,
                "channel parameter is abnormal !!")
        i_ret = COM_DEF.i_RET_TLV_ABNORMAL

    # set the channel infomation for the result
    d_ch_info["ControlFreq"] = i_controlfreq
    d_ch_info["BandWidth"] = s_bandwidth
    d_ch_info["CenterFreq"] = i_centerfreq
    if "80+80" in s_bandwidth:
        d_ch_info["CenterFreq2"] = i_centerfreq + 80
    else:
        d_ch_info["CenterFreq2"] = 0

    Dbg.log(COM_DEF.INFO,
            "CONTROL FREQ : %d" % (i_controlfreq))
    Dbg.log(COM_DEF.INFO,
            "BANDWIDTH    : %s MHz" % (s_bandwidth))
    Dbg.log(COM_DEF.INFO,
            "CENTER FREQ  : %d" % (i_centerfreq))

    Dbg.log(COM_DEF.TRACE, "[E] calculate_freq")

    return i_ret, d_ch_info


##
#  @brief set channel parameter to the wlan device interface
#  @param l_com_hdr_info    com header info
#  @param soc               socket number
#  @param d_tlv_param       TLV parameter \n
#      **["Channel"]**      the channel number (int) \n
#      **["Bandwidth"]**    string of the bandwidth (str) \n
#  @param Dbg            debug parameter for debug
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
def set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] set_channel")

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
        Dbg.log(COM_DEF.ERROR,
                "bandwidth parameter is abnormal (%d)!!"
                % i_chanwidth)
        return COM_DEF.i_RET_TLV_ABNORMAL

    if 'Sideband' in d_tlv_param:
        i_sideband = d_tlv_param['Sideband']
    else:
        i_sideband = 0

    # calculate channel freq
    i_ret, d_ch_info = calculate_freq(i_channel, s_bandwidth, i_sideband, Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret
    else:
        pass

    # set band
    if 0 != d_ch_info["ControlFreq"] and 0 != d_ch_info["CenterFreq"]:

        # create iw dev command
        if COM_DEF.i_Bandwidth_20MHz == i_chanwidth:
            l_cmd_data = ["iw", "dev", s_wlan_ifname, "set", "freq",
                          str(d_ch_info["ControlFreq"])]
        else:
            l_cmd_data = ["iw", "dev", s_wlan_ifname, "set", "freq",
                          str(d_ch_info["ControlFreq"]),
                          d_ch_info["BandWidth"],
                          str(d_ch_info["CenterFreq"])]

        if "80+80" in d_ch_info["BandWidth"]:
            l_cmd_data += [str(d_ch_info["CenterFreq2"])]
        else:
            pass

        # execute iw dev command
        i_ret = exec_command(l_com_hdr_info, soc, l_cmd_data, Dbg)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            return i_ret
        else:
            pass
    else:
        pass

    Dbg.log(COM_DEF.TRACE, "[E] set_channel")

    return i_ret


##
#  @brief convert "pcap" file to "json" file
#  @param l_com_hdr_info    com header info
#  @param s_cap_file    the "pcap" file name
#  @param Dbg        debug parameter for debug
#  @param soc               socket descriptor
#  @retval i_ret        the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
#  @return **s_json_file**    "json" file name
def pcap2json(l_com_hdr_info, s_cap_file, Dbg, soc):

    Dbg.log(COM_DEF.TRACE, "[S] pcap2json")

    i_ret = COM_DEF.i_RET_SUCCESS
    s_json_file = s_cap_file.replace(".pcap", ".json")
    l_cmd_data = ["tshark", "-r", s_cap_file, "-T", "json"]

    snd_req_cmd(l_com_hdr_info, ' '.join(l_cmd_data), soc,
                COM_DEF.i_MODULE_AIRCAP)

    Dbg.log(COM_DEF.INFO, ' '.join(l_cmd_data))

    try:
        json_data = subprocess.check_output(l_cmd_data).decode("utf-8")
        json_data = json_data.replace("  {", "[\n  {")
        json_data = json_data.replace("  }\n\n", "  }\n]")
        json_data = json_data.replace("  ,", ",")
        json_data = json_data.replace("]]", "]\n]")
        # print(json_data)

        with open(s_json_file, "w") as fw_json:
            fw_json.write(json_data)
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "subprocess.check_output error")
        Dbg.log(COM_DEF.ERROR, err_info)
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR

    return i_ret


##
#  @brief count the number of the packets in the "pcap" file
#  @param l_com_hdr_info    com header info
#  @param s_cap_file    the "pcap" file name
#  @param Dbg        debug parameter for debug
#  @param soc               socket descriptor
#  @retval i_num_of_pkt the number of the packets
#  @retval i_ret        the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
def count_packet(l_com_hdr_info, s_cap_file, Dbg, soc):

    Dbg.log(COM_DEF.TRACE, "[S] count_packet")

    i_num_of_pkt = 0
    i_ret = COM_DEF.i_RET_SUCCESS
    l_cmd_data = ["tshark", "-r", s_cap_file,
                  "-T", "fields", "-e", "frame.time_epoch"]

    snd_req_cmd(l_com_hdr_info, ' '.join(l_cmd_data), soc,
                COM_DEF.i_MODULE_AIRCAP)

    Dbg.log(COM_DEF.INFO, ' '.join(l_cmd_data))

    try:
        s_cmd_result = subprocess.check_output(l_cmd_data).decode("utf-8")
        l_cmd_result = s_cmd_result.split("\n")
        l_cmd_result.remove("")

        i_num_of_pkt = len(l_cmd_result)
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "subprocess.check_output error")
        Dbg.log(COM_DEF.ERROR, err_info)
        i_ret = COM_DEF.i_RET_SYSTEM_ERROR

    Dbg.log(COM_DEF.TRACE, "[E] count_packet")

    return i_num_of_pkt, i_ret


##
#  @brief set the packet filter for thark's option
#  @param i_analyzemsg    AnalyzeMsg type which is defined
#                         in "CLS_Define.py" file
#  @param Dbg          debug parameter for debug
#  @retval s_filter       the packet filter for thark's option
def set_pkt_filter(i_analyzemsg, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] set_pkt_filter")

    # read packet filter file
    s_filter_file = COM_DEF.s_TOPDIR + \
        "/Others/src/device/AIRCAP/sub/filter.json"

    try:
        with open(s_filter_file, "r") as fr_filter:
            # set dict data for the packet filter
            d_pkt_filter = json.load(fr_filter, object_pairs_hook=OrderedDict)
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "failed to open filter.json")
        Dbg.log(COM_DEF.ERROR, err_info)
        return ""

    s_filter = [v for v in d_pkt_filter[str(i_analyzemsg)].values()][0]

    Dbg.log(COM_DEF.TRACE, "[E] set_pkt_filter")

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
#  @param Dbg            debug parameter for debug
#  @retval s_filter         the address filter set for thark's option
def create_addr_filter(d_tlv_param, i_analyzemsg, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] create_addr_filter")

    s_filter = ""

    # option parameter
    if "NumOfLink" in d_tlv_param:
        i_num_of_link = d_tlv_param["NumOfLink"]
    else:
        i_num_of_link = 1

    Dbg.log(COM_DEF.DEBUG, "the number of filter [%d]" % i_num_of_link)

    for num in range(i_num_of_link):
        if "" != s_filter:
            s_filter += " or "
        else:
            pass

        if "DataList" in d_tlv_param:
            d_tmp_dict = OrderedDict()
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

    Dbg.log(COM_DEF.TRACE, "[E] create_addr_filter")

    return s_filter


##
#  @brief create the filter string of both of the address filter and
#         the packet filter for thark's option
#  @param d_tlv_param   TLV parameter
#  @param i_analyzemsg  AnalyzeMsg type which is defined in
#                       "CLS_Define.py" file, to be selected
#  @param Dbg        debug parameter for debug
#  @retval s_filter   filter set string of both the address filter and
#                     the packet filter for thark's option
def create_filter(d_tlv_param, i_analyzemsg, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] create_filter")

    s_filter1 = ""
    s_filter2 = ""

    s_filter1 = create_addr_filter(d_tlv_param, i_analyzemsg, Dbg)
    Dbg.log(COM_DEF.DEBUG, "address filters : %s" % s_filter1)
    s_filter2 = set_pkt_filter(i_analyzemsg, Dbg)
    Dbg.log(COM_DEF.DEBUG, "message filters : %s" % s_filter2)

    if "" != s_filter1 and "" != s_filter2:
        s_filter = s_filter1 + " and " + s_filter2
    elif "" != s_filter1:
        s_filter = s_filter1
    else:
        s_filter = s_filter2

    Dbg.log(COM_DEF.TRACE, "[E] create_filter")

    return s_filter


##
#  @brief search the packet of AnalyzeMsg which is specified at the filter,
#  and create the filtered "pcap" file.
#  @param s_capturefilename     the capture file name with the directory path
#  @param s_filter            the filter for thark's option
#  @param Dbg              debug parameter for debug
#  @retval i_ret              the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_SYSTEM_ERROR
#      .
#  @retval s_filtered_file    the name of the filtered "pcap" file
#                             with the directory path
def create_filtered_file(s_capturefilename, s_filter, Dbg):

    Dbg.log(COM_DEF.TRACE, "[S] create_filtered_file")

    i_base_length = 0
    s_filtered_file = ""
    i_ret = COM_DEF.i_RET_SUCCESS
    b_skip_target_check = False
    i_skiped_packet_num = 0
    dumper = 0

    try:
        # open capture file
        pcap = pcapy.open_offline(s_capturefilename)
        s_filtered_file = s_capturefilename.replace(".pcap", "-f.pcap")
        dumper = pcap.dump_open(s_filtered_file)
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "failed to open capture file")
        Dbg.log(COM_DEF.ERROR, err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, s_filtered_file

    # set filter
    Dbg.log(COM_DEF.DEBUG,
            "capture file : %s" % (s_filtered_file))
    # check target for skip process
    if (s_filter == "wlan subtype probe-req") or \
       (s_filter == "wlan subtype probe-resp") or \
       (s_filter == "wlan subtype beacon"):
        b_skip_target_check = True
    else:
        pass

    pcap.setfilter(s_filter)

    try:
        # read packet one by one
        (header, payload) = pcap.next()
        if header and payload:
            dumper.dump(header, payload)
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "failed to read first pcap data")
        Dbg.log(COM_DEF.ERROR, err_info)
        del dumper
        return COM_DEF.i_RET_SYSTEM_ERROR, s_filtered_file

    # check whether target packet is or not
    if not header:
        Dbg.log(COM_DEF.INFO, "target packet is none !!")
    else:
        pass

    while header:
        # skip to check same packet
        if i_base_length == header.getlen():
            try:
                (header, payload) = pcap.next()
                if not b_skip_target_check:
                    dumper.dump(header, payload)
                else:
                    i_skiped_packet_num += 1
            except Exception as err_info:
                Dbg.log(COM_DEF.ERROR,
                        "failed to read next pcap data")
                Dbg.log(COM_DEF.ERROR, err_info)
                break
            continue
        else:
            i_base_length = header.getlen()

        try:
            (header, payload) = pcap.next()
            dumper.dump(header, payload)
        except Exception as err_info:
            Dbg.log(COM_DEF.ERROR, err_info)

    # close s_filtered_file
    del dumper

    Dbg.log(COM_DEF.DEBUG,
            "beacon or probe packet of same " +
            "length is skiped, Skipped packet num : %d" %
            (i_skiped_packet_num))
    Dbg.log(COM_DEF.TRACE, "[E] create_filtered_file")

    return i_ret, s_filtered_file


##
#  @brief get the number of the packets in the "pcap" file
#  @param l_com_hdr_info    com header info
#  @param s_capturefilename the capture file name
#  @param i_analyzemsg      AnalyzeMsg type which is defined
#                           in "CLS_Define.py" file, to be counted
#  @param d_tlv_param       TLV parameter
#  @param Dbg            debug parameter for debug
#  @param soc               socket descriptor
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
#  @retval s_filtered_file  the name of the filtered "pcap" file
#                           with the directory path
#  @retval i_num_of_pkt     the number of the packets of
#                           AnalyzeMsg type
def get_pkt_num(l_com_hdr_info, s_capturefilename, i_analyzemsg,
                d_tlv_param, Dbg, soc):

    Dbg.log(COM_DEF.TRACE, "[S] get_pkt_num")

    s_filter = ""
    s_filtered_file = ""
    i_num_of_pkt = 0
    i_ret = COM_DEF.i_RET_SUCCESS

    # create filter
    s_filter = create_filter(d_tlv_param, i_analyzemsg, Dbg)
    if "" == s_filter:
        Dbg.log(COM_DEF.ERROR, "TLV abnormal !!")
        return COM_DEF.i_RET_TLV_ABNORMAL, s_filtered_file, i_num_of_pkt
    else:
        s_cmd_str = "tshark filters : %s" % s_filter
        snd_req_cmd(l_com_hdr_info, s_cmd_str, soc,
                    COM_DEF.i_MODULE_AIRCAP)
        Dbg.log(COM_DEF.INFO, s_cmd_str)

    # search capture file
    i_ret, s_filtered_file_name = create_filtered_file(
        s_capturefilename, s_filter, Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        # rename the filtered file for the each AnalyzeMsg
        s_suffix = "-f-" + str(i_analyzemsg) + ".pcap"
        s_filtered_file = s_filtered_file_name.replace("-f.pcap", s_suffix)
        os.rename(s_filtered_file_name, s_filtered_file)

        s_cmd_str = "filtered file name : %s" % s_filtered_file
        snd_req_cmd(l_com_hdr_info, s_cmd_str, soc,
                    COM_DEF.i_MODULE_AIRCAP)
        Dbg.log(COM_DEF.INFO, s_cmd_str)

    # count num of packet
    i_num_of_pkt, i_ret = \
        count_packet(l_com_hdr_info, s_filtered_file, Dbg, soc)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        s_cmd_str = "the number of packet : %d" % (i_num_of_pkt)
        snd_req_cmd(l_com_hdr_info, s_cmd_str, soc,
                    COM_DEF.i_MODULE_AIRCAP)
        Dbg.log(COM_DEF.INFO, s_cmd_str)

    Dbg.log(COM_DEF.TRACE, "[E] get_pkt_num")

    return i_ret, s_filtered_file, i_num_of_pkt


##
#  @brief search the packet of AnalyzeMsg in the "pcap" file,
#         and return the filtered "pcap" file.
#  @param l_com_hdr_info    com header info
#  @param s_cap_file        the "pcap" file name
#  @param i_analyzemsg      AnalyzeMsg type which is defined
#                           in "CLS_Define.py" file, to be selected
#  @param d_tlv_param       TLV parameter
#  @param Dbg            debug parameter for debug
#  @param soc               socket descriptor
#  @retval i_ret            the value of the result \n
#      - i_RET_SUCCESS \n
#      - i_RET_TLV_ABNORMAL
#      .
#  @retval s_filtered_file  the name of the filtered "pcap" file
#                           with the directory path
#  @retval i_num_of_pkt     the number of the packets of AnalyzeMsg type
def search(l_com_hdr_info, s_capturefilename, i_analyzemsg,
           d_tlv_param, Dbg, soc):

    Dbg.log(COM_DEF.TRACE, "[S] search")

    s_filter = ""
    s_filtered_file = ""
    i_num_of_pkt = 0
    i_ret = COM_DEF.i_RET_SUCCESS

    # create filter
    s_filter = create_filter(d_tlv_param, i_analyzemsg, Dbg)
    if "" == s_filter:
        Dbg.log(COM_DEF.ERROR, "TLV abnormal !!")
        return COM_DEF.i_RET_TLV_ABNORMAL, s_filtered_file, i_num_of_pkt
    else:
        s_cmd_str = "tshark filters : %s" % s_filter
        snd_req_cmd(l_com_hdr_info, s_cmd_str, soc,
                    COM_DEF.i_MODULE_AIRCAP)
        Dbg.log(COM_DEF.INFO, s_cmd_str)

    # search capture file
    i_ret, s_filtered_file_name = create_filtered_file(
        s_capturefilename, s_filter, Dbg)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        # rename the filtered file for the each AnalyzeMsg
        s_suffix = "-f-" + str(i_analyzemsg) + ".pcap"
        s_filtered_file = s_filtered_file_name.replace("-f.pcap", s_suffix)
        os.rename(s_filtered_file_name, s_filtered_file)

        s_cmd_str = "filtered file name : %s" % s_filtered_file
        snd_req_cmd(l_com_hdr_info, s_cmd_str, soc,
                    COM_DEF.i_MODULE_AIRCAP)
        Dbg.log(COM_DEF.INFO, s_cmd_str)

    # cnv pcap to json
    if debug_level() > 0:
        i_ret = pcap2json(l_com_hdr_info, s_filtered_file, Dbg, soc)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            Dbg.log(COM_DEF.ERROR, "failed to convert json !!")
            return i_ret, s_filtered_file, i_num_of_pkt
        else:
            pass

    # count num of packet
    i_num_of_pkt, i_ret = count_packet(l_com_hdr_info, s_filtered_file,
                                       Dbg, soc)
    if COM_DEF.i_RET_SUCCESS != i_ret:
        return i_ret, s_filtered_file, i_num_of_pkt
    else:
        s_cmd_str = "the number of packet : %d" % (i_num_of_pkt)
        snd_req_cmd(l_com_hdr_info, s_cmd_str, soc,
                    COM_DEF.i_MODULE_AIRCAP)
        Dbg.log(COM_DEF.INFO, s_cmd_str)

    Dbg.log(COM_DEF.TRACE, "[E] search")

    return i_ret, s_filtered_file, i_num_of_pkt


##
#  @brief compare the IE value between the capture data and the reference data
#  @param l_com_hdr_info    com header info
#  @param i_analyzemsg      AnalyzeMsg type which is defined
#                           in "CLS_Define.py" file, to be analyzed
#  @param l_ie_name_list    list of the IE name which will be compared
#  @param d_ref_data        dict data of IE values of the reference data
#  @param d_cap_ie          dict data of IE values of the capture data
#  @param d_rply_tlv        input data of reply TLV
#  @param i_cnt             input value of the counter of NG ie
#  @param Dbg            debug parameter for debug
#  @param soc               socket descriptor
#  @retval i_cnt            output value of the counter of NG ie
#  @retval d_rply_tlv       output data of reply TLV data to MC \n
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
def compare_ie_val(l_com_hdr_info, i_analyzemsg, l_ie_name_list,
                   d_ref_data, d_cap_ie, d_rply_tlv, i_cnt, Dbg, soc):

    l_tlv_list = []
    i_in_cnt = 0
    Dbg.log(COM_DEF.TRACE, "[S] compare_ie_val")

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
            Dbg.log(COM_DEF.TRACE,
                    "reference data is none... (%s)"
                    % (s_ie_name))
            continue
        # check l_ref_ie_val which is included in s_cap_ie_val
        elif l_ref_ie_val == l_cap_ie_val_result:
            s_check_result = \
                "Pass (%s) : [REF IE] %s [CAP IE] %s" % \
                (s_ie_name, s_ref_ie_val, s_cap_ie_val)
            snd_req_cmd(l_com_hdr_info, s_check_result, soc,
                        COM_DEF.i_MODULE_AIRCAP)
            Dbg.log(COM_DEF.INFO, s_check_result)
            continue
        else:
            # set NG result & reason
            s_check_result = \
                "NG (%s) : [REF IE] %s [CAP IE] %s" % \
                (s_ie_name, s_ref_ie_val, s_cap_ie_val)
            snd_req_cmd(l_com_hdr_info, s_check_result, soc,
                        COM_DEF.i_MODULE_AIRCAP)
            Dbg.log(COM_DEF.INFO, s_check_result)

            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkNg
            # add NG result to DataList
            d_list_tlv = OrderedDict()
            d_list_tlv["AnalyzeMsg"] = i_analyzemsg
            d_list_tlv["NgIeName"] = s_ie_name
            d_list_tlv["NgIeValueLen"] = len(s_cap_ie_val)
            d_list_tlv["NgIeValue"] = s_cap_ie_val
            d_list_tlv["NgReason"] = COM_DEF.i_IeNotMatch
            l_tlv_list.append(d_list_tlv)
            i_in_cnt += 1

    if i_in_cnt:
        d_rply_tlv["DataList"].extend(l_tlv_list)
        d_rply_tlv["NumOfNg"] = i_in_cnt + i_cnt
    else:
        pass

    # for loop end

    Dbg.log(COM_DEF.TRACE, "[E] compare_ie_val")

    return i_in_cnt + i_cnt, d_rply_tlv
