#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control Buffalo WAPM-2133TR
# @author E2N3
# @date 2019.05.28

# -*- coding: utf-8 -*-

import time
from CLS_Define import COM_DEF
from Control import AP_ENV
from bs4 import BeautifulSoup


##
# @brief login to AP
# @param sel_func    selenium function table
# @param i_wait_time    wait time for web update
# @param debug    object for debug
# @param s_tagName    edit page info
# @param s_eddit_pattern  delete or create or open
# @retval i_ret    response data \n
#                     ["Result"] value of the result \n
#                       - Success : COM_DEF.i_RET_SUCCESS \n
#                       - Failure : Value other than
#                                   COM_DEF.i_RET_SUCCESS
def save_config(sel_func, i_wait_time, debug,
                s_tagName, s_edit_pattern):

    if 'create' == s_edit_pattern or 'open' == s_edit_pattern:
        # save config
        s_xpath = "//input[@type='submit' and @name='" \
                  + s_tagName + "']"
        i_ret = sel_func.ctrl_radioButton("UPDATE",
                                          s_xpath,
                                          i_wait_time)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            debug.log(COM_DEF.DEBUG, "failed to save config")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            debug.log(COM_DEF.INFO, "%s resource..." % s_edit_pattern)
    else:
        pass

    if 'delete' == s_edit_pattern or 'create' == s_edit_pattern:

        for i in range(5):

            debug.log(COM_DEF.DEBUG, "try to save...%s", str(i))

            # submit button
            s_xpath = "//input[@type='submit' and @name='go']"
            i_ret = sel_func.ctrl_radioButton("UPDATE",
                                              s_xpath,
                                              i_wait_time)

            if i_ret < COM_DEF.i_RET_SUCCESS:
                debug.log(COM_DEF.DEBUG, "failed to submit")
                time.sleep(1)
            else:
                break
        # for loop end

        if 5 <= i:
            debug.log(COM_DEF.DEBUG, "skip to submit")
#            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass
    else:
        pass

    debug.log(COM_DEF.INFO, "wait for it to be reflected...(%d sec)" %
              (i_wait_time))
    time.sleep(i_wait_time)

    return i_ret


##
# @brief login to AP
# @param sel_func    selenium function table
# @param i_wait_time    wait time for web update
# @param debug    object for debug
# @param login_page    login page url
# @param top_page    top page url
# @param s_User    login id
# @param s_Password    login password
# @retval i_ret    response data \n
#                   - Success : COM_DEF.i_RET_SUCCESS \n
#                   - Failure : Value other than \n
#                               COM_DEF.i_RET_SUCCESS
def start_loginProcedure(sel_func, i_wait_time, debug,
                         login_page, top_page, s_User, s_Password):

    for i in range(5):
        debug.log(COM_DEF.DEBUG, "try to login..." + str(i+1))

        # attach login menu.
        i_ret = sel_func.setPage(login_page)
        if (i_ret):
            debug.log(COM_DEF.ERROR, "failed to get web page : %s" %
                      (login_page))
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        # login name
        s_xpath = "//input[@id='form_USERNAME']"
        i_ret = sel_func.ctrl_textBox("UPDATE",
                                      s_xpath,
                                      i_wait_time,
                                      s_User)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            debug.log(COM_DEF.ERROR, "failed to set %s to text box" %
                      (s_User))
        else:
            debug.log(COM_DEF.INFO, "User Name        : %s" % s_User)

        if i_ret < COM_DEF.i_RET_SUCCESS:
            pass
        else:
            # password
            s_xpath = "//input[@id='form_PASSWORD']"
            i_ret = sel_func.ctrl_textBox("UPDATE",
                                          s_xpath,
                                          i_wait_time,
                                          s_Password)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                debug.log(COM_DEF.ERROR, "failed to set %s to text box" %
                          (s_Password))
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                debug.log(COM_DEF.INFO, "Password         : %s" %
                          (s_Password))

        if i_ret < COM_DEF.i_RET_SUCCESS:
            pass
        else:
            # login button
            s_xpath = "//input[@class='button_login']"
            i_ret = sel_func.ctrl_radioButton("UPDATE",
                                              s_xpath,
                                              i_wait_time)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                debug.log(COM_DEF.DEBUG, "failed to put button")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                debug.log(COM_DEF.INFO, "try to login...")

        if i_ret < COM_DEF.i_RET_SUCCESS:
            pass
        else:
            # attach url info page
            i_ret = sel_func.setPage(top_page)
            if i_ret:
                debug.log(COM_DEF.ERROR, "failed to get web page : %s" %
                          (top_page))
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

        if i_ret < COM_DEF.i_RET_SUCCESS:
            pass
        else:
            s_xpath = "//frame[@name='mnu']"
            i_ret = sel_func.ctrl_switch_to_frame(s_xpath,
                                                  i_wait_time)
            if i_ret:
                debug.log(COM_DEF.ERROR, "login error " + str(i+1))
            else:
                debug.log(COM_DEF.DEBUG, "login complete...")
                break

        time.sleep(1)
    # for loop end

    return i_ret


##
# @brief get url info
# @param sel_func    selenium function table
# @param debug    object for debug
# @param top_page    top page url
# @param ip_addr    ip address
# @param s_key_id    id=13: wireless 2G page \n
#                    id=16: wireless W52&W53 page \n
#                    id=19: wireless W56&W58 page \n
#                    id=21: edit ssid page
# @retval url_info    response data \n
#                         ["Result"] value of the result \n
#                           - Success : url_info \n
#                           - Failure : ""
def get_urlInfo(sel_func, debug, top_page, s_ipaddr, s_key_id):

    s_target_url = ""
    s_tmp_url = top_page

    for i in range(5):

        i_ret = sel_func.setPage(s_tmp_url)
        if i_ret:
            debug.log(COM_DEF.ERROR, "failed to get web page : %s" %
                      (top_page))
            return ""
        else:
            pass

        s_xpath = "//frame[@name='mnu']"
        i_ret = sel_func.ctrl_switch_to_frame(s_xpath, 2)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            debug.log(COM_DEF.DEBUG, "failed to switch frame")
            return ""
        else:
            pass

        html = sel_func.getPageSource()
        if "" == html:
            debug.log(COM_DEF.DEBUG, "can't get web page")
            return ""
        else:
            pass

        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all('a'):
            href = tag.get('href')
#        debug.log(COM_DEF.DEBUG, "href=" + str(href))
            if 'id=11' in str(href):
                s_tmp_url = 'http://' \
                            + s_ipaddr \
                            + str(href)
            elif s_key_id in str(href):
                s_target_url = 'http://' \
                               + s_ipaddr \
                               + str(href)
                break
            else:
                pass

        if s_target_url:
            debug.log(COM_DEF.DEBUG, "get target url")
            break
        else:
            pass
    # for loop end

    return s_target_url


