#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control common procedure
# @author E2N3
# @date 2019.05.28

# -*- coding: utf-8 -*-

import time
import json
import sys
import subprocess
import netifaces as ni

from CLS_Define import COM_DEF
from tx_snd import cre_seq_list
from tx_snd import set_base_time
from Debug import Debug_GetObj
from netifaces import AF_INET


##
# @brief Define AP related processing.
class AP_ENV():

    def __init__(self, s_model_name):
        # @cond
        # Get debug info
        self.Dbg = Debug_GetObj(COM_DEF.i_MODULE_AP)

        device_path = "./device/AP/Selenium/" + s_model_name
        sys.path.append(device_path)
        fp = open((device_path + "/vendor_param.json"), 'r')
        d_ap_data = json.load(fp)
        # parameter
        self.d_instance_info = {}
        self.i_wait_time = 20
        self.s_AP_IpAddr = d_ap_data["AP_IpAddr"]
        self.s_DriverMode = d_ap_data["WebDriverMode"]
        self.s_User = d_ap_data["User"]
        self.s_Password = d_ap_data["Password"]
        fp.close()
        self.i_module_type = COM_DEF.i_MODULE_AP


##
# @brief Define AP related processing.
class AP_FUNC(AP_ENV):

    ##
    # @brief Run when instantiating the AP_FUNC class.
    # @param cls_soc    socket used for sending response command to \n
    #                   MC (class object)
    # @param s_host     MC IP Address
    # @param s_model_name  AP model name. (AP folder name)
    # @retval None
    def __init__(self, cls_soc, s_host, s_model_name):
        super().__init__(s_model_name)

        # @cond
        # create class
        from CLS_Debug import CTRL_DBG
        from CLS_Vendor import CTRL_VENDOR
        self.s_MC_IpAddr = s_host
        self.dbg = CTRL_DBG(cls_soc, self.Dbg)
        self.vndr_func = CTRL_VENDOR(self.dbg, s_model_name)
        # @endcond

        cre_seq_list(COM_DEF.i_MODULE_AP)

    ##
    # @brief get frequency info from d_instance_info
    # @param i_dst_id    key parameter
    # @retval s_freq_param    - Success : "2.4GHz" or "5GHz" \n
    #                           Failure : ""
    def get_freq_info(self, i_dst_id):

        if i_dst_id in self.d_instance_info:
            if "Band" in self.d_instance_info[i_dst_id]:
                if COM_DEF.i_BandType_24GHz == \
                   self.d_instance_info[i_dst_id]["Band"]:
                    s_freq_param = "2.4GHz"
                else:
                    s_freq_param = "5GHz"
            else:
                s_freq_param = ""
        else:
            s_freq_param = ""

        return s_freq_param

    ##
    # @brief Log-in to AP and connect
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["User"] login user \n
    #                         ["Password"] password for login
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def attach(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        i_freq_cnt = 0

        self.Dbg.log(COM_DEF.TRACE, "[S] attach")

        i_dst_id = l_com_hdr[0][0]
        if (0 == (i_dst_id & COM_DEF.i_INSTANCEID_MASK) or
           i_dst_id in self.d_instance_info):
            pass
        else:
            self.d_instance_info[i_dst_id] = {}

        # @cond
        # mandatory parameter
        if "Band" in d_tlv_param:
            i_band_type = d_tlv_param["Band"]
            if i_band_type == COM_DEF.i_BandType_24GHz or \
               i_band_type == COM_DEF.i_BandType_5GHz:

                self.d_instance_info[i_dst_id]["Band"] = i_band_type
            else:
                pass
        else:
            s_dbg_str = "band parameter is not found"
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)

        # mandatory parameter
        if "LogName" in d_tlv_param:
            self.Dbg.log(COM_DEF.INFO,
                         "related log name : %s" %
                         d_tlv_param["LogName"])
        else:
            s_dbg_str = "LogName parameter is not found"
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)

        # option parameter
        if "User" in d_tlv_param:
            self.s_User = d_tlv_param["User"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "USER         : " + self.s_User)
        else:
            pass

        # option parameter
        if "Password" in d_tlv_param:
            self.s_Password = d_tlv_param["Password"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "PASSWORD     : " + self.s_Password)
        else:
            pass

        # selenium webdriver
        i_ret = self.vndr_func.start_webdriver("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to start web driver"
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # Get page information
        getPageString = self.vndr_func.radio_update_page
        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # radio off (2.4GHz/5GHz)
        while i_freq_cnt < 2:
            if i_freq_cnt == 0:
                s_freq_param = "2.4GHz"
            else:
                s_freq_param = "5GHz"

            # select frequency
            i_ret = self.vndr_func.select_freq("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to select frequency : " + \
                            s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # 802.11n enabled
            i_ret = self.vndr_func.ieee80211n("UPDATE",
                                              self.i_wait_time,
                                              l_com_hdr,
                                              1)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to enable 802.11n"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # radio off
            i_ret = self.vndr_func.radio("UPDATE",
                                         self.i_wait_time,
                                         l_com_hdr,
                                         0)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "can't control radio off"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if COM_DEF.i_RET_SUCCESS < i_ret:

                # save page
                i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                # check to update
                i_ret = self.vndr_func.select_freq("CHECK",
                                                   self.i_wait_time,
                                                   l_com_hdr,
                                                   s_freq_param)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update frequency : " + \
                                    s_freq_param
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                i_ret = self.vndr_func.radio("CHECK",
                                             self.i_wait_time,
                                             l_com_hdr,
                                             0)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update radio status (" + \
                                str(i_ret) + ")"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                if i_freq_cnt < 1:

                    # refresh page : press F5
                    self.Dbg.log(COM_DEF.DEBUG, "refresh")
                    i_ret = self.vndr_func.refresh(self.i_wait_time, l_com_hdr)
                    if COM_DEF.i_RET_SUCCESS > i_ret:
                        s_dbg_str = "failed to refresh (" + \
                                    str(i_ret) + ")"
                        return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                    else:
                        pass
                else:
                    pass
            else:
                s_dbg_str = "already radio off : " + s_freq_param
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)

            i_freq_cnt += 1
        # while loop end

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] attach")

        return d_rply_tlv

    ##
    # @brief Perform time setting for AP
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Date"] year, month, day \n
    #                         ["Time"] hours, minutes, and seconds
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def date(self, l_com_hdr, d_tlv_param):

        global CLS_BASE_TIME
        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        b_date_command_skip = False

        self.Dbg.log(COM_DEF.TRACE, "[S] date")

        self.Dbg.log(COM_DEF.DEBUG,
                     "MC Ip : %s"
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

            # @cond
            # mandatory parameter
            i_date = d_tlv_param["Date"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "DATE         : " + str(i_date))

            # mandatory parameter
            i_time = d_tlv_param["Time"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "TIME         : " + str(i_date))

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
            self.Dbg.log(COM_DEF.INFO, date_string)

            try:
                i_ret = subprocess.call(date_string, shell=True)
            except Exception as err_info:
                s_dbg_str = str(err_info)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)

            if COM_DEF.i_RET_SUCCESS != i_ret:
                s_dbg_str = "date command fail"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass
        # end if

        set_base_time(time.perf_counter(), COM_DEF.i_MODULE_AP)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] date")

        return d_rply_tlv

    ##
    # @brief Set ssid for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Ssid"] ssid of AP
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ssid(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        # Get parameter
        self.Dbg.log(COM_DEF.TRACE, "[S] ssid")

        # mandatory parameter
        s_ssid = d_tlv_param["Ssid"]
        i_ssid_len = len(s_ssid)
        self.Dbg.log(COM_DEF.DEBUG,
                     "SSID         : %s (len=%d)" %
                     (s_ssid, i_ssid_len))

        if i_ssid_len < COM_DEF.i_Ssid_Length_Min or \
                COM_DEF.i_Ssid_Length_Max < i_ssid_len:
            s_dbg_str = "ssid parameter is abnormal : " + \
                        "%s (len=%d)" % (s_ssid, len(s_ssid))
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            pass

        i_update_enable = 1
        l_freq_list = [ "2.4GHz",  "5GHz" ]
        for s_freq_param in l_freq_list:

            # Get page information
            getPageString = self.vndr_func.ssid_update_page
            i_ret = self.vndr_func.setPage(getPageString)
            if (i_ret):
                s_dbg_str = "failed to get web page : " + getPageString
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # select frequency
            i_ret = self.vndr_func.select_freq("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to select frequency : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            elif i_update_enable < i_ret:
                # SSID parameters are commonly managed in 2G and 5G.
                skip_5g_flg = 1
            else:
                skip_5g_flg = 0

            i_ret = self.vndr_func.ssid("UPDATE",
                                        self.i_wait_time,
                                        l_com_hdr,
                                        s_ssid)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to set ssid : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if COM_DEF.i_RET_SUCCESS < i_ret:

                # save page
                i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                # check to update
                i_ret = self.vndr_func.select_freq("CHECK",
                                                   self.i_wait_time,
                                                   l_com_hdr,
                                                   s_freq_param)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update frequency : " + \
                                s_freq_param
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                i_ret = self.vndr_func.ssid("CHECK",
                                            self.i_wait_time,
                                            l_com_hdr,
                                            s_ssid)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to get ssid : " + s_ssid
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass
            else:
                s_dbg_str = "Update data is none..."
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)

            if skip_5g_flg:
                self.Dbg.log(COM_DEF.DEBUG, "skip next component...")
                break
            else:
                pass

        # loop for 2.4G/5G component access

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] ssid")

        return d_rply_tlv

    ##
    # @brief Set security OPEN for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
    def open(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] open")

        i_update_enable = 1
        l_freq_list = [ "2.4GHz",  "5GHz" ]
        for s_freq_param in l_freq_list:

            # Get page information
            getPageString = self.vndr_func.ieee80211n_update_page
            i_ret = self.vndr_func.setPage(getPageString)
            if (i_ret):
                s_dbg_str = "failed to get web page : " + getPageString
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # select frequency
            i_ret = self.vndr_func.select_freq("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to select frequency : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            elif i_update_enable < i_ret:
                # SSID parameters are commonly managed in 2G and 5G.
                skip_5g_flg = 1
            else:
                skip_5g_flg = 0

            # wireless mode
            i_onoff_flg = 1
            i_ret = self.vndr_func.ieee80211n("UPDATE",
                                              self.i_wait_time,
                                              l_com_hdr,
                                              i_onoff_flg)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to set 11n mode : " + str(i_onoff_flg)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if COM_DEF.i_RET_SUCCESS < i_ret:

                # save page
                i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass
            else:
                pass

            # Get page information
            getPageString = self.vndr_func.security_update_page
            i_ret = self.vndr_func.setPage(getPageString)
            if (i_ret):
                s_dbg_str = "failed to get web page : " + getPageString
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # Set open security
            i_ret = self.vndr_func.open_security("UPDATE",
                                                 l_com_hdr,
                                                 self.i_wait_time)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to set security open : " + \
                            str(i_ret)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if COM_DEF.i_RET_SUCCESS < i_ret:

                # save page
                i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                # check to update
                i_ret = self.vndr_func.select_freq("CHECK",
                                                   self.i_wait_time,
                                                   l_com_hdr,
                                                   s_freq_param)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update frequency : " + s_freq_param
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                i_ret = self.vndr_func.open_security("CHECK",
                                                     l_com_hdr,
                                                     self.i_wait_time)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to check security open"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass
            else:
                s_dbg_str = "Update data is none..."
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)

            if skip_5g_flg:
                self.Dbg.log(COM_DEF.DEBUG, "skip next component...")
                break
            else:
                pass

        # loop for 2.4G/5G component access

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] open")

        return d_rply_tlv

    ##
    # @brief Set security WEP for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["AuthFlg"] authentication method \n
    #                         ["KeyIdx"] index of wep key \n
    #                         ["WepKey"] wep key \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] wep")

        # authentication method
        i_authFlg = d_tlv_param["AuthFlg"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "AUTH FLG     : " + str(i_authFlg))

        if i_authFlg < COM_DEF.i_AuthFlg_Open or \
                COM_DEF.i_AuthFlg_RangeErr <= i_authFlg:
            s_dbg_str = "AuthFlg parameter is abnormal : " \
                        + str(i_authFlg)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            pass

        # key index
        i_keyidx = d_tlv_param["KeyIdx"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "KEY INDEX    : " + str(i_keyidx))

        if i_keyidx < COM_DEF.i_KeyIdx_MIN or \
                COM_DEF.i_KeyIdx_MAX < i_keyidx:
            s_dbg_str = "KeyIdx parameter is abnormal : " \
                        + str(i_keyidx)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            pass

        # wep key
        s_wepkey = d_tlv_param["WepKey"]
        i_wepkey_len = len(s_wepkey)
        self.Dbg.log(COM_DEF.DEBUG,
                     "WEP KEY      : %s (len=%d)" %
                     (s_wepkey, i_wepkey_len))

        if COM_DEF.i_WepKey_Hex64_Length == i_wepkey_len or \
                COM_DEF.i_WepKey_Hex128_Length == i_wepkey_len or \
                COM_DEF.i_WepKey_Ascii64_Length == i_wepkey_len or \
                COM_DEF.i_WepKey_Ascii128_Length == i_wepkey_len:
            pass
        else:
            s_dbg_str = "WepKey parameter is abnormal : " \
                        + s_wepkey
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)

        i_update_enable = 1
        l_freq_list = [ "2.4GHz",  "5GHz" ]
        for s_freq_param in l_freq_list:

            # Get page information
            getPageString = self.vndr_func.ieee80211n_update_page
            i_ret = self.vndr_func.setPage(getPageString)
            if (i_ret):
                s_dbg_str = "failed to get web page : " + getPageString
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # select frequency
            i_ret = self.vndr_func.select_freq("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to select frequency : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            elif i_update_enable < i_ret:
                # SSID parameters are commonly managed in 2G and 5G.
                skip_5g_flg = 1
            else:
                skip_5g_flg = 0

            # wireless mode
            i_onoff_flg = 0
            i_ret = self.vndr_func.ieee80211n("UPDATE",
                                              self.i_wait_time,
                                              l_com_hdr,
                                              i_onoff_flg)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to set 11n mode : " + str(i_onoff_flg)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if i_ret:
                i_ret = self.vndr_func.submit_page(self.i_wait_time,
                                                   l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass
            else:
                pass

            # Get page information
            getPageString = self.vndr_func.security_update_page
            i_ret = self.vndr_func.setPage(getPageString)
            if (i_ret):
                s_dbg_str = "failed to get web page : " + getPageString
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # set wep security
            i_ret = self.vndr_func.wep_security("UPDATE",
                                                self.i_wait_time,
                                                l_com_hdr,
                                                i_authFlg,
                                                i_keyidx,
                                                s_wepkey)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to set security wep"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if i_ret:

                # save page
                i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                # check to update
                i_ret = self.vndr_func.select_freq("CHECK",
                                                   self.i_wait_time,
                                                   l_com_hdr,
                                                   s_freq_param)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update frequency : " + s_freq_param
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                i_ret = self.vndr_func.wep_security("CHECK",
                                                    self.i_wait_time,
                                                    l_com_hdr,
                                                    i_authFlg,
                                                    i_keyidx,
                                                    s_wepkey)

                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to check security wep"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass
            elif i_ret < COM_DEF.i_RET_SUCCESS:
                s_dbg_str = "wep security parameter error"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                s_dbg_str = "Update data is none..."
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)

            if skip_5g_flg:
                self.Dbg.log(COM_DEF.DEBUG, "skip next component...")
                break
            else:
                pass

        # loop for 2.4G/5G component access

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] wep")

        return d_rply_tlv

    ##
    # @brief Set security WPA for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["KeyMgmt"] key management \n
    #                         ["WpaType"] wpa authentication method \n
    #                         ["WpaPairwise"] wpa pairwise \n
    #                         ["WpaPassphrase"] wpa passphrase \n
    #                         ["Pmf"] protected management frames \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wpa(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        i_pmf_settings = 0
        s_psk = ''
        s_sae_pwd = ''

        self.Dbg.log(COM_DEF.TRACE, "[S] wpa")

        # mandatory parameter
        i_WpaType = d_tlv_param["WpaType"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "WPA TYPE     : " + str(i_WpaType))

        if i_WpaType < COM_DEF.i_WpaType_WPA or \
                COM_DEF.i_WpaType_RangeErr <= i_WpaType:
            s_dbg_str = "WpaType parameter is abnormal : " \
                        + str(i_WpaType)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            pass

        # mandatory parameter
        i_WpaPairwise = d_tlv_param["WpaPairwise"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "WPA PAIRWISE : " + str(i_WpaPairwise))

        if i_WpaPairwise < COM_DEF.i_WpaPairwise_TKIP or \
                COM_DEF.i_WpaPairwise_RangeErr <= i_WpaPairwise:
            s_dbg_str = "WpaPairwise parameter is abnormal : " \
                        + str(i_WpaPairwise)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            pass

        # mandatory parameter
        i_keymgmt = d_tlv_param["KeyMgmt"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "KEYMGMT      : " + str(i_keymgmt))

        if i_keymgmt < COM_DEF.i_KeyMgmt_PSK or \
                COM_DEF.i_KeyMgmt_RangeErr <= i_keymgmt:
            s_dbg_str = "KeyMgmt parameter is abnormal : " \
                        + str(i_keymgmt)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            pass

        # optional parameter
        if "WpaPassphrase" in d_tlv_param:
            s_psk = d_tlv_param["WpaPassphrase"]
            i_psk_len = len(s_psk)
            self.Dbg.log(COM_DEF.DEBUG,
                         "PASSPHRASE    : %s (len=%d)" %
                         (s_psk, i_psk_len))

            if i_psk_len < COM_DEF.i_WpaPassphrase_Length_Min or \
                    COM_DEF.i_WpaPassphrase_Length_Max < i_psk_len:
                s_dbg_str = "PassPhrase parameter is abnormal : " + \
                            "%s (len=%d)" % (s_psk, i_psk_len)
                return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                           COM_DEF.i_RET_TLV_ABNORMAL)
            else:
                pass
        else:
            pass

        # optional parameter
        if "SaePassword" in d_tlv_param:
            s_sae_pwd = d_tlv_param["SaePassword"]
            i_sae_len = len(s_sae_pwd)
            self.Dbg.log(COM_DEF.DEBUG,
                         "SAE PASSWORD  : %s (len=%d)" %
                         (s_sae_pwd, i_sae_len))
        else:
            pass

        # option parameter
        if "Pmf" in d_tlv_param:
            i_pmf = d_tlv_param["Pmf"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "PMF          : " + str(i_pmf))

            if COM_DEF.i_Pmf_Disabled == i_pmf or \
                    COM_DEF.i_Pmf_Enabled == i_pmf:
                pass
            else:
                s_dbg_str = "Pmf parameter is abnormal : " \
                            + str(i_pmf)
                return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                           COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            i_pmf = 0

        # option parameter
        if COM_DEF.i_Pmf_Enabled == i_pmf and "PmfSettings" in d_tlv_param:
            i_pmf_settings = d_tlv_param["PmfSettings"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "PMF SETTINGS : " + str(i_pmf_settings))

            if i_pmf_settings < COM_DEF.i_PmfSettings_Disable or \
                    COM_DEF.i_PmfSettings_RangeErr <= i_pmf_settings:
                s_dbg_str = "PmfSettings parameter is abnormal : " \
                            + str(i_pmf_settings)
                return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                           COM_DEF.i_RET_TLV_ABNORMAL)
            else:
                pass
        else:
            pass

        # pmf check
        if COM_DEF.i_Pmf_Enabled == i_pmf:
            if COM_DEF.i_WpaPairwise_TKIP == i_WpaPairwise or \
                    COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
                s_dbg_str = "Pairwise only be AES when pmf is enabled"
                return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                           COM_DEF.i_RET_TLV_ABNORMAL)
            elif i_WpaType < COM_DEF.i_WpaType_RSN:
                s_dbg_str = "WPA Type should be more than " \
                            + "RSN when pmf is enabled"
                return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                           COM_DEF.i_RET_TLV_ABNORMAL)
            else:
                pass
        else:
            pass

        i_update_enable = 1
        l_freq_list = [ "2.4GHz",  "5GHz" ]
        for s_freq_param in l_freq_list:

            # Get page information
            getPageString = self.vndr_func.security_update_page
            i_ret = self.vndr_func.setPage(getPageString)
            if i_ret:
                s_dbg_str = "failed to get web page : " + getPageString
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # select frequency
            i_ret = self.vndr_func.select_freq("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to select frequency : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            elif i_update_enable < i_ret:
                # SSID parameters are commonly managed in 2G and 5G.
                skip_5g_flg = 1
            else:
                skip_5g_flg = 0

            # set wpa security
            i_ret = self.vndr_func.wpa_security("UPDATE",
                                                self.i_wait_time,
                                                l_com_hdr,
                                                i_WpaType,
                                                i_WpaPairwise,
                                                i_keymgmt,
                                                s_psk,
                                                s_sae_pwd,
                                                i_pmf,
                                                i_pmf_settings)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to set security wpa"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if i_ret:

                # save page
                i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                # check to update
                i_ret = self.vndr_func.select_freq("CHECK",
                                                   self.i_wait_time,
                                                   l_com_hdr,
                                                   s_freq_param)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update frequency : " \
                                    + s_freq_param
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                i_ret = self.vndr_func.wpa_security("CHECK",
                                                    self.i_wait_time,
                                                    l_com_hdr,
                                                    i_WpaType,
                                                    i_WpaPairwise,
                                                    i_keymgmt,
                                                    s_psk,
                                                    s_sae_pwd,
                                                    i_pmf,
                                                    i_pmf_settings)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to check security wpa"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass
            else:
                s_dbg_str = "Update data is none..."
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)

            if skip_5g_flg:
                self.Dbg.log(COM_DEF.DEBUG, "skip next component...")
                break
            else:
                pass

        # loop for 2.4G/5G component access

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] wpa")

        return d_rply_tlv

    ##
    # @brief Set channel for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Channel"] AP channel \n
    #                         ["Bandwidth"] bandwidth of AP
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def channel(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] channel")

        # Get page information
        getPageString = self.vndr_func.channel_update_page
        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # mandatory parameter
        i_channel = d_tlv_param["Channel"]
        i_chanwidth = d_tlv_param["Bandwidth"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "CHANNEL      : " + str(i_channel))
        self.Dbg.log(COM_DEF.DEBUG,
                     "BANDWIDTH    : " + str(i_chanwidth))

        # optional
        if 'Sideband' in d_tlv_param:
            i_sideband = d_tlv_param["Sideband"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "SIDEBAND     : " + str(i_sideband))
        else:
            i_sideband = 0

        if 0 < i_channel and i_channel < 15:
            # auto channel is not supported in autoeva system.
            s_freq_param = "2.4GHz"
            i_band_type = COM_DEF.i_BandType_24GHz
        elif 36 <= i_channel and i_channel <= 64 or \
                100 <= i_channel and i_channel <= 144 and \
                0 == i_channel % 4:
            s_freq_param = "5GHz"
            i_band_type = COM_DEF.i_BandType_5GHz
        elif 149 <= i_channel and i_channel <= 169 or \
                1 == i_channel % 4:
            s_freq_param = "5GHz"
            i_band_type = COM_DEF.i_BandType_5GHz
        else:
            s_dbg_str = "channel parameter is abnormal : " \
                        + str(i_channel)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)

        if i_chanwidth < COM_DEF.i_Bandwidth_20MHz or \
                COM_DEF.i_Bandwidth_RangeErr <= i_chanwidth:
            s_dbg_str = "Bandwidth parameter is abnormal : " \
                        + str(i_chanwidth)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)
        else:
            pass

        # select frequency
        i_ret = self.vndr_func.select_freq("UPDATE",
                                           self.i_wait_time,
                                           l_com_hdr,
                                           s_freq_param)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to select frequency : " + s_freq_param
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        i_ret = self.vndr_func.channel_param("UPDATE",
                                             self.i_wait_time,
                                             l_com_hdr,
                                             i_channel,
                                             i_chanwidth,
                                             i_sideband)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to set channel parameter"
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        if i_ret:

            # save page
            i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
            if i_ret:
                s_dbg_str = "can't submit page"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # check to update
            i_ret = self.vndr_func.select_freq("CHECK",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update frequency : " \
                                + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            i_ret = self.vndr_func.channel_param("CHECK",
                                                 self.i_wait_time,
                                                 l_com_hdr,
                                                 i_channel,
                                                 i_chanwidth,
                                                 i_sideband)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update channel parameter : " \
                            + str(i_channel) + '/' + str(i_chanwidth)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass
        else:
            s_dbg_str = "Update data is none..."
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        # set band info
        i_dst_id = l_com_hdr[0][0]
        self.d_instance_info[i_dst_id]["Band"] = i_band_type

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] channel")

        return d_rply_tlv

    ##
    # @brief Set country code for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["CountryCode"] country code \n
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def country(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        i_revision = -1

        self.Dbg.log(COM_DEF.TRACE, "[S] country")

        # mandatory parameter
        s_countrycode = d_tlv_param["CountryCode"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "COUNTRYCODE : " + s_countrycode)

        # option parameter (revision)
        if "RevisionCode" in d_tlv_param:
            i_revision = d_tlv_param["RevisionCode"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "REVISIONCODE : " + str(i_revision))
        else:
            pass

        i_update_enable = 1
        l_freq_list = [ "2.4GHz",  "5GHz" ]
        for s_freq_param in l_freq_list:

            # Get page information
            getPageString = self.vndr_func.country_update_page
            if "Not Support" == getPageString:
                s_dbg_str = "country command is not supported"
                return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                           COM_DEF.i_RET_SYSTEM_ERROR)
            else:
                pass

            i_ret = self.vndr_func.setPage(getPageString)
            if (i_ret):
                s_dbg_str = "failed to get web page : " + getPageString
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                s_dbg_str = getPageString
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)

            # select frequency
            i_ret = self.vndr_func.select_freq("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to select frequency : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            elif i_update_enable < i_ret:
                # country parameters are commonly managed in 2G and 5G.
                skip_5g_flg = 1
            else:
                skip_5g_flg = 0

            i_ret = self.vndr_func.country_param("UPDATE",
                                                 self.i_wait_time,
                                                 l_com_hdr,
                                                 s_countrycode,
                                                 i_revision)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to set country parameter"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            if i_ret:

                # save page
                i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
                if i_ret:
                    s_dbg_str = "can't submit page"
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                # check to update
                i_ret = self.vndr_func.select_freq("CHECK",
                                                   self.i_wait_time,
                                                   l_com_hdr,
                                                   s_freq_param)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update frequency : " \
                                    + s_freq_param
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass

                i_ret = self.vndr_func.country_param("CHECK",
                                                     self.i_wait_time,
                                                     l_com_hdr,
                                                     s_countrycode,
                                                     i_revision)
                if COM_DEF.i_RET_SUCCESS > i_ret:
                    s_dbg_str = "failed to update country parameter : " \
                                + s_countrycode + '/' + str(i_revision)
                    return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
                else:
                    pass
            else:
                s_dbg_str = "Update data is none..."
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)

            if skip_5g_flg:
                self.Dbg.log(COM_DEF.DEBUG, "skip next component...")
                break
            else:
                pass

        # loop for 2.4G/5G component access

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] country")

        return d_rply_tlv

    ##
    # @brief Set up stealth for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["OnOffFlag"] stealth enable/disable flag \n
    #                           - 0 : stealth disable \n
    #                           - 1 : stealth enable
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def stealth(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] stealth")

        # Get dst id parameter to select frequency
        i_dst_id = l_com_hdr[0][0]
        s_freq_param = self.get_freq_info(i_dst_id)
        if "" == s_freq_param:
            s_dbg_str = "freq info could not be selected"
            return self.dbg.error_info(l_com_hdr,
                                       s_dbg_str,
                                       COM_DEF.i_RET_SYSTEM_ERROR)
        else:
            pass

        # Get page information
        getPageString = self.vndr_func.stealth_update_page
        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # select frequency
        i_ret = self.vndr_func.select_freq("UPDATE",
                                           self.i_wait_time,
                                           l_com_hdr,
                                           s_freq_param)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to select frequency : " + s_freq_param
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # mandatory parameter
        i_onoff_flg = d_tlv_param["OnOffFlag"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "FLAG         : " + str(i_onoff_flg))

        if i_onoff_flg == COM_DEF.i_Disabled or \
                i_onoff_flg == COM_DEF.i_Enabled:
            pass
        else:
            s_dbg_str = "SetStealthMode parameter is abnormal : " \
                        + str(i_onoff_flg)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)

        i_ret = self.vndr_func.closed("UPDATE",
                                      self.i_wait_time,
                                      l_com_hdr,
                                      i_onoff_flg)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to change 802.11n parameter"
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        if i_ret:

            # save page
            i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
            if i_ret:
                s_dbg_str = "can't submit page"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # check to update
            i_ret = self.vndr_func.select_freq("CHECK",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update frequency : " + \
                            s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            i_ret = self.vndr_func.closed("CHECK",
                                          self.i_wait_time,
                                          l_com_hdr,
                                          i_onoff_flg)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update closed : " + \
                            str(i_onoff_flg)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass
        else:
            s_dbg_str = "Update data is none..."
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] stealth")

        return d_rply_tlv

    ##
    # @brief Enable/disable wireless output for AP.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
    #                         ["Channel"] AP channel
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def controlbss(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        s_freq_param = ""

        self.Dbg.log(COM_DEF.TRACE, "[S] controlbss")

        # Get dst id parameter to select frequency
        i_dst_id = l_com_hdr[0][0]
        s_freq_param = self.get_freq_info(i_dst_id)
        if "" == s_freq_param:
            s_dbg_str = "freq info could not be selected"
            return self.dbg.error_info(l_com_hdr,
                                       s_dbg_str,
                                       COM_DEF.i_RET_SYSTEM_ERROR)
        else:
            pass

        # Get page information
        getPageString = self.vndr_func.bss_update_page
        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # select frequency
        i_ret = self.vndr_func.select_freq("UPDATE",
                                           self.i_wait_time,
                                           l_com_hdr,
                                           s_freq_param)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to select frequency : " + s_freq_param
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # mandatory parameter
        i_onoff_flg = d_tlv_param["OnOffFlag"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "FLAG         : " + str(i_onoff_flg))
        if i_onoff_flg == COM_DEF.i_Disabled or \
                i_onoff_flg == COM_DEF.i_Enabled:
            pass
        else:
            s_dbg_str = "SetRadioOutput parameter is abnormal : " \
                        + str(i_onoff_flg)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)

        # radio parameter
        i_ret = self.vndr_func.radio("UPDATE",
                                     self.i_wait_time,
                                     l_com_hdr,
                                     i_onoff_flg)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "can't control radio : " \
                        + str(i_onoff_flg)
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        if i_ret:

            # save page
            i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
            if i_ret:
                s_dbg_str = "can't submit page"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # check to update
            i_ret = self.vndr_func.select_freq("CHECK",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update frequency : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            i_ret = self.vndr_func.radio("CHECK",
                                         self.i_wait_time,
                                         l_com_hdr,
                                         i_onoff_flg)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update radio status : " \
                            + str(i_onoff_flg)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass
        else:
            s_dbg_str = "Update data is none..."
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] controlbss")

        return d_rply_tlv

    ##
    # @brief Return BSSID of connected STA.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def stalist(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS
        i_cnt = 0

        self.Dbg.log(COM_DEF.TRACE, "[S] stalist")

        # Get page information
        getPageString = self.vndr_func.get_stalist_page
        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # refresh
        i_ret = self.vndr_func.refresh(self.i_wait_time, l_com_hdr)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to refresh (" + \
                        str(i_ret) + ")"
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        html = self.vndr_func.getPageSource()
        if "" == html:
            s_dbg_str = "can't get web page"
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        i_cnt, l_macaddr = self.vndr_func.getStalist(l_com_hdr,
                                                     html)

        s_dbg_str = "NumOfSta = " + str(i_cnt)
        self.dbg.dbg_info(l_com_hdr, s_dbg_str)
        s_dbg_str = "DataList = " + str(l_macaddr)
        self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS
        d_rply_tlv["NumOfSta"] = i_cnt
        d_rply_tlv["DataList"] = l_macaddr

        self.Dbg.log(COM_DEF.TRACE, "[E] stalist")

        return d_rply_tlv

    ##
    # @brief control to set up connection restrictions
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def limit(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}

        self.Dbg.log(COM_DEF.TRACE, "[S] limit")

        # Get dst id parameter to select frequency
        i_dst_id = l_com_hdr[0][0]
        s_freq_param = self.get_freq_info(i_dst_id)
        if "" == s_freq_param:
            s_dbg_str = "freq info could not be selected"
            return self.dbg.error_info(l_com_hdr,
                                       s_dbg_str,
                                       COM_DEF.i_RET_SYSTEM_ERROR)
        else:
            pass

        # Get page information
        getPageString = self.vndr_func.limit_update_page
        if "Not Support" == getPageString:
            s_dbg_str = "max limix command is not supported"
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_SYSTEM_ERROR)
        else:
            pass

        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            s_dbg_str = getPageString
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        # select frequency
        i_ret = self.vndr_func.select_freq("UPDATE",
                                           self.i_wait_time,
                                           l_com_hdr,
                                           s_freq_param)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to select frequency : " + s_freq_param
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        i_max_assoc = d_tlv_param["MaxAssoc"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "MAX ASSOC    : " + str(i_max_assoc))

        i_ret = self.vndr_func.max_limit("UPDATE",
                                         self.i_wait_time,
                                         l_com_hdr,
                                         i_max_assoc)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "can't control max associations"
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        if i_ret:

            # save page
            i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
            if i_ret:
                s_dbg_str = "can't submit page"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # check to update
            i_ret = self.vndr_func.select_freq("CHECK",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update frequency : " + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            i_ret = self.vndr_func.max_limit("CHECK",
                                             self.i_wait_time,
                                             l_com_hdr,
                                             i_max_assoc)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update limit associatoins : " + \
                            str(i_max_assoc)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass
        else:
            s_dbg_str = "Update data is none..."
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] limit")

        return d_rply_tlv

    ##
    # @brief Return BSSID of connected STA.
    # @param l_com_hdr    command header parameter
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
    def control11n(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] control11n")

        # Get dst id parameter to select frequency
        i_dst_id = l_com_hdr[0][0]
        s_freq_param = self.get_freq_info(i_dst_id)
        if "" == s_freq_param:
            s_dbg_str = "freq info could not be selected"
            return self.dbg.error_info(l_com_hdr,
                                       s_dbg_str,
                                       COM_DEF.i_RET_SYSTEM_ERROR)
        else:
            pass

        # Get page information
        getPageString = self.vndr_func.ieee80211n_update_page
        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # select frequency
        i_ret = self.vndr_func.select_freq("UPDATE",
                                           self.i_wait_time,
                                           l_com_hdr,
                                           s_freq_param)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "failed to select frequency : " + s_freq_param
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        # wireless mode
        i_onoff_flg = d_tlv_param["OnOffFlag"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "FLAG         : " + str(i_onoff_flg))

        if i_onoff_flg == COM_DEF.i_Disabled or \
                i_onoff_flg == COM_DEF.i_Enabled:
            pass
        else:
            s_dbg_str = "Set11nMode parameter is abnormal : " \
                        + str(i_onoff_flg)
            return self.dbg.error_info(l_com_hdr, s_dbg_str,
                                       COM_DEF.i_RET_TLV_ABNORMAL)

        i_ret = self.vndr_func.ieee80211n("UPDATE",
                                          self.i_wait_time,
                                          l_com_hdr,
                                          i_onoff_flg)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "can't set 11n options : " + str(i_onoff_flg)
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        if i_ret:

            # save page
            i_ret = self.vndr_func.submit_page(self.i_wait_time, l_com_hdr)
            if i_ret:
                s_dbg_str = "can't submit page"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            # check to update
            i_ret = self.vndr_func.select_freq("CHECK",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_freq_param)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update frequency : " \
                            + s_freq_param
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            i_ret = self.vndr_func.ieee80211n("CHECK",
                                              self.i_wait_time,
                                              l_com_hdr,
                                              i_onoff_flg)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update 11n mode : " \
                            + str(i_onoff_flg)
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass
        else:
            s_dbg_str = "Update data is none..."
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] control11n")

        return d_rply_tlv

    ##
    # @brief Detach processing of AP control.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def detach(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] detach")

        i_ret = self.vndr_func.ctrl_quit()
        if COM_DEF.i_RET_SUCCESS > i_ret:
            s_dbg_str = "can't release webdriver"
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        s_dbg_str = "detach webdriver"
        self.dbg.dbg_info(l_com_hdr, s_dbg_str)
        time.sleep(1)

        s_dbg_str = "detach command complete."
        self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] detach")

        return d_rply_tlv

    ##
    # @brief Node ID check as to whether the opposite device connected
    #        from the MC side is the same as the actually
    #        connected device, and performs time synchronization with
    #        the MC side.
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def test_ready(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] test_ready")

        # get node id
        i_dst_id = l_com_hdr[0][0]
        i_node_id = (i_dst_id & COM_DEF.i_NODEID_MASK) >> 8
        self.Dbg.log(COM_DEF.DEBUG, "NODE ID : 0x%02x" % (i_node_id))

        # node id check
        if i_node_id < COM_DEF.i_NODE_AP_START or \
                COM_DEF.i_NODE_AP_END < i_node_id:
            s_dbg_str = "node id error [0x%04x]" % (i_dst_id)
            i_ret = COM_DEF.i_RET_NODE_CHK_ERROR
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            d_rply_tlv['IpAddress'] = self.s_AP_IpAddr

        d_rply_tlv["Result"] = i_ret

        self.Dbg.log(COM_DEF.TRACE, "[E] test_ready")

        return d_rply_tlv

    ##
    # @brief DHCP server Enable
    #        Enable CISCO controller DHCP server
    #        Configure Cisco AP to refer to controller DHCP server
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter \n
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
    def dhcpd(self, l_com_hdr, d_tlv_param):

        d_rply_tlv = {}
        i_ret = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[S] dhcpd")

        # Get page information
        getPageString = self.vndr_func.dhcpd_update_page
        i_ret = self.vndr_func.setPage(getPageString)
        if (i_ret):
            s_dbg_str = "failed to get web page : " + getPageString
            return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
        else:
            pass

        s_start_ip = d_tlv_param["IpAddress"]
        s_netmask = d_tlv_param["NetMask"]
        i_assign_num = d_tlv_param["AssignNum"]
        s_lease = str(d_tlv_param["LeaseTime"])
        s_gateway = d_tlv_param["GateWay"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "START IP ADDRESS : " + s_start_ip)
        self.Dbg.log(COM_DEF.DEBUG,
                     "NETMASK          : " + s_netmask)
        self.Dbg.log(COM_DEF.DEBUG,
                     "ASSIGN NUMBER    : " + str(i_assign_num))
        self.Dbg.log(COM_DEF.DEBUG,
                     "LEASE TIME       : " + s_lease)
        self.Dbg.log(COM_DEF.DEBUG,
                     "GATEWAY          : " + s_gateway)

        i_ret = self.vndr_func.dhcpd_param("UPDATE",
                                           self.i_wait_time,
                                           l_com_hdr,
                                           s_start_ip,
                                           s_netmask,
                                           i_assign_num,
                                           s_lease,
                                           s_gateway)

        if COM_DEF.i_RET_SUCCESS < i_ret:

            i_ret = self.vndr_func.submit_page(60, l_com_hdr)
            if i_ret:
                s_dbg_str = "can't submit page"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass

            i_ret = self.vndr_func.dhcpd_param("UPDATE",
                                               self.i_wait_time,
                                               l_com_hdr,
                                               s_start_ip,
                                               s_netmask,
                                               i_assign_num,
                                               s_lease,
                                               s_gateway)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                s_dbg_str = "failed to update dhcpd"
                return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)
            else:
                pass
        else:
            s_dbg_str = "Update data is none..."
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.TRACE, "[E] dhcpd")

        return d_rply_tlv

    ##
    # @brief Set IpAddress to Cisco AP
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter
    #                         ["IpAddress"] IpAddress \n
    #                         ["NetMask"] Netmask \n
    #                         ["GateWay"] Gateway
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def setipinfo(self, l_com_hdr, d_tlv_param):

        self.Dbg.log(COM_DEF.TRACE, "[S] setipinfo")

        s_dbg_str = "set ip command is not supported. !!"

        i_ret = COM_DEF.i_RET_SYSTEM_ERROR
        return self.dbg.error_info(l_com_hdr, s_dbg_str, i_ret)

    ##
    # @brief Get the IpAddress
    # @param l_com_hdr    command header parameter
    # @param d_tlv_param    tlv parameter
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def getipinfo(self, l_com_hdr, d_tlv_param):

        self.Dbg.log(COM_DEF.TRACE, "[S] getipinfo")

        s_dbg_str = "get ip command is not supported. !!"

        i_ret = COM_DEF.i_RET_SYSTEM_ERROR
        return self.dbg.error_info(l_com_hdr,
                                   s_dbg_str, i_ret)
