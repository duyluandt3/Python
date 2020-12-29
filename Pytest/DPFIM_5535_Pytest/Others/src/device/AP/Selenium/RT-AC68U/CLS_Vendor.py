#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control ASUS RT-AC68U
# @author E2N3
# @date 2019.05.28

# -*- coding: utf-8 -*-

from CLS_Define import COM_DEF
from Control import AP_ENV
import socket
import struct
import ipaddress
import time


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
        self.radio_update_page = \
            "http://%s:%s@%s/Advanced_WAdvanced_Content.asp" % \
            (self.s_User, self.s_Password, self.s_AP_IpAddr)
        self.ssid_update_page = \
            "http://%s:%s@%s/Advanced_Wireless_Content.asp" % \
            (self.s_User, self.s_Password, self.s_AP_IpAddr)
        self.security_update_page = self.ssid_update_page
        self.channel_update_page = self.ssid_update_page
        self.country_update_page = "Not Support"
        self.stealth_update_page = self.ssid_update_page
        self.bss_update_page = self.radio_update_page
        self.get_stalist_page = \
            "http://%s:%s@%s/device-map/clients.asp" % \
            (self.s_User, self.s_Password, self.s_AP_IpAddr)
        self.limit_update_page = "Not Support"
        self.ieee80211n_update_page = self.ssid_update_page
        self.dhcpd_update_page = \
            "http://%s:%s@%s/Advanced_DHCP_Content.asp" % \
            (self.s_User, self.s_Password, self.s_AP_IpAddr)
        from CLS_Selenium import CTRL_SELENIUM
        self.sel_func = CTRL_SELENIUM(s_model_name)

    ##
    # @brief start web driver
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def start_webdriver(self, s_method, i_wait_time, l_com_hdr):

        return self.sel_func.start_webdriver()

    ##
    # @brief set URL
    # @param pageString     web page address
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def submit_page(self, i_wait_time, l_com_hdr):

        xpath_apply = "//input[@class='button_gen']"

        i_ret = self.sel_func.ctrl_submit(xpath_apply, i_wait_time)
        if (i_ret):
            self.Dbg.log(COM_DEF.DEBUG, "failed to submit button")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            s_dbg_str = "Apply"
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief selet to frequency
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_freq_param   "2.4GHz" or "5GHz"
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def select_freq(self, s_method, i_wait_time, l_com_hdr, s_freq_param):

        if s_freq_param == "2.4GHz":
            xpath_freq = \
                "//select[@name='wl_unit']/option[@value='0']"
        else:
            xpath_freq = \
                "//select[@name='wl_unit']/option[@value='1']"

        i_ret = self.sel_func.ctrl_radioButton(s_method,
                                               xpath_freq,
                                               i_wait_time)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_freq_param))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "select to " + s_freq_param
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_cur_freq = s_freq_param
            else:
                pass

        return i_ret

    ##
    # @brief refresh page
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def refresh(self, i_wait_time, l_com_hdr):
        # refresh page : press F5
        return self.sel_func.ctrl_refresh()

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
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ssid(self, s_method, i_wait_time, l_com_hdr, s_ssid):

        xpath_ssid = "//input[@id='wl_ssid']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_ssid,
                                           i_wait_time,
                                           s_ssid)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method,  s_ssid))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "SSID                  : " + s_ssid
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set authentication mode
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_auth_val      authentication mode \n
    #                        "open" \n
    #                        "shared"
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def auth_mode(self, s_method, i_wait_time, l_com_hdr, s_auth_val):

        xpath_auth = "//select[@name='wl_auth_mode_x']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_auth,
                                             i_wait_time,
                                             s_auth_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_auth_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Authentication Method : %s" % \
                            (s_auth_val)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wep encryption
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_wep_encrypto   wep encryption
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep_mode(self, s_method, i_wait_time, l_com_hdr, s_wep_encrypto):

        xpath_wep_enc = "//select[@name='wl_wep_x']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_wep_enc,
                                             i_wait_time,
                                             s_wep_encrypto)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_wep_encrypto))
        else:
            if "UPDATE" == s_method:
                if '1' == s_wep_encrypto:
                    s_wep_enc_dbg = "WEP-64bits"
                else:
                    s_wep_enc_dbg = "WEP-128bits"

                s_dbg_str = "WEP Encryption        : %s" % \
                            (s_wep_enc_dbg)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set key index
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_key_index   key index
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def key_idx(self, s_method, i_wait_time, l_com_hdr, s_key_index):

        xpath_wep_enc = "//select[@name='wl_key']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_wep_enc,
                                             i_wait_time,
                                             s_key_index)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_key_index))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Key Index             : " + s_key_index
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wep key
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_key_index   key index
    # @param s_wepkey   wep key
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep_key(self, s_method, i_wait_time, l_com_hdr, s_key_index, s_wepkey):

        xpath_wep_key = "//input[@id='wl_key" + s_key_index + "']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_wep_key,
                                           i_wait_time,
                                           s_wepkey)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_wepkey))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WEP Key %s             : %s" % \
                            (s_key_index, s_wepkey)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa encryption
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_crypto   wpa encryption
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def crypto(self, s_method, i_wait_time, l_com_hdr, s_crypto_val):

        xpath_crypto = "//select[@name='wl_crypto']"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_crypto,
                                             i_wait_time,
                                             s_crypto_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_crypto_val))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA Encryption        : " + s_crypto_val
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set wpa pre-shared key
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_psk   wpa pre-shared key
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def psk(self, s_method, i_wait_time, l_com_hdr, s_psk):

        xpath_psk = "//input[@name='wl_wpa_psk']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_psk,
                                           i_wait_time,
                                           s_psk)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method,  s_psk))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "WPA Pre-Shared Key    : " + s_psk
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set protect management frame category
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_pmf   protect management frame key
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def pmf(self, s_method, i_wait_time, l_com_hdr, i_pmf_param):

        xpath_pmf = "//select[@name='wl_mfp']"

        if 0 == i_pmf_param:
            s_pmf_str = "Disable"
        elif 1 == i_pmf_param:
            s_pmf_str = "Capable"
        else:
            s_pmf_str = "Required"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_pmf,
                                             i_wait_time,
                                             str(i_pmf_param))
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_pmf_str))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Protected Management Fraemes : %s" % \
                            (s_pmf_str)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set open security
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def open_security(self, s_method, l_com_hdr, i_wait_time):

        # set oepn security
        s_auth_val = "open"

        i_ret = self.auth_mode(s_method,
                               self.i_wait_time,
                               l_com_hdr,
                               s_auth_val)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.DEBUG, "%s : failed to select %s" %
                         (s_method, s_auth_val))
        else:
            pass

        return i_ret

    ##
    # @brief set wep security
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_authtype      authentication mode \n
    #                        0 = "open" \n
    #                        1 = "shared"
    # @param i_keyidx        key index [0 - 3]
    # @param s_wepkey        wep key
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep_security(self, s_method, i_wait_time, l_com_hdr,
                     i_authtype, i_keyidx, s_wepkey):

        i_update = 0
        i_wep_hex64_len = 10
        i_wep_ascii64_len = 5

        # authentication mode
        if i_authtype == COM_DEF.i_AuthFlg_Open:
            s_auth_val = "open"
        else:
            s_auth_val = "shared"

        i_ret = self.auth_mode(s_method,
                               i_wait_time,
                               l_com_hdr,
                               s_auth_val)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set auth mode : %s" %
                         (s_method, s_auth_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # wep key length
        if i_wep_hex64_len == len(s_wepkey) or \
           i_wep_ascii64_len == len(s_wepkey):
            s_wep_encrypto = '1'
        else:
            s_wep_encrypto = '2'

        i_ret = self.wep_mode(s_method,
                              i_wait_time,
                              l_com_hdr,
                              s_wep_encrypto)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set wep encryption : %s" %
                         (s_method, s_wep_encrypto))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # key index
        s_keyidx = str(i_keyidx + 1)
        i_ret = self.key_idx(s_method,
                             i_wait_time,
                             l_com_hdr,
                             s_keyidx)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set key index : %s" %
                         (s_method, s_keyidx))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # wep key
        i_ret = self.wep_key(s_method,
                             i_wait_time,
                             l_com_hdr,
                             s_keyidx,
                             s_wepkey)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set wep key%s : %s" %
                         (s_method, s_keyidx, s_wepkey))
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
    # @param i_keymgmt       key mgment \n
    #                        0 = "psk" \n
    #                        1 = "eap"
    # @param s_psk           pre-shared key
    # @param s_sae_pwd       sae password
    # @param i_pmf           0 = "disalbe" \n
    #                        1 = "enabled"
    # @param i_pmf_settings  0 = "Disablied" \n
    #                        1 = "Optional" \n
    #                        2 = "Required"
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wpa_security(self, s_method, i_wait_time, l_com_hdr,
                     i_WpaType, i_WpaPairwise, i_keymgmt, s_psk,
                     s_sae_pwd, i_pmf, i_pmf_settings):

        i_update = 0
        s_auth_val = ""
        s_crypto_val = ""

        self.Dbg.log(COM_DEF.DEBUG,
                     "Wpa Type       : " + str(i_WpaType))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Wpa Pairwise   : " + str(i_WpaPairwise))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Key Mgmt       : " + str(i_keymgmt))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Pre-Shared Key : " + s_psk)
        self.Dbg.log(COM_DEF.DEBUG,
                     "Pmf            : " + str(i_pmf))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Pmf Settings   : " + str(i_pmf_settings))

        if COM_DEF.i_KeyMgmt_PSK == i_keymgmt:
            # PSK
            if COM_DEF.i_WpaType_RSN == i_WpaType and \
               COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
                s_auth_val = "psk2"
                s_crypto_val = "aes"
            elif COM_DEF.i_WpaType_MIX == i_WpaType and \
                    COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
                s_auth_val = "pskpsk2"
                s_crypto_val = "aes"
            elif COM_DEF.i_WpaType_MIX == i_WpaType and \
                    COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
                s_auth_val = "pskpsk2"
                s_crypto_val = "tkip+aes"
            elif COM_DEF.i_WpaType_WPA == i_WpaType and \
                    COM_DEF.i_WpaPairwise_TKIP == i_WpaPairwise:
                s_auth_val = "psk"
                s_crypto_val = "tkip"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : pattern is not supported %d/%d" %
                             (s_method, i_WpaType, i_WpaPairwise))
                return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            # Enterprise
            if COM_DEF.i_WpaType_RSN == i_WpaType and \
               COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
                s_auth_val = "wpa2"
                s_crypto_val = "aes"
            elif COM_DEF.i_WpaType_MIX == i_WpaType and \
                    COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
                s_auth_val = "wpawpa2"
                s_crypto_val = "aes"
            elif COM_DEF.i_WpaType_MIX == i_WpaType and \
                    COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
                s_auth_val = "wpawpa2"
                s_crypto_val = "tkip+aes"
            elif COM_DEF.i_WpaType_WPA == i_WpaType and \
                    COM_DEF.i_WpaPairwise_TKIP == i_WpaPairwise:
                s_auth_val = "wpa"
                s_crypto_val = "tkip"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : pattern is not supported %d/%d" %
                             (s_method, i_WpaType, i_WpaPairwise))
                return COM_DEF.i_RET_SYSTEM_ERROR

        if "wpa2" == s_auth_val or \
                "wpawpa2" == s_auth_val or \
                "wpa" == s_auth_val:
            self.Dbg.log(COM_DEF.ERROR, "enterprise is not supported")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        # authentication method
        i_ret = self.auth_mode(s_method, i_wait_time, l_com_hdr, s_auth_val)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set auth method : %s" %
                         (s_method, s_auth_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # WPA Encryption
        i_ret = self.crypto(s_method, i_wait_time, l_com_hdr, s_crypto_val)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.logger.log(COM_DEF.ERROR,
                            "%s : failed to set wpa encryption : %s" %
                            (s_method, s_crypto_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # Pre-shared Key
        i_ret = self.psk(s_method, i_wait_time, l_com_hdr, s_psk)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set pre-shared key : %s" %
                         (s_method, s_psk))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        if (s_auth_val == "psk2" or s_auth_val == "wpa2") and \
                s_crypto_val == "aes" and i_pmf:

            i_ret = self.pmf(s_method,
                             i_wait_time,
                             l_com_hdr,
                             i_pmf_settings)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set pmf : %d" %
                             (s_method, i_pmf_settings))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass
        elif (s_auth_val == "psk2" or s_auth_val == "wpa2") and \
                s_crypto_val == "aes":

            i_ret = self.pmf(s_method,
                             i_wait_time,
                             l_com_hdr,
                             0)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set pmf : %d" %
                             (s_method, i_pmf_settings))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass
        elif i_pmf:
            self.Dbg.log(COM_DEF.ERROR, "PMF only be supported by WPA2-PSK")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        return i_update

    ##
    # @brief set sideband parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_sideband   1:uppser or 2:lower
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def sideband(self, s_method, i_wait_time, l_com_hdr, i_sideband):

        xpath_width = "//select[@name='wl_nctrlsb']"
        if COM_DEF.i_Sideband_upper == i_sideband:
            s_sb_dbg = "above"
            s_opt_val = "l"
        else:
            s_sb_dbg = "below"
            s_opt_val = "u"

        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_width,
                                             i_wait_time,
                                             s_opt_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_sb_dbg))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = \
                    "Extention Channel     : %s" % s_sb_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set bandwidth parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_width   bandwidth '1': 20MHz '2': 40MHz '3': 80MHz
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def bandwidth(self, s_method, i_wait_time, l_com_hdr, s_width):

        xpath_width = "//select[@name='wl_bw']"
        if '1' == s_width:
            s_width_dbg = "20 MHz"
        elif '2' == s_width:
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
                s_dbg_str = "Channel bandwidth     : " + s_width_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief select channel
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_channel   channel parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def channel(self, s_method, i_wait_time, l_com_hdr, s_channel):

        xpath_channel = "//select[@name='wl_channel']"

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
                s_dbg_str = "Control Channel       : " + s_channel
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def channel_param(self, s_method, i_wait_time, l_com_hdr,
                      i_channel, i_chanwidth, i_sideband):
        i_update = 0
        i_sideband_update = 0

        if COM_DEF.i_Bandwidth_20MHz == i_chanwidth:
            s_bandwidth = '1'
            s_channel = str(i_channel)
        elif COM_DEF.i_Bandwidth_40MHz == i_chanwidth:
            s_bandwidth = '2'
            s_bandwidth_dbg = "40 MHz"
            if 1 <= i_channel and i_channel <= 14:
                s_channel = str(i_channel)
                i_sideband_update = 1
            else:
                if 36 == i_channel:
                    s_channel = str(i_channel) + "l"
                elif 40 == i_channel:
                    s_channel = str(i_channel) + "u"
                else:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "only support 36 or 40 channe on " +
                                 "5GHz/40MHz")
                    return COM_DEF.i_RET_SYSTEM_ERROR
        elif COM_DEF.i_Bandwidth_80MHz == i_chanwidth and \
                15 < i_channel:
            s_bandwidth = '3'
            s_bandwidth_dbg = "80 MHz"
            s_channel = str(i_channel) + "/80"
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "unexpected bandwidth parameter : %d/%d" %
                         (i_channel, i_chanwidth))
            return COM_DEF.i_RET_SYSTEM_ERROR

        # Bandwidth
        i_ret = self.bandwidth(s_method, i_wait_time, l_com_hdr,
                               s_bandwidth)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : failed to set bandwidth : %s" %
                         (s_method, s_bandwidth_dbg))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # Channel
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

        # Sideband
        if i_sideband and i_sideband_update:
            i_ret = self.sideband(s_method, i_wait_time,
                                  l_com_hdr, i_sideband)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set sideband : %d" %
                             (s_method, i_sideband))
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def closed(self, s_method, i_wait_time, l_com_hdr, i_onoff_flg):

        if 1 == i_onoff_flg:
            xpath_closed = "//input[@value='1' and @name='wl_closed']"
            s_dbg = "Yes"
        else:
            xpath_closed = "//input[@value='0' and @name='wl_closed']"
            s_dbg = "No"

        i_ret = self.sel_func.ctrl_radioButton(s_method,
                                               xpath_closed,
                                               i_wait_time)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %d" %
                         (s_method, i_onoff_flg))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Hide SSID             : " + s_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief control radio on/off
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_onoff_flg   0 : "OFF"  1: "ON"
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def radio(self, s_method, i_wait_time, l_com_hdr, i_onoff_flg):

        if 1 == i_onoff_flg:
            s_dbg = "Yes"
            xpath_radio = \
                "//input[@value='1' and @name='wl_radio']"
        else:
            s_dbg = "No"
            xpath_radio = \
                "//input[@value='0' and @name='wl_radio']"

        i_ret = self.sel_func.ctrl_radioButton(s_method,
                                               xpath_radio,
                                               i_wait_time)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select radio button" %
                         s_method)
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Enable Radio          : " + s_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief get the connected station list
    # @param l_com_hdr    command header parameter
    # @param html   html page info
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
    def getStalist(self, l_com_hdr, html):

        i_cnt = 0
        l_macAddr = []
        s_targetStr = ""
        s_parseStr = ""

        print(html)
        for s_parseStr in html.split('\n'):
            if "var client_list_array" in s_parseStr:
                # ex) <6>>192.168.0.199>4C:E6:76:55:5D:64>0>0>0,
                #     <6>>192.168.0.30>3C:28:6D:01:28:9B>0>0>0
                self.Dbg.log(COM_DEF.DEBUG, s_parseStr)
                break
            else:
                pass

        for s_targetStr in s_parseStr.split('>'):
            if len(s_targetStr) == 17 and ':' in s_targetStr:
                if i_cnt:
                    d_list_tlv = {}
                    # ex) [0] 4C:E6:76:55:5D:64 -- skip
                    #     [1] 3C:28:6D:01:28:9B
                    self.Dbg.log(COM_DEF.DEBUG, s_targetStr)
                    d_list_tlv["MacAddress"] = s_targetStr
                    l_macAddr.append(d_list_tlv)
                else:
                    # skip list[0] mac address because it is LAN side.
                    pass
                i_cnt += 1
            else:
                pass

        if i_cnt:
            i_cnt -= 1
        else:
            pass

        s_dbg_str = str(i_cnt) + " : " + str(l_macAddr)
        self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        return i_cnt, l_macAddr

    ##
    # @brief control 11n mode on/off
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param i_onoff_flg   0: "OFF", 1: "ON"
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ieee80211n(self, s_method, i_wait_time, l_com_hdr, i_onoff_flg):

        # ASUS AP has 11n mode parameter on ssid page.
        # Therefore, change from current page to ssid page at this point.
        # When procedure is finished, retry to set prior page.

        for i_cnt in range(5):
            cur_url = self.sel_func.getCurrentURL()

            if "" == cur_url or \
                    "apply.cgi" in cur_url:
                time.sleep(1)
            else:
                pageString = self.ieee80211n_update_page
                i_ret = self.sel_func.setPage(pageString)
                if (i_ret):
                    self.Dbg.log(COM_DEF.ERROR,
                                 "failed to get web page : %s" %
                                 (pageString))
                    return COM_DEF.i_RET_SYSTEM_ERROR
                else:
                    break
        # for loop end

        if "" == cur_url or \
                "apply.cgi" in cur_url:
            self.Dbg.log(COM_DEF.ERROR, "failed to get url")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        if 1 == i_onoff_flg:
            s_dbg = "Auto"
            s_value = '0'
        else:
            s_dbg = "Legacy"
            s_value = '2'

        xpath_nmode = "//select[@name='wl_nmode_x']"
        i_ret = self.sel_func.ctrl_selectBox(s_method,
                                             xpath_nmode,
                                             i_wait_time,
                                             s_value)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %d" %
                         (s_method, i_onoff_flg))
        else:
            if i_ret:
                i_submit_ret = self.submit_page(i_wait_time,
                                                l_com_hdr)
                if i_submit_ret < 0:
                    self.Dbg.log(COM_DEF.ERROR, "failed to submit")
                    return i_submit_ret
                else:
                    pass
            else:
                pass

        self.Dbg.log(COM_DEF.DEBUG, "re-set : " + cur_url)
        i_ret = self.sel_func.setPage(cur_url)
        if (i_ret):
            self.Dbg.log(COM_DEF.ERROR,
                         "failed to get web page : %s" %
                         (pageString))
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        # reopen setting 2.4GHz or 5GHz page
        i_ret = self.select_freq(s_method,
                                 i_wait_time,
                                 l_com_hdr,
                                 self.s_cur_freq)
        if COM_DEF.i_RET_SUCCESS > i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to select freq")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        if "UPDATE" == s_method:
            s_dbg_str = "Wireless Mode         : " + s_dbg
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)
        else:
            pass

        return i_ret

    ##
    # @brief start or stop dhcpd
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_ctrl_str   "OFF" or "ON"
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def dhcpd(self, s_method, i_wait_time, l_com_hdr, s_ctrl_str):

        if "ON" == s_ctrl_str:
            xpath_dhcpd = \
                "//input[@value='1' and @name='dhcp_enable_x']"
        else:
            xpath_dhcpd = \
                "//input[@value='0' and @name='dhcp_enable_x']"

        i_ret = self.sel_func.ctrl_radioButton(s_method,
                                               xpath_dhcpd,
                                               i_wait_time)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select %s" %
                         (s_method, s_ctrl_str))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Enable Radio          : " + s_ctrl_str
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set start ip address to dhcpd server parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_startIp   start IP Address
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def startIPaddr(self, s_method, i_wait_time, l_com_hdr, s_startIp):

        xpath_startAddr = "//input[@name='dhcp_start']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_startAddr,
                                           i_wait_time,
                                           s_startIp)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method,  s_startIp))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "IP Pool Starting Address : " + s_startIp
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set end ip address to dhcpd server parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_endIp   end IP Address
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
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
                s_dbg_str = "IP Pool Ending Address: " + s_endIp
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set lease time to dhcpd server parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_leaseTime   lease time
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def leaseTime(self, s_method, i_wait_time, l_com_hdr, s_leaseTime):

        xpath_lease = "//input[@name='dhcp_lease']"

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
                s_dbg_str = "Lease TIme            : " + s_leaseTime
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set gateway address to dhcpd server parameter
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_gwAddr   gateway address
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def gwAddr(self, s_method, i_wait_time, l_com_hdr, s_gwAddr):

        xpath_dhcp_gateway = "//input[@name='dhcp_gateway_x']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_dhcp_gateway,
                                           i_wait_time,
                                           s_gwAddr)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_gwAddr))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Default Gateway       : " + s_gwAddr
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def dhcpd_param(self, s_method, i_wait_time, l_com_hdr,
                    s_start_ip, s_netmask, i_assign_num, s_lease, s_gateway):
        i_update = 0

        if "0.0.0.0" == s_start_ip:
            # when start ip address is "0.0.0.0", disable dhcpd server.
            # dhcp disable
            s_ctrl_str = "OFF"
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
                i_prefix = bin(struct.unpack(
                            '!L', socket.inet_pton(
                                    socket.AF_INET, s_netmask)
                            )[0])[2:].index('0')
                i_available_num = 2**(32 - i_prefix) - 1
            except Exception as err_info:
                self.Dbg.log(COM_DEF.ERROR,
                             "NetMask format error")
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
                self.Dbg.log(COM_DEF.ERROR, "IpAddress format error")
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

            # gateway
            i_ret = self.gwAddr(self,
                                s_method,
                                i_wait_time,
                                l_com_hdr,
                                s_gateway)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set gateway ip address : %s" %
                             (s_method, s_gateway))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

            # dhcpd enable
            s_ctrl_str = "ON"

        i_ret = self.dhcpd(self, s_method, i_wait_time, l_com_hdr, s_ctrl_str)
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_quit(self):

        return self.sel_func.ctrl_quit()