##
# @brief switch ssid edit frame in ssid page.\n
#        And if edit button is none, craete new resource.
# @param sel_func    selenium function table
# @param i_wait_time    wait time for web update
# @param debug    object for debug
# @param edit_page    edit page url
# @param value     0: delete 1: create or open
# @retval i_ret    response data \n
#                           - Success : COM_DEF.i_RET_SUCCESS \n
#                                       COM_DEF.i_RET_SUCCESS+1 \n
#                                       (open)
#                           - Failure : Value other than \n
#                                       COM_DEF.i_RET_SUCCESS
#         s_editNames    response data \n
#                           - Success : edit name \n
#                           - Failure : ""
def editPage(sel_func, i_wait_time, debug, edit_page, value):

    s_tag_name = ''
    s_before_tag_name = ''
    s_edit_pattern = ''

    for i_cnt in range(5):

        # get url page
        i_ret = sel_func.setPage(edit_page)
        if (i_ret):
            debug.log(COM_DEF.ERROR, "failed to get web page : %s" %
                      (edit_page))
            return COM_DEF.i_RET_SYSTEM_ERROR, s_tag_name
        else:
            pass

        # change frame
        s_xpath = "//frame[@name='frm']"
        i_ret = sel_func.ctrl_switch_to_frame(s_xpath, i_wait_time)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            debug.log(COM_DEF.DEBUG, "failed to switch frame")
        else:
            debug.log(COM_DEF.DEBUG, "switch frame...")

            html = sel_func.getPageSource()
            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup.find_all('input'):
                tag_type = tag.get('type')
                if 'button' in str(tag_type):
                    if "DO_EDIT" in str(tag.get('name')):
                        if s_tag_name:
                            s_before_tag_name = s_tag_name
                        else:
                            pass
                        s_tag_name = str(tag.get('name'))
                    else:
                        pass
                else:
                    pass

            debug.log(COM_DEF.DEBUG, "before tag name = %s" %
                      (s_before_tag_name))
            debug.log(COM_DEF.DEBUG, "next tag name = %s" %
                      (s_tag_name))

            if "DO_EDIT" in s_tag_name:

                if 1 == value:
                    # create edit page
                    xpath_type = 'button'

                    if "" != s_before_tag_name:
                        # open edit page
                        s_tag_name = s_before_tag_name
                        s_edit_pattern = 'open'
                    else:
                        # create edit page
                        s_edit_pattern = 'create'
                else:
                    # delete edit page
                    xpath_type = 'submit'

                    s_edit_pattern = 'delete'
                    # delete edit page
                    if 8 == len(s_before_tag_name):
                        s_target_number = s_before_tag_name[7:]
                        s_tag_name = "DO_DELETE" + s_target_number
                    else:
                        debug.log(COM_DEF.DEBUG, "failed to get edit number")
                        return COM_DEF.i_RET_SYSTEM_ERROR, s_tag_name

                s_xpath = "//input[@type='" + xpath_type + \
                          "' and @name='" + str(s_tag_name) + "']"

                i_ret = sel_func.ctrl_radioButton("UPDATE",
                                                  s_xpath,
                                                  i_wait_time)
                if i_ret < COM_DEF.i_RET_SUCCESS:
                    debug.log(COM_DEF.DEBUG, "failed to get edit page")
                    return COM_DEF.i_RET_SYSTEM_ERROR, s_tag_name
                else:
                    debug.log(COM_DEF.INFO, "%s edit page : %s" %
                              (s_edit_pattern, s_tag_name))
                    break
            else:
                debug.log(COM_DEF.ERROR, "can't get tag name")

        time.sleep(1)

    # for loop end

    if 'open' == s_edit_pattern:
        i_ret = COM_DEF.i_RET_SUCCESS + 1
    else:
        i_ret = COM_DEF.i_RET_SUCCESS

    return i_ret, s_tag_name


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
        self.url_info = ''
        self.s_tagName = ''
        self.s_ssid = ''
        self.i_ssid_update = 0
        self.i_broadcast_ssid = 1
        self.i_broadcast_ssid_update = 0
        self.s_auth_mode = ''
        self.i_auth_mode_update = 0
        self.s_encrypto_type = ''
        self.i_encrypto_type_update = 0
        self.encrypto_xpath = ''
        # WEP security info
        self.s_wep_key_type = ''
        self.i_wep_key_type_update = 0
        self.wepkey_type_xpath = "//select[@name='weptype']"
        self.s_wep_key_idx = ''
        self.i_wep_key_idx_update = 0
        self.wepkey_idx_xpath = "//select[@name='primarykey']"
        self.s_wep_key = ''
        self.i_wep_key_update = 0
        self.wepkey_xpath = ''
        # WPA security info
        self.s_psk = ''
        self.i_psk_update = 0
        self.psk_xpath = "//td[@id='adt_wpapsk']/input[@name='wpapsk']"
        self.s_pmf = ''
        self.i_pmf_update = 0
        self.pmf_xpath = "//td[@id='adt_mfp']/select[@name='mfp']"
        # Currently setting frequency
        self.s_cur_freq = ""
        self.s_cur_2g_channel = ""
        self.d_2g_freq = {}
        self.d_2g_freq["CHANNEL"] = '0'
        self.d_2g_freq["CHANNEL_UPDATE"] = 0
        self.d_2g_freq["BANDWIDTH"] = '20'
        self.d_2g_freq["BANDWIDTH_UPDATE"] = 0
        self.d_2g_freq["11N_STATUS"] = "11bg"
        self.d_2g_freq["11N_STATUS_UPDATE"] = 0
        self.s_cur_5g_channel = ""
        self.d_5g_low_freq = {}
        self.d_5g_low_freq["CHANNEL"] = '0'
        self.d_5g_low_freq["CHANNEL_UPDATE"] = 0
        self.d_5g_low_freq["BANDWIDTH"] = '20'
        self.d_5g_low_freq["BANDWIDTH_UPDATE"] = 0
        self.d_5g_low_freq["11N_STATUS"] = "11a"
        self.d_5g_low_freq["11N_STATUS_UPDATE"] = 0
        self.d_5g_high_freq = {}
        self.d_5g_high_freq["CHANNEL"] = '0'
        self.d_5g_high_freq["CHANNEL_UPDATE"] = 0
        self.d_5g_high_freq["BANDWIDTH"] = '20'
        self.d_5g_high_freq["BANDWIDTH_UPDATE"] = 0
        self.d_5g_high_freq["11N_STATUS"] = "11a"
        self.d_5g_high_freq["11N_STATUS_UPDATE"] = 0
        # Page information
        self.login_page = "http://" \
                          + self.s_AP_IpAddr \
                          + "/cgi-bin/cgi?req=frm&frm=login.html"
        self.top_page = "http://" \
                        + self.s_AP_IpAddr \
                        + "/cgi-bin/cgi?req=tfr&rag=bridge_lan"
        self.radio_update_page = self.top_page
        self.ssid_update_page = self.top_page
        self.security_update_page = self.top_page
        self.channel_update_page = self.top_page
        self.country_update_page = "Not Support"
        self.stealth_update_page = self.top_page
        self.bss_update_page = self.top_page
        self.get_stalist_page = "id=24"
        self.limit_update_page = "Not Support"
        self.ieee80211n_update_page = self.top_page
        self.dhcpd_update_page = self.top_page

        from CLS_Selenium import CTRL_SELENIUM
        self.sel_func = CTRL_SELENIUM(s_model_name)

    ##
    # @brief start web driver
    # @brief start web driver
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def start_webdriver(self, s_method, i_wait_time, l_com_hdr):

        self.s_tagName = ""
        url_list = ['id=13', 'id=16', 'id=19']
        freq_list = [self.d_2g_freq, self.d_5g_low_freq, self.d_5g_high_freq]

        # initialize parameter
        self.s_ssid = ""
        self.i_broadcast_ssid = 1
        self.i_broadcast_ssid_update = 0
        self.s_auth_mode = ''
        self.i_auth_mode_update = 0
        self.s_encrypto_type = ''
        self.i_encrypto_type_update = 0
        self.s_wep_key_type = ''
        self.i_wep_key_type_update = 0
        self.s_wep_key_idx = ''
        self.i_wep_key_idx_update = 0
        self.s_wep_key = ''
        self.i_wep_key_update = 0
        self.s_psk = ''
        self.i_psk_update = 0
        self.s_pmf = ''
        self.i_pmf_update = 0
        self.s_cur_freq = ""
        self.s_cur_2g_channel = ""
        self.d_2g_freq = {}
        self.d_2g_freq["CHANNEL"] = '0'
        self.d_2g_freq["CHANNEL_UPDATE"] = 0
        self.d_2g_freq["BANDWIDTH"] = '20'
        self.d_2g_freq["BANDWIDTH_UPDATE"] = 0
        self.d_2g_freq["11N_STATUS"] = "11bg"
        self.d_2g_freq["11N_STATUS_UPDATE"] = 0
        self.s_cur_5g_channel = ""
        self.d_5g_low_freq = {}
        self.d_5g_low_freq["CHANNEL"] = '0'
        self.d_5g_low_freq["CHANNEL_UPDATE"] = 0
        self.d_5g_low_freq["BANDWIDTH"] = '20'
        self.d_5g_low_freq["BANDWIDTH_UPDATE"] = 0
        self.d_5g_low_freq["11N_STATUS"] = "11a"
        self.d_5g_low_freq["11N_STATUS_UPDATE"] = 0
        self.d_5g_high_freq = {}
        self.d_5g_high_freq["CHANNEL"] = '0'
        self.d_5g_high_freq["CHANNEL_UPDATE"] = 0
        self.d_5g_high_freq["BANDWIDTH"] = '20'
        self.d_5g_high_freq["BANDWIDTH_UPDATE"] = 0
        self.d_5g_high_freq["11N_STATUS"] = "11a"
        self.d_5g_high_freq["11N_STATUS_UPDATE"] = 0

        i_ret = self.sel_func.start_webdriver()
        if i_ret:
            self.Dbg.log(COM_DEF.ERROR, "failed to start web driver")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        # login buffalo ap
        i_ret = start_loginProcedure(self.sel_func,
                                     2,
                                     self.Dbg,
                                     self.login_page,
                                     self.top_page,
                                     self.s_User,
                                     self.s_Password)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.DEBUG, "failed to login AP")
            return i_ret
        else:
            pass

        # initialize band parameter
        self.Dbg.log(COM_DEF.DEBUG, "initialize band parameter...")
        self.d_2g_freq["CHANNEL"] = '1'
        self.d_2g_freq["CHANNEL_UPDATE"] = 1
        self.s_cur_2g_channel = self.d_2g_freq["CHANNEL"]
        self.d_2g_freq["BANDWIDTH"] = '20'
        self.d_2g_freq["BANDWIDTH_UPDATE"] = 1
        self.d_2g_freq["11N_STATUS"] = '11bgn'
        self.d_2g_freq["11N_STATUS_UPDATE"] = 1

        self.d_5g_low_freq["CHANNEL"] = '36'
        self.d_5g_low_freq["CHANNEL_UPDATE"] = 1
        self.s_cur_5g_channel = self.d_5g_low_freq["CHANNEL"]
        self.d_5g_low_freq["BANDWIDTH"] = '20'
        self.d_5g_low_freq["BANDWIDTH_UPDATE"] = 1
        self.d_5g_low_freq["11N_STATUS"] = '11a/n/ac'
        self.d_5g_low_freq["11N_STATUS_UPDATE"] = 1

        self.d_5g_high_freq["BANDWIDTH"] = '20'
        self.d_5g_high_freq["BANDWIDTH_UPDATE"] = 1
        self.d_5g_high_freq["11N_STATUS"] = '11a/n/ac'
        self.d_5g_high_freq["11N_STATUS_UPDATE"] = 1

        for i_cnt in range(len(url_list)):

            i_ret = self.update_channel_basic_page(s_method,
                                                   i_wait_time,
                                                   freq_list[i_cnt],
                                                   url_list[i_cnt])
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR, "failed to set basic channel")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

        # for loop end

        # get ssid page
        ssid_page = get_urlInfo(self.sel_func,
                                self.Dbg,
                                self.top_page,
                                self.s_AP_IpAddr,
                                'id=21')
        if "" == ssid_page:
            self.Dbg.log(COM_DEF.DEBUG, "failed to get ssid page")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            # open or create edit page
            i_ret, self.s_tagName = editPage(self.sel_func,
                                             2,
                                             self.Dbg,
                                             ssid_page,
                                             1)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to get edit page")
            elif i_ret:
                s_edit_pattern = 'open'
            else:
                s_edit_pattern = 'create'

        if '' == self.s_ssid:
            # temporary ssid
            s_xpath = "//input[@id='adt_ssid_manssid']"
            s_tmp_ssid = 'tmp'
            i_ret = self.sel_func.ctrl_textBox(s_method,
                                               s_xpath,
                                               i_wait_time,
                                               s_tmp_ssid)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set %s to text box" %
                             (s_method, s_tmp_ssid))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                s_edit_pattern = 'create'
            else:
                self.s_ssid = s_tmp_ssid
                self.Dbg.log(COM_DEF.INFO,
                             "SSID (temporary) : %s" %
                             (self.s_ssid))

            # ssid broadcast enabled
            s_xpath = "//td[@class='tbl']/input[@id='adt_hydessid']"
            i_onoff_flg = 1
            i_ret = self.sel_func.ctrl_checkbox(s_method,
                                                s_xpath,
                                                i_wait_time,
                                                i_onoff_flg)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to set checkbox")
                return i_ret
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG, "Update broadcast ssid : %s" %
                             (self.i_broadcast_ssid))
            else:
                pass

            # save config
            i_ret = save_config(self.sel_func,
                                i_wait_time,
                                self.Dbg,
                                self.s_tagName,
                                s_edit_pattern)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG,
                             "%s : failed to save config" % s_method)
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                self.Dbg.log(COM_DEF.INFO, "create new resource...")

            # re-login buffalo ap
            i_ret = start_loginProcedure(self.sel_func,
                                         2,
                                         self.Dbg,
                                         self.login_page,
                                         self.top_page,
                                         self.s_User,
                                         self.s_Password)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to login AP")
                return i_ret
            else:
                pass
        else:
            self.Dbg.log(COM_DEF.INFO, "Update is none...")

        return i_ret

    ##
    # @brief set URL
    # @param pageString     web page address
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def setPage(self, pageString):

        self.url_info = pageString

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief get web page information
    # @retval html    html code
    def getPageSource(self):

        if 'id=24' == self.url_info:
            client_monitor_page = get_urlInfo(self.sel_func,
                                              self.Dbg,
                                              self.top_page,
                                              self.s_AP_IpAddr,
                                              self.url_info)
            self.url_info = ''
            i_ret = self.sel_func.setPage(client_monitor_page)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG,
                             "failed to get client monitor page : %s" %
                             (self.top_page))
                return ""
            else:
                pass

            # change frame
            s_xpath = "//frame[@name='frm']"
            i_ret = self.sel_func.ctrl_switch_to_frame(s_xpath, 2)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to switch frame")
                return ""
            else:
                self.Dbg.log(COM_DEF.DEBUG, "switch frame...")

            s_xpath = "//input[@type='button' and @value='Refresh']"
            i_ret = self.sel_func.ctrl_submit(s_xpath, 20)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to refresh page")
                return ""
            else:
                pass

        else:
            pass

        return self.sel_func.getPageSource()

    ##
    # @brief submit web page
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
    def submit_page(self, i_wait_time, l_com_hdr):

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
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
    def select_freq(self, s_method, i_wait_time, l_com_hdr, s_freq_param):

        s_dbg_str = "skip select freq"
        self.dbg.dbg_info(l_com_hdr, s_dbg_str)

        SKIP_SELECT_FREQ = 2
        return SKIP_SELECT_FREQ

    ##
    # @brief refresh page
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
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

        if "UPDATE" == s_method:
            if self.s_ssid != s_ssid:
                s_dbg_str = "SSID                    : " + s_ssid
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_ssid = s_ssid
                self.i_ssid_update = 1
                return COM_DEF.i_RET_SUCCESS + 1
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set wireless authentication
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param l_com_hdr    command header parameter
    # @param s_auth_mode    authentication mode \n
    #                           "open": No encryption(Open) \n
    #                           "owe-only": Enhanced Open \n
    #                           "owe-trans": Open/Enhanced Open \n
    #                           "eap": IEEE802.1X/EAP \n
    #                           "wpa2-psk": WPA2 Personal \n
    #                           "wpa3-sae": WPA3 Personal \n
    #                           "mixed-psk": WPA/WPA2 Personal \n
    #                           "wpa3-wpa2": WPA2/WPA3 Personal \n
    #                           "wpa2-ent": WPA2 Enterprise \n
    #                           "wpa3-ent": WPA3 Enterprise \n
    #                           "mixed-ent": WPA/WPA2 Enterprisse \n
    #                           "mixed-23-ent": WPA2/WPA3 Enterprisse \n
    #                           "wpa3-192ent": WPA3 Enterprise
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
    def wireless_auth(self, s_method, i_wait_time, l_com_hdr, s_auth_mode):

        if "open" == s_auth_mode:
            s_dbg = "No encryption(Open)"
        elif "owe-only" == s_auth_mode:
            s_dbg = "Enhanced Open"
        elif "owe-trans" == s_auth_mode:
            s_dbg = "Open/Enhanced Open"
        elif "eap" == s_auth_mode:
            s_dbg = "IEEE802.1X/EAP"
        elif "wpa2-psk" == s_auth_mode:
            s_dbg = "WPA2 Personal"
        elif "wpa3-sae" == s_auth_mode:
            s_dbg = "WPA3 Personal"
        elif "mixed-psk" == s_auth_mode:
            s_dbg = "WPA/WPA2 Personal"
        elif "wpa3-wpa2" == s_auth_mode:
            s_dbg = "WPA2/WPA3 Personal"
        elif "wpa2-ent" == s_auth_mode:
            s_dbg = "WPA2 Enterprise"
        elif "wpa3-ent" == s_auth_mode:
            s_dbg = "WPA3 Enterprise"
        elif "mixed-ent" == s_auth_mode:
            s_dbg = "WPA/WPA2 Enterprisse"
        elif "mixed-23-ent" == s_auth_mode:
            s_dbg = "WPA2/WPA3 Enterprisse"
        elif "wpa3-192ent" == s_auth_mode:
            s_dbg = "WPA3 Enterprise"
        else:
            self.Dbg.log(COM_DEF.ERROR, "argument failed : " + s_auth_mode)
            return COM_DEF.i_RET_TLV_ABNORMAL

        if "UPDATE" == s_method:
            if self.s_auth_mode != s_auth_mode:
                s_dbg_str = "Wireless authentication : " + s_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_auth_mode = s_auth_mode
                self.i_auth_mode_update = 1
                return COM_DEF.i_RET_SUCCESS + 1
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set encryption type
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_encrypto     "none": open security \n
    #                       "wep": wep encryption \n
    #                       "aes": ccmp encryption \n
    #                       "tkip+aes": mixed mode encryption \n
    #                       "64": eap key length \n
    #                       "128": eap key length \n
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than \n
    #                                       COM_DEF.i_RET_SUCCESS
    def encrypto_type(self, s_method, i_wait_time, l_com_hdr, s_encrypto):

        s_dbg = ""
        i_update = 0

        if "open" == self.s_auth_mode:
            self.encrypto_xpath = "//select[@id='auth_id']"
            i_update = 1
            if "none" == s_encrypto:
                s_dbg = "Not Encryption"
            elif "wep" == s_encrypto:
                s_dbg = "WEP"
            else:
                pass
        elif "owe-only" == self.s_auth_mode or \
             "wpa2-psk" == self.s_auth_mode or \
             "wpa3-sae" == self.s_auth_mode or \
             "wpa3-wpa2" == self.s_auth_mode:
            self.encrypto_xpath = "//select[@name='auth-psk']"
            s_dbg = "AES"
        elif "wpa2-ent" == self.s_auth_mode or \
             "wpa3-ent" == self.s_auth_mode or \
             "mixed-23-ent" == self.s_auth_mode or \
             "wpa3-192ent" == self.s_auth_mode:
            self.encrypto_xpath = "//select[@name='auth-eap']"
            s_dbg = "AES"
        elif "owe-trans" == self.s_auth_mode:
            s_dbg = "Open/AES"
        elif "eap" == self.s_auth_mode:
            self.encrypto_xpath = "//select[@name='wep_autokey_type']"
            i_update = 1
            if "64" == s_encrypto:
                s_dbg = "64-bit"
            elif "128" == s_encrypto:
                s_dbg = "128-bit"
            else:
                pass
        elif "mixed-psk" == self.s_auth_mode:
            self.encrypto_xpath = "//tr[@id='crypto-mixpsk-tbl']" \
                                  + "/td[@id='adt_auth-pskmix']" \
                                  + "/select[@name='auth-pskmix]"
            s_dbg = "tkip+aes"
        elif "mixed-ent" == self.s_auth_mode:
            self.encrypto_xpath = "//tr[@id='crypto-mixeap-tbl']" \
                                  + "/td[@class='tbl']" \
                                  + "/select[@id='auth-eapmix]"
            s_dbg = "tkip+aes"
        else:
            pass

        if "" == s_dbg:
            self.Dbg.log(COM_DEF.ERROR,
                         "encrypto parameter error : %s" %
                         (s_encrypto))
            return COM_DEF.i_RET_TLV_ABNORMAL
        else:
            pass

        if "UPDATE" == s_method:
            if self.s_encrypto_type != s_encrypto:
                if "eap" == self.s_auth_mode:
                    s_dbg_str = "Key Length              : " + s_dbg
                else:
                    s_dbg_str = "Encrption Type          : " + s_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_encrypto_type = s_encrypto
                if i_update:
                    self.i_encrypto_type_update = 1
                else:
                    pass
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    # @brief set wep key type
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_wep_key_type   wep key type \n
    #                            "1": Text Input /5 characters(WEP64) \n
    #                            "2": Text Input /13 characters(WEP128) \n
    #                            "3": Hexadecimal Input /10 digit(WEP64) \n
    #                            "4": Hexadecimal Input /26 digit(WEP128)
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep_type(self, s_method, i_wait_time, l_com_hdr, s_wep_key_type):

        if '1' == s_wep_key_type:
            s_dbg = "Text Input /5 characters(WEP64)"
        elif '2' == s_wep_key_type:
            s_dbg = "Text Input /13 characters(WEP128)"
        elif '3' == s_wep_key_type:
            s_dbg = "Hexadecimal Input /10 digit(WEP64)"
        else:
            s_dbg = "Hexadecimal Input /26 digit(WEP128)"

        if "UPDATE" == s_method:
            if self.s_wep_key_type != s_wep_key_type:
                s_dbg_str = "Key Type                : " + s_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_wep_key_type = s_wep_key_type
                self.i_wep_key_type_update = 1
                return COM_DEF.i_RET_SUCCESS + 1
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set key index
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_key_index   key index (1 - 4)
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def key_idx(self, s_method, i_wait_time, l_com_hdr, s_key_index):

        if '1' == s_key_index:
            s_dbg = "Key 1"
        elif '2' == s_key_index:
            s_dbg = "Key 2"
        elif '3' == s_key_index:
            s_dbg = "Key 3"
        else:
            s_dbg = "Key 4"

        if "UPDATE" == s_method:
            if self.s_wep_key_idx != s_key_index:
                s_dbg_str = "Deault Key              : " + s_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_wep_key_idx = s_key_index
                self.i_wep_key_idx_update = 1
                return COM_DEF.i_RET_SUCCESS + 1
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set wep key
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_key_index   key index
    # @param s_wepkey   wep key
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep_key(self, s_method, i_wait_time, l_com_hdr, s_key_index, s_wepkey):

        if "UPDATE" == s_method:
            if self.s_wep_key != s_wepkey:
                s_dbg_str = "Encryption Key " \
                            + s_key_index \
                            + "        : " \
                            + s_wepkey
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_wep_key = s_wepkey
                self.i_wep_key_update = 1
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set wpa pre-shared key
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_psk   wpa pre-shared key
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def psk(self, s_method, i_wait_time, l_com_hdr, s_psk):

        if "UPDATE" == s_method:
            if self.s_psk != s_psk:
                s_dbg_str = "Pre-shared Key          : " + s_psk
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.s_psk = s_psk
                self.i_psk_update = 1
                return COM_DEF.i_RET_SUCCESS + 1
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set protect management frame category
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_pmf   protect management frame key
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def pmf(self, s_method, i_wait_time, l_com_hdr, i_pmf_param):

        if 0 == i_pmf_param:
            s_pmf_str = "Disabled"
        elif 1 == i_pmf_param:
            s_pmf_str = "Enabled(Optional)"
        elif 2 == i_pmf_param:
            s_pmf_str = "Enabled(Required)"
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "pmf parameter abnormal : %d" %
                         (i_pmf_param))
            return COM_DEF.i_RET_TLV_ABNORMAL

        if "UPDATE" == s_method:
            s_dbg_str = "Management Frames Protection : %s" % \
                        (s_pmf_str)
            self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            self.s_pmf = str(i_pmf_param)
            self.i_pmf_update = 1
            return COM_DEF.i_RET_SUCCESS + 1
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set open security
    # @param s_method     "UPDATE" or "CHECK"
    # @param l_com_hdr    command header parameter
    # @param i_wait_time    wait time for web update
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def open_security(self, s_method, l_com_hdr, i_wait_time):

        i_update = COM_DEF.i_RET_SUCCESS

        s_auth_val = "open"
        i_ret = self.wireless_auth(s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_auth_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select auth mode : %s" %
                         (s_method, s_auth_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_ecrypto_val = "none"
        i_ret = self.encrypto_type(s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_ecrypto_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select encrypto type : " %
                         (s_method, s_ecrypto_val))
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def wep_security(self, s_method, i_wait_time, l_com_hdr,
                     i_authFlg, i_keyidx, s_wepkey):

        i_update = COM_DEF.i_RET_SUCCESS

        self.Dbg.log(COM_DEF.DEBUG, "Auth Flag : " + str(i_authFlg))
        self.Dbg.log(COM_DEF.DEBUG, "Key Index : " + str(i_keyidx))
        self.Dbg.log(COM_DEF.DEBUG, "Wep Key   : " + s_wepkey)

        # authentication mode
        if COM_DEF.i_AuthFlg_Open == i_authFlg:
            s_auth_val = "0"
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "Not support wireless authentication : shared")
            return COM_DEF.i_RET_SYSTEM_ERROR

        s_auth_val = "open"
        i_ret = self.wireless_auth(s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_auth_val)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, s_method +
                         "%s : failed to select wirelss authentication : " %
                         (s_method, s_auth_val))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_encrypto = "wep"
        i_ret = self.encrypto_type(s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_encrypto)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select encryption type : " %
                         (s_method, s_encrypto))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        if COM_DEF.i_WepKey_Ascii64_Length == len(s_wepkey):
            s_wep_type = '1'
        elif COM_DEF.i_WepKey_Ascii128_Length == len(s_wepkey):
            s_wep_type = '2'
        elif COM_DEF.i_WepKey_Hex64_Length == len(s_wepkey):
            s_wep_type = '3'
        elif COM_DEF.i_WepKey_Hex128_Length == len(s_wepkey):
            s_wep_type = '4'
        else:
            self.Dbg.log(COM_DEF.ERROR, "wep key length abnormal : %d" %
                         (len(s_wepkey)))
            return COM_DEF.i_RET_TLV_ABNORMAL

        i_ret = self.wep_type(s_method, i_wait_time, l_com_hdr, s_wep_type)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select wep type : %s" %
                         (s_method, s_wep_type))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        s_key_idx = str(i_keyidx + 1)
        if 3 < i_keyidx:
            self.Dbg.log(COM_DEF.ERROR, "wep key index error : %d" %
                         (i_keyidx + 1))
            return COM_DEF.i_RET_TLV_ABNORMAL
        else:
            i_ret = self.key_idx(s_method, i_wait_time, l_com_hdr, s_key_idx)
            if i_ret < 0:
                self.Dbg.log(COM_DEF.DEBUG,
                             "%s : " % s_method +
                             "failed to select current network key : %s" %
                             (s_key_idx))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

        i_ret = self.wep_key(s_method,
                             i_wait_time,
                             l_com_hdr,
                             s_key_idx,
                             s_wepkey)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set wep key : %s" %
                         (s_method, s_wepkey))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            self.wepkey_xpath = "//tr[@id='adt_key" + str(i_keyidx) + \
                                "']/td[@class='tbl']" + \
                                "/input[@name='key" + \
                                str(i_keyidx) + "']"

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
    #                        2 = "sae" \n
    #                        3 = "wpa2-sae mix"
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

        i_update = COM_DEF.i_RET_SUCCESS
        s_auth_val = ""

        self.Dbg.log(COM_DEF.DEBUG,
                     "Wpa Type       : " + str(i_WpaType))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Wpa Pairwise   : " + str(i_WpaPairwise))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Key Mgmt       : " + str(i_keymgmt))
        if len(s_psk):
            self.Dbg.log(COM_DEF.DEBUG,
                         "Pre-Shared Key : " + s_psk)
        else:
            pass

        if len(s_sae_pwd):
            self.Dbg.log(COM_DEF.DEBUG,
                         "SAE Password   : " + s_sae_pwd)
            s_psk = s_sae_pwd
        else:
            pass

        self.Dbg.log(COM_DEF.DEBUG,
                     "Pmf            : " + str(i_pmf))
        self.Dbg.log(COM_DEF.DEBUG,
                     "Pmf Settings   : " + str(i_pmf_settings))

        # wpa3 parameter check
        if COM_DEF.i_KeyMgmt_SAE <= i_keymgmt:
            if COM_DEF.i_Pmf_Disabled == i_pmf or \
                    COM_DEF.i_PmfSettings_Disable == i_pmf_settings or \
                    COM_DEF.i_PmfSettings_Enable == i_pmf_settings:
                s_dbg_str = "PMF requried is mandatory parameter " \
                            + "when wpa3 is used"
                self.Dbg.log(COM_DEF.ERROR, s_dbg_str)
                return COM_DEF.i_RET_TLV_ABNORMAL
            elif COM_DEF.i_WpaPairwise_TKIP == i_WpaPairwise or \
                    COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
                s_dbg_str = "Pairwise only be AES when wpa3 is used"
                self.Dbg.log(COM_DEF.ERROR, s_dbg_str)
                return COM_DEF.i_RET_TLV_ABNORMAL
            else:
                pass
        else:
            pass

        if COM_DEF.i_WpaType_WPA == i_WpaType:
            pass
        elif COM_DEF.i_WpaType_RSN == i_WpaType:
            if COM_DEF.i_KeyMgmt_PSK == i_keymgmt:
                s_auth_val = "wpa2-psk"
            elif COM_DEF.i_KeyMgmt_EAP == i_keymgmt:
                # s_auth_val = "wpa2-ent"
                pass
            elif COM_DEF.i_KeyMgmt_SAE == i_keymgmt:
                s_auth_val = "wpa3-sae"
            elif COM_DEF.i_KeyMgmt_PSK_SAE_MIX == i_keymgmt:
                s_auth_val = "wpa3-wpa2"
            else:
                pass
        elif COM_DEF.i_WpaType_MIX == i_WpaType:
            if COM_DEF.i_KeyMgmt_PSK == i_keymgmt:
                s_auth_val = "mixed-psk"
            elif COM_DEF.i_KeyMgmt_EAP == i_keymgmt:
                # s_auth_val = "mixed-eap"
                pass
            else:
                pass
        else:
            pass

        if "" == s_auth_val:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : not supported " % s_method +
                         "[WPA TYPE] %d [KEY MGMT] %d" %
                         (i_WpaType, i_keymgmt))
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            i_ret = self.wireless_auth(s_method,
                                       i_wait_time,
                                       l_com_hdr,
                                       s_auth_val)
            if i_ret < 0:
                self.Dbg.log(COM_DEF.DEBUG,
                             "%s : " % s_method +
                             "failed to select wirelss auth : %s" %
                             (s_auth_val))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

        # pairwise
        if COM_DEF.i_WpaPairwise_CCMP == i_WpaPairwise:
            if "mixed-psk" == s_auth_val or \
                    "mixed-eap" == s_auth_val:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : " % s_method +
                             "Only CCMP security is not supported " +
                             "in WPA/WPA2 mixed")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                s_encrypto = "aes"
        elif COM_DEF.i_WpaPairwise_MIX == i_WpaPairwise:
            if "mixed-psk" == s_auth_val or \
                    "mixed-eap" == s_auth_val:
                s_encrypto = "tkip+aes"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : CCMP/TKIP security is supported" %
                             (s_method) + " by only WPA/WPA2 mixed")
                return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            if "wpa3-sae" == s_auth_val or \
                    "wpa3-ent" == s_auth_val or \
                    "wpa3-wpa2" == s_auth_val or \
                    "mixed-23-ent" == s_auth_val:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : WPA3 security is not supported" %
                             (s_method) + " by tkip pairwise")
                return COM_DEF.i_RET_TLV_ABNORMAL
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : Can't support encryption method : " %
                             (s_method) + "TKIP only")
                return COM_DEF.i_RET_SYSTEM_ERROR

        i_ret = self.encrypto_type(s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_encrypto)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to select encryption type : %s" %
                         (s_method, s_encrypto))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        # Pre-Shared key
        i_ret = self.psk(s_method, i_wait_time, l_com_hdr, s_psk)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set psk : %s" %
                         (s_method, s_psk))
            return i_ret
        elif i_ret:
            i_update = 1
        else:
            pass

        if i_pmf:
            if (s_auth_val == "wpa2-psk" or s_auth_val == "wpa2-ent" or
                    s_auth_val == "wpa3-sae" or s_auth_val == "wpa3-ent" or
                    s_auth_val == "wpa3-wpa2") and s_encrypto == "aes":
                pass
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select pmf : %s/%s" %
                             (s_method, s_auth_val, s_encrypto))
                return COM_DEF.i_RET_SYSTEM_ERROR
        elif (s_auth_val == "wpa2-psk" or s_auth_val == "wpa2-ent") and \
                s_encrypto == "aes":
            i_pmf = 1
            i_pmf_settings = 0
        else:
            pass

        if i_pmf:
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
        else:
            pass

        return i_update

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

        s_bandwidth = ""
        s_channel = ""
        i_update = COM_DEF.i_RET_SUCCESS

        # check channel parameter
        if 1 <= i_channel and i_channel <= 13:
            self.s_cur_freq = "2.4GHz"
        elif 36 <= i_channel and i_channel <= 64 and \
                0 == i_channel % 4:
            self.s_cur_freq = "5GHz"
        elif 100 <= i_channel and i_channel <= 140 and \
                0 == i_channel % 4:
            self.s_cur_freq = "5GHz"
        else:
            self.Dbg.log(COM_DEF.ERROR, "Not supported : " + str(i_channel))
            return COM_DEF.i_RET_TLV_ABNORMAL
        s_channel = str(i_channel)

        if 52 <= i_channel:
            s_chan_dbg = "Channel " + s_channel + " [Use DFS]"
        else:
            s_chan_dbg = "Channel " + s_channel

        # check bandwidth parameter
        if COM_DEF.i_Bandwidth_20MHz == i_chanwidth:
            s_bandwidth = '20'
        elif COM_DEF.i_Bandwidth_40MHz == i_chanwidth:
            s_bandwidth = '40'
            if 1 <= i_channel and i_channel <= 4:
                s_bandwidth += 'u'
            elif 5 <= i_channel and i_channel <= 9:
                if COM_DEF.i_Sideband_upper == i_sideband:
                    s_bandwidth += 'u'
                elif COM_DEF.i_Sideband_lower == i_sideband:
                    s_bandwidth += 'l'
                else:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "can't get sideband parameter...\
                                  set lower to sideband from 5ch to 9ch")
                    s_bandwidth += 'l'
            elif 10 <= i_channel and i_channel <= 14:
                s_bandwidth += 'l'
            elif i_channel < 140:
                pass
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "Not supported : %s/%s" %
                             (s_channel, s_bandwidth))
                return COM_DEF.i_RET_SYSTEM_ERROR
        elif COM_DEF.i_Bandwidth_80MHz == i_chanwidth:
            s_bandwidth = '80'
            if 36 <= i_channel and i_channel <= 128:
                pass
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "Not supported : %s/%s" %
                             (s_channel, s_bandwidth))
                return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s : Unexpected bandwidth : %d" %
                         (s_method, i_chanwidth))
            return COM_DEF.i_RET_TLV_ABNORMAL

        if "UPDATE" == s_method:
            if (1 <= i_channel and i_channel <= 13):
                if self.d_2g_freq["CHANNEL"] != s_channel:
                    self.d_2g_freq["CHANNEL"] = s_channel
                    self.d_2g_freq["CHANNEL_UPDATE"] = 1
                    i_update = 1
                else:
                    pass

                if self.d_2g_freq["BANDWIDTH"] != s_bandwidth:
                    self.d_2g_freq["BANDWIDTH"] = s_bandwidth
                    self.d_2g_freq["BANDWIDTH_UPDATE"] = 1
                    i_update = 1
                else:
                    pass

            elif (36 <= i_channel and i_channel <= 64):
                if self.d_5g_low_freq["CHANNEL"] != s_channel:
                    self.d_5g_low_freq["CHANNEL"] = s_channel
                    self.d_5g_low_freq["CHANNEL_UPDATE"] = 1
                    i_update = 1
                else:
                    pass

                if self.d_5g_low_freq["BANDWIDTH"] != s_bandwidth:
                    self.d_5g_low_freq["BANDWIDTH"] = s_bandwidth
                    self.d_5g_low_freq["BANDWIDTH_UPDATE"] = 1
                    i_update = 1
                else:
                    pass

            else:
                if self.d_5g_high_freq["CHANNEL"] != s_channel:
                    self.d_5g_high_freq["CHANNEL"] = s_channel
                    self.d_5g_high_freq["CHANNEL_UPDATE"] = 1
                    i_update = 1
                else:
                    pass

                if self.d_5g_high_freq["BANDWIDTH"] != s_bandwidth:
                    self.d_5g_high_freq["BANDWIDTH"] = s_bandwidth
                    self.d_5g_high_freq["BANDWIDTH_UPDATE"] = 1
                    i_update = 1
                else:
                    pass

            if i_update:
                s_dbg_str = "Wireless Channel        : " \
                            + s_chan_dbg
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                s_dbg_str = "         Bandwidth      : " \
                            + s_bandwidth
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
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

        if i_onoff_flg:
            s_param = "Disabled"
            i_onoff_flg = 0
        else:
            s_param = "Enabled"
            i_onoff_flg = 1

        if "UPDATE" == s_method:
            if self.i_broadcast_ssid != i_onoff_flg:
                s_dbg_str = "Broadcast SSID          : " \
                            + s_param
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                self.i_broadcast_ssid = i_onoff_flg
                self.i_broadcast_ssid_update = 1
                return COM_DEF.i_RET_SUCCESS + 1
            else:
                pass
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief update the basic page of each band
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param d_freq    the parameters of each frequency
    # @param s_url_key    the key for getting url
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def update_channel_basic_page(self, s_method, i_wait_time,
                                  d_freq, s_url_key):

        i_update = COM_DEF.i_RET_SUCCESS

        if 'id=13' == s_url_key:
            i_band_flg = 0
        else:
            i_band_flg = 1

        # get frequency basic page
        freq_page = get_urlInfo(self.sel_func,
                                self.Dbg,
                                self.top_page,
                                self.s_AP_IpAddr,
                                s_url_key)
        if "" == freq_page:
            # re-login buffalo ap
            i_ret = start_loginProcedure(self.sel_func,
                                         2,
                                         self.Dbg,
                                         self.login_page,
                                         self.top_page,
                                         self.s_User,
                                         self.s_Password)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to re-login AP")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                freq_page = get_urlInfo(self.sel_func,
                                        self.Dbg,
                                        self.top_page,
                                        self.s_AP_IpAddr,
                                        s_url_key)
                if i_ret < COM_DEF.i_RET_SUCCESS:
                    self.Dbg.log(COM_DEF.DEBUG, "failed to get URL info")
                    return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        # open each frequency basic page
        i_ret = self.sel_func.setPage(freq_page)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.DEBUG,
                         "failed to get freqency basic page : %s" %
                         (s_url_key))
            return i_ret
        else:
            pass

        # change frame
        s_xpath = "//frame[@name='frm']"
        i_ret = self.sel_func.ctrl_switch_to_frame(s_xpath, 2)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.DEBUG, "failed to switch frame")
            return ""
        else:
            self.Dbg.log(COM_DEF.DEBUG, "switch frame...")

        # --------------------------------------------------
        # check whether 11n parameter is updated
        # --------------------------------------------------
        if d_freq["11N_STATUS_UPDATE"]:

            d_freq["11N_STATUS_UPDATE"] = 0

            if 0 == i_band_flg:
                s_xpath = "//span[@id='adt_wlan_gmode']/select[@name='gmode']"
            else:
                s_xpath = "//span[@id='adt_wlan_amode']/select[@name='amode']"

            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 s_xpath,
                                                 i_wait_time,
                                                 d_freq["11N_STATUS"])
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, d_freq["11N_STATUS"]))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update 11n status : %s" %
                             (d_freq["11N_STATUS"]))
                i_update = 1
            else:
                pass
        else:
            pass

        # --------------------------------------------------
        # check whether channel is updated
        # --------------------------------------------------
        if d_freq["CHANNEL_UPDATE"]:

            d_freq["CHANNEL_UPDATE"] = 0

            s_xpath = "//select[@name='channel']"

            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 s_xpath,
                                                 i_wait_time,
                                                 d_freq["CHANNEL"])
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, d_freq["CHANNEL"]))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update channel : %s" %
                             (d_freq["CHANNEL"]))
                i_update = 1
            else:
                pass

            if 0 == i_band_flg:
                self.s_cur_2g_channel = d_freq["CHANNEL"]
            else:
                self.s_cur_5g_channel = d_freq["CHANNEL"]
        else:
            pass

        # --------------------------------------------------
        # check whether bandwidth is updated
        # --------------------------------------------------
        if d_freq["BANDWIDTH_UPDATE"]:

            d_freq["BANDWIDTH_UPDATE"] = 0

            s_xpath = "//select[@id='ex_channel']"

            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 s_xpath,
                                                 i_wait_time,
                                                 d_freq["BANDWIDTH"])
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, d_freq["BANDWIDTH"]))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update bandwidth : %s" %
                             (d_freq["BANDWIDTH"]))
                i_update = 1
            else:
                pass
        else:
            pass

        if i_update:

            i_ret = save_config(self.sel_func,
                                i_wait_time,
                                self.Dbg,
                                'SETUP',
                                'open')
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG,
                             "%s : failed to save config" % s_method)
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass
        else:
            pass

        return i_update

    ##
    # @brief control radio on/off
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update (default 20sec)
    # @param i_onoff_flg   0 : "OFF"  1: "ON"
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def radio(self, s_method, i_wait_time, l_com_hdr, i_onoff_flg):

        i_update = COM_DEF.i_RET_SUCCESS
        i_chg_ssid = 0
        url_list = []
        freq_list = []
        l_wireless_band_xpath = []
        s_cur_freq_dbg = ""

        # ----------------------------------------------
        # check whether basic frequency info is or not
        # ----------------------------------------------
        self.Dbg.log(COM_DEF.DEBUG, "radio                  : " +
                     str(i_onoff_flg))
        self.Dbg.log(COM_DEF.DEBUG, "current 2g channel     : " +
                     self.s_cur_2g_channel)
        self.Dbg.log(COM_DEF.DEBUG, "current 5g channel     : " +
                     self.s_cur_5g_channel)
        self.Dbg.log(COM_DEF.DEBUG, "2g channel     update  : " +
                     str(self.d_2g_freq["CHANNEL_UPDATE"]))
        self.Dbg.log(COM_DEF.DEBUG, "5g low channel update  : " +
                     str(self.d_5g_low_freq["CHANNEL_UPDATE"]))
        self.Dbg.log(COM_DEF.DEBUG, "5g high channel update : " +
                     str(self.d_5g_high_freq["CHANNEL_UPDATE"]))

        if "2.4GHz" == self.s_cur_freq and \
            (self.d_2g_freq["11N_STATUS_UPDATE"] or
             self.d_2g_freq["CHANNEL_UPDATE"] or
             self.d_2g_freq["BANDWIDTH_UPDATE"]):
            url_list.append('id=13')
            freq_list.append(self.d_2g_freq)
        else:
            pass

        if "5GHz" == self.s_cur_freq and  \
            (self.d_5g_low_freq["11N_STATUS_UPDATE"] or
             self.d_5g_low_freq["CHANNEL_UPDATE"] or
             self.d_5g_low_freq["BANDWIDTH_UPDATE"]):
            url_list.append('id=16')
            freq_list.append(self.d_5g_low_freq)
        else:
            pass

        if "5GHz" == self.s_cur_freq and  \
            (self.d_5g_high_freq["11N_STATUS_UPDATE"] or
             self.d_5g_high_freq["CHANNEL_UPDATE"] or
             self.d_5g_high_freq["BANDWIDTH_UPDATE"]):
            url_list.append('id=19')
            freq_list.append(self.d_5g_high_freq)
        else:
            pass

        # ------------------------------------------------------
        # start to change basic frequency parameter
        # ------------------------------------------------------

        for i_cnt in range(len(url_list)):

            i_ret = self.update_channel_basic_page(s_method,
                                                   i_wait_time,
                                                   freq_list[i_cnt],
                                                   url_list[i_cnt])
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR, "failed to set basic channel")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

        # for loop end

        # ------------------------------------------------------
        # start to change common parameter
        # ------------------------------------------------------

        # get ssid page
        ssid_page = get_urlInfo(self.sel_func,
                                self.Dbg,
                                self.top_page,
                                self.s_AP_IpAddr,
                                'id=21')
        if "" == ssid_page:
            # re-login buffalo ap
            i_ret = start_loginProcedure(self.sel_func,
                                         2,
                                         self.Dbg,
                                         self.login_page,
                                         self.top_page,
                                         self.s_User,
                                         self.s_Password)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to re-login AP")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                ssid_page = get_urlInfo(self.sel_func,
                                        self.Dbg,
                                        self.top_page,
                                        self.s_AP_IpAddr,
                                        'id=21')
                if "" == ssid_page:
                    self.Dbg.log(COM_DEF.DEBUG, "failed to get ssid page")
                    return COM_DEF.i_RET_SYSTEM_ERROR
                else:
                    pass
        else:
            pass

        # open or create edit page
        i_ret, self.s_tagName = editPage(self.sel_func,
                                         2,
                                         self.Dbg,
                                         ssid_page,
                                         1)
        if i_ret < COM_DEF.i_RET_SUCCESS:
            self.Dbg.log(COM_DEF.DEBUG, "failed to get edit page")
        else:
            pass

        # --------------------------------------------------
        # check whether ssid is updated
        # --------------------------------------------------
        if self.i_ssid_update:

            self.i_ssid_update = 0
            i_update = 1
            i_chg_ssid = 1

            s_xpath = "//input[@id='adt_ssid_manssid']"
            i_ret = self.sel_func.ctrl_textBox(s_method,
                                               s_xpath,
                                               i_wait_time,
                                               self.s_ssid)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set %s to text box" %
                             (s_method, self.s_ssid))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG, "Update ssid : %s" %
                             (self.s_ssid))
            else:
                pass
        else:
            pass

        # --------------------------------------------------
        # check whether broadcast ssid is updated
        # --------------------------------------------------
        if self.i_broadcast_ssid_update:

            self.i_broadcast_ssid_update = 0
            i_update = 1

            s_xpath = "//td[@class='tbl']/input[@id='adt_hydessid']"
            i_ret = self.sel_func.ctrl_checkbox(s_method,
                                                s_xpath,
                                                i_wait_time,
                                                self.i_broadcast_ssid)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to set checkbox")
                return i_ret
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update broadcast ssid : %d" %
                             (self.i_broadcast_ssid))
            else:
                pass
        else:
            pass

        # --------------------------------------------------
        # check whether wireless authentication is updated
        # --------------------------------------------------
        if self.i_auth_mode_update:

            self.i_auth_mode_update = 0
            i_update = 1

            s_xpath = "//select[@id='authmode_id']"
            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 s_xpath,
                                                 i_wait_time,
                                                 self.s_auth_mode)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, self.s_auth_mode))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update wireless authentication : %s" %
                             (self.s_auth_mode))
            else:
                pass
        else:
            pass

        # -----------------------------------------
        # check whether encryption type is updated
        # -----------------------------------------
        if self.i_encrypto_type_update:

            self.i_encrypto_type_update = 0
            i_update = 1

            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 self.encrypto_xpath,
                                                 i_wait_time,
                                                 self.s_encrypto_type)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, self.s_encrypto_type))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update encryption type : %s"
                             (self.s_encrypto_type))
            else:
                pass
        else:
            pass

        # -----------------------------------------
        # check whether wep key type is updated
        # -----------------------------------------
        if self.i_wep_key_type_update:

            self.i_wep_key_type_update = 0
            i_update = 1

            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 self.wepkey_type_xpath,
                                                 i_wait_time,
                                                 self.s_wep_key_type)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, self.s_wep_key_type))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update wep key type : %s" %
                             (self.s_wep_key_type))
            else:
                pass
        else:
            pass

        # -----------------------------------------
        # check whether wep key index is updated
        # -----------------------------------------
        if self.i_wep_key_idx_update:

            self.i_wep_key_idx_update = 0
            i_update = 1

            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 self.wepkey_idx_xpath,
                                                 i_wait_time,
                                                 self.s_wep_key_idx)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, self.s_wep_key_idx))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update wep key index : %s" %
                             (self.s_wep_key_idx))
            else:
                pass
        else:
            pass

        # -----------------------------------------
        # check whether wep key is updated
        # -----------------------------------------
        if self.i_wep_key_update:

            self.i_wep_key_update = 0
            i_update = 1

            # if other encryption key is remained,
            # buffalo ap occur wep key length abnormal.
            # by using following code, it erase other encryption key
            for i_cnt in range(4):

                s_wepkey_xpath = "//tr[@id='adt_key" + \
                                 str(i_cnt) + \
                                 "']/td[@class='tbl']" + \
                                 "/input[@name='key" + \
                                 str(i_cnt) + \
                                 "']"
                if self.wepkey_xpath == s_wepkey_xpath:
                    s_wep_key = self.s_wep_key
                else:
                    s_wep_key = ''

                i_ret = self.sel_func.ctrl_textBox(s_method,
                                                   s_wepkey_xpath,
                                                   i_wait_time,
                                                   s_wep_key)
                if i_ret < COM_DEF.i_RET_SUCCESS:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "%s : failed to select %s"
                                 (s_method, self.s_wep_key))
                    return COM_DEF.i_RET_SYSTEM_ERROR
                elif i_ret:
                    if self.wepkey_xpath == s_wepkey_xpath:
                        self.Dbg.log(COM_DEF.DEBUG,
                                     "Update wep key : %s" %
                                     (self.s_wep_key))
                    else:
                        pass
                else:
                    pass
        else:
            pass

        # -----------------------------------------
        # check whether pre-shared key is updated
        # -----------------------------------------
        if self.i_psk_update:

            self.i_psk_update = 0
            i_update = 1

            i_ret = self.sel_func.ctrl_textBox(s_method,
                                               self.psk_xpath,
                                               i_wait_time,
                                               self.s_psk)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, self.s_psk))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update pre-shared key : %s" %
                             (self.s_psk))
            else:
                pass
        else:
            pass

        # -----------------------------------------------------
        # check whether protected management frame is updated
        # -----------------------------------------------------
        if self.i_pmf_update:

            self.i_pmf_update = 0
            i_update = 1

            if "wpa2-psk" == self.s_auth_mode:
                self.pmf_xpath = "//td[@id='adt_mfp']/select[@name='mfp']"
            elif "wpa3-sae" == self.s_auth_mode:
                self.pmf_xpath = "//td[@id='adt_mfp4']/select[@name='mfp4']"
            elif "wpa3-wpa2" == self.s_auth_mode:
                self.pmf_xpath = "//td[@id='adt_mfp3']/select[@name='mfp3']"
            elif "wpa2-ent" == self.s_auth_mode:
                self.pmf_xpath = "//td[@id='adt_mfp2']/select[@name='mfp2']"
            elif "wpa3-ent" == self.s_auth_mode:
                self.pmf_xpath = "//td[@id='adt_mfp5']/select[@name='mfp5']"
            elif "mixed-23-ent" == self.s_auth_mode:
                self.pmf_xpath = "//td[@id='adt_mfp3']/select[@name='mfp3']"
            elif "wpa3-192ent" == self.s_auth_mode:
                self.pmf_xpath = "//td[@id='adt_mfp5']/select[@name='mfp5']"
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : unexpected auth mode" % self.s_auth_mode)
                return COM_DEF.i_RET_SYSTEM_ERROR

            i_ret = self.sel_func.ctrl_selectBox(s_method,
                                                 self.pmf_xpath,
                                                 i_wait_time,
                                                 self.s_pmf)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to select %s" %
                             (s_method, self.s_pmf))
                return COM_DEF.i_RET_SYSTEM_ERROR
            elif i_ret:
                self.Dbg.log(COM_DEF.DEBUG,
                             "Update protected management frame : %s" %
                             (self.s_pmf))
            else:
                pass
        else:
            pass

        if "2.4GHz" == self.s_cur_freq:
            s_cur_freq_dbg = "2.4GHz"
            l_wireless_band_xpath.append("//input[@id='adt_device1']")
        else:
            if i_onoff_flg:
                i_channel = int(self.s_cur_5g_channel)
                if i_channel < 100:
                    s_cur_freq_dbg = "5GHz Low"
                    l_wireless_band_xpath.append("//input[@id='adt_device2']")
                else:
                    s_cur_freq_dbg = "5GHz High"
                    l_wireless_band_xpath.append("//input[@id='adt_device3']")
            else:
                s_cur_freq_dbg = "5GHz Low/High"
                l_wireless_band_xpath.append("//input[@id='adt_device2']")
                l_wireless_band_xpath.append("//input[@id='adt_device3']")

        # ----------------------------------------------
        # wireless interface is updated
        # ----------------------------------------------
        for s_xpath in l_wireless_band_xpath:

            self.Dbg.log(COM_DEF.DEBUG,
                         "band xpath    : " + s_xpath)
            self.Dbg.log(COM_DEF.DEBUG,
                         "radio status  : " + str(i_onoff_flg))

            # control radio
            i_ret = self.sel_func.ctrl_checkbox(s_method,
                                                s_xpath,
                                                i_wait_time,
                                                i_onoff_flg)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to set checkbox")
                return i_ret
            elif i_ret:
                if "UPDATE" == s_method:
                    s_dbg_str = "Wireless band           : " \
                                + s_cur_freq_dbg
                    self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                    i_update = 1
                else:
                    pass
            else:
                pass

            # interface
            if i_ret:
                if i_onoff_flg:
                    s_value = 'set'
                    s_radio_dbg = "Enable"
                else:
                    s_value = 'none'
                    s_radio_dbg = "Disable"
                s_xpath = "//input[@type='radio' and @value='" \
                          + s_value + "']"
                i_ret = self.sel_func.ctrl_radioButton(s_method,
                                                       s_xpath,
                                                       i_wait_time)
                if i_ret < COM_DEF.i_RET_SUCCESS:
                    self.Dbg.log(COM_DEF.DEBUG, "failed to set inferface")
                    return i_ret
                elif i_ret:
                    if "UPDATE" == s_method:
                        s_dbg_str = "Wireless                : " \
                                    + s_radio_dbg
                        self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                    else:
                        pass
                else:
                    pass
            else:
                pass

            if i_update:

                if i_chg_ssid:
                    s_edit_pattern = 'create'
                else:
                    s_edit_pattern = 'open'

                # save config
                i_ret = save_config(self.sel_func,
                                    i_wait_time,
                                    self.Dbg,
                                    self.s_tagName,
                                    s_edit_pattern)
                if i_ret < COM_DEF.i_RET_SUCCESS:
                    self.Dbg.log(COM_DEF.DEBUG,
                                 "%s : failed to save config" %
                                 (s_method))
                    return COM_DEF.i_RET_SYSTEM_ERROR
                else:
                    self.Dbg.log(COM_DEF.INFO, "save config...")

                time.sleep(1)

                # re-login buffalo ap
                i_ret = start_loginProcedure(self.sel_func,
                                             2,
                                             self.Dbg,
                                             self.login_page,
                                             self.top_page,
                                             self.s_User,
                                             self.s_Password)
                if i_ret < COM_DEF.i_RET_SUCCESS:
                    self.Dbg.log(COM_DEF.DEBUG, "failed to login AP")
                    return i_ret
                else:
                    ssid_page = get_urlInfo(self.sel_func,
                                            self.Dbg,
                                            self.top_page,
                                            self.s_AP_IpAddr,
                                            'id=21')
                    if "" == ssid_page:
                        self.Dbg.log(COM_DEF.DEBUG,
                                     "failed to get ssid page")
                        return COM_DEF.i_RET_SYSTEM_ERROR
                    else:
                        i_ret, self.s_tagName = editPage(self.sel_func,
                                                         2,
                                                         self.Dbg,
                                                         ssid_page,
                                                         1)
                        if i_ret < COM_DEF.i_RET_SUCCESS:
                            self.Dbg.log(COM_DEF.DEBUG,
                                         "failed to get edit page")
                            return i_ret
                        else:
                            pass
            else:
                if 'UPDATE' == s_method:
                    self.Dbg.log(COM_DEF.INFO, "Update is none...")
                else:
                    pass
        # for loop end

        return i_update

    ##
    # @brief get the connected station list
    # @param l_com_hdr    command header parameter
    # @param html   html page info
    # @retval i_cnt    the number of datalist \n
    # @retval DataList    the mac address list of station
    def getStalist(self, l_com_hdr, html):

        l_macAddr = []

        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all('td'):
            if ':' in tag.text and 17 == len(tag.text):
                l_macAddr.append(tag.text)
            else:
                pass
        # for loop end

        self.Dbg.log(COM_DEF.DEBUG, "mac address list : " + str(l_macAddr))

        i_cnt = 0
        l_list_tlv = []
        for s_mac in l_macAddr:
            d_list_tlv = {}
            d_list_tlv["MacAddress"] = s_mac
            s_dbg_str = "MAC Address [" + str(i_cnt) + "] : " + s_mac
            self.Dbg.log(COM_DEF.DEBUG, s_dbg_str)
            l_list_tlv.append(d_list_tlv)
            i_cnt += 1
        # for loop end

        self.Dbg.log(COM_DEF.DEBUG, "NumOfSta = " + str(i_cnt))
        self.Dbg.log(COM_DEF.DEBUG, "MacList  = " + str(l_list_tlv))

        return i_cnt, l_list_tlv

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

        if "2.4GHz" == self.s_cur_freq:
            if i_onoff_flg:
                s_set_param = "11bgn"
            else:
                s_set_param = "11bg"

            if 'UPDATE' == s_method:
                if self.d_2g_freq["11N_STATUS"] != s_set_param:
                    s_dbg_str = "Band                    : " \
                                + s_set_param
                    self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                    self.d_2g_freq["11N_STATUS"] = s_set_param
                    self.d_2g_freq["11N_STATUS_UPDATE"] = 1
                    return COM_DEF.i_RET_SUCCESS + 1
                else:
                    pass
            else:
                pass
        else:
            if i_onoff_flg:
                s_set_param = "11a/n/ac"
            else:
                s_set_param = "11a"

            if 'UPDATE' == s_method:
                s_dbg_str = "Band                    : " \
                            + s_set_param
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                if "" == self.s_cur_5g_channel:
                    if self.d_5g_low_freq["11N_STATUS"] != s_set_param:
                        self.d_5g_low_freq["11N_STATUS"] = s_set_param
                        self.d_5g_low_freq["11N_STATUS_UPDATE"] = 1
                    else:
                        pass

                    if self.d_5g_high_freq["11N_STATUS"] != s_set_param:
                        self.d_5g_high_freq["11N_STATUS"] = s_set_param
                        self.d_5g_high_freq["11N_STATUS_UPDATE"] = 1
                    else:
                        pass

                    if self.d_5g_low_freq["11N_STATUS_UPDATE"] or \
                            self.d_5g_high_freq["11N_STATUS_UPDATE"]:
                        return COM_DEF.i_RET_SUCCESS + 1
                    else:
                        return COM_DEF.i_RET_SUCCESS
                else:
                    if int(self.s_cur_5g_channel) < 100 and \
                           self.d_5g_low_freq["11N_STATUS"] != s_set_param:
                        self.d_5g_low_freq["11N_STATUS"] = s_set_param
                        self.d_5g_low_freq["11N_STATUS_UPDATE"] = 1
                        return COM_DEF.i_RET_SUCCESS + 1
                    elif self.d_5g_high_freq["11N_STATUS"] != s_set_param:
                        self.dbg.dbg_info(l_com_hdr, s_dbg_str)
                        self.d_5g_high_freq["11N_STATUS"] = s_set_param
                        return COM_DEF.i_RET_SUCCESS + 1
                    else:
                        pass
            else:
                pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief start or stop dhcpd
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_ctrl_str   "0": disabled "1": enabled
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def dhcpd(self, s_method, i_wait_time, l_com_hdr, s_ctrl_str):

        xpath_dhcpd = "//select[@name='dhcps_use']"
        if "1" == s_ctrl_str:
            s_dbg = "Deploy own DHCP server"
        else:
            s_dbg = "Disabled"

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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def startIPaddr(self, s_method, i_wait_time, l_com_hdr, s_startIp):

        xpath_startAddr = "//input[@id='mandhcpstart_id']"

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
                s_dbg_str = "Address assignment       : %s" % \
                            (s_startIp)
                self.dbg.dbg_info(l_com_hdr, s_dbg_str)
            else:
                pass

        return i_ret

    ##
    # @brief set the number of assigned ip address
    # @param s_method     "UPDATE" or "CHECK"
    # @param i_wait_time    wait time for web update
    # @param s_assign_num   the number of assigned ip address
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def assignNum(self, s_method, i_wait_time, l_com_hdr, s_assign_num):

        xpath_assignNum = "//input[@id='mandhcpnum_id']"

        i_ret = self.sel_func.ctrl_textBox(s_method,
                                           xpath_assignNum,
                                           i_wait_time,
                                           s_assign_num)
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG,
                         "%s : failed to set %s to text box" %
                         (s_method, s_assign_num))
        else:
            if "UPDATE" == s_method:
                s_dbg_str = "Numer of ip address      : %s" % \
                            (s_assign_num)
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
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def leaseTime(self, s_method, i_wait_time, l_com_hdr, s_leaseTime):

        xpath_lease = "//input[@name='lstime']"

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
                s_dbg_str = \
                    "Lease Time               : %s" % (s_leaseTime)
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
    # @param s_lease      lease time (sec)
    # @param s_gateway   gateway ip address
    # @retval i_ret    response data \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def dhcpd_param(self, s_method, i_wait_time, l_com_hdr,
                    s_start_ip, s_netmask, i_assign_num, s_lease, s_gateway):

        i_update = COM_DEF.i_RET_SUCCESS

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

            # assigned number of ip address
            i_ret = self.assignNum(self,
                                   s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   str(i_assign_num))
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set assign num : %d" %
                             (s_method, i_assign_num))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

            # lease time
            i_lease_time = int(s_lease)
            if i_lease_time < 3600:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set lease time : %s" %
                             (s_method, s_lease))
                return COM_DEF.i_RET_TLV_ABNORMAL
            else:
                s_lease_hour = str(i_lease_time/3600)

            i_ret = self.leaseTime(self,
                                   s_method,
                                   i_wait_time,
                                   l_com_hdr,
                                   s_lease_hour)
            if COM_DEF.i_RET_SUCCESS > i_ret:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s : failed to set lease time : %s" %
                             (s_method, s_lease_hour))
                return i_ret
            elif i_ret:
                i_update = 1
            else:
                pass

            # dhcpd enable
            s_ctrl_str = "1"

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

        if i_update:

            i_ret = save_config(self.sel_func,
                                i_wait_time,
                                self.Dbg,
                                'SETUP',
                                'open')
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG,
                             "%s : failed to save config" %
                             s_method)
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

            # re-login buffalo ap
            i_ret = start_loginProcedure(self.sel_func,
                                         2,
                                         self.Dbg,
                                         self.login_page,
                                         self.top_page,
                                         self.s_User,
                                         self.s_Password)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to re-login AP")
                return i_ret
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
    #                   - Success : COM_DEF.i_RET_SUCCESS \n
    #                   - Failure : Value other than
    #                               COM_DEF.i_RET_SUCCESS
    def ctrl_quit(self):

        for cnt in range(3):

            # get ssid page
            ssid_page = get_urlInfo(self.sel_func,
                                    self.Dbg,
                                    self.top_page,
                                    self.s_AP_IpAddr,
                                    'id=21')
            if "" == ssid_page:
                self.Dbg.log(COM_DEF.DEBUG,
                             "failed to get ssid page : %d" %
                             (cnt))

                # re-login buffalo ap
                i_ret = start_loginProcedure(self.sel_func,
                                             2,
                                             self.Dbg,
                                             self.login_page,
                                             self.top_page,
                                             self.s_User,
                                             self.s_Password)
                if i_ret < COM_DEF.i_RET_SUCCESS:
                    self.Dbg.log(COM_DEF.DEBUG, "failed to re-login AP")
                else:
                    pass
            else:
                self.Dbg.log(COM_DEF.DEBUG, "edit page=" + ssid_page)
                break
        # for loop end

        if "" != ssid_page:

            # delete edit page
            i_ret, s_tagName = editPage(self.sel_func,
                                        2,
                                        self.Dbg,
                                        ssid_page,
                                        0)
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to delete edit page")
            else:
                pass

            i_ret = save_config(self.sel_func,
                                10,
                                self.Dbg,
                                self.s_tagName,
                                "delete")
            if i_ret < COM_DEF.i_RET_SUCCESS:
                self.Dbg.log(COM_DEF.DEBUG, "failed to submit")
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

        else:
            pass

        # release web driver resource
        i_ret = self.sel_func.ctrl_quit()
        if i_ret < 0:
            self.Dbg.log(COM_DEF.DEBUG, "failed to quit driver")
        else:
            pass

        return i_ret
