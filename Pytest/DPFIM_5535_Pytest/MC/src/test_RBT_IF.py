# -*- coding: utf-8 -*-
import time
import json
import sys
import os
import pytest
import subprocess
import unittest
from mock import Mock
from mock import MagicMock
import collections
from collections import OrderedDict


sys.path.append('../../Others/device/AIRCAP/sub/')
sys.path.append('../../Common/debug/')
sys.path.append('../../Common/debug/json/')
sys.path.append('../../Common/decode_encode/')
sys.path.append('../../Common/interface')
sys.path.append('../../Common/inc')
sys.path.append('./class/')
sys.path.append('./class/sub_func')
sys.path.append('./')
sys.path.append('./common')

from Debug import Debug_Init
from Debug import Debug_GetObj
from RBT_IF import RBT_IF
import json
import sys
import threading
import logging
from mock import Mock
from CLS_Define import COM_DEF
from TEST_CTRL import TEST_CTRL
from CLS_Define import COM_DEF

rbt = RBT_IF()
Debug_Init = Mock(return_value=COM_DEF.i_RET_SUCCESS)
Debug_getObj=Mock(return_value=logging.getLogger('test'))
TEST_CTRL.init_env=Mock(return_value={"Result":"OK"})

rbt.Request_test_controller_start('test')

def Mock_call():
    #for attach and detach function

    Debug_Init = Mock(return_value=COM_DEF.i_RET_SUCCESS)

def Mock_count():
     print("[Call count] TEST_CTRL.start_capture_log " + str(TEST_CTRL.start_capture_log))

