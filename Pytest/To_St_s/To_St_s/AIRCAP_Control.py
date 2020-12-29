# -*- coding: utf-8 -*-
import time
import json
import sys
import os
import pytest
import subprocess
import unittest
from unittest import mock as mm
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
sys.path.append('../../Others/src/device/AIRCAP')
sys.path.append('../../Others/src/device/AIRCAP/sub')
sys.path.append('../../Others/src/common')
sys.path.append('../../Control_PC/src/class')
sys.path.append('../../Control_PC/src')
sys.path.append('../../Common/decode_encode/')
sys.path.append('../../Common/decode_encode/json/')
sys.path.append('../../Common/interface')
sys.path.append('../../Common/inc')
sys.path.append('./common')
sys.path.append('./device')
sys.path.append('./env')
sys.path.append('./device/AIRCAP/sub/')
import Chk_packet as packet
import json
import sys
import threading

from CLS_Define import COM_DEF
from tx_snd import snd_ack_cmd
from tx_snd import snd_rsp_cmd
from tx_snd import snd_req_cmd
from Debug import Logger_Init
from Debug import Logger_GetObj
from Decode_TLV import Decode_TLV
from Decode_ComHdr import Decode_ComHdr
from CLS_Socket import COM_SOCKET
import logging
from mock import Mock
import Control
from Control import AIRCAP_FUNC
import AIRCAP_main


AIRCAP_main.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
AIRCAP_main.Logger_GetStubMode = Mock(return_value=0)
Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
Control.Logger_GetStubMode = Mock(return_value=0)
air = AIRCAP_FUNC(1)


def Mock_call():
    #for attach and detach function
    packet.set_wlan_if = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    Control.snd_req_cmd = Mock()
    
    #for date function
    Control.set_base_time =Mock(return_value=COM_DEF.i_RET_SUCCESS)
    #subprocess.call = Mock()

    #for stop_aircap function
    #subprocess.Popen =Mock()

    #for confirm_stat functon
    Control.date = Mock()

    #for get_airlog
    Control.packet.make_zip_file =Mock()
    Control.packet.transfer_file =Mock()

    #for start Aircap
    Control.packet.set_channel =Mock()
    Control.packet.create_addr_filter = Mock()

    #for decrypt Aircap
    Control.packet.set_capture_file_name =Mock()

    #
    Control.packet.get_pkt_num=Mock()
    #Control.packet.search=Mock()

def Mock_count():
     print("[Call count] packet.set_wlan_if: " + str(packet.set_wlan_if.call_count))
     print("[Call count] snd_req_cmd: " + str(Control.snd_req_cmd.call_count))
     print("[Call count] Control.set_base_time: " + str(Control.set_base_time.call_count))
     print("[Call count] Control.date: " + str(Control.date.call_count))
     print("[Call count]  Control.packet.make_zip_file: " + str( Control.packet.make_zip_file.call_count))
     print("[Call count]  Control.packet.transfer_file: " + str( Control.packet.transfer_file.call_count))
     print("[Call count]  Control.packet.set_channel: " + str( Control.packet.set_channel.call_count))
     print("[Call count]  Control.packet.create_addr_filter: " + str( Control.packet.create_addr_filter.call_count))
     print("[Call count]  Control.packet.set_capture_file_name: " + str( Control.packet.set_capture_file_name.call_count))
def test_init_airfunc_1():
    COM_SOCKET =Mock()
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    patcher = mm.patch("json.load")
    mock_control = patcher.start()
    #mock_control.side_effect = Exception("Test")
    air = AIRCAP_FUNC(soc)
    patcher.stop()
    print("000000000000000000000000000000")

def test_init_airfunc_2():
    COM_SOCKET =Mock()
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")

    air = AIRCAP_FUNC(soc)

