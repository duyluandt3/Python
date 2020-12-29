#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control Cisco AP.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import time
import json
import struct
import socket
import ipaddress
import netifaces as ni
import subprocess

from CLS_Define import COM_DEF
from tx_snd import cre_seq_list
from tx_snd import set_base_time
from tx_snd import snd_req_cmd
from Debug import Debug_GetObj
from CLS_Serial import COM_SERIAL
from netifaces import AF_INET

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##
# @brief Sets encode of TLV and common header, and transmits response command.
# @param l_com_hdr_info    command header parameter
# @param ser    communication port (class object)
# @param soc    socket object class (class object)
# @param s_snd_cmd    Send command
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
# @retval s_read_data : received data
def static_snd_rcv_cmd(l_com_hdr_info, ser, soc, s_snd_cmd):

    i_count = 0

    s_read_cmd = ""

    # Get debug info
    debug = Debug_GetObj(COM_DEF.i_MODULE_AP)

    debug.log(COM_DEF.TRACE, "[S] static_snd_rcv_cmd")

    # Send debug log
    snd_req_cmd(l_com_hdr_info, s_snd_cmd, soc, COM_DEF.i_MODULE_AP)

    ser.write(s_snd_cmd)

    if "show client summary" == s_snd_cmd:
        s_pattern = "Local"
        i_string_len = len(s_snd_cmd)
    elif "y" == s_snd_cmd or "logout" == s_snd_cmd:
        if COM_DEF.i_CMD_TestReady == l_com_hdr_info[0][2]:
            return COM_DEF.i_RET_SUCCESS, s_read_cmd
        else:
            s_pattern = s_snd_cmd
            i_string_len = len(s_snd_cmd)
    else:
        return COM_DEF.i_RET_SUCCESS, s_read_cmd

    while(i_count < 3):
        try:
            s_read_data = ser.read()
        except Exception as err_info:
            debug.log(COM_DEF.ERROR, err_info)
            debug.log(COM_DEF.ERROR, "failed to read")
            return COM_DEF.i_RET_SYSTEM_ERROR, ""

        if isinstance(s_read_data, str) and 0 < len(s_read_data):
            s_read_cmd += s_read_data

            debug.log(COM_DEF.DEBUG,
                      "rcv cmd : %s"
                      % (s_read_cmd))

            if i_string_len <= len(s_read_cmd):
                if s_pattern in s_read_cmd:
                    debug.log(COM_DEF.TRACE,
                              "[E] static_snd_rcv_cmd")
                    return COM_DEF.i_RET_SUCCESS, s_read_cmd
                else:
                    i_count += 1
            else:
                # wait next data
                i_count += 1
        else:
            i_count += 1
    # while end

    debug.error(COM_DEF.ERROR,
                "wait pattern : %s rcv cmd : %s"
                % (s_pattern, s_read_cmd))

    return COM_DEF.i_RET_SYSTEM_ERROR, ""


