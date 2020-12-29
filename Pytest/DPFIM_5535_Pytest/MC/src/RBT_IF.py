#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#
##
# @brief test suite generator
# @author E2N3
# @date 2019/12/13

# -*- coding: utf-8 -*-#

# ----- import -----
from collections import OrderedDict
import copy
import sys
from CLS_Define import COM_DEF
from TEST_CTRL import TEST_CTRL

# @cond
# store the TEST CONTROL object
TC = None
# @endcond


class RBT_IF:
#...
    """ Robotframework I/F class """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        pass

    def Request_test_controller_start(self, config_name):
        global TC

        # Initialize local variable
        d_rt_params = {}

        if None is TC:
            # generate TEST_CTRL object
            TC = TEST_CTRL()
        else:
            pass

        # initialize TEST_CTRL object
        d_rt_params = TC.init_env(config_name)

        return d_rt_params

    def Request_log_start(self, s_test_name):
        # Initialize local variable
        global TC

        d_rt_params = {}

        d_rt_params = TC.start_capture_log(s_test_name)

        return d_rt_params

    def Request_log_stop(self):
        # Initialize local variable
        global TC

        d_rt_params = {}

        d_rt_params = TC.stop_capture_log()

        return d_rt_params

    def Request_flush_command(self):
        global TC

        # Initialize local variable
        d_rt_params = {}

        d_rt_params = \
            TC.flush_testcmd()

        return d_rt_params

    def Get_target_value(self, rt_params, DeviceID, KeyName, TargetKey):

        l_result_params = []

        KeyName = KeyName.replace(' ', '_')

        if list == type(rt_params):
            for d_result_param in rt_params:
                if DeviceID in d_result_param and \
                    KeyName in d_result_param[DeviceID] and \
                        TargetKey in d_result_param[DeviceID][KeyName]:
                        l_result_params.append(
                            d_result_param[DeviceID][KeyName][TargetKey])
                elif DeviceID in d_result_param and \
                        KeyName in d_result_param[DeviceID] and \
                            "None" == TargetKey:
                            l_result_params.append(
                                d_result_param[DeviceID][KeyName])
                else:
                    pass
            # for loop end

        else:
            if dict == type(rt_params) or OrderedDict == type(rt_params):
                if TargetKey in rt_params:
                    l_result_params.append(rt_params[TargetKey])
                else:
                    pass
            else:
                pass

        return len(l_result_params), l_result_params

    def Get_target_scandata(self, scan_results, target_key, target_value):
        l_scandata_list = []
        if "DataList" in scan_results:
            for scandata in scan_results["DataList"]:
                if target_key in scandata and \
                        scandata[target_key] == target_value:
                    l_scandata_list.append(scandata)
                else:
                    pass
        else:
            pass

        return len(l_scandata_list), l_scandata_list

    def Request_reset_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_initialization_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_termination_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_country_code_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_country_code_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_disconnection_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_rssi_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_macaddr_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_ip_to(self, d_TestParams):
        d_rt_params = {}
        d_tlv_params = {}

        d_tlv_params = copy.deepcopy(d_TestParams)

        key_name = \
            sys._getframe().f_code.co_name

        if 'UseMethod' in d_tlv_params:
            use_method = \
                d_tlv_params.pop('UseMethod')

            if use_method == 1:
                key_name = "Set_ip_by_dhcp_to"
            else:
                pass

            d_rt_params = \
                self.__common_proc(key_name, d_tlv_params)

        else:
            d_rt_params['Result'] = COM_DEF.i_RET_TLV_ABNORMAL

        return d_rt_params

    def Get_ip_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_ping_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_iperf_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_iperf_server_stop_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_channel_info_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_channel_list_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_send_rate_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_bandwidth_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_bandwidth_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_firmware_version_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_rx_packet_counter_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_band_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_band_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_frameburst_mode_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_frameburst_mode_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_11ac_mode_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_11ac_mode_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_11n_mode_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_11n_mode_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_event_wait_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_sleep_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        if COM_DEF.i_RET_WAIT_NEXT_CMD == d_rt_params['Result']:
            d_rt_params['Result'] = COM_DEF.i_RET_SUCCESS
        else:
            pass

        return d_rt_params

    def Request_dhcp_server_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_mpc_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_mpc_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_scan_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_scanresults_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_connection_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_ap_info_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_powersave_mode_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_powersave_mode_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_ssid_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_security_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_hidden_ssid_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_radio_out_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_macaddr_list_from(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_max_connections_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Set_channel_info_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_packet_capture_start_to(self, d_TestParams):
        d_rt_params = {}

        d_TestParams['CaptureFileName'] = \
            d_TestParams['CaptureFileName'].replace(' ', '_')

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_packet_capture_stop_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_packet_decrypt_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_packet_check_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Get_packet_capture_from(self, d_TestParams):
        d_rt_params = {}

        d_TestParams['CaptureFileName'] = \
            d_TestParams['CaptureFileName'].replace(' ', '_')

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def Request_packet_search_to(self, d_TestParams):
        d_rt_params = {}

        key_name = \
            sys._getframe().f_code.co_name

        d_rt_params = \
            self.__common_proc(key_name, d_TestParams)

        return d_rt_params

    def __common_proc(self, key_name, d_TestParams):
        global TC

        d_rt_params = {}
        d_tlv_params = {}

        d_tlv_params = copy.deepcopy(d_TestParams)
        reg_flg = 0

        deviceid = \
            d_tlv_params.pop('DeviceId')

        if 'RegFlg' in d_TestParams:
            reg_flg = \
                d_tlv_params.pop('RegFlg')
        else:
            pass

        if reg_flg == 1:
            d_rt_params = TC.register_testcmd(deviceid,
                                              key_name,
                                              d_tlv_params)
        else:
            d_rt_params = TC.run_testcmd(deviceid,
                                         key_name,
                                         d_tlv_params)

        return d_rt_params