@pytest.mark.one
def test_Request_log_start():
    print()
    print("TEST Order: Request_log_start function call")
    Mock_call()

    s_test_name = "001_001_02_01"
    TEST_CTRL.start_capture_log=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_log_start(s_test_name)

    print("[In] s_test_name: " + str(s_test_name))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Request_log_stop():
    print()
    print("TEST Order: Request_log_stop function call")
    Mock_call()

    s_test_name = "001_001_02_01"
    TEST_CTRL.stop_capture_log=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_log_stop()

    print("[In] s_test_name: " + str(s_test_name))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Request_flush_command():
    print()
    print("TEST Order: Request_flush_command function call")
    Mock_call()

    TEST_CTRL.flush_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_flush_command()

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Request_reset_to():
    print()
    print("TEST Order: Request_reset_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_reset_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_initialization_to():
    print()
    print("TEST Order: Request_initialization_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_initialization_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_termination_to():
    print()
    print("TEST Order: Request_termination_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_termination_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_country_code_to():
    print()
    print("TEST Order: Set_country_code_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_country_code_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_country_code_from():
    print()
    print("TEST Order: Get_country_code_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_country_code_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_disconnection_to():
    print()
    print("TEST Order: Request_disconnection_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_disconnection_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_rssi_from():
    print()
    print("TEST Order: Get_rssi_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_rssi_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_macaddr_from():
    print()
    print("TEST Order: Get_macaddr_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_macaddr_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"




def test_Get_ip_from():
    print()
    print("TEST Order: Get_ip_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_ip_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_ping_to():
    print()
    print("TEST Order: Request_ping_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_ping_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_iperf_to():
    print()
    print("TEST Order: Request_iperf_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_iperf_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_iperf_server_stop_to():
    print()
    print("TEST Order: Request_iperf_server_stop_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_iperf_server_stop_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_channel_info_from():
    print()
    print("TEST Order: Get_channel_info_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_channel_info_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_channel_list_from():
    print()
    print("TEST Order: Get_channel_list_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_channel_list_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_send_rate_from():
    print()
    print("TEST Order: Get_send_rate_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_send_rate_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_bandwidth_to():
    print()
    print("TEST Order: Set_bandwidth_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_bandwidth_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_bandwidth_from():
    print()
    print("TEST Order: Get_bandwidth_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_bandwidth_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_firmware_version_from():
    print()
    print("TEST Order: Get_firmware_version_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_firmware_version_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_rx_packet_counter_from():
    print()
    print("TEST Order: Get_rx_packet_counter_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_rx_packet_counter_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_band_to():
    print()
    print("TEST Order: Set_band_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_band_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_band_from():
    print()
    print("TEST Order: Get_band_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_band_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_frameburst_mode_to():
    print()
    print("TEST Order: Set_frameburst_mode_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_frameburst_mode_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_frameburst_mode_from():
    print()
    print("TEST Order: Get_frameburst_mode_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_frameburst_mode_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_11ac_mode_to():
    print()
    print("TEST Order: Set_11ac_mode_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_11ac_mode_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_11ac_mode_from():
    print()
    print("TEST Order: Get_11ac_mode_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_11ac_mode_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_11n_mode_to():
    print()
    print("TEST Order: Set_11n_mode_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_11n_mode_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_11n_mode_from():
    print()
    print("TEST Order: Get_11n_mode_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_11n_mode_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_event_wait_to():
    print()
    print("TEST Order: Request_event_wait_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_event_wait_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Get_target_value():
    print()
    print("TEST Order: Get_target_value function call")
    Mock_call()
    rt_params={"DeviceID":"NETWORKTOOL","SSID":"DUT_AP"}
    DeviceID="NETWORKTOOL"
    target_key="SSID"
    target_value="DUT_AP"

    lenx,i_ret = rbt.Get_target_value(rt_params,DeviceID,target_key,target_value)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret[0]== "DUT_AP"
    assert lenx == 1

def test_Get_target_scandata():
    print()
    print("TEST Order: Get_target_scandata function call")
    Mock_call()
    scan_results={}
    scan_results["DataList"]=[{"SSID":"DUT_AP"},{"SSID2":"DUT_AP2"}]
    target_key="SSID"
    target_value="DUT_AP"

    lenx,i_ret = rbt.Get_target_scandata(scan_results,target_key,target_value)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret[0]["SSID"] == "DUT_AP"
    assert lenx == 1

def test_Get_target_scandata_2():
    print()
    print("TEST Order: Get_target_scandata function call")
    Mock_call()
    scan_results={}
    scan_results["DataList"]=[{"SSID":"DUT_AP"},{"SSID2":"DUT_AP2"}]
    target_key="SSID"
    target_value="DUT_AP3"

    lenx,i_ret = rbt.Get_target_scandata(scan_results,target_key,target_value)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert lenx == 0

def test_Set_ip_to():
    print()
    print("TEST Order: Set_ip_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL","UseMethod":1}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_ip_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Set_ip_to2():
    print()
    print("TEST Order: Set_ip_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_ip_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_Request_sleep_to():
    print()
    print("TEST Order: Request_sleep_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":COM_DEF.i_RET_WAIT_NEXT_CMD})
    i_ret = rbt.Request_sleep_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS


def test_Request_sleep_to2():
    print()
    print("TEST Order: Request_sleep_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_sleep_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Request_scan_to():
    print()
    print("TEST Order: Request_scan_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_scan_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_scanresults_from():
    print()
    print("TEST Order: Get_scanresults_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_scanresults_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_connection_to():
    print()
    print("TEST Order: Request_connection_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_connection_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_ap_info_from():
    print()
    print("TEST Order: Get_ap_info_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_ap_info_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_powersave_mode_to():
    print()
    print("TEST Order: Set_powersave_mode_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_powersave_mode_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_powersave_mode_from():
    print()
    print("TEST Order: Get_powersave_mode_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_powersave_mode_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_ssid_to():
    print()
    print("TEST Order: Set_ssid_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_ssid_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_security_to():
    print()
    print("TEST Order: Set_security_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_security_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_hidden_ssid_to():
    print()
    print("TEST Order: Set_hidden_ssid_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_hidden_ssid_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_radio_out_to():
    print()
    print("TEST Order: Request_radio_out_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_radio_out_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Get_macaddr_list_from():
    print()
    print("TEST Order: Get_macaddr_list_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_macaddr_list_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_max_connections_to():
    print()
    print("TEST Order: Request_max_connections_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_max_connections_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Set_channel_info_to():
    print()
    print("TEST Order: Set_channel_info_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Set_channel_info_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"



def test_Request_packet_capture_stop_to():
    print()
    print("TEST Order: Request_packet_capture_stop_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_packet_capture_stop_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_packet_decrypt_to():
    print()
    print("TEST Order: Request_packet_decrypt_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_packet_decrypt_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_packet_check_to():
    print()
    print("TEST Order: Request_packet_check_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_packet_check_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_packet_search_to():
    print()
    print("TEST Order: Request_packet_search_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_packet_search_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Request_packet_search_to_2():
    print()
    print("TEST Order: Request_packet_search_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL","RegFlg":1}

    TEST_CTRL.register_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_packet_search_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"

def test_Get_packet_capture_from():
    print()
    print("TEST Order: Get_packet_capture_from function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL","CaptureFileName":"ABC DEF"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Get_packet_capture_from(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"


def test_Request_packet_capture_start_to():
    print()
    print("TEST Order: Request_packet_capture_start_to function call")
    Mock_call()
    d_TestParams={"DeviceId":"NETTOOL","CaptureFileName":"ABC DEF"}

    TEST_CTRL.run_testcmd=Mock(return_value={"Result":"OK"})
    i_ret = rbt.Request_packet_capture_start_to(d_TestParams)

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == "OK"