##
# @brief Define AP related processing.
class AP_FUNC():

    ##
    # @brief Run when instantiating the AP_FUNC class.
    # @param cls_soc    socket used for sending response command to
    #                   MC (class object)
    # @param s_host     MC IP Address
    # @retval None
    def __init__(self, cls_soc, s_host):

        # @cond
        # Get debug info
        self.Dbg = Debug_GetObj(COM_DEF.i_MODULE_AP)

        # read environment file
        env_file = "./device/AP/Cisco/vendor_param.json"
        fp = open(str(env_file), 'r')
        d_ap_data = json.load(fp)
        fp.close()

        self.s_ComPort = d_ap_data["ComPort"]
        self.i_Baudrate = d_ap_data["Baudrate"]
        self.s_User = d_ap_data["User"]
        self.s_Password = d_ap_data["Password"]
        self.s_ApName = d_ap_data["ApName"]
        self.s_controller_ip = d_ap_data["Controller_Ip"]
        self.soc = cls_soc
        self.i_module_type = COM_DEF.i_MODULE_AP
        self.b_com_flg = False
        self.i_channel = 0
        self.i_bandwidth = 0
        self.s_MC_IpAddr = s_host
        # @endcond

        cre_seq_list(COM_DEF.i_MODULE_AP)

    ##
    # @brief Log-in to AP and connect
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["User"] login user \n
    #                         ["Password"] password for login
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def attach(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] attach")

        # @cond
        # mandatory parameter
        if "Band" in d_tlv_param:
            i_band_type = d_tlv_param["Band"]
            if i_band_type == COM_DEF.i_BandType_24GHz or \
               i_band_type == COM_DEF.i_BandType_5GHz:
                i_dst_id = l_com_hdr_info[0][0]
                self.d_instance_info[i_dst_id]["Band"] = i_band_type
            else:
                pass
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "band parameter is not found")
            d_rply_tlv['Result'] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # mandatory parameter
        if "LogName" in d_tlv_param:
            self.Dbg.log(COM_DEF.INFO,
                         "related log name : %s" %
                         d_tlv_param["LogName"])
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "LogName parameter is not found")
            d_rply_tlv['Result'] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # @cond
        # option parameter
        if "User" in d_tlv_param:
            self.s_User = d_tlv_param["User"]
        else:
            pass

        # option parameter
        if "Password" in d_tlv_param:
            self.s_Password = d_tlv_param["Password"]
        else:
            pass

        if not self.b_com_flg:
            self.ser = COM_SERIAL(self.s_ComPort,
                                  self.i_Baudrate,
                                  self.s_User,
                                  self.s_Password,
                                  False,
                                  COM_DEF.i_MODULE_AP)
            self.b_com_flg = True
        else:
            pass

        # @endcond

        if not self.ser.comport.is_open:
            self.Dbg.log(COM_DEF.ERROR,
                         "failed to open com port")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = i_ret
        d_rply_tlv["IpAddress"] = self.s_controller_ip

        self.Dbg.log(COM_DEF.DEBUG, "[E] attach")

        return d_rply_tlv

    ##
    # @brief Perform time setting for AP
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

        self.Dbg.log(COM_DEF.DEBUG, "[S] date")

        # get date command paramter

        # mandatory parameter
        i_date = d_tlv_param["Date"]
        # mandatory parameter
        i_time = d_tlv_param["Time"]

        # option parameter
        if "Location" in d_tlv_param:
            i_location = d_tlv_param["Location"]
        else:
            self.Dbg.error("cisco ap must be Location parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # change date and time format
        i_year = (i_date >> 16) & 0x0000ffff
        i_offset_year = i_year - 2000
        i_mon = (i_date >> 8) & 0x000000ff
        i_day = i_date & 0x000000ff
        s_apdate = str(i_mon) + "/" + str(i_day) + "/" + str(i_offset_year)

        i_hour = (i_time >> 24) & 0x000000ff
        i_min = (i_time >> 16) & 0x000000ff
        i_sec = (i_time >> 8) & 0x000000ff
        s_aptime = str(i_hour) + ":" + str(i_min) + ":" + str(i_sec)

        # start to set ap settings

        # location
        s_snd_cmd = "config time timezone location " + str(i_location)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser, self.soc,
                                            s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # set time manual
        s_snd_cmd = "config time manual " + s_apdate + " " + s_aptime
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser, self.soc,
                                            s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

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
            s_date = str(i_year) + "/" + str(i_mon) + "/" + str(i_day)

            l_cmd_data = ["date", "-s", s_date + " " + s_aptime]
            snd_req_cmd(l_com_hdr_info, ' '.join(l_cmd_data), self.soc,
                        COM_DEF.i_MODULE_AP)
            self.Dbg.log(COM_DEF.INFO, ' '.join(l_cmd_data))

            try:
                i_ret = subprocess.call(l_cmd_data, shell=True)
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

        set_base_time(time.perf_counter(), COM_DEF.i_MODULE_AP)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] date")

        return d_rply_tlv

    ##
    # @brief Set ssid for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Ssid"] ssid of AP \n
    #                         ["WlanId"] WLAN identifier \n
    #                         ["ProfileName"] AP profile name
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ssid(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] ssid")

        # get ssid command paramter

        # mandatory parameter
        s_ssid = d_tlv_param["Ssid"]

        # option parameter
        if "WlanId" in d_tlv_param:
            i_wlanid = d_tlv_param["WlanId"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "WLAN ID  : %d" % i_wlanid)
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WlanId parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "ProfileName" in d_tlv_param:
            s_profilename = d_tlv_param["ProfileName"]
        else:
            s_profilename = s_ssid

        # create cisco instance
        s_snd_cmd = "config wlan create " + str(i_wlanid) + " " + \
            s_profilename + " " + s_ssid
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable cisco interface
        s_snd_cmd = "config wlan disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.11b wlan interface
        s_snd_cmd = "config 802.11b disable " + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.11a wlan interface
        s_snd_cmd = "config 802.11a disable " + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wpa security
        s_snd_cmd = "config wlan security wpa disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable cisco interface
        s_snd_cmd = "config wlan enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] ssid")

        return d_rply_tlv

    ##
    # @brief Set security OPEN for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["WlanId"] WLAN identifier \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def open(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] open")

        # get open command paramter

        # option parameter
        if "WlanId" in d_tlv_param:
            i_wlanid = d_tlv_param["WlanId"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "WLAN ID  : %d" % i_wlanid)
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WlanId parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "Channel" in d_tlv_param:
            i_channel = d_tlv_param["Channel"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "CHANNEL  : %d" % i_channel)
            if i_channel < 14:
                s_band = "802.11b"
            else:
                s_band = "802.11a"
        else:
            if 0 == self.i_channel:
                self.Dbg.log(COM_DEF.ERROR,
                             "cisco ap must be channel parameter")
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
            else:
                i_channel = self.i_channel

        # start to set ap settings

        # disable cisco interface
        s_snd_cmd = "config wlan disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.11a or b wlan interface
        s_snd_cmd = "config " + s_band + " disable " + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.1X security
        s_snd_cmd = "config wlan security 802.1X disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wep security
        s_snd_cmd = "config wlan security static-wep-key disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wpa security
        s_snd_cmd = "config wlan security wpa disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable cisco interface
        s_snd_cmd = "config wlan enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] open")

        return d_rply_tlv

    ##
    # @brief Set security WEP for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["AuthFlg"] authentication method \n
    #                         ["KeyIdx"] index of wep key \n
    #                         ["WepKey"] wep key \n
    #                         ["WlanId"] WLAN identifier \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] wep")

        # get wep command paramter

        # mandatory parameter
        if "AuthFlg" in d_tlv_param:
            i_AuthFlg = d_tlv_param["AuthFlg"]
            if COM_DEF.i_AuthFlg_Open == i_AuthFlg:
                s_authtype = "open"
            elif COM_DEF.i_AuthFlg_Shared == i_AuthFlg:
                s_authtype = "shared-key"
            else:
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be AuthFlg parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # mandatory parameter
        if "KeyIdx" in d_tlv_param:
            # the key index of cisco ap is started from "1".
            # this number means key index 0.
            i_keyidx = d_tlv_param["KeyIdx"] + 1
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be KeyIdx parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # mandatory parameter
        if "WepKey" in d_tlv_param:
            s_wepkey = d_tlv_param["WepKey"]
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WepKey parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        if COM_DEF.i_WepKey_Ascii64_Length == len(s_wepkey):
            s_strtype = "ascii"
            s_keybit = "40"
        elif COM_DEF.i_WepKey_Ascii128_Length == len(s_wepkey):
            s_strtype = "ascii"
            s_keybit = "104"
        elif COM_DEF.i_WepKey_Hex64_Length == len(s_wepkey):
            s_strtype = "hex"
            s_keybit = "40"
        elif COM_DEF.i_WepKey_Hex128_Length == len(s_wepkey):
            s_strtype = "hex"
            s_keybit = "104"
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "wepkey length error : %d"
                         % len(s_wepkey))
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "WlanId" in d_tlv_param:
            i_wlanid = d_tlv_param["WlanId"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "WLAN ID  : %d" % i_wlanid)
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WlanId parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "Channel" in d_tlv_param:
            i_channel = d_tlv_param["Channel"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "CHANNEL  : %d" % i_channel)
            if i_channel < 14:
                s_band = "802.11b"
            else:
                s_band = "802.11a"
        else:
            if 0 == self.i_channel:
                self.Dbg.log(COM_DEF.ERROR,
                             "cisco ap must be channel parameter")
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
            else:
                i_channel = self.i_channel

        # start to set ap settings

        # disable cisco interface
        s_snd_cmd = "config wlan disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.11a or b wlan interface
        s_snd_cmd = "config " + s_band + "disable" + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.1X security
        s_snd_cmd = "config wlan security 802.1X disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wpa security
        s_snd_cmd = "config wlan security wpa disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable wep security
        s_snd_cmd = "config wlan security static-wep-key enable " + \
                    str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # authentication type (open or shared)
        s_snd_cmd = "config wlan security static-wep-key authentication " \
            + s_authtype + " " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # wep key
        s_snd_cmd = "config wlan security static-wep-key encryption " + \
            str(i_wlanid) + " " + s_keybit + " " + s_strtype + " " + \
            s_wepkey + " " + str(i_keyidx)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable cisco interface
        s_snd_cmd = "config wlan enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] wep")

        return d_rply_tlv

    ##
    # @brief Set security WPA for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["KeyMgmt"] key management \n
    #                         ["WpaType"] wpa authentication method \n
    #                         ["WpaPairwise"] wpa pairwise \n
    #                         ["WpaPassphrase"] wpa passphrase \n
    #                         ["Pmf"] protected management frames \n
    #                         ["WlanId"] WLAN identifier \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wpa(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] wpa")

        # get wpa command paramter

        # option parameter
        if "KeyMgmt" in d_tlv_param:
            i_keymgmt = d_tlv_param["KeyMgmt"]
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be KeyMgmt parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "WpaType" in d_tlv_param:
            i_WpaType = d_tlv_param["WpaType"]
            if COM_DEF.i_WpaType_WPA == i_WpaType:
                s_wpa_status = "enable"
                s_wpa2_status = "disable"
            elif COM_DEF.i_WpaType_RSN == i_WpaType:
                s_wpa_status = "disable"
                s_wpa2_status = "enable"
            elif COM_DEF.i_WpaType_MIX == i_WpaType:
                s_wpa_status = "enable"
                s_wpa2_status = "enable"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "WpaType parameter error : %d"
                             % i_WpaType)
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WpaType parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "WpaPairwise" in d_tlv_param:
            i_WpaPairwise = d_tlv_param["WpaPairwise"]
            if COM_DEF.i_WpaPairwise_TKIP == i_WpaPairwise:
                s_wpa_status = "enable"
                s_wpa2_status = "disable"
            elif COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
                s_wpa_status = "disable"
                s_wpa2_status = "enable"
            elif COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
                s_wpa_status = "enable"
                s_wpa2_status = "enable"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "WpaPairwise parameter error : %d"
                             % i_WpaPairwise)
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WpaPairwise parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "WpaPassphrase" in d_tlv_param:
            s_wpapassphrase = d_tlv_param["WpaPassphrase"]
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WpaPassphrase parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "Pmf" in d_tlv_param:
            i_pmf = d_tlv_param["Pmf"]
        else:
            i_pmf = 0

        # option parameter
        if i_pmf != 0 and "PmfSettings" in d_tlv_param:
            i_pmf_settings = d_tlv_param["PmfSettings"]
        else:
            pass

        # option parameter
        if "WlanId" in d_tlv_param:
            i_wlanid = d_tlv_param["WlanId"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "WLAN ID  : %d" % i_wlanid)
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WlanId parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # option parameter
        if "Channel" in d_tlv_param:
            i_channel = d_tlv_param["Channel"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "CHANNEL  : %d" % i_channel)
            if i_channel < 14:
                s_band = "802.11b"
            else:
                s_band = "802.11a"
        else:
            if 0 == self.i_channel:
                self.Dbg.log(COM_DEF.ERROR,
                             "cisco ap must be channel parameter")
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
            else:
                i_channel = self.i_channel

        # start to set ap settings

        # disable cisco interface
        s_snd_cmd = "config wlan disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.11a or b wlan interface
        s_snd_cmd = "config " + s_band + " disable " + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.1X security
        s_snd_cmd = "config wlan security 802.1X disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable wpa security
        s_snd_cmd = "config wlan security wpa enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # wpa security
        s_snd_cmd = "config wlan security wpa wpa1 " + s_wpa_status + \
            " " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # rsn security
        s_snd_cmd = "config wlan security wpa wpa2 " + s_wpa2_status + \
            " " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wpa/tkip
        s_snd_cmd = "config wlan security wpa wpa1 ciphers tkip disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wpa/aes
        s_snd_cmd = "config wlan security wpa wpa1 ciphers aes  disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wpa2/tkip
        s_snd_cmd = "config wlan security wpa wpa2 ciphers tkip disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable wpa2/aes
        s_snd_cmd = "config wlan security wpa wpa2 ciphers aes  disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable wpa pairwise
        if COM_DEF.i_WpaPairwise_TKIP == i_WpaPairwise:
            if "enable" == s_wpa_status:
                s_snd_cmd = \
                    "config wlan security wpa wpa1 ciphers tkip enable " + \
                    str(i_wlanid)
                i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info,
                                                    self.ser, self.soc,
                                                    s_snd_cmd)
            else:
                pass
            if "enable" == s_wpa2_status:
                s_snd_cmd = \
                    "config wlan security wpa wpa2 ciphers tkip enable " + \
                    str(i_wlanid)
                i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                    self.soc, s_snd_cmd)
            else:
                pass
        elif COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
            if "enable" == s_wpa_status:
                s_snd_cmd = \
                    "config wlan security wpa wpa1 ciphers aes enable " + \
                    str(i_wlanid)
                i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                    self.soc, s_snd_cmd)
            else:
                pass
            if "enable" == s_wpa2_status:
                s_snd_cmd = \
                    "config wlan security wpa wpa2 ciphers aes enable " + \
                    str(i_wlanid)
                i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                    self.soc, s_snd_cmd)
            else:
                pass
        elif COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
            if "enable" == s_wpa_status:
                s_snd_cmd = \
                    "config wlan security wpa wpa1 ciphers tkip enable " + \
                    str(i_wlanid)
                i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                    self.soc, s_snd_cmd)
                if COM_DEF.i_RET_SUCCESS == i_ret:
                    s_snd_cmd = \
                        "config wlan security wpa wpa1 ciphers aes enable " + \
                        str(i_wlanid)
                    i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info,
                                                        self.ser, self.soc,
                                                        s_snd_cmd)
                else:
                    pass
            else:
                pass

                if "enable" == s_wpa2_status:
                    s_snd_cmd = \
                        "config wlan security wpa wpa2 ciphers tkip enable " \
                        + str(i_wlanid)
                    i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info,
                                                        self.ser, self.soc,
                                                        s_snd_cmd)
                    if COM_DEF.i_RET_SUCCESS == i_ret:
                        s_snd_cmd = \
                            "config wlan security wpa wpa1 ciphers aes enable "
                        s_snd_cmd += str(i_wlanid)
                        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info,
                                                            self.ser,
                                                            self.soc,
                                                            s_snd_cmd)
                    else:
                        pass
                else:
                    pass
        else:
            pass

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable key management 802.1x
        s_snd_cmd = "config wlan security wpa akm 802.1x disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable key management psk
        s_snd_cmd = "config wlan security wpa akm psk disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable key management cckm
        s_snd_cmd = "config wlan security wpa akm cckm disable " + \
                    str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        if COM_DEF.i_KeyMgmt_PSK == i_keymgmt:
            s_snd_cmd = "config wlan security wpa akm psk enable " + \
                str(i_wlanid)
            i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                self.soc, s_snd_cmd)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
                return d_rply_tlv
            else:
                pass

            if len(s_wpapassphrase) < COM_DEF.i_WpaPassphrase_Length_Max:
                s_snd_cmd = "config wlan security wpa akm psk set-key ascii " \
                    + s_wpapassphrase + " " + str(i_wlanid)
            else:
                s_snd_cmd = "config wlan security wpa akm psk set-key hex   " \
                    + s_wpapassphrase + " " + str(i_wlanid)

            i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                self.soc, s_snd_cmd)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
                return d_rply_tlv
            else:
                pass

        else:
            # i_KeyMgmt_EAP
            s_snd_cmd = "config wlan security wpa akm 802.1x enable " + \
                str(i_wlanid)
            i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                self.soc, s_snd_cmd)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
                return d_rply_tlv
            else:
                pass

        # disable protect management frame 802.1x key management
        s_snd_cmd = "config wlan security wpa akm pmf 802.1x disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable protect management frame psk key management
        s_snd_cmd = "config wlan security wpa akm pmf psk disable " + \
            str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable protect management frame
        s_snd_cmd = "config wlan security pmf disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        if 0 == i_pmf:
            self.Dbg.log(COM_DEF.DEBUG, "[AP CTRL] pmf off")
        else:
            if COM_DEF.i_KeyMgmt_PSK == i_keymgmt:
                s_snd_cmd = "config wlan security wpa akm pmf psk enable " + \
                    str(i_wlanid)
            else:
                s_snd_cmd = \
                    "config wlan security wpa akm pmf 802.1x enable " + \
                    str(i_wlanid)
            i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                self.soc, s_snd_cmd)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
                return d_rply_tlv
            else:
                pass

            if COM_DEF.i_KeyMgmt_PSK == i_keymgmt:
                s_snd_cmd = "config wlan security wpa akm psk disable " + \
                    str(i_wlanid)
            else:
                s_snd_cmd = \
                    "config wlan security wpa akm 802.1x disable " + \
                    str(i_wlanid)
            i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                self.soc, s_snd_cmd)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
                return d_rply_tlv
            else:
                pass

            if COM_DEF.i_PmfSettings_Disable == i_pmf_settings:
                s_snd_cmd = "config wlan security pmf disable " + \
                            str(i_wlanid)
            elif COM_DEF.i_PmfSettings_Enable == i_pmf_settings:
                s_snd_cmd = "config wlan security pmf optional " + \
                            str(i_wlanid)
            else:  # COM_DEF.i_PmfSettings_Required == pmfsetting:
                s_snd_cmd = "config wlan security pmf required " + \
                            str(i_wlanid)
            i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                self.soc, s_snd_cmd)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
                return d_rply_tlv
            else:
                pass

            if COM_DEF.i_KeyMgmt_PSK == i_keymgmt:
                s_snd_cmd = "config wlan security wpa akm psk enable " + \
                    str(i_wlanid)
            else:
                s_snd_cmd = \
                    "config wlan security wpa akm 802.1x enable " + \
                    str(i_wlanid)
            i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                                self.soc, s_snd_cmd)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
                return d_rply_tlv
            else:
                pass

        # enable cisco interface
        s_snd_cmd = "config wlan enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] wpa")

        return d_rply_tlv

    ##
    # @brief Set channel for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Channel"] AP channel \n
    #                         ["Bandwidth"] bandwidth of AP
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def channel(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] channel")

        # mandatory parameter
        self.i_channel = d_tlv_param["Channel"]
        if self.i_channel < 14:
            s_band = "802.11b"
        else:
            s_band = "802.11a"

        # mandatory parameter
        self.i_chanwidth = d_tlv_param["Bandwidth"]
        if COM_DEF.i_Bandwidth_20MHz == self.i_chanwidth:
            s_bandwidth = "20"
        elif COM_DEF.i_Bandwidth_40MHz == self.i_chanwidth:
            s_bandwidth = "40"
        elif COM_DEF.i_Bandwidth_80MHz == self.i_chanwidth:
            s_bandwidth = "80"
        elif COM_DEF.i_Bandwidth_80_80MHz == self.i_chanwidth:
            s_bandwidth = "80+80"
        elif COM_DEF.i_Bandwidth_160MHz == self.i_chanwidth:
            s_bandwidth = "160"
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "bandwidth parameter is abnormal")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        s_snd_cmd = "config " + s_band + " disable " + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config " + s_band + " chan_width " + self.s_ApName + \
            " " + s_bandwidth
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config " + s_band + " channel ap " + self.s_ApName + \
            " " + str(self.i_channel)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] channel")

        return d_rply_tlv

    ##
    # @brief Set country code for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["CountryCode"] country code \n
    #                         ["WlanId"] WLAN identifier
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def country(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] country")

        # mandatory parameter
        s_countrycode = d_tlv_param["CountryCode"]

        # option parameter
        if "WlanId" in d_tlv_param:
            i_wlanid = d_tlv_param["WlanId"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "WLAN ID  : %d" % i_wlanid)
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WlanId parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # disable cisco interface
        s_snd_cmd = "config wlan disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.1a interface
        s_snd_cmd = "config 802.11a disable network"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        time.sleep(1)

        s_snd_cmd = "y"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # disable 802.1b interface
        s_snd_cmd = "config 802.11b disable network"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        time.sleep(1)

        s_snd_cmd = "y"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # country code
        s_snd_cmd = "config country " + s_countrycode
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        time.sleep(1)

        s_snd_cmd = "y"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable 802.1a interface
        s_snd_cmd = "config 802.11a enable network"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable 802.1b interface
        s_snd_cmd = "config 802.11b enable network"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable cisco interface
        s_snd_cmd = "config wlan enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] country")

        return d_rply_tlv

    ##
    # @brief Set up stealth for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["WlanId"] WLAN identifier \n
    #                         ["OnOffFlag"] stealth enable/disable flag \n
    #                           - 0 : stealth disable \n
    #                           - 1 : stealth enable
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def stealth(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] stealth")

        # mandatory parameter
        i_onoff_flg = d_tlv_param["OnOffFlag"]

        # option parameter
        if "WlanId" in d_tlv_param:
            i_wlanid = d_tlv_param["WlanId"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "WLAN ID  : %d" % i_wlanid)
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WlanId parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # disable cisco interface
        s_snd_cmd = "config wlan disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        if 1 == i_onoff_flg:
            s_snd_cmd = "config wlan broadcast-ssid disable " + str(i_wlanid)
        else:  # 0 == i_onoff_flg:
            s_snd_cmd = "config wlan broadcast-ssid enable  " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable cisco interface
        s_snd_cmd = "config wlan enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] stealth")

        return d_rply_tlv

    ##
    # @brief Enable/disable wireless output for AP.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def controlbss(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] controlbss")

        # mandatory parameter
        i_onoff_flg = d_tlv_param["OnOffFlag"]

        # option parameter
        if "Channel" in d_tlv_param:
            i_channel = d_tlv_param["Channel"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "CHANNEL  : %d" % i_channel)
            if i_channel < 14:
                s_band = "802.11b"
            else:
                s_band = "802.11a"
        else:
            if 0 == self.i_channel:
                self.Dbg.log(COM_DEF.ERROR,
                             "cisco ap must be channel parameter")
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
            else:
                i_channel = self.i_channel

        # guarantee to ready radio
        time.sleep(3)

        if 0 == i_onoff_flg:
            s_snd_cmd = "config " + s_band + " disable " + self.s_ApName
        else:  # 1 == i_onoff_flg:
            s_snd_cmd = "config " + s_band + " enable " + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # guarantee to up radio
        if i_channel < 52:
            time.sleep(5)
        else:
            time.sleep(60)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] controlbss")

        return d_rply_tlv

    ##
    # @brief Return BSSID of connected STA.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def stalist(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] stalist")

        s_snd_cmd = "show client summary"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