def test_check_airfunc_1():
    print()
    print("TEST Order: check function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"NumOfMsg":0}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    i_ret = air.check(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL


def test_check_airfunc_9():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file = Mock()
    packet.search = Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"AnalyzeMsg":5,"ReferenceData":"5"}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value = COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SUCCESS,"./Test.pcap",3
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_check_airfunc_7():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file = Mock()
    packet.search = Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":5,"ReferenceData":"5"},{"AnalyzeMsg":6,"ReferenceData":"6"}]}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value = COM_DEF.i_RET_SUCCESS
    Control.packet.search.return_value = COM_DEF.i_RET_SYSTEM_ERROR,"",3
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_check_airfunc_2():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()
    packet.search =Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":2,"ReferenceData":"2"},{"AnalyzeMsg":3,"ReferenceData":"3"}]}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value =COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SUCCESS,"",3

    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))


    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_check_airfunc_3():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()
    packet.search =Mock()
    subprocess.check_output = Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":2,"ReferenceData":"2"},{"AnalyzeMsg":3,"ReferenceData":"3"}]}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value =COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SUCCESS,"./Test.pcap",3
    subprocess.check_output = COM_DEF.i_RET_SUCCESS

    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_check_airfunc_3():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()
    packet.search =Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":2,"ReferenceData":"2"},{"AnalyzeMsg":3,"ReferenceData":"3"}]}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value =COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SUCCESS,"",3
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_check_airfunc_4():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()
    packet.search =Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":5,"ReferenceData":"5"},{"AnalyzeMsg":6,"ReferenceData":"6"}]}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value =COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SUCCESS,"",3
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_check_airfunc_5():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":5,"ReferenceData":"5"},{"AnalyzeMsg":6,"ReferenceData":"6"}]}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SYSTEM_ERROR,""
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_check_airfunc_6():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":5,"ReferenceData":"5"},{"AnalyzeMsg":6,"ReferenceData":"6"}]}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value = COM_DEF.i_RET_SYSTEM_ERROR
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_check_airfunc_7():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"NumOfMsg":2,"DataList":[{"AnalyzeMsg":1,"ReferenceData":"1"},{"AnalyzeMsg":2,"ReferenceData":"2"}]}

    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value = COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SYSTEM_ERROR,"",0
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv["Result"]))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR
    assert d_rply_tlv["ChkResult"] == COM_DEF.i_PktChkNg


def test_check_airfunc_9():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"AnalyzeMsg":1,"ReferenceData":"1"}

    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value = COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SYSTEM_ERROR,"",0
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv["Result"]))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR
    assert d_rply_tlv["ChkResult"] == COM_DEF.i_PktChkNg

def test_check_airfunc_10():
    print()
    print("TEST Order: check function call")
    Mock_call()
    packet.transfer_file=Mock()
    packet.compare_ie_val = Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param={"AnalyzeMsg":1,"ReferenceData":"1"}

    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.transfer_file.return_value = COM_DEF.i_RET_SUCCESS
    packet.search.return_value = COM_DEF.i_RET_SUCCESS,"0001.pcap",3
    packet.compare_ie_val.return_value = 1,{"DataList":[],"Result":COM_DEF.i_RET_SUCCESS}
    d_rply_tlv = air.check(l_com_hdr_info, d_tlv_param)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(d_rply_tlv["Result"]))

    Mock_count()
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SUCCESS


