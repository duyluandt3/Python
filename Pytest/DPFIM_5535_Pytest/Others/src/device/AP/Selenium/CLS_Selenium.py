#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control firefox web driver by selenium
# @author E2N3
# @date 2019.05.28

# -*- coding: utf-8 -*-

import time
from CLS_Define import COM_DEF
from Control import AP_ENV
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##
# @brief wait until element is presencen
# @param driver    web driver object
# @param s_xpath    xpath stirng
# @param i_clicable_wait_time   wait to presence of element
# @param debug    object for debug
# @retval i_ret    response data \n
#                         ["Result"] value of the result \n
#                           - Success : element of web page \n
#                           - Failure : error info
def wait_presence_of_element(driver, s_xpath, i_clicable_wait_time,
                             debug):

    try:
        element = WebDriverWait(driver, i_clicable_wait_time).until(
                  EC.presence_of_element_located((By.XPATH, s_xpath)))
    except Exception as err_info:
        debug.log(COM_DEF.ERROR, "Set XPATH : " + s_xpath)
        debug.log(COM_DEF.ERROR, err_info)
        return 0, str(err_info)

    return element, ""


##
# @brief Define AP related processing.
class CTRL_SELENIUM(AP_ENV):

    ##
    # @brief Run when instantiating the SUB_FUNC class.
    # @param debug    object for debug
    # @param s_model_name  AP model name. (AP folder name)
    # @retval None
    def __init__(self, s_model_name):
        super().__init__(s_model_name)

    ##
    # @brief start web driver
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def start_webdriver(self):

        for i in range(5):

            self.Dbg.log(COM_DEF.INFO,
                         "try to start web driver...%s", str(i))

            try:
                # selenium webdriver
                if "headless" in self.s_DriverMode:
                    options = FirefoxOptions()
                    options.add_argument('-headless')
                    self.driver = Firefox(options=options)
                else:
                    self.driver = Firefox()
                self.Dbg.log(COM_DEF.DEBUG,
                             "start firefox driver")
                break

            except Exception as err_info:
                self.Dbg.log(COM_DEF.DEBUG,
                             "failed to start web driver")
                self.Dbg.log(COM_DEF.ERROR, err_info)
                time.sleep(1)
        # for end

        if 5 <= i:
            self.Dbg.log(COM_DEF.ERROR,
                         "failed to start web driver")
            return COM_DEF.i_RET_SYSTEM_ERROR
        else:
            pass

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief set URL information to webdriver
    # @param s_PageString     url
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def setPage(self, s_PageString):

        try:
            self.driver.get(s_PageString)
            self.Dbg.log(COM_DEF.DEBUG, s_PageString)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "failed to get web page")
            self.Dbg.log(COM_DEF.ERROR, err_info)

            i_ret = self.start_webdriver()
            if i_ret:
                self.Dbg.log(COM_DEF.ERROR, "failed to get web driver")
            else:
                pass
            return COM_DEF.i_RET_SYSTEM_ERROR

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief get web page information
    # @retval html    html code
    def getPageSource(self):

        time.sleep(1)
        try:
            html = self.driver.page_source
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "failed to get html code")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return ""

        return html

    ##
    # @brief get current url
    # @retval url
    def getCurrentURL(self):

        try:
            url = self.driver.current_url
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "failed to get url")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return ""

        return url

    ##
    # @brief set value to textbox, check the value of text box
    # @param s_method     "UPDATE" or "CHECK"
    # @param s_xpath     xpath string
    # @param i_clicable_wait_time    wait until element is enable.
    # @param s_text_value   text value
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_textBox(self, s_method, s_xpath, i_clicable_wait_time,
                     s_text_value):

        self.Dbg.log(COM_DEF.DEBUG,
                     "method      : " + s_method)
        self.Dbg.log(COM_DEF.DEBUG,
                     "xpath       : " + s_xpath)
        self.Dbg.log(COM_DEF.DEBUG,
                     "wait        : " + str(i_clicable_wait_time))
        self.Dbg.log(COM_DEF.DEBUG,
                     "value       : " + s_text_value)

        # wait until element is presence
        element, s_err_info = \
            wait_presence_of_element(self.driver, s_xpath,
                                     i_clicable_wait_time,
                                     self.Dbg)
        if (element):
            pass
        else:
            self.Dbg.log(COM_DEF.ERROR, "can't attach to element")
            return COM_DEF.i_RET_SYSTEM_ERROR

        if "UPDATE" == s_method:
            if s_text_value == element.get_attribute('value'):
                self.Dbg.log(COM_DEF.INFO, "(" + s_xpath +
                             ") already be selected")
                return COM_DEF.i_RET_SUCCESS
            else:
                # text
                element.clear()
                element.send_keys(s_text_value)
                # update
                return COM_DEF.i_RET_SUCCESS + 1
        else:
            if s_text_value == element.get_attribute('value'):
                return COM_DEF.i_RET_SUCCESS
            else:
                self.Dbg.log(COM_DEF.ERROR, "failed to update : " +
                             s_xpath)
                return COM_DEF.i_RET_SYSTEM_ERROR

    ##
    # @brief select the value of select box, check the chosen value \n
    #        of select box
    # @param s_method     "UPDATE" or "CHECK"
    # @param s_xpath     xpath string
    # @param i_clicable_wait_time    wait until element is enable.
    # @param s_select_val   select value
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_selectBox(self, s_method, s_xpath, i_clicable_wait_time,
                       s_select_val):

        self.Dbg.log(COM_DEF.DEBUG,
                     "method      : " + s_method)
        self.Dbg.log(COM_DEF.DEBUG,
                     "xpath       : " + s_xpath)
        self.Dbg.log(COM_DEF.DEBUG,
                     "wait        : " + str(i_clicable_wait_time))
        self.Dbg.log(COM_DEF.DEBUG,
                     "value       : " + s_select_val)

        # wait until element is presence
        element, s_err_info = \
            wait_presence_of_element(self.driver, s_xpath,
                                     i_clicable_wait_time,
                                     self.Dbg)
        if (element):
            pass
        else:
            self.Dbg.log(COM_DEF.ERROR, "can't attach to element")
            return COM_DEF.i_RET_SYSTEM_ERROR

        if "UPDATE" == s_method:

            if s_select_val == element.get_attribute('value'):
                self.Dbg.log(COM_DEF.INFO, "(" + s_xpath +
                             ") already be selected")
                return COM_DEF.i_RET_SUCCESS
            else:
                select = Select(element)
                try:
                    select.select_by_value(s_select_val)
                except Exception as err_info:
                    self.Dbg.log(COM_DEF.ERROR, "failed to select value")
                    self.Dbg.log(COM_DEF.ERROR, err_info)
                    return COM_DEF.i_RET_SYSTEM_ERROR
                # update
                return COM_DEF.i_RET_SUCCESS + 1
        else:
            if s_select_val == element.get_attribute('value'):
                return COM_DEF.i_RET_SUCCESS
            else:
                self.Dbg.log(COM_DEF.ERROR, "get value : %s" %
                             (element.get_attribute('value')))
                self.Dbg.log(COM_DEF.ERROR, "failed to update : %s" %
                             (s_xpath))
                return COM_DEF.i_RET_SYSTEM_ERROR

    ##
    # @brief select the value of radio button, check the chosen \n
    #        value of radio button
    # @param s_method     "UPDATE" or "CHECK"
    # @param s_xpath     xpath string
    # @param i_clicable_wait_time    wait until element is enable.
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_radioButton(self, s_method, s_xpath, i_clicable_wait_time):

        self.Dbg.log(COM_DEF.DEBUG,
                     "method      : " + s_method)
        self.Dbg.log(COM_DEF.DEBUG,
                     "xpath       : " + s_xpath)
        self.Dbg.log(COM_DEF.DEBUG,
                     "wait        : " + str(i_clicable_wait_time))

        # wait until element is presence
        element, s_err_info = \
            wait_presence_of_element(self.driver, s_xpath,
                                     i_clicable_wait_time, self.Dbg)
        if (element):
            pass
        else:
            self.Dbg.log(COM_DEF.ERROR, "can't attach to element")
            return COM_DEF.i_RET_SYSTEM_ERROR

        if "UPDATE" == s_method:
            if element.is_selected():
                self.Dbg.log(COM_DEF.INFO,
                             "(" + s_xpath + ") already be selected")
                return COM_DEF.i_RET_SUCCESS
            else:
                try:
                    element.click()
                except Exception as err_info:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "(" + s_xpath + ") + failed to click")
                    self.Dbg.log(COM_DEF.ERROR, err_info)
                    return COM_DEF.i_RET_SYSTEM_ERROR
                # update
                return COM_DEF.i_RET_SUCCESS + 1
        else:
            if element.is_selected():
                return COM_DEF.i_RET_SUCCESS
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "failed to update : " + s_xpath)
                return COM_DEF.i_RET_SYSTEM_ERROR

    ##
    # @brief select the checkbox
    # @param s_method     "UPDATE" or "CHECK"
    # @param s_chkid     id string
    # @param i_clicable_wait_time    wait until element is enable.
    # @param i_onoff_flg    0: disabled 1: enable
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                                     : COM_DEF.i_RET_SUCCESS + 1 \n
    #                                       (Update) \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_checkbox(self, s_method, s_xpath, i_clicable_wait_time,
                      i_onoff_flg):

        self.Dbg.log(COM_DEF.DEBUG,
                     "method      : " + s_method)
        self.Dbg.log(COM_DEF.DEBUG,
                     "xpath       : " + s_xpath)
        self.Dbg.log(COM_DEF.DEBUG,
                     "wait        : " + str(i_clicable_wait_time))

        if i_onoff_flg:
            s_dbg = "True"
        else:
            s_dbg = "False"

        element, s_err_info = \
            wait_presence_of_element(self.driver, s_xpath,
                                     i_clicable_wait_time, self.Dbg)
        if (element):
            pass
        else:
            self.Dbg.log(COM_DEF.ERROR, "can't attach to element")
            return COM_DEF.i_RET_SYSTEM_ERROR

        self.Dbg.log(COM_DEF.DEBUG,
                     "change status  : " + s_dbg)
        self.Dbg.log(COM_DEF.DEBUG,
                     "current status : " + str(element.is_selected()))

        if "UPDATE" == s_method:
            if (element.is_selected() and 0 == i_onoff_flg) or \
                    (False is element.is_selected() and 1 == i_onoff_flg):
                try:
                    element.click()
                except Exception as err_info:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "failed to select checkbox : %d" %
                                 (i_onoff_flg))
                    self.Dbg.log(COM_DEF.ERROR, err_info)
                    return COM_DEF.i_RET_SYSTEM_ERROR
                # update
                return COM_DEF.i_RET_SUCCESS + 1
            else:
                self.Dbg.log(COM_DEF.DEBUG, "already is set...")
                return COM_DEF.i_RET_SUCCESS
        else:
            if (element.is_selected() and 1 == i_onoff_flg) or \
                    (False is element.is_selected() and 0 == i_onoff_flg):
                return COM_DEF.i_RET_SUCCESS
            else:
                self.Dbg.log(COM_DEF.ERROR, "failed to update checkbox")
                return COM_DEF.i_RET_SYSTEM_ERROR

    ##
    # @brief submit_button
    # @param s_xpath     xpath string
    # @param i_clicable_wait_time    wait until element is enable.
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_submit(self, s_xpath, i_clicable_wait_time):

        self.Dbg.log(COM_DEF.DEBUG,
                     "xpath       : " + s_xpath)
        self.Dbg.log(COM_DEF.DEBUG,
                     "wait        : " + str(i_clicable_wait_time))

        element, s_err_info = \
            wait_presence_of_element(self.driver, s_xpath,
                                     i_clicable_wait_time, self.Dbg)
        if (element):
            pass
        else:
            self.Dbg.log(COM_DEF.ERROR, "can't attach to element")
            return COM_DEF.i_RET_SYSTEM_ERROR

        try:
            element.click()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "(" + s_xpath + ")" +
                         "failed to click submit button")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return COM_DEF.i_RET_SYSTEM_ERROR

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief refresh page
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_refresh(self):

        try:
            self.driver.refresh()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "can't refresh...")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return COM_DEF.i_RET_SYSTEM_ERROR

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief switch_to_alert
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_switch_to_alert(self):

        try:
            alert = self.driver.switch_to_alert()
            alert.accept()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "can't switch_to_alert...")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return COM_DEF.i_RET_SYSTEM_ERROR

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief switch_to_frame
    # @param s_xpath     xpath string
    # @param i_clicable_wait_time    wait until element is enable.
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_switch_to_frame(self, s_xpath, i_clicable_wait_time):

        # wait until element is presence
        element, s_err_info = \
            wait_presence_of_element(self.driver, s_xpath,
                                     i_clicable_wait_time, self.Dbg)
        try:
            self.driver.switch_to.frame(element)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "can't switch_to_frame...")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return COM_DEF.i_RET_SYSTEM_ERROR

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief release webdriver resource
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def ctrl_quit(self):

        try:
            self.driver.quit()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "can't release resource...")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return COM_DEF.i_RET_SYSTEM_ERROR

        return COM_DEF.i_RET_SUCCESS