#        snd_req_cmd(l_com_hdr_info, rcv_str, self.soc, COM_DEF.i_MODULE_AP)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        # analyzing command string
        rcv_str = rcv_str.replace('\n', ' ')
        l_rcv_data_list = rcv_str.split(" ")
        self.Dbg.log(COM_DEF.DEBUG,
                     ' '.join(l_rcv_data_list))
        i_cnt = 0
        s_macddr_list = []
        for s_data in l_rcv_data_list:
            if ":" in s_data:
                s_macddr_list.append(s_data)
            else:
                pass
            i_cnt += 1
        # for loop end

        i_cnt = 0
        l_macAddr = []
        for s_mac in s_macddr_list:
            d_list_tlv = {}
            d_list_tlv["MacAddress"] = s_mac
            l_macAddr.append(d_list_tlv)
            i_cnt += 1
        # for loop end

        d_rply_tlv["NumOfSta"] = i_cnt
        d_rply_tlv["DataList"] = l_macAddr

        self.Dbg.log(COM_DEF.DEBUG, "[E] stalist")

        return d_rply_tlv

    ##
    # @brief control to set up connection restrictions
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def limit(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}

        self.Dbg.log(COM_DEF.DEBUG, "[S] limit")

        s_func_str = "limit command is not supported. !!"
        self.Dbg.log(COM_DEF.ERROR, (s_func_str))
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc,
                    COM_DEF.i_MODULE_AP)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR

        self.Dbg.log(COM_DEF.DEBUG, "[E] limit")

        return d_rply_tlv

    ##
    # @brief control to enable or disable 11n
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Channel"] AP channel \n
    #                         ["OnOffFlag"] 11n enable/disable flag \n
    #                           - 0 : 11n disable \n
    #                           - 1 : 11n enable
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def control11n(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] control11n")

        # mandatory parameter
        i_onoff_flg = d_tlv_param["OnOffFlag"]

        # mandatory parameter
        if "Channel" in d_tlv_param:
            i_channel = d_tlv_param["Channel"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "CHANNEL  : %d" % i_channel)
            if i_channel < 14:
                s_band = "802.11b"
            else:
                s_band = "802.11a"
        else:
            if 0 == self.i_channel:
                self.Dbg.log(COM_DEF.ERROR,
                             "cisco ap must be channel parameter")
                d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
                return d_rply_tlv
            else:
                i_channel = self.i_channel

        # disable 802.11a/b network
        s_snd_cmd = "config " + s_band + " disable network"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        if 0 == i_onoff_flg:
            s_snd_cmd = "config " + s_band + " 11nSupport disable"
        else:  # 1 == i_onoff_flg:
            s_snd_cmd = "config " + s_band + " 11nSupport enable"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        # enable 802.11a/b network
        s_snd_cmd = "config " + s_band + " enable network"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] control11n")

        return d_rply_tlv

    ##
    # @brief Detach processing of AP control.
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["WlanId"] WLAN identifier
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def detach(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}

        self.Dbg.log(COM_DEF.DEBUG, "[S] detach")

        driver = Firefox()
        self.Dbg.log(COM_DEF.DEBUG, "Open Firefox")

        # get web page
        driver.get(
            'http://admin:a1B2c3@192.168.0.25/screens/apf/wlan_list.html')

        # select remove menu
        xpath_string = "//select[@name='wlanaction']"
        s_select_val = "removeall"

        try:
            element = WebDriverWait(driver, 10).until(
                          EC.presence_of_element_located(
                              (By.XPATH, xpath_string)))
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "Set XPATH : %s" %
                         (xpath_string))
            self.Dbg.log(COM_DEF.ERROR, err_info)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            driver.quit()
            return d_rply_tlv

        self.Dbg.log(COM_DEF.TRACE, "select to remove all")
        select = Select(element)
        select.select_by_value(s_select_val)

        # select delete checkbox (fixed number 9 and only 1 checkbox)
        xpath_string = \
            "//td[@class='listNoPad']/input[@id='wlan_sel' \
            and @name='1.0.1.wlan_sel']"

        try:
            element = WebDriverWait(driver, 10).until(
                          EC.presence_of_element_located(
                              (By.XPATH, xpath_string)))
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "Set XPATH : %s" %
                         (xpath_string))
            self.Dbg.log(COM_DEF.ERROR, err_info)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            driver.quit()
            return d_rply_tlv

        self.Dbg.log(COM_DEF.TRACE, "delete...")
        element.click()

        self.Dbg.log(COM_DEF.TRACE, "select save button")
        xpath_string = "//input[@class='buttonstretch' and @value=' Go ']"

        try:
            element = WebDriverWait(driver, 10).until(
                          EC.presence_of_element_located(
                              (By.XPATH, xpath_string)))
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "Set XPATH : %s" %
                         (xpath_string))
            self.Dbg.log(COM_DEF.ERROR, err_info)
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            driver.quit()
            return d_rply_tlv

        self.Dbg.log(COM_DEF.TRACE, "save...")
        element.click()

        self.Dbg.log(COM_DEF.TRACE, "accept popup")
        # accept popup menu
        try:
            alert = driver.switch_to_alert()
            alert.accept()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, err_info)
            self.Dbg.error("failed to switch alert box")
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            driver.quit()
            return d_rply_tlv

        self.Dbg.log(COM_DEF.INFO, "release driver")
        driver.quit()
        self.Dbg.log(COM_DEF.INFO, "detach serial")
        self.ser.detach()

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        # @cond
        self.b_com_flg = False
        # @endcond

        self.Dbg.log(COM_DEF.DEBUG, "[E] detach")

        return d_rply_tlv

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

        self.Dbg.log(COM_DEF.DEBUG, "[S] test_ready")

        # get node id
        i_dst_id = l_com_hdr_info[0][0]
        i_node_id = (i_dst_id & COM_DEF.i_NODEID_MASK) >> 8
        self.Dbg.log(COM_DEF.DEBUG,
                     "NODE ID : 0x%02x" % (i_node_id))

        # node id check
        if i_node_id < COM_DEF.i_NODE_AIRCAP_START or \
                COM_DEF.i_NODE_AIRCAP_END < i_node_id:
            self.Dbg.log(COM_DEF.ERROR,
                         "node id error [0x%04x]"
                         % (i_dst_id))
            d_rply_tlv["Result"] = COM_DEF.i_RET_NODE_CHK_ERROR
        else:
            # attch command
            d_rply_tlv = self.attach(l_com_hdr_info, d_tlv_param)

        self.Dbg.log(COM_DEF.DEBUG, "[E] test_ready")

        return d_rply_tlv

    ##
    # @brief DHCP server Enable
    #        Enable CISCO controller DHCP server
    #        Configure Cisco AP to refer to controller DHCP server
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["WlanId"] WLAN identifier \n
    #                         ["IpAddress"] Payout Start IPAddress \n
    #                         ["NetMask"] Netmask \n
    #                         ["GateWay"] Gateway \n
    #                         ["AssignNum"] IPAddress Payout Count \n
    #                         ["LeaseTime"] Lease Time
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def dhcpd(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] dhcpd")

        # option parameter
        if "WlanId" in d_tlv_param:
            i_wlanid = d_tlv_param["WlanId"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "WLAN ID  : %d" % i_wlanid)
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "cisco ap must be WlanId parameter")
            d_rply_tlv["Result"] = COM_DEF.i_RET_TLV_ABNORMAL
            return d_rply_tlv

        # set parameter
        s_start_ip = d_tlv_param["IpAddress"]
        s_netmask = d_tlv_param["NetMask"]
        s_gateway = d_tlv_param["GateWay"]
        i_assign_num = d_tlv_param["AssignNum"]
        i_lease = d_tlv_param["LeaseTime"]

        s_snd_cmd = "config dhcp disable cisco_controller_dhcp"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config dhcp delete-scope cisco_controller_dhcp"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config dhcp create-scope cisco_controller_dhcp"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config dhcp disable cisco_controller_dhcp"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        try:
            i_prefix = bin(struct.unpack('!L', socket.inet_pton(
                                         socket.AF_INET,
                                         s_netmask))[0])[2:].index('0')
            i_available_num = 2**(32 - i_prefix) - 1

        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "NetMask format error (" +
                         str(err_info) + ")")
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv

        try:
            # create network address
            s_ipaddr = s_start_ip + "/" + str(i_prefix)
            s_netaddr = str(ipaddress.IPv4Network(s_ipaddr, False))
            s_netaddr = s_netaddr.rstrip("/" + str(i_prefix))

            s_max_Ip = ipaddress.IPv4Address(s_netaddr) + i_available_num

            i_available_num = int(s_max_Ip) - int(ipaddress.IPv4Address(
                              s_start_ip))

            if i_available_num >= i_assign_num:
                s_end_Ip = str(ipaddress.IPv4Address(s_start_ip) +
                               i_assign_num)
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "Exceeded IPAddress setting range")
                d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                return d_rply_tlv

        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "Start IpAddress format error (" +
                         str(err_info) + ")")
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv

        s_snd_cmd = "config dhcp address-pool cisco_controller_dhcp " \
                    + s_start_ip + " " + s_end_Ip
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config dhcp network cisco_controller_dhcp " + s_netaddr \
                    + " " + s_netmask
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config dhcp default-router cisco_controller_dhcp " \
                    + s_gateway
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config dhcp lease cisco_controller_dhcp " + str(i_lease)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config dhcp enable cisco_controller_dhcp"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config wlan disable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config wlan dhcp_server " + str(i_wlanid) + " " \
                    + self.s_controller_ip
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        s_snd_cmd = "config wlan enable " + str(i_wlanid)
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS != i_ret:
            d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
            return d_rply_tlv
        else:
            pass

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] dhcpd")

        return d_rply_tlv

    ##
    # @brief Set IpAddress is Cisco AP
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    #                         ["IpAddress"] IpAddress \n
    #                         ["NetMask"] Netmask \n
    #                         ["GateWay"] Gateway
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def setipinfo(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[S] setipinfo")

        s_ip = d_tlv_param["IpAddress"]
        s_netmask = d_tlv_param["NetMask"]
        s_gateway = d_tlv_param["GateWay"]

        s_snd_cmd = "config ap static-IP enable " + self.s_ApName + " " + \
                    s_ip + " " + s_netmask + " " + s_gateway

        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS == i_ret:
            pass
        else:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv

        s_snd_cmd = "y"
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS == i_ret:
            pass
        else:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv

        s_snd_cmd = "show ap config 802.11a " + self.s_ApName
        i_ret, rcv_str = static_snd_rcv_cmd(l_com_hdr_info, self.ser,
                                            self.soc, s_snd_cmd)

        if COM_DEF.i_RET_SUCCESS == i_ret:
            pass
        else:
            d_rply_tlv["Result"] = COM_DEF.i_RET_WLAN_ERROR
            return d_rply_tlv

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "[E] setipinfo")

        return d_rply_tlv

    ##
    # @brief Get the IpAddress of Cisco AP
    # @param l_com_hdr_info    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def getipinfo(self, l_com_hdr_info, d_tlv_param):

        d_rply_tlv = {}

        self.Dbg.log(COM_DEF.DEBUG, "[S] getipinfo")

        s_func_str = "getipinfo command is not supported"
        self.Dbg.log(COM_DEF.DEBUG, s_func_str)
        snd_req_cmd(l_com_hdr_info, s_func_str, self.soc, COM_DEF.i_MODULE_AP)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SYSTEM_ERROR

        self.Dbg.log(COM_DEF.DEBUG, "[E] getipinfo")

        return d_rply_tlv