def test_start_aircap_airfunc_1():
    print()
    print("TEST Order: start_aircap function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"AircapIfId":COM_DEF.i_IfId_Aircap1,"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname ="wlp"
    air.tshark_proc = subprocess.Popen("ls")
    air.cap_file_path ="/Home/"
    air.filename_extension =".json"
    Control.packet.set_channel.return_value = COM_DEF.i_RET_SUCCESS
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_start_aircap_airfunc_2():
    print()
    print("TEST Order: start_aircap function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"AircapIfId":COM_DEF.i_IfId_Aircap2,"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname2 ="wlp2"
    air.tshark_proc = subprocess.Popen("ls")
    air.cap_file_path ="/Home/"
    air.filename_extension =".json"
    os.path.exists.return_value = False
    Control.packet.set_channel.return_value = COM_DEF.i_RET_TLV_ABNORMAL
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)
    
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname2: " + str(air.wlan_ifname2))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] os.path.exists.return_value: " + str(os.path.exists))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_start_aircap_airfunc_3():
    print()
    print("TEST Order: start_aircap function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"AircapIfId":COM_DEF.i_IfId_Aircap3,"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname3 ="wlp3"
    air.tshark_proc = subprocess.Popen("ls")
    air.cap_file_path ="/Home/"
    air.filename_extension =".json"
    os.path.exists.return_value = False
    Control.packet.set_channel.return_value = COM_DEF.i_RET_TLV_ABNORMAL
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname3: " + str(air.wlan_ifname3))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] os.path.exists.return_value: " + str(os.path.exists))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_start_aircap_airfunc_4():
    print()
    print("TEST Order: start_aircap function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"AircapIfId":COM_DEF.i_IfId_Aircap4,"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname4 ="wlp4"
    air.tshark_proc = subprocess.Popen("ls")
    air.cap_file_path ="/Home/"
    air.filename_extension =".json"
    os.path.exists.return_value = False
    Control.packet.set_channel.return_value = COM_DEF.i_RET_TLV_ABNORMAL
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname4: " + str(air.wlan_ifname4))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] os.path.exists.return_value: " + str(os.path.exists))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_start_aircap_airfunc_5():
    print()
    print("TEST Order: start_aircap function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"AircapIfId":9,"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname ="wlp"
    air.tshark_proc = subprocess.Popen("ls")
    air.cap_file_path ="/Home/"
    air.filename_extension =".json"
    os.path.exists.return_value = False
    Control.packet.set_channel.return_value = COM_DEF.i_RET_TLV_ABNORMAL
    Control.packet.create_addr_filter.return_value = "CaptureAddress"     
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] os.path.exists.return_value: " + str(os.path.exists))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_start_aircap_airfunc_6():
    print()
    print("TEST Order: start_aircap function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname ="wlp"
    air.tshark_proc = subprocess.Popen("ls")
    air.cap_file_path ="/Home/"
    air.filename_extension =".json"
    Control.packet.set_channel.return_value = COM_DEF.i_RET_TLV_ABNORMAL
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_start_aircap_airfunc_7():
    print()
    print("TEST Order: start_aircap function call")
    
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname ="wlp"
    air.tshark_proc = subprocess.Popen("ls")
    air.cap_file_path ="./common1"
    air.filename_extension =".json"
    Control.packet.set_channel.return_value = COM_DEF.i_RET_SUCCESS
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_start_aircap_airfunc_8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaException():
    print()
    print("TEST Order: start_aircap function call")
    Mock_call()
    subprocess.check_output = Mock()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"CaptureFileName":"ABCD","Channel":1}
    air.wlan_ifname ="wlp"
    air.tshark_flag = True
    air.cap_file_path ="./common1"
    air.filename_extension =".json"
    Control.packet.set_channel.return_value = COM_DEF.i_RET_SUCCESS
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    subprocess.check_output=Mock(side_effect=Exception("Test"))
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] air.tshark_proc: " + str(air.tshark_proc))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] subprocess.check_output: " + str(subprocess.check_output))
    print("[Out] i_ret: " + str(i_ret))


    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_start_aircap_airfunc_9AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaException():
    print()
    print("TEST Order: start_aircap function call")
    subprocess.check_output = Mock(return_value=b'11667767')
    subprocess.Popen = Mock(side_effect=Exception("TMockException"))
    #subprocess.check_out = Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"CaptureFileName":"ABCD","Channel":1}
    air.tshark_flag = True
    air.wlan_ifname ="lo"
    air.cap_file_path ="./common1"
    air.filename_extension =".json"
    Control.packet.set_channel.return_value = COM_DEF.i_RET_SUCCESS
    Control.packet.create_addr_filter.return_value = "CaptureAddress"
    i_ret = air.start_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))

    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.filename_extension: " + str(air.filename_extension))
    print("[In] Control.packet.set_channel.return_value: " + str(Control.packet.set_channel))
    print("[In] Control.packet.create_addr_filter.return_value: " + str(Control.packet.create_addr_filter))
    print("[Out] i_ret: " + str(i_ret))


    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR
    assert air.tshark_flag == False

