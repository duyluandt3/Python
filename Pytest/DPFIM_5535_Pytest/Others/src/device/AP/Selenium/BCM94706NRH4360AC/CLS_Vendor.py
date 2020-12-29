#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control Broadcom BCM94706NRH4380AC
# @author E2N3
# @date 2019.05.28

# -*- coding: utf-8 -*-

import time
import struct
import ipaddress
import socket
from CLS_Define import COM_DEF
from Control import AP_ENV
from bs4 import BeautifulSoup


##
# @brief Define vendor related processing.
class CTRL_VENDOR(AP_ENV):

    ##
    # @brief Run when instantiating the CTRL_VENDOR class.
    # @param cls_dbg    class for sending debug info
    # @param s_model_name  AP model name. (AP folder name)
    # @retval None
    def __init__(self, cls_dbg, s_model_name):
        super().__init__(s_model_name)
        self.dbg = cls_dbg
        self.basic_page = "http://%s:%s@%s/index.asp" % \
                          (self.s_User, self.s_Password, self.s_AP_IpAddr)
        self.radio_update_page = "http://%s:%s@%s/radio.asp" % \
                                 (self.s_User, self.s_Password,
                                  self.s_AP_IpAddr)
        self.ssid_update_page = "http://%s:%s@%s/ssid.asp" % \
                                (self.s_User, self.s_Password,
                                 self.s_AP_IpAddr)
        self.security_update_page = "http://%s:%s@%s/security.asp" % \
                                    (self.s_User, self.s_Password,
                                     self.s_AP_IpAddr)
        self.channel_update_page = self.radio_update_page
        self.country_update_page = self.radio_update_page
        self.stealth_update_page = self.ssid_update_page
        self.bss_update_page = self.radio_update_page
        self.get_stalist_page = self.ssid_update_page
        self.limit_update_page = self.radio_update_page
        self.ieee80211n_update_page = self.radio_update_page
        self.dhcpd_update_page = "http://%s:%s@%s/lan.asp" % \
                                 (self.s_User, self.s_Password,
                                  self.s_AP_IpAddr)
        from CLS_Selenium import CTRL_SELENIUM
        self.update_11n_enable_flag = 0
        self.sel_func = CTRL_SELENIUM(s_model_name)

    ##
    # @brief start web driver
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def start_webdriver(self, s_method, i_wait_time, l_com_hdr):

        return self.sel_func.start_webdriver()

    ##
    # @brief set URL
    # @param pageString     web page address
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def setPage(self, pageString):

        return self.sel_func.setPage(pageString)

    ##
    # @brief get web page information
    # @retval html    html code
    def getPageSource(self):

        return self.sel_func.getPageSource()

    ##
    # @brief submit web page
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                   - Failure : Value other than \n
    #                               COM_DEF.i_RET_SUCCESS
    def submit_page(self, i_wait_time, l_com_hdr):

        xpath_apply = "//input[@value='Apply']"

        i_ret = self.sel_func.ctrl_submit(xpath_apply, i_wait_time)
        if (i_ret):
            self.Dbg.log(COM_DEF.DEBUG, "failed to submit button")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            s_dbg_str = "Apply"
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        # for apply and continue timing
        time.sleep(3)

        # continue the page
        xpath_cont = "//input[@value='Continue']"
        i_ret = self.sel_func.ctrl_submit(xpath_cont, i_wait_time)
        if COM_DEF.i_RET_SUCCESS != i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to submit button")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            s_dbg_str = "Press Continue"
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        # reopen setting 2.4GHz or 5GHz page
        i_ret = self.select_freq("UPDATE", 20, l_com_hdr, self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        if self.update_11n_enable_flag:

            self.Dbg.log(COM_DEF.DEBUG, "try to enable 11n")

            self.update_11n_enable_flag = 0

            cur_url = self.sel_func.getCurrentURL()

            if "" == cur_url:
                self.Dbg.log(COM_DEF.ERROR, "failed to get url")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pageString = self.radio_update_page
                i_ret = self.sel_func.setPage(pageString)
                if (i_ret):
                    self.Dbg.log(COM_DEF.ERROR,
                                 "failed to get web page : %s" %
                                 (pageString))
                    return COM_DEF.i_RET_SYSTEM_ERROR
                else:
                    pass

            # In case of CCMP and mixed, enable 802.11n.
            i_ret = self.ieee80211n("UPDATE",
                                    i_wait_time,
                                    l_com_hdr,
                                    1)
            if i_ret < 0:
                self.Dbg.log(COM_DEF.ERROR,
                             "failed to enable 802.11n mode")
                return i_ret
            elif i_ret:
                i_ret = self.submit_page(i_wait_time, l_com_hdr)
                if i_ret < 0:
                    self.Dbg.log(COM_DEF.ERROR, "failed to submit")
                    return i_ret
                else:
                    pass
            else:
                pass

            i_ret = self.sel_func.setPage(cur_url)
            if (i_ret):
                self.Dbg.log(COM_DEF.ERROR, "failed to get web page : %s" %
                             (pageString))
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

            # reopen setting 2.4GHz or 5GHz page
            i_ret = self.select_freq("UPDATE", 20, l_com_hdr, self.s_cur_freq)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief selet to frequency
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_freq_param   "2.4GHz" or "5GHz"
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than \n
    #                               COM_DEF.i_RET_SUCCESS
    def select_freq(self, s_method, i_wait_time, l_com_hdr, s_freq_param):

        xpath_freq = "//select[@name='wl_unit']"

        if s_freq_param == "2.4GHz":
            s_wl_unit_val = "1"
        else:
            s_wl_unit_val = "0"

        i_ret = self.sel_func.ctrl_selectBox(s_method, xpath_freq,
                                             i_wait_time, s_wl_unit_val)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "UPDATE : failed to select " + s_freq_param)
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "select to " + s_freq_param
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_cur_freq = s_freq_param
                # After the frequency information update,
                # webpage access fails if time is not left.
                time.sleep(3)
            else:
                pass

        return i_ret

    ##
    # @brief refresh page
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                   - Failure : Value other than \n
    #                               COM_DEF.i_RET_SUCCESS
    def refresh(self, i_wait_time, l_com_hdr):

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set ssid
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_ssid   ssid parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
    def ssid(self, s_method, i_wait_time, l_com_hdr, s_ssid):

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        xpath_ssid = "//input[@name='wl_ssid']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_ssid,
                                           i_wait_time,
                                           s_ssid)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set %s to text box" %
                         (s_method, s_ssid))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Network Name (SSID)   : " + s_ssid
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set authentication mode
    # @param driver    webdriver object
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @s_auth_mode_val      authentication mode \n
    #                       "0" : Open \n
    #                       "1" : Shared
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 (Update) \n
    #                   - Failure : Value other than \n
    #                               COM_DEF.i_RET_SUCCESS
    def auth_mode(self, s_method, i_wait_time, l_com_hdr, s_auth_mode_val):

        # check whether same parameter is set or not
        xpath_auth = "//select[@name='wl_auth']"
        s_dbg = ["Open", "Shared"]

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_auth,
                                             i_wait_time,
                                             s_auth_mode_val)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select %s" %
                         (s_method, s_auth_mode_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "802.11 Authentication : %s" % \
                            (s_dbg[int(s_auth_mode_val)])
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set key management parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_keymgmt   key management parameter \n
    #                            "none" : psk \n
    #                            "radius" : enterprise
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def key_mgmt(self, s_method, i_wait_time, l_com_hdr, s_keymgmt):

        xpath_keymgmt = "//select[@name='wl_auth_mode']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_keymgmt,
                                             i_wait_time,
                                             s_keymgmt)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_keymgmt))
        else:
            if "UPDATE" == s_method:
                if "none" == s_keymgmt:
                    s_dbg = "disabled"
                else:
                    s_dbg = "enabled"
                s_dbg_str = "802.1X Authentication : " + s_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wep encryption
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_wep_encrypto   wep encryption \n
    #                            "enabled": wep enabled \n
    #                            "disabled" : wep disabled
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def wep_mode(self, s_method, i_wait_time, l_com_hdr, s_wep_encrypto):

        xpath_wep_mode = "//select[@name='wl_wep']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_wep_mode,
                                             i_wait_time,
                                             s_wep_encrypto)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_wep_encrypto))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WEP Encryption        : %s" % \
                            (s_wep_encrypto)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set key index
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_key_index   key index (1 - 4)
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def key_idx(self, s_method, i_wait_time, l_com_hdr, s_key_index):

        xpath_key_idx = "//select[@name='wl_key']/option[@value='" \
                        + s_key_index + "']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_key_idx,
                                             i_wait_time,
                                             s_key_index)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select key idx %s" %
                         (s_method, s_key_index))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Current Network Key   : %s" % \
                            (s_key_index)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wep key
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_key_index   key index
    # @param s_wepkey   wep key
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def wep_key(self, s_method, i_wait_time, l_com_hdr,
                s_key_index, s_wepkey):

        xpath_wep_key = "//input[@name='wl_key" + s_key_index + "']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_wep_key,
                                           i_wait_time,
                                           s_wepkey)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_wepkey))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Network Key %s         : %s" % \
                            (s_key_index, s_wepkey)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa akm
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_akm_wpa_val    wpa akm \n
    #                           "disabled" : disabled
    #                           "enabled" : enabled
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def akm_wpa(self, s_method, i_wait_time, l_com_hdr, s_akm_wpa_val):

        # check whether same parameter is set or not
        xpath_akm_wpa = "//select[@name='wl_akm_wpa']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_akm_wpa,
                                             i_wait_time,
                                             s_akm_wpa_val)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_akm_wpa_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA                   : %s" % \
                            (s_akm_wpa_val)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa encryption
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_akm_psk_val    akm psk \n
    #                           "disabled" : disabled
    #                           "enabled" : enabled
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def akm_psk(self, s_method, i_wait_time, l_com_hdr, s_akm_psk_val):

        # check whether same parameter is set or not
        xpath_akm_psk = "//select[@name='wl_akm_psk']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_akm_psk,
                                             i_wait_time,
                                             s_akm_psk_val)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select %s" %
                         (s_method, s_akm_psk_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA-PSK               : %s" % \
                            (s_akm_psk_val)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa akm
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_akm_wpa2_val    wpa akm \n
    #                            "disabled" : disabled
    #                            "enabled" : enabled
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def akm_wpa2(self, s_method, i_wait_time, l_com_hdr, s_akm_wpa2_val):

        # check whether same parameter is set or not
        xpath_akm_wpa2 = "//select[@name='wl_akm_wpa2']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_akm_wpa2,
                                             i_wait_time,
                                             s_akm_wpa2_val)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select %s" %
                         (s_method, s_akm_wpa2_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA2                  : %s" % \
                            (s_akm_wpa2_val)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa encryption
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_akm_psk2_val    akm psk \n
    #                            "disabled" : disabled
    #                            "enabled" : enabled
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def akm_psk2(self, s_method, i_wait_time, l_com_hdr, s_akm_psk2_val):

        # check whether same parameter is set or not
        xpath_akm_psk2 = "//select[@name='wl_akm_psk2']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_akm_psk2,
                                             i_wait_time,
                                             s_akm_psk2_val)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select %s" %
                         (s_method, s_akm_psk2_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA2-PSK              : %s" % \
                            (s_akm_psk2_val)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa encryption
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_crypto   wpa encryption
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def crypto(self, s_method, i_wait_time, l_com_hdr, s_crypto_val):

        xpath_crypto = "//select[@name='wl_crypto']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_crypto,
                                             i_wait_time,
                                             s_crypto_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_crypto_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA Encryption        : %s" % \
                            (s_crypto_val)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa pre-shared key
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_Psk   wpa pre-shared key
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def psk(self, s_method, i_wait_time, l_com_hdr, s_Psk):

        xpath_psk = "//input[@name='wl_wpa_psk']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_psk,
                                           i_wait_time,
                                           s_Psk)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_Psk))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA passphrase        : %s" % \
                            (s_Psk)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set protect management frame category
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_pmf   protect management frame key
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def pmf(self, s_method, i_wait_time, l_com_hdr, i_Pmf_param):

        xpath_pmf = "//select[@name='wl_mfp']"

        if 0 == i_Pmf_param:
            s_pmf_str = "Disable"
        elif 1 == i_Pmf_param:
            s_pmf_str = "Capable"
        else:
            s_pmf_str = "Required"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_pmf,
                                             i_wait_time,
                                             str(i_Pmf_param))
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_pmf_str))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Protected Management Frames : " \
                            + s_pmf_str
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set open security
    # @param s_method     "UPDATE" or "CHECK"
    # @param l_com_hdr    command header parameter
    # @param i_wait_time    wait time for web update
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def open_security(self, s_method, l_com_hdr, i_wait_time):

        i_ret = COM_DEF.i_RET_SUCCESS
        i_update = 0

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        s_auth_val = "0"
        i_ret = self.auth_mode(s_method, i_wait_time, l_com_hdr, s_auth_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select auth mode : %s" %
                         (s_method, s_auth_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_wep_mode = "disabled"
        i_ret = self.wep_mode(s_method, i_wait_time, l_com_hdr, s_wep_mode)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wep mode : %s" %
                         (s_method, s_wep_mode))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_key_mgmt = "none"
        i_ret = self.key_mgmt(s_method, i_wait_time, l_com_hdr, s_key_mgmt)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select key management : %s" %
                         (s_method, s_key_mgmt))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_wpa_val = "disabled"
        i_ret = self.akm_wpa(s_method, i_wait_time, l_com_hdr, s_akm_wpa_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa enterprise : %s" %
                         (s_method, s_akm_wpa_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_psk_val = "disabled"
        i_ret = self.akm_psk(s_method, i_wait_time, l_com_hdr, s_akm_psk_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa psk : %s" %
                         (s_method, s_akm_psk_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_wpa2_val = "disabled"
        i_ret = self.akm_wpa2(s_method, i_wait_time, l_com_hdr, s_akm_wpa2_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa2 enterprise : %s" %
                         (s_method, s_akm_wpa2_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_psk2_val = "disabled"
        i_ret = self.akm_psk2(s_method, i_wait_time, l_com_hdr, s_akm_psk2_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa2 psk : %s" %
                         (s_method, s_akm_psk2_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        return i_update

    ##
    # @brief set wep security
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_authFlg      authentication mode \n
    #                        0 = "open" \n
    #                        1 = "shared"
    # @param i_keyidx        key index [0 - 3]
    # @param s_wepkey        wep key
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def wep_security(self, s_method, i_wait_time, l_com_hdr,
                     i_authFlg, i_keyidx, s_wepkey):

        i_update = 0

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        # authentication mode
        if COM_DEF.i_AuthFlg_Open == i_authFlg:
            s_auth_val = "0"
        else:
            s_auth_val = "1"

        i_ret = self.auth_mode(s_method, i_wait_time, l_com_hdr, s_auth_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select auth mode : %s" %
                         (s_method, s_auth_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_key_mgmt = "none"
        i_ret = self.key_mgmt(s_method, i_wait_time, l_com_hdr, s_key_mgmt)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select key management : %s" %
                         (s_method, s_key_mgmt))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_wpa_val = "disabled"
        i_ret = self.akm_wpa(s_method, i_wait_time, l_com_hdr, s_akm_wpa_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa enterprise : %s" %
                         (s_method, s_akm_wpa_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_psk_val = "disabled"
        i_ret = self.akm_psk(s_method, i_wait_time, l_com_hdr, s_akm_psk_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa psk : %s" %
                         (s_method, s_akm_psk_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_wpa2_val = "disabled"
        i_ret = self.akm_wpa2(s_method, i_wait_time, l_com_hdr, s_akm_wpa2_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa2 enterprise : %s" %
                         (s_method, s_akm_wpa2_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_akm_psk2_val = "disabled"
        i_ret = self.akm_psk2(s_method, i_wait_time, l_com_hdr, s_akm_psk2_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wpa2 psk : %s" %
                         (s_method, s_akm_psk2_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_wep_mode = "enabled"
        i_ret = self.wep_mode(s_method, i_wait_time, l_com_hdr, s_wep_mode)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wep mode : %s" %
                         (s_method, s_wep_mode))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_key_idx = str(i_keyidx + 1)
        i_ret = self.key_idx(s_method, i_wait_time, l_com_hdr, s_key_idx)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select current network key : %s" %
                         (s_method, s_key_idx))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        i_ret = self.wep_key(s_method, i_wait_time, l_com_hdr,
                             s_key_idx, s_wepkey)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set wep key : %s" %
                         (s_method, s_wepkey))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        return i_update

    ##
    # @brief set wpa security
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_WpaType      wpa type \n
    #                        0 = "wpa \n
    #                        1 = "wpa2" \n
    #                        2 = "mix"
    # @param i_WpaPairwise   wpa pairwise \n
    #                        0 = "tkip" \n
    #                        1 = "rsn" \n
    #                        2 = "mix"
    # @param i_KeyMgmt       key mgment \n
    #                        0 = "psk" \n
    #                        1 = "eap"
    # @param s_Psk           pre-shared key
    # @param s_SaePwd        sae password
    # @param i_Pmf           0 = "disalbe" \n
    #                        1 = "enabled"
    # @param i_PmfSettings  0 = "Disablied" \n
    #                        1 = "Optional" \n
    #                        2 = "Required"
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def wpa_security(self, s_method, i_wait_time, l_com_hdr,
                     i_WpaType, i_WpaPairwise, i_KeyMgmt, s_Psk,
                     s_SaePwd, i_Pmf, i_PmfSettings):

        i_update = 0

        self.Dbg.log(COM_DEF.DEBUG,
                     "Wpa Type       : " + str(i_WpaType))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Wpa Pairwise   : " + str(i_WpaPairwise))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Key Mgmt       : " + str(i_KeyMgmt))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Pre-Shared Key : " + s_Psk)
        self.Dbg.log(COM_DEF.DEBUG,
                     "Pmf            : " + str(i_Pmf))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Pmf Settings   : " + str(i_PmfSettings))

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        if COM_DEF.i_WpaType_WPA == i_WpaType:
            if COM_DEF.i_KeyMgmt_PSK == i_KeyMgmt:
                s_akm_wpa_val = "disabled"
                s_akm_psk_val = "enabled"
                s_akm_wpa2_val = "disabled"
                s_akm_psk2_val = "disabled"
                s_key_mgmt = "none"
            elif COM_DEF.i_KeyMgmt_EAP == i_KeyMgmt:
                s_akm_wpa_val = "enabled"
                s_akm_psk_val = "disabled"
                s_akm_wpa2_val = "disabled"
                s_akm_psk2_val = "disabled"
                s_key_mgmt = "radius"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : pattern is not supported %d/%d" %
                             (s_method, i_WpaType, i_KeyMgmt))
                return COM_DEF.i_RET_SYSTEM_ERROR
        elif COM_DEF.i_WpaType_RSN == i_WpaType:
            if COM_DEF.i_KeyMgmt_PSK == i_KeyMgmt:
                s_akm_wpa_val = "disabled"
                s_akm_psk_val = "disabled"
                s_akm_wpa2_val = "disabled"
                s_akm_psk2_val = "enabled"
                s_key_mgmt = "none"
            elif COM_DEF.i_KeyMgmt_EAP == i_KeyMgmt:
                s_akm_wpa_val = "disabled"
                s_akm_psk_val = "disabled"
                s_akm_wpa2_val = "enabled"
                s_akm_psk2_val = "disabled"
                s_key_mgmt = "radius"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : pattern is not supported : %d/%d" %
                             (s_method, i_WpaType, i_KeyMgmt))
                return COM_DEF.i_RET_SYSTEM_ERROR
        elif COM_DEF.i_WpaType_MIX == i_WpaType:
            if COM_DEF.i_KeyMgmt_PSK == i_KeyMgmt:
                s_akm_wpa_val = "disabled"
                s_akm_psk_val = "enabled"
                s_akm_wpa2_val = "disabled"
                s_akm_psk2_val = "enabled"
                s_key_mgmt = "none"
            elif COM_DEF.i_KeyMgmt_EAP == i_KeyMgmt:
                s_akm_wpa_val = "enabled"
                s_akm_psk_val = "disabled"
                s_akm_wpa2_val = "enabled"
                s_akm_psk2_val = "disabled"
                s_key_mgmt = "radius"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : pattern is not supported : %d/%d" %
                             (s_method, i_WpaType, i_KeyMgmt))
                return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : pattern is not supported : %d/%d" %
                         (s_method, i_WpaType, i_KeyMgmt))
            return COM_DEF.i_RET_SYSTEM_ERROR

        if "radius" == s_key_mgmt:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : pattern is not supported : %d/%d" %
                         (s_method, i_WpaType, i_KeyMgmt))
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        s_wep_mode = "disabled"
        i_ret = self.wep_mode(s_method, i_wait_time, l_com_hdr, s_wep_mode)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select wep mode : %s" %
                         (s_method, s_wep_mode))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_auth_val = "0"
        i_ret = self.auth_mode(s_method, i_wait_time, l_com_hdr, s_auth_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select auth mode : %s" %
                         (s_method, s_auth_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # 802.1x disabled (none) or enabled (radius)
        i_ret = self.key_mgmt(s_method, i_wait_time, l_com_hdr, s_key_mgmt)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select key management : %s" %
                         (s_method, s_key_mgmt))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # wpa-eap
        i_ret = self.akm_wpa(s_method, i_wait_time, l_com_hdr, s_akm_wpa_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select wpa enterprise : %s" %
                         (s_method, s_akm_wpa_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # wpa-psk (disabled or enabled)
        i_ret = self.akm_psk(s_method, i_wait_time, l_com_hdr, s_akm_psk_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select wpa psk : %s" %
                         (s_method, s_akm_psk_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # wpa2-eap (disabled or enabled)
        i_ret = self.akm_wpa2(s_method, i_wait_time, l_com_hdr, s_akm_wpa2_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select wpa2 enterprise : %s" %
                         (s_method, s_akm_wpa2_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # wpa2-psk (disabled or enabled)
        i_ret = self.akm_psk2(s_method, i_wait_time, l_com_hdr, s_akm_psk2_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select wpa2 psk : %s" %
                         (s_method, s_akm_psk2_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # pairwise
        if COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
            s_crypto_val = "aes"
        elif COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
            s_crypto_val = "tkip+aes"
        elif COM_DEF.i_WpaPairwise_TKIP == i_WpaPairwise:
            s_crypto_val = "tkip"
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : can't support encryption method : %d" %
                         (s_method, i_WpaPairwise))
            return COM_DEF.i_RET_SYSTEM_ERROR

        i_ret = self.crypto(s_method, i_wait_time, l_com_hdr, s_crypto_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to select crypto : %s" %
                         (s_method, s_crypto_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # Pre-Shared key
        i_ret = self.psk(s_method, i_wait_time, l_com_hdr, s_Psk)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set psk : %s" %
                         (s_method, s_Psk))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        if ((s_akm_psk2_val == "enabled" or s_akm_wpa2_val == "enabled") and
                s_crypto_val == "aes" and i_Pmf):

            i_ret = self.pmf(s_method,
                             i_wait_time,
                             l_com_hdr,
                             i_PmfSettings)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set pmf : %d" %
                             (s_method, i_PmfSettings))
                return i_ret
            else:
                pass
        else:
            pass

        if COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise or \
                COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
            self.update_11n_enable_flag = 1
        else:
            pass

        return i_update

    ##
    # @brief set bandwidth parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_width   bandwidth '1': 20MHz '3': 40MHz '7': 80MHz
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def bandwidth(self, s_method, i_wait_time, l_com_hdr, s_width):

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        xpath_width = "//select[@name='wl_bw_cap']"
        if '1' == s_width:
            s_width_dbg = "20 MHz"
        elif '3' == s_width:
            s_width_dbg = "40 MHz"
        else:
            s_width_dbg = "80 MHz"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_width,
                                             i_wait_time,
                                             s_width)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_width_dbg))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Bandwidth             : %s" % \
                            (s_width_dbg)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief select channel
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_channel   channel parameter
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def channel(self, s_method, i_wait_time, l_com_hdr, s_channel):

        xpath_channel = "//select[@name='wl_chanspec']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_channel,
                                             i_wait_time,
                                             s_channel)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_channel))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Chanel Specificatioin : %s" % \
                            (s_channel)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set channel and bandwidth
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_channel       channel parameter
    # @param i_chanwidth     bandwidth parameter
    # @param i_sideband      sideband parameter (2.4GHz 40MHz only)
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def channel_param(self, s_method, i_wait_time, l_com_hdr,
                      i_channel, i_chanwidth, i_sideband):
        i_update = 0

        if COM_DEF.i_Bandwidth_20MHz == i_chanwidth:
            s_bandwidth = '1'
            s_channel = str(i_channel)
        elif COM_DEF.i_Bandwidth_40MHz == i_chanwidth:
            s_bandwidth = '3'
            if 1 <= i_channel and i_channel <= 4:
                s_channel = str(i_channel) + "l"
            elif 5 <= i_channel and i_channel <= 9:
                if COM_DEF.i_Sideband_upper == i_sideband:
                    s_channel = str(i_channel) + "l"
                elif COM_DEF.i_Sideband_lower == i_sideband:
                    s_channel = str(i_channel) + "u"
                else:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "can't get sideband parameter...\
                                  set lower to sideband from 5ch to 9ch")
                    s_channel = str(i_channel) + "u"
            elif 9 <= i_channel and i_channel <= 14:
                s_channel = str(i_channel) + "u"
            else:
                if 36 <= i_channel and i_channel <= 144:
                    if 0 == (i_channel - 36) % 8:
                        s_channel = str(i_channel) + "l"
                    else:
                        s_channel = str(i_channel) + "u"
                elif 149 <= i_channel and i_channel <= 169:
                    if 0 == (i_channel - 149) % 8:
                        s_channel = str(i_channel) + "l"
                    else:
                        s_channel = str(i_channel) + "u"
                else:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "%s : %d ch can not be specified" %
                                 (s_method, i_channel))
                    return COM_DEF.i_RET_SYSTEM_ERROR

        elif COM_DEF.i_Bandwidth_80MHz == i_chanwidth:
            s_bandwidth = '7'
            s_channel = str(i_channel) + "/80"
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : Unexpected bandwidth parameter : %d:%d" %
                         (s_method, i_channel, i_chanwidth))
            return COM_DEF.i_RET_SYSTEM_ERROR

        # bandwidth
        i_ret = self.bandwidth(s_method, i_wait_time, l_com_hdr,
                               s_bandwidth)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set bandwidth : %s" %
                         (s_method, s_bandwidth))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # channel
        i_ret = self.channel(s_method, i_wait_time, l_com_hdr,
                             s_channel)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set channel : %s" %
                         (s_method, s_channel))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        return i_update

    ##
    # @brief set country code
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_countrycode       country code
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def country(self, s_method, i_wait_time, l_com_hdr, s_countrycode):

        xpath_country = "//select[@name='wl_country_code']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_country,
                                             i_wait_time,
                                             s_countrycode)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select " %
                         (s_method, s_countrycode))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Country               : %s" % \
                            (s_countrycode)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set country code
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_revision       revision code
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def revision_code(self, s_method, i_wait_time, l_com_hdr,
                      s_revision):

        xpath_revision = "//select[@name='wl_country_rev']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_revision,
                                             i_wait_time,
                                             s_revision)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_revision))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Regulatory Revision   : %s" % \
                            (s_revision)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set country parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_countrycode       country code
    # @param i_revision     revision code (-1 is meaning of skip)
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def country_param(self, s_method, i_wait_time, l_com_hdr,
                      s_countrycode, i_revision):
        i_update = 0

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        i_ret = self.country(s_method, i_wait_time, l_com_hdr,
                             s_countrycode)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set country code : %s" %
                         (s_method, s_countrycode))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        if 0 <= i_revision:
            i_ret = self.revision_code(s_method,
                                       i_wait_time,
                                       l_com_hdr,
                                       str(i_revision))
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set revision code : %d" %
                             (s_method, i_revision))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass
        else:
            pass

        return i_update

    ##
    # @brief set hidden ssid (ssid broadcast on/off)
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_onoff_flg   '0' broadcast ssid '1' hidden ssid
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def closed(self, s_method, i_wait_time, l_com_hdr, i_onoff_flg):

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        xpath_closed = "//select[@name='wl_closed']"

        if i_onoff_flg:
            s_dbg = "Closed"
        else:
            s_dbg = "Open"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_closed,
                                             i_wait_time,
                                             str(i_onoff_flg))
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_dbg))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Network Type          : %s" % \
                            (s_dbg)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief control radio on/off
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param i_onoff_flg   0 : "OFF"  1: "ON"
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def radio(self, s_method, i_wait_time, l_com_hdr, i_onoff_flg):

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        if 1 == i_onoff_flg:
            s_dbg = "enabled"
        else:
            s_dbg = "disabled"

        xpath_radio = \
            "//select[@name='wl_radio']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_radio,
                                             i_wait_time,
                                             str(i_onoff_flg))
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select radio button : %s" %
                         (s_method, s_dbg))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "interface             : %s" % \
                            (s_dbg)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief get the connected station list
    # @param l_com_hdr    command header parameter
    # @param html   html page info
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than \n
    #                               COM_DEF.i_RET_SUCCESS
    def getStalist(self, l_com_hdr, html):

        i_cnt = 0
        l_macAddr = []

        i_ret = self.select_freq("UPDATE", 20, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            # Broadcom AP always loads a 5GHz page first.
            # Therefore, the HTML of the corresponding page is read again.
            html = self.getPageSource()
            if "" == html:
                self.Dbg.log(COM_DEF.ERROR, "failed to get page")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

        soup = BeautifulSoup(html, 'html.parser')

        table_border = soup.find_all("table", border="1",
                                     cellpadding="2")
        self.Dbg.log(COM_DEF.DEBUG,
                     "table_border : " + str(table_border))

        for row_table in table_border:
            tr_data = row_table.find_all("tr")

        self.Dbg.log(COM_DEF.DEBUG, "tr_data : " + str(len(tr_data)))
        for row_tr in tr_data:
            td_data = row_tr.find("td")
            if i_cnt == 0:
                i_cnt += 1
                continue
            else:
                pass

            s_mac = td_data.text
            self.Dbg.log(COM_DEF.DEBUG, "mac addr : " + s_mac)
            l_macAddr.append(s_mac)
            i_cnt += 1

        self.Dbg.log(COM_DEF.DEBUG,
                     "mac address list : " + str(l_macAddr))

        i_cnt = 0
        l_list_tlv = []
        for s_mac in l_macAddr:
            self.Dbg.log(COM_DEF.DEBUG, "TEST813 : " + s_mac)
            d_list_tlv = {}
            d_list_tlv["MacAddress"] = s_mac
            s_dbg_str = "MacAddress [" + str(i_cnt) + "] : " + s_mac
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            l_list_tlv.append(d_list_tlv)
            i_cnt += 1
        # for loop end

        return i_cnt, l_list_tlv

    ##
    # @brief control association limit
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_max_assoc   the number of limit
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def max_limit(self, s_method, i_wait_time, l_com_hdr, i_max_assoc):

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        xpath_limit = "//input[@name='wl_maxassoc']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_limit,
                                           i_wait_time,
                                           str(i_max_assoc))
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %d" %
                         (i_max_assoc))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Max Associations Limit: %d" % \
                            (i_max_assoc)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief control 11n mode on/off
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_onoff_flg   0: "OFF", 1: "ON"
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def ieee80211n(self, s_method, i_wait_time, l_com_hdr, i_onoff_flg):

        # The enabled setting of 802.11n may fail at this timing.
        # WEP Encryption parameter must be "disabled"
        # and WPA2-PSK parameter musb be "enabled"
        # when 802.11n mode is "enabled" in Broadcom AP specification.

        i_ret = self.select_freq("UPDATE", i_wait_time, l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        xpath_nmode = "//select[@name='wl_nmode']"

        if 1 == i_onoff_flg:
            # auto
            s_value = "-1"
            s_dbg = "Auto"
        else:
            # legacy
            s_value = "0"
            s_dbg = "Off"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_nmode,
                                             i_wait_time,
                                             s_value)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s result : %d" %
                         (s_method, s_value, i_ret))
            if self.update_11n_enable_flag:
                pass
            else:
                self.Dbg.log(COM_DEF.DEBUG, "skip to 11n mode error")
                i_ret = COM_DEF.i_RET_SUCCESS
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "802.11n Proctection   : %s" % \
                            (s_dbg)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief start or stop dhcpd
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_ctrl_str   "OFF" or "ON"
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def dhcpd(self, s_method, i_wait_time, l_com_hdr, s_ctrl_str):

        xpath_dhcpd = "//select[@name='lan_proto']"
        if "dhcp" == s_ctrl_str:
            s_dbg = "enabled"
        else:
            s_dbg = "disabled"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_dhcpd,
                                             i_wait_time,
                                             s_ctrl_str)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_ctrl_str))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "DHCP Server           : %s" % \
                            (s_dbg)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set start ip address to dhcpd server parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_startIp   start IP Address
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def startIPaddr(self, s_method, i_wait_time, l_com_hdr, s_startIp):

        xpath_startAddr = "//input[@name='dhcp_start']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_startAddr,
                                           i_wait_time,
                                           s_startIp)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_startIp))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "DHCP Starting IP Address : %s" % \
                            (s_startIp)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set end ip address to dhcpd server parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_endIp   end IP Address
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def endIPaddr(self, s_method, i_wait_time, l_com_hdr, s_endIp):

        xpath_endAddr = "//input[@name='dhcp_end']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_endAddr,
                                           i_wait_time,
                                           s_endIp)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_endIp))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "DHCP Ending IP Address : %s" % \
                            (s_endIp)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set lease time to dhcpd server parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_leaseTime   lease time
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def leaseTime(self, s_method, i_wait_time, l_com_hdr, s_leaseTime):

        xpath_lease = "//input[@name='lan_lease']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_lease,
                                           i_wait_time,
                                           s_leaseTime)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_leaseTime))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "DHCP Lease Time : " + s_leaseTime
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief start or stop dhcpd
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_start_ip   start ip address
    # @param s_netmask    netmask
    # @param i_assign_num   the number of assigned ip address
    # @param s_lease      lease time
    # @param s_gateway   gateway ip address
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def dhcpd_param(self, s_method, i_wait_time, l_com_hdr,
                    s_start_ip, s_netmask, i_assign_num, s_lease, s_gateway):

        if "0.0.0.0" == s_start_ip:
            # when start ip address is "0.0.0.0", disable dhcpd server.
            # dhcp disable
            s_ctrl_str = "static"
        else:
            # start ip address
            i_ret = self.startIPaddr(s_method,
                                     i_wait_time,
                                     l_com_hdr,
                                     s_start_ip)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set start ip : %s" %
                             (s_method, s_start_ip))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

            try:
                i_prefix = bin(struct.unpack('!L', socket.inet_pton(
                                            socket.AF_INET,
                                            s_netmask))[0])[2:].index('0')
                i_available_num = 2**(32 - i_prefix) - 1
            except Exception as err_info:
                self.Dbg.log(COM_DEF.ERROR, "NetMask format error")
                self.Dbg.log(COM_DEF.ERROR, err_info)
                return COM_DEF.i_RET_SYSTEM_ERROR

            s_end_ip = ''
            try:
                # create network address
                s_ipaddr = s_start_ip + "/" + str(i_prefix)
                s_netaddr = str(ipaddress.IPv4Network(s_ipaddr, False))
                s_netaddr = s_netaddr.rstrip("/" + str(i_prefix))

                s_max_Ip = ipaddress.IPv4Address(s_netaddr) + i_available_num
                i_available_num = int(s_max_Ip) - int(ipaddress.IPv4Address(
                                  s_start_ip))
                if i_available_num >= i_assign_num:
                    s_end_ip = str(ipaddress.IPv4Address(s_start_ip) +
                                   i_assign_num)
                else:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "Exceeded IPAddress setting range")
                    return COM_DEF.i_RET_SYSTEM_ERROR

            except Exception as err_info:
                self.Dbg.log(COM_DEF.ERROR,
                             "IpAddress format error")
                self.Dbg.log(COM_DEF.ERROR, err_info)
                return COM_DEF.i_RET_SYSTEM_ERROR

            # ending ip address
            i_ret = self.endIPaddr(self,
                                   s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_end_ip)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set ending ip : %s" %
                             (s_method, s_end_ip))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

            # lease time
            i_ret = self.leaseTime(self,
                                   s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_lease)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set lease time : %s" %
                             (s_method, s_lease))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

            # dhcpd enable
            s_ctrl_str = "dhcp"

        i_ret = self.dhcpd(self,
                           s_method,
                           i_wait_time,
                           l_com_hdr,
                           s_ctrl_str)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to control dhcpd : %s" %
                         (s_method, s_ctrl_str))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        return i_update

    ##
    # @brief set ip address to lan parameters
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_lanIpAddr   ip address to lan port
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def lanIPaddr(self, s_method, i_wait_time, l_com_hdr, s_lanIpAddr):

        xpath_ipAddr = "//input[@name='lan_ipaddr']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_ipAddr,
                                           i_wait_time,
                                           s_lanIpAddr)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_lanIpAddr))
        else:
            pass

        return i_ret

    ##
    # @brief set netmask to lan parameters
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_lanNetMask   Netmask to lan port
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                             : COM_DEF.i_RET_SUCCESS + 1 \n
    #                               (Update) \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def lanNetMask(self, s_method, i_wait_time, l_com_hdr, s_lanNetMask):

        xpath_netMask = "//input[@name='lan_netmask']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_netMask,
                                           i_wait_time,
                                           s_lanNetMask)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_lanNetMask))
        else:
            pass

        return i_ret

    ##
    # @brief release webdriver resource
    # @retval i_ret    response data \n
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def ctrl_quit(self):

        return self.sel_func.ctrl_quit()