def test_attach_airfunc_1():
    print()
    print("TEST Order: attach function call")
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_Attach]]
    d_tlv_param = {}
    i_ret = air.attach(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_detach_airfunc_1():
    print()
    print("TEST Order: detach function call")
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_Attach]]
    d_tlv_param = {}
    i_ret = air.detach(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS
def test_date_airfunc_1():
    print()
    print("TEST Order: date function call")
    subprocess.call = Mock()
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_SetCurrentTime]]
    d_tlv_param = {"Date":123456,"Time":12345}
    subprocess.call.return_value =COM_DEF.i_RET_SUCCESS
    i_ret = air.date(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] subprocess.call.return_value: " + str(subprocess.call))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_date_airfunc_2():
    print()
    print("TEST Order: date function call")
    subprocess.call=Mock()
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_SetCurrentTime]]
    d_tlv_param = {"Date":123456,"Time":12345}
    subprocess.call.return_value =COM_DEF.i_RET_BUSY
    i_ret = air.date(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] subprocess.call.return_value: " + str(subprocess.call))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.call: " + str(subprocess.call.call_count))
    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_stop_aircap_airfunc_1():
    print()
    print("TEST Order: stop_aircap function call")
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_StopAirCapture]]
    d_tlv_param = {}
    air.tshark_flag = False
    i_ret = air.stop_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.tshark_proc: " + str(air.tshark_proc))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_stop_aircap_airfunc_2():
    print()
    print("TEST Order: stop_aircap function call")
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_StopAirCapture]]
    d_tlv_param = {}
    #air.tshark_proc = subprocess.Popen("ls")
    air.tshark_flag = True
    i_ret = air.stop_aircap(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] air.tshark_proc: " + str(air.tshark_proc))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_confirm_stat_airfunc_1():
    print()
    print("TEST Order: confirm_stat function call")
    Mock_call()

    TESTPARA = COM_DEF.i_NODE_AP_END << 8
    l_com_hdr_info = [[COM_DEF.i_NODE_AP_END, "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {}
    i_ret = air.confirm_stat(l_com_hdr_info, d_tlv_param)

    print("[In] TESTPARA: " + str(TESTPARA))
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_NODE_CHK_ERROR

def test_confirm_stat_airfunc_2():
    print()
    print("TEST Order: confirm_stat function call")
    Mock_call()

    TESTPARA = COM_DEF.i_NODE_ENDPOINT_START << 8
    l_com_hdr_info = [[COM_DEF.i_NODE_ENDPOINT_START, "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {}
    i_ret = air.confirm_stat(l_com_hdr_info, d_tlv_param)

    print("[In] TESTPARA: " + str(TESTPARA))
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_NODE_CHK_ERROR

def test_confirm_stat_airfunc_3():
    print()
    print("TEST Order: confirm_stat function call")
    air.date = Mock()
    Mock_call()

    TESTPARA = COM_DEF.i_NODE_AIRCAP_END << 8
    l_com_hdr_info = [[TESTPARA, "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"Date":123456,"Time":12345}
    air.date.return_value = {"Result":COM_DEF.i_RET_SUCCESS}
    i_ret = air.confirm_stat(l_com_hdr_info, d_tlv_param)

    print("[In] TESTPARA: " + str(TESTPARA))
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.date.return_value: " + str(air.date))
    print("[In] i_ret: " + str(i_ret))

    print("[Call count] air.date: " + str(air.date.call_count))
    Mock_count()
    print("[Call count] air.date: " + str(air.date.call_count))
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_get_airlog_airfunc_1():
    print()
    print("TEST Order: get_airlog function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {}
    Control.packet.make_zip_file.return_value = COM_DEF.i_RET_NODE_CHK_ERROR,""
    i_ret = air.get_airlog(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.make_zip_file.return_value: " + str(Control.packet.make_zip_file))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_NODE_CHK_ERROR

def test_get_airlog_airfunc_2():
    print()
    print("TEST Order: get_airlog function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {}
    Control.packet.make_zip_file.return_value = COM_DEF.i_RET_SUCCESS,""
    Control.packet.transfer_file.return_value = COM_DEF.i_RET_NODE_CHK_ERROR
    i_ret = air.get_airlog(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.make_zip_file.return_value: " + str(Control.packet.make_zip_file))
    print("[In] Control.packet.transfer_file.return_value: " + str(Control.packet.transfer_file))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_NODE_CHK_ERROR

def test_get_airlog_airfunc_3():
    print()
    print("TEST Order: get_airlog function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {}
    Control.packet.make_zip_file.return_value = COM_DEF.i_RET_SUCCESS,""
    Control.packet.transfer_file.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = air.get_airlog(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.make_zip_file.return_value: " + str(Control.packet.make_zip_file))
    print("[In] Control.packet.transfer_file.return_value: " + str(Control.packet.transfer_file))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_decrypt_airfunc_1():
    print()
    print("TEST Order: decrypt function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {}
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_NODE_CHK_ERROR, ""
    i_ret = air.decrypt(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_NODE_CHK_ERROR

def test_decrypt_airfunc_2():
    print()
    print("TEST Order: decrypt function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"Ssid":"Ssid_test_decrypt_airfunc_2","WepKey":"WepKey_test_decrypt_airfunc_2"}
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS, ""
    i_ret = air.decrypt(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[In] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_decrypt_airfunc_3():
    print()
    print("TEST Order: decrypt function call")
    subprocess.call=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"Ssid":"Ssid_test_airfunc_3","WepKey":"WepKey_decrypt_airfunc_3","WpaPassphrase":"WpaPassphrase_decrypt_airfunc_3"}
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS, ""
    subprocess.call.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = air.decrypt(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[In] subprocess.call.return_value: " + str(subprocess.call))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.call: " + str(subprocess.call.call_count))
    Mock_count()
    print("[Call count]  subprocess.call: " + str( subprocess.call.call_count))
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_decrypt_airfunc_4():
    print()
    print("TEST Order: decrypt function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"Ssid":"Ssid_test_airfunc_4"}
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS, ""
    i_ret = air.decrypt(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_decrypt_airfunc_5():
    print()
    print("TEST Order: decrypt function call")
    subprocess.call=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"WepKey":"WepKey","WpaPassphrase":"WpaPassphrase_decrypt_airfunc_3WpaPassphrase_decrypt_airfunc_344"}
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS, ""
    i_ret = air.decrypt(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.call: " + str(subprocess.call.call_count))
    Mock_count()
    print("[Call count]  subprocess.call: " + str( subprocess.call.call_count))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR

def test_decrypt_airfunc_6():
    print()
    print("TEST Order: decrypt function call")
    subprocess.call=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"WepKey":"WepKey","WpaPassphrase":"WpaPassphrase_decrypt_airfunc_3WpaPassphrase_decrypt_airfunc_3454"}
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS, ""
    i_ret = air.decrypt(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.call: " + str(subprocess.call.call_count))
    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_decrypt_airfunc_7():
    print()
    print("TEST Order: decrypt function call")
    subprocess.call=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {"WepKey":"WepKey","WpaPassphrase":"WpaPassphrase_decrypt_airfunc_3WpaPassphrase_decrypt_airfunc_34"}
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS, ""
    i_ret = air.decrypt(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    print("[Call count]  subprocess.call: " + str( subprocess.call.call_count))
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_check_msg_num_airfunc_1():
    print()
    print("TEST Order: check_msg_num function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {}
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_TLV_ABNORMAL,""
    i_ret = air.check_msg_num(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] packet.set_capture_file_name.return_value: " + str(packet.set_capture_file_name))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_check_msg_num_airfunc_2():
    print()
    print("TEST Order: check_msg_num function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {
                  "NumOfMsg":0x02,
                  "DataList":[
                         {
                             "AnalyzeMsg": 0x01
                         },
                         {
                             "AnalyzeMsg": 0x02
                         }
                 ]
    }
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    Control.packet.get_pkt_num.return_value = COM_DEF.i_RET_SUCCESS,"",2
    i_ret = air.check_msg_num(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[In] Control.packet.get_pkt_num.return_value: " + str(Control.packet.get_pkt_num))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS

def test_check_msg_num_airfunc_3():
    print()
    print("TEST Order: check_msg_num function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {
                      "NumOfMsg":1,
                      "AnalyzeMsg":0x02
                  }
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    Control.packet.get_pkt_num.return_value = COM_DEF.i_RET_SUCCESS,"",0
    i_ret = air.check_msg_num(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[In] Control.packet.get_pkt_num.return_value: " + str(Control.packet.get_pkt_num))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS


def test_check_msg_num_airfunc_4():
    print()
    print("TEST Order: check_msg_num function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {
                      "NumOfMsg":1,
                      "AnalyzeMsg":0x02
                  }
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    Control.packet.get_pkt_num.return_value = COM_DEF.i_RET_TLV_ABNORMAL,"",0
    i_ret = air.check_msg_num(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[In] Control.packet.get_pkt_num.return_value: " + str(Control.packet.get_pkt_num))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL

def test_check_msg_num_airfunc_5():
    print()
    print("TEST Order: check_msg_num function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {
                      "AnalyzeMsg":0x02
                  }
    Control.packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    Control.packet.get_pkt_num.return_value = COM_DEF.i_RET_TLV_ABNORMAL,"",0
    i_ret = air.check_msg_num(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[In] Control.packet.get_pkt_num.return_value: " + str(Control.packet.get_pkt_num))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL


def test_check_msg_num_airfunc_6():
    print()
    print("TEST Order: check_msg_num function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param = {
                  "NumOfMsg":0x02,
                  "DataList":[
                         {
                             "AnalyzeMsg": 0x01
                         },
                         {
                             "AnalyzeMsg": 0x02
                         }
                 ]
    }
    packet.set_capture_file_name.return_value = COM_DEF.i_RET_SUCCESS,""
    packet.get_pkt_num.return_value = COM_DEF.i_RET_TLV_ABNORMAL,"",0
    i_ret = air.check_msg_num(l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Control.packet.set_capture_file_name.return_value: " + str(Control.packet.set_capture_file_name))
    print("[In] Control.packet.get_pkt_num.return_value: " + str(Control.packet.get_pkt_num))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL




