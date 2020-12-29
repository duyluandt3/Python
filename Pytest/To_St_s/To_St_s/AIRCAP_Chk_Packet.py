# -*- coding: utf-8 -*-
import time
import json
import sys
import os
import pytest
import subprocess
import pcapy
import shutil
import glob
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
import Chk_packet
import AIRCAP_main


AIRCAP_main.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
AIRCAP_main.Logger_GetStubMode = Mock(return_value=0)
Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
Control.Logger_GetStubMode = Mock(return_value=0)

air =AIRCAP_FUNC(1)

def Mock_call():
    #for attach and detach function
    Chk_packet.snd_req_cmd =Mock()


def Mock_count():
     print("[Call count] Chk_packet.snd_req_cmd: " + str(Chk_packet.snd_req_cmd.call_count))

def test_calculate_freq_airfunc_1():
    print()
    print("TEST Order: calculate_freq function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    i_channel =1 
    s_bandwidth ="20"
    i_ret,info = Chk_packet.calculate_freq(i_channel, s_bandwidth, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] i_channel: " + str(i_channel))
    print("[In] s_bandwidth: " + str(s_bandwidth))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] info: " + str(info))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert info["CenterFreq2"] == 0

def test_calculate_freq_airfunc_2():
    print()
    print("TEST Order: calculate_freq function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    i_channel =14
    s_bandwidth ="20"
    i_ret,info = Chk_packet.calculate_freq(i_channel, s_bandwidth, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] i_channel: " + str(i_channel))
    print("[In] s_bandwidth: " + str(s_bandwidth))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] info: " + str(info))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert info["CenterFreq2"] == 0

def test_calculate_freq_airfunc_3():
    print()
    print("TEST Order: calculate_freq function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    i_channel =14
    s_bandwidth ="40"
    i_ret,info = Chk_packet.calculate_freq(i_channel, s_bandwidth, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] i_channel: " + str(i_channel))
    print("[In] s_bandwidth: " + str(s_bandwidth))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] info: " + str(info))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert info["CenterFreq2"] == 0

def test_calculate_freq_airfunc_4():
    print()
    print("TEST Order: calculate_freq function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    i_channel =169
    s_bandwidth ="80+80"
    i_ret,info = Chk_packet.calculate_freq(i_channel, s_bandwidth, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] i_channel: " + str(i_channel))
    print("[In] s_bandwidth: " + str(s_bandwidth))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] info: " + str(info))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert info["CenterFreq2"] == 5935


def test_calculate_freq_airfunc_6():
    print()
    print("TEST Order: calculate_freq function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    i_channel =100
    s_bandwidth ="80"
    i_ret,info = Chk_packet.calculate_freq(i_channel, s_bandwidth, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] i_channel: " + str(i_channel))
    print("[In] s_bandwidth: " + str(s_bandwidth))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] info: " + str(info))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert info["CenterFreq2"] == 0
    assert info["BandWidth"] == '80'
    assert info["ControlFreq"] == 5500
    assert info["CenterFreq"] == 5530

def test_calculate_freq_airfunc_7():
    print()
    print("TEST Order: calculate_freq function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    i_channel =101
    s_bandwidth ="80"
    i_ret,info = Chk_packet.calculate_freq(i_channel, s_bandwidth, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] i_channel: " + str(i_channel))
    print("[In] s_bandwidth: " + str(s_bandwidth))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] info: " + str(info))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert info["CenterFreq2"] == 0
    assert info["BandWidth"] == '80'
    assert info["ControlFreq"] == 0
    assert info["CenterFreq"] == 0


def test_calculate_freq_airfunc_8():
    print()
    print("TEST Order: calculate_freq function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    i_channel =165
    s_bandwidth ="80"
    i_ret,info = Chk_packet.calculate_freq(i_channel, s_bandwidth, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] i_channel: " + str(i_channel))
    print("[In] s_bandwidth: " + str(s_bandwidth))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] info: " + str(info))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL

def test_debug_level_airfunc_1():
    print()
    print("TEST Order: debug_level function call")
    Mock_call()

    i_ret = Chk_packet.debug_level()

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == 0


def test_debug_level_airfunc_2():
    print()
    print("TEST Order: debug_level function call")
    open = Mock(side_effect = Exception("MockException"))
    Mock_call()

    i_ret = Chk_packet.debug_level()

    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == 0
def test_exec_command_airfunc_1():
    print()
    print("TEST Order: exec_command function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    air.soc ="2222"
    s_cmd_str ="ls" #["ip","link","set","192.168.0.1","down"]
    i_ret = Chk_packet.exec_command(l_com_hdr_info, air.soc, s_cmd_str, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] air.soc: " + str(air.soc))
    print("[In] s_cmd_str: " + str(s_cmd_str))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_exec_command_airfunc_2():
    print()
    print("TEST Order: exec_command function call")
    Chk_packet.subprocess.call=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    air.soc ="2222"
    s_cmd_str ="ls"
    Chk_packet.subprocess.call.return_value =  -3
    i_ret = Chk_packet.exec_command(l_com_hdr_info, air.soc, s_cmd_str, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] air.soc: " + str(air.soc))
    print("[In] s_cmd_str: " + str(s_cmd_str))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.call: " + str(subprocess.call.call_count))
    Mock_count()
    assert i_ret == -3

def test_set_channel_airfunc_1():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"Channel":1,"Bandwidth":5}
    s_wlan_ifname ="wlan0"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)

    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    print("[Call count] COM_SOCKET: " + str(COM_SOCKET.call_count))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL

def test_set_channel_airfunc_2():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_StartAirCapture]]
    d_tlv_param ={ "Channel":1, "Bandwidth":0 }
    s_wlan_ifname ="enp0s25"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)

    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret != COM_DEF.i_RET_SUCCESS

def test_set_channel_airfunc_3():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_StartAirCapture]]
    d_tlv_param ={ "Channel":36, "Bandwidth":3 }
    s_wlan_ifname ="enp0s25"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)


    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret != COM_DEF.i_RET_SUCCESS

def test_set_channel_airfunc_4():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Chk_packet.exec_command=Mock()

    Mock_call()
    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_StartAirCapture]]
    d_tlv_param ={ "Channel":36, "Bandwidth":3 }
    s_wlan_ifname ="enp0s25"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)

    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.exec_command: " + str(Chk_packet.exec_command.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_set_channel_airfunc_5():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Chk_packet.exec_command=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_StartAirCapture]]
    d_tlv_param ={ "Channel":36, "Bandwidth":1 }
    s_wlan_ifname ="enp0s25"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)

    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.exec_command: " + str(Chk_packet.exec_command.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_set_channel_airfunc_6():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Chk_packet.exec_command=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_StartAirCapture]]
    d_tlv_param ={ "Channel":36, "Bandwidth":2 }
    s_wlan_ifname ="enp0s25"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)

    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.exec_command: " + str(Chk_packet.exec_command.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_set_channel_airfunc_6():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Chk_packet.exec_command=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_StartAirCapture]]
    d_tlv_param ={ "Channel":36, "Bandwidth":4 }
    s_wlan_ifname ="enp0s25"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)

    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.exec_command: " + str(Chk_packet.exec_command.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_set_channel_airfunc_7():
    print()
    print("TEST Order: set_channel function call")
    COM_SOCKET =Mock()
    Chk_packet.calculate_freq=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_StartAirCapture]]
    d_tlv_param ={ "Channel":36, "Bandwidth":2 }
    s_wlan_ifname ="enp0s25"
    soc =COM_SOCKET(5200,9600,"AIRCAP")
    soc.bind("127.0.0.1")
    Chk_packet.calculate_freq.return_value = COM_DEF.i_RET_BUSY,""
    i_ret = Chk_packet.set_channel(l_com_hdr_info, soc, d_tlv_param, s_wlan_ifname, Control.Logger_GetObj)

    print("[Input] l_com_hdr_info: " +str(l_com_hdr_info))
    print("[Input] d_tlv_param: " +str(d_tlv_param))
    print("[Input] s_wlan_ifname: " +str(s_wlan_ifname))
    print("[In] Chk_packet.calculate_freq.return_value: " + str(Chk_packet.calculate_freq))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.calculate_freq: " + str(Chk_packet.calculate_freq.call_count))
    Mock_count()


    assert i_ret == COM_DEF.i_RET_BUSY

def test_set_external_wlan_dev_airfunc_1():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "wlan1"
    air.wlan_ifname = "wlp2s"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))    
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL

def test_pcap2json_airfunc_1():
    print()
    print("TEST Order: pcap2json function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_cap_file = "abcdef.pcap"
    i_ret = Chk_packet.pcap2json(s_cap_file,Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_cap_file: " + str(s_cap_file))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_pcap2json_airfunc_2():
    print()
    print("TEST Order: pcap2json function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_cap_file = "Test.pcap" 
    i_ret = Chk_packet.pcap2json(s_cap_file,Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_cap_file: " + str(s_cap_file))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_count_packet_airfunc_1():
    print()
    print("TEST Order: count_packet function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_cap_file = "abcdef.pcap"
    i_num_of_pkt, i_ret = Chk_packet.count_packet(s_cap_file,Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_cap_file: " + str(s_cap_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR
    assert i_num_of_pkt == 0

def test_count_packet_airfunc_2():
    print()
    print("TEST Order: count_packet function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_cap_file = "Test.pcap"
    i_num_of_pkt, i_ret = Chk_packet.count_packet(s_cap_file,Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_cap_file: " + str(s_cap_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert i_num_of_pkt != 0

def test_set_internal_wlan_dev_airfunc_1():
    print()
    print("TEST Order: set_internal_wlan_dev function call")
    Chk_packet.exec_command=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "enp0s25"
    air.wlan_ifname = "enp0s25"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.exec_command.return_value: " + str(Chk_packet.exec_command))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    print("[Call count] Chk_packet.exec_command: " + str(Chk_packet.exec_command.call_count))
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_set_internal_wlan_dev_airfunc_2():
    print()
    print("TEST Order: set_internal_wlan_dev function call")
    subprocess.getoutput=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = ""
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    subprocess.getoutput.return_value = "Have some device"
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.exec_command.return_value: " + str(Chk_packet.exec_command))
    print("[In] subprocess.getoutput.return_value: " + str(subprocess.getoutput))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.getoutput: " + str(subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_set_internal_wlan_dev_airfunc_3():
    print()
    print("TEST Order: set_internal_wlan_dev function call")
    subprocess.getoutput=Mock(side_effect=Exception("TEST_Exception"))
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = ""
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.getoutput: " + str(subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR


def test_set_internal_wlan_dev_airfunc_4():
    print()
    print("TEST Order: set_internal_wlan_dev function call")
    Chk_packet.subprocess.getoutput = Mock(return_value = "No such device")
    Chk_packet.exec_command = MagicMock(side_effect=[COM_DEF.i_RET_TLV_ABNORMAL])
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = ""
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.getoutput: " + str(subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL

def test_set_internal_wlan_dev_airfunc_5():
    print()

    print("TEST Order: set_internal_wlan_dev function call")

    Chk_packet.subprocess.getoutput = Mock(return_value = "No such device")
    Chk_packet.exec_command = MagicMock(side_effect=[COM_DEF.i_RET_TLV_ABNORMAL])
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = ""
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))
    print("[Call count] subprocess.getoutput: " + str(subprocess.getoutput.call_count))

    Mock_count()

    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_set_internal_wlan_dev_airfunc_6():
    print()
    print("TEST Order: set_internal_wlan_dev function call")
    Chk_packet.subprocess.getoutput = Mock(return_value = "No such device")
    Chk_packet.exec_command = MagicMock(side_effect=[0,COM_DEF.i_RET_TLV_ABNORMAL])
    Mock_call()
    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = ""
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))
    print("[Call count] subprocess.getoutput: " + str(subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL

def test_set_internal_wlan_dev_airfunc_7():
    print()
    print("TEST Order: set_internal_wlan_dev function call")
    Chk_packet.subprocess.getoutput = Mock(return_value = "No such device")
    Chk_packet.exec_command = MagicMock(side_effect=[0,0,COM_DEF.i_RET_TLV_ABNORMAL])
    Mock_call()
    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = ""
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))
    print("[Call count] subprocess.getoutput: " + str(subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_set_internal_wlan_dev_airfunc_8():
    print()
    print("TEST Order: set_internal_wlan_dev function call")
    Chk_packet.subprocess.getoutput = Mock(return_value = "No such device")
    Chk_packet.exec_command = MagicMock(side_effect=[0,0,0,COM_DEF.i_RET_TLV_ABNORMAL])
    Mock_call()
    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = ""
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_internal_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)
    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))
    print("[Call count] subprocess.getoutput: " + str(subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL

def test_create_filtered_file_airfunc_1():
    print()
    print("TEST Order: create_filtered_file function call")
    Mock_call()

    s_filter =""
    s_capturefilename="./Test.pcap"
    i_ret, s_filtered_file  = Chk_packet.create_filtered_file(s_capturefilename, s_filter, Control.Logger_GetObj)

    print("[In] s_filter: " + str(s_filter))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert s_filtered_file =="./Test-f.pcap"

def test_create_filtered_file_airfunc_2():
    print()
    print("TEST Order: create_filtered_file function call")
    Mock_call()

    s_filter =""
    s_capturefilename={"Test.pcap"}
    i_ret, s_filtered_file  = Chk_packet.create_filtered_file(s_capturefilename, s_filter, Control.Logger_GetObj)

    print("[In] s_filter: " + str(s_filter))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_create_filtered_file_airfunc_3():
    print()
    print("TEST Order: create_filtered_file function call")
    pcapy.open_offline=Mock()
    Mock_call()

    s_filter =""
    s_capturefilename="Test.pcap"
    i_ret, s_filtered_file  = Chk_packet.create_filtered_file(s_capturefilename, s_filter, Control.Logger_GetObj)

    print("[In] s_filter: " + str(s_filter))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))

    print("[Call count] pcapy.open_offline: " + str(pcapy.open_offline.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_create_filtered_file_airfunc_4():
    print()
    print("TEST Order: create_filtered_file function call")
    pcapy.open_offline=Mock()
    Mock_call()

    s_filter =""
    s_capturefilename="Test.pcap"
    i_ret, s_filtered_file  = Chk_packet.create_filtered_file(s_capturefilename, s_filter, Control.Logger_GetObj)

    print("[In] s_filter: " + str(s_filter))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))

    print("[Call count] pcapy.open_offline: " + str(pcapy.open_offline.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR


def test_create_filtered_file_airfunc_5():
    print()
    print("TEST Order: create_filtered_file function call")
    Mock_call()

    s_filter ="wlan subtype beacon"
    s_capturefilename="0003.pcap"
    i_ret, s_filtered_file  = Chk_packet.create_filtered_file(s_capturefilename, s_filter, Control.Logger_GetObj)

    print("[In] s_filter: " + str(s_filter))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))

    print("[Call count] pcapy.open_offline: " + str(pcapy.open_offline.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_set_external_wlan_dev_airfunc_1():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Chk_packet.subprocess.getoutput=Mock(side_effect = Exception("TESTMOCK"))
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = ""
    air.wlan_ifname = "wlp2s0"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_set_external_wlan_dev_airfunc_2():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "enp0s25"
    air.wlan_ifname = "enp0s25"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == -8

def test_set_external_wlan_dev_airfunc_3():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Chk_packet.exec_command=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "wlan0"
    air.wlan_ifname = "wlp2s0"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.exec_command.return_value: " + str(Chk_packet.exec_command))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.exec_command: " + str(Chk_packet.exec_command.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_set_external_wlan_dev_airfunc_4():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "wlan0 info info "
    air.wlan_ifname = "1"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.exec_command.return_value: " + str(Chk_packet.exec_command))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_set_external_wlan_dev_airfunc_5():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Chk_packet.subprocess.getoutput=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "enp0s25 "
    air.wlan_ifname = "enp0s25"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.subprocess.getoutput.return_value ="OK"
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.exec_command.return_value: " + str(Chk_packet.exec_command))
    print("[In] Chk_packet.subprocess.getoutput.return_value: " + str(Chk_packet.subprocess.getoutput))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.subprocess.getoutput: " + str(Chk_packet.subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_set_external_wlan_dev_airfunc_6():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Chk_packet.subprocess.getoutput=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "enp0s25 "
    air.wlan_ifname = "enp0s25"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.exec_command.return_value = COM_DEF.i_RET_TLV_ABNORMAL
    Chk_packet.subprocess.getoutput.return_value ="OK"
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.exec_command.return_value: " + str(Chk_packet.exec_command))
    print("[In] Chk_packet.subprocess.getoutput.return_value: " + str(Chk_packet.subprocess.getoutput))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.subprocess.getoutput: " + str(Chk_packet.subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_set_external_wlan_dev_airfunc_7():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Chk_packet.subprocess.getoutput=Mock()
    Chk_packet.exec_command = MagicMock(side_effect=[0,COM_DEF.i_RET_TLV_ABNORMAL])
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "enp0s25 "
    air.wlan_ifname = "enp0s25"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.subprocess.getoutput.return_value ="OK"
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.subprocess.getoutput.return_value: " + str(Chk_packet.subprocess.getoutput))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.subprocess.getoutput: " + str(Chk_packet.subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL

def test_set_external_wlan_dev_airfunc_8():
    print()
    print("TEST Order: set_external_wlan_dev function call")
    Chk_packet.subprocess.getoutput=Mock()
    Chk_packet.exec_command = MagicMock(side_effect=[0,0,COM_DEF.i_RET_TLV_ABNORMAL])
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    s_wlan_ifname = "enp0s25 "
    air.wlan_ifname = "enp0s25"
    Chk_packet.snd_req_cmd.return_value = COM_DEF.i_RET_SUCCESS
    Chk_packet.subprocess.getoutput.return_value ="OK"
    i_ret = Chk_packet.set_external_wlan_dev(air,l_com_hdr_info, s_wlan_ifname)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] s_wlan_ifname: " + str(s_wlan_ifname))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.snd_req_cmd.return_value: " + str(Chk_packet.snd_req_cmd))
    print("[In] Chk_packet.subprocess.getoutput.return_value: " + str(Chk_packet.subprocess.getoutput))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.subprocess.getoutput: " + str(Chk_packet.subprocess.getoutput.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
def test_set_wlan_if_airfunc_1():
    print()
    print("TEST Order: set_wlan_if function call")
    Chk_packet.set_internal_wlan_dev=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={}
    air.wlan_ifname = "wlp"
    Chk_packet.set_internal_wlan_dev.return_value=2222
    i_ret = Chk_packet.set_wlan_if(air,l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.set_internal_wlan_dev.return_value: " + str(Chk_packet.set_internal_wlan_dev))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.set_internal_wlan_dev: " + str(Chk_packet.set_internal_wlan_dev.call_count))
    Mock_count()
    assert i_ret == 2222

def test_set_wlan_if_airfunc_2():
    print()
    print("TEST Order: set_wlan_if function call")
    Chk_packet.set_external_wlan_dev=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={}
    air.wlan_ifname = "wp"
    Chk_packet.set_external_wlan_dev.return_value = 333
    i_ret = Chk_packet.set_wlan_if(air,l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.set_external_wlan_dev.return_value: " + str(Chk_packet.set_external_wlan_dev))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.set_external_wlan_dev: " + str(Chk_packet.set_external_wlan_dev.call_count))
    Mock_count()
    assert i_ret == 333

def test_set_wlan_if_airfunc_3():
    print()
    print("TEST Order: set_wlan_if function call")
    Chk_packet.set_external_wlan_dev=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":COM_DEF.i_IfId_Aircap1}
    air.wlan_ifname = "wp0"
    Chk_packet.set_external_wlan_dev.return_value = 333
    i_ret = Chk_packet.set_wlan_if(air,l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.set_external_wlan_dev.return_value: " + str(Chk_packet.set_external_wlan_dev))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.set_external_wlan_dev: " + str(Chk_packet.set_external_wlan_dev.call_count))
    Mock_count()
    assert i_ret == 333

def test_set_wlan_if_airfunc_4():
    print()
    print("TEST Order: set_wlan_if function call")
    Chk_packet.set_external_wlan_dev=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":COM_DEF.i_IfId_Aircap2}
    air.wlan_ifname2 = "wp2"
    Chk_packet.set_external_wlan_dev.return_value = 333
    i_ret = Chk_packet.set_wlan_if(air,l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname2: " + str(air.wlan_ifname2))
    print("[In] Chk_packet.set_external_wlan_dev.return_value: " + str(Chk_packet.set_external_wlan_dev))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.set_external_wlan_dev: " + str(Chk_packet.set_external_wlan_dev.call_count))
    Mock_count()
    assert i_ret == 333

def test_set_wlan_if_airfunc_5():
    print()
    print("TEST Order: set_wlan_if function call")
    Chk_packet.set_external_wlan_dev=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":COM_DEF.i_IfId_Aircap3}
    air.wlan_ifname3 = "wp3"
    Chk_packet.set_external_wlan_dev.return_value = 333
    i_ret = Chk_packet.set_wlan_if(air,l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname3: " + str(air.wlan_ifname3))
    print("[In] Chk_packet.set_external_wlan_dev.return_value: " + str(Chk_packet.set_external_wlan_dev))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.set_external_wlan_dev: " + str(Chk_packet.set_external_wlan_dev.call_count))
    Mock_count()
    assert i_ret == 333


def test_set_wlan_if_airfunc_6():
    print()
    print("TEST Order: set_wlan_if function call")
    Chk_packet.set_external_wlan_dev=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":COM_DEF.i_IfId_Aircap4}
    air.wlan_ifname4 = "wp4"
    Chk_packet.set_external_wlan_dev.return_value = 333
    i_ret = Chk_packet.set_wlan_if(air,l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname4: " + str(air.wlan_ifname4))
    print("[In] Chk_packet.set_external_wlan_dev.return_value: " + str(Chk_packet.set_external_wlan_dev))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] Chk_packet.set_external_wlan_dev: " + str(Chk_packet.set_external_wlan_dev.call_count))
    Mock_count()
    assert i_ret == 333

def test_set_wlan_if_airfunc_7():
    print()
    print("TEST Order: set_wlan_if function call")
    Chk_packet.set_external_wlan_dev=Mock()
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":6}
    air.wlan_ifname = "wp5"
    Chk_packet.set_external_wlan_dev.return_value = 333
    i_ret = Chk_packet.set_wlan_if(air,l_com_hdr_info, d_tlv_param)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.wlan_ifname: " + str(air.wlan_ifname))
    print("[In] Chk_packet.set_external_wlan_dev.return_value: " + str(Chk_packet.set_external_wlan_dev))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    print("[Call count] Chk_packet.set_external_wlan_dev: " + str(Chk_packet.set_external_wlan_dev.call_count))
    assert i_ret == 333



def test_set_capture_file_name_airfunc_1():
    print()
    print("TEST Order: set_capture_file_name function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"CaptureFileName":"ABCD"}
    air.s_filename=""
    i_ret,zipfile = Chk_packet.set_capture_file_name(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert zipfile == ""

def test_set_capture_file_name_airfunc_2():
    print()
    print("TEST Order: set_capture_file_name function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":"ABCD"}
    air.s_filename="FILENAME"
    i_ret,zipfile = Chk_packet.set_capture_file_name(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.s_filename: " + str(air.s_filename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert zipfile != ""

def test_set_capture_file_name_airfunc_3():
    print()
    print("TEST Order: set_capture_file_name function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":"ABCD"}
    air.s_filename=""
    i_ret,zipfile = Chk_packet.set_capture_file_name(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.s_filename: " + str(air.s_filename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert zipfile == ""

def test_set_capture_file_name_airfunc_4():
    print()
    print("TEST Order: set_capture_file_name function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":"ABCD/", "CaptureFileName":"a"}  
    air.cap_file_path="./"
    air.s_filename=""
    i_ret,zipfile = Chk_packet.set_capture_file_name(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[In] air.s_filename: " + str(air.s_filename))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_make_zip_file_airfunc_1():
    print()
    print("TEST Order: make_zip_file function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"AircapIfId":6}
    i_ret,zipfile = Chk_packet.make_zip_file(air,d_tlv_param, Control.Logger_GetObj)


    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert zipfile == ""

def test_make_zip_file_airfunc_2():
    print()
    print("TEST Order: make_zip_file function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={}
    i_ret,zipfile = Chk_packet.make_zip_file(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert zipfile == ""

def test_make_zip_file_airfunc_3():
    print()
    print("TEST Order: make_zip_file function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={}
    i_ret,zipfile = Chk_packet.make_zip_file(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert zipfile == ""

def test_make_zip_file_airfunc_4():
    print()
    print("TEST Order: make_zip_file function call")
    Mock_call()

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"CaptureFileName":"ABCD"}
    air.cap_file_path="PATH"
    i_ret,zipfile = Chk_packet.make_zip_file(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR
    assert zipfile == ""

def test_make_zip_file_airfunc_5():
    print()
    print("TEST Order: make_zip_file function call")
    Mock_call()
    Chk_packet.shutil.make_archive = Mock()
    Chk_packet.shutil.move=Mock()
    Chk_packet.glob.glob=Mock(return_value =['./Test1.txt','./Test2.txt'])

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"CaptureFileName":"ABCD"}
    air.cap_file_path="PATH"
    i_ret,zipfile = Chk_packet.make_zip_file(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR


def test_make_zip_file_airfunc_6():
    print()
    print("TEST Order: make_zip_file function call")
    Mock_call()
    Chk_packet.shutil.make_archive = Mock()
    Chk_packet.shutil.move=Mock()
    Chk_packet.glob.glob=Mock(return_value =['./Test1.txt','./Test2.txt'])
    os.path.exists = Mock(return_value = True)

    l_com_hdr_info = [["Test1", "test2", COM_DEF.i_CMD_ConfirmDevStat]]
    d_tlv_param ={"CaptureFileName":"ABCD"}
    air.cap_file_path="PATH"
    i_ret,zipfile = Chk_packet.make_zip_file(air,d_tlv_param, Control.Logger_GetObj)

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] air.cap_file_path: " + str(air.cap_file_path))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] zipfile: " + str(zipfile))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_transfer_file_airfunc_1():
    print()
    print("TEST Order: transfer_file function call")
    Mock_call()

    s_src_file ="src.doc"
    s_dst_file ="dst.doc"
    s_passwd ="12345678" 
    i_ret = Chk_packet.transfer_file(s_src_file, s_dst_file, s_passwd, Control.Logger_GetObj)

    print("[In] s_src_file: " + str(s_src_file))
    print("[In] s_dst_file: " + str(s_dst_file))
    print("[In] s_passwd: " + str(s_passwd))
    print("[Out] i_ret: " + str(i_ret))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_SYSTEM_ERROR

def test_transfer_file_airfunc_2():
    print()
    print("TEST Order: transfer_file function call")
    subprocess.check_output=Mock()
    Mock_call()

    s_src_file ="Test.pcap"
    s_dst_file ="testtest.pcap"
    s_passwd ="12345678" 
    i_ret = Chk_packet.transfer_file(s_src_file, s_dst_file, s_passwd, Control.Logger_GetObj)

    print("[In] s_src_file: " + str(s_src_file))
    print("[In] s_dst_file: " + str(s_dst_file))
    print("[In] s_passwd: " + str(s_passwd))
    print("[Out] i_ret: " + str(i_ret))

    print("[Call count] subprocess.check_output: " + str(subprocess.check_output.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS

def test_compare_ie_val_airfunc_1():
    print()
    print("TEST Order: compare_ie_val function call")
    Mock_call()

    i_analyzemsg =""
    d_cap_ie={}
    d_ref_data = {"wlan.fc.type_subtype":"0"}
    l_ie_name_list={}
    d_rply_tlv={}
    i_cnt=0 
    i_cnt, d_rply_tlv = Chk_packet.compare_ie_val(i_analyzemsg, l_ie_name_list, d_ref_data, d_cap_ie, d_rply_tlv, i_cnt,Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_cap_ie: " + str(d_cap_ie))
    print("[In] d_ref_data: " + str(d_ref_data))
    print("[In] l_ie_name_list: " + str(l_ie_name_list))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] i_cnt: " + str(i_cnt))
    print("[Out] i_cnt: " + str(i_cnt))
    print("[Out] d_rply_tlv: " + str(d_rply_tlv))

    Mock_count()
    assert i_cnt == 0
    #assert d_rply_tlv["Result"] == 0
    #assert d_rply_tlv["ChkResult"] == COM_DEF.i_PktChkOk

def test_compare_ie_val_airfunc_2():
    print()
    print("TEST Order: compare_ie_val function call")
    Mock_call()

    i_analyzemsg =""
    d_ref_data = {"wlan.fc.type_subtype":"0", "wlan.fc.subtype":"1"}
    l_ie_name_list=["wlan.fc.type_subtype","wlan.fc.subtype"]
    d_cap_ie={"wlan.fc.type_subtype":"0,1,2,3","wlan.fc.subtype":"0,1,2,3"}
    d_rply_tlv={}
    i_cnt=0
    i_cnt, d_rply_tlv = Chk_packet.compare_ie_val(i_analyzemsg, l_ie_name_list, 
                                                  d_ref_data, d_cap_ie, d_rply_tlv, i_cnt, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_ref_data: " + str(d_ref_data))
    print("[In] l_ie_name_list: " + str(l_ie_name_list))
    print("[In] d_cap_ie: " + str(d_cap_ie))
    print("[Out] d_rply_tlv: " + str(d_rply_tlv))
    print("[Out] i_cnt: " + str(i_cnt))


    Mock_count()
    assert i_cnt == 0
    #assert d_rply_tlv["ChkResult"] == COM_DEF.i_PktChkOk

def test_compare_ie_val_airfunc_3():
    print()
    print("TEST Order: compare_ie_val function call")
    Mock_call()

    i_analyzemsg =""
    d_ref_data = {"wlan.fc.type_subtype":"2", "wlan.fc.subtype":"1"}
    l_ie_name_list=["wlan.fc.type_subtype","wlan.fc.subtype"]
    d_cap_ie={"wlan.fc.type_subtype":"","wlan.fc.subtype":""}
    d_rply_tlv={}
    d_rply_tlv["DataList"]=[]

    d_rply_tlv["Result"] = COM_DEF.i_RET_SUCCESS
    d_rply_tlv["ChkResult"] = COM_DEF.i_PktChkOk
    i_cnt=0
    i_cnt, d_rply_tlv = Chk_packet.compare_ie_val(i_analyzemsg, l_ie_name_list, 
                                                  d_ref_data, d_cap_ie, d_rply_tlv, i_cnt, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_ref_data: " + str(d_ref_data))
    print("[In] l_ie_name_list: " + str(l_ie_name_list))
    print("[In] d_cap_ie: " + str(d_cap_ie))
    print("[Out] d_rply_tlv: " + str(d_rply_tlv))
    print("[Out] i_cnt: " + str(i_cnt))

    Mock_count()
    assert i_cnt == 2
    assert d_rply_tlv["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_compare_ie_val_airfunc_4():
    print()
    print("TEST Order: compare_ie_val function call")
    Mock_call()

    i_analyzemsg =""
    d_ref_data = {"wlan.fc.type_subtype":"", "wlan.fc.subtype":""}
    l_ie_name_list=["wlan.fc.type_subtype","wlan.fc.subtype"]
    d_cap_ie={"wlan.fc.type_subtype":"1","wlan.fc.subtype":"2"}
    d_rply_tlv ={}
    d_rply_tlv["DataList"]=[]
    i_cnt=0
    i_cnt, d_rply_tlv = Chk_packet.compare_ie_val(i_analyzemsg, l_ie_name_list, 
                                                  d_ref_data, d_cap_ie, d_rply_tlv, i_cnt, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_ref_data: " + str(d_ref_data))
    print("[In] l_ie_name_list: " + str(l_ie_name_list))
    print("[In] d_cap_ie: " + str(d_cap_ie))
    print("[Out] d_rply_tlv: " + str(d_rply_tlv))
    print("[Out] i_cnt: " + str(i_cnt))

    Mock_count()
    assert i_cnt == 0

def test_create_filter_airfunc_1():
    print()
    print("TEST Order: create_filter function call")
    Mock_call()

    i_analyzemsg ="15"
    d_tlv_param={}
    s_filter  = Chk_packet.create_filter(d_tlv_param, i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert "wlan subtype beacon" in s_filter

def test_create_filter_airfunc_2():
    print()
    print("TEST Order: create_filter function call")
    Mock_call()

    i_analyzemsg ="15"
    d_tlv_param={"NumberOfLink":1,"TransAddr":"AAA"}
    s_filter  = Chk_packet.create_filter(d_tlv_param, i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert "wlan host AAA and wlan subtype beacon" in s_filter


def test_search_airfunc_1():
    print()
    print("TEST Order: search function call")
    Chk_packet.create_filter=Mock()
    Chk_packet.create_filtered_file =Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = ""
    d_tlv_param={}
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_TLV_ABNORMAL,"abc"
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.search(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.create_filtered_file: " + str(Chk_packet.create_filtered_file.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == ""
    assert i_num_of_pkt == 0

def test_search_airfunc_2():
    print()
    print("TEST Order: search function call")
    Chk_packet.create_filter=Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = ""
    d_tlv_param={}
    Chk_packet.create_filter.return_value =""
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.search(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.create_filter.return_value: " + str(Chk_packet.create_filter))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == ""
    assert i_num_of_pkt == 0

def test_search_airfunc_3():
    print()
    print("TEST Order: search function call")
    Chk_packet.create_filter=Mock()
    Chk_packet.debug_level =Mock()
    Chk_packet.pcap2json =Mock()
    os.rename =Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = ""
    d_tlv_param={}
    Chk_packet.debug_level.return_value  = 1
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_SUCCESS,"abc"
    Chk_packet.pcap2json.return_value  = COM_DEF.i_RET_TLV_ABNORMAL
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.search(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.debug_level.return_value: " + str(Chk_packet.debug_level))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[In] Chk_packet.pcap2json.return_value: " + str(Chk_packet.pcap2json))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.debug_level: " + str(Chk_packet.debug_level.call_count))
    print("[Call count] Chk_packet.pcap2json: " + str(Chk_packet.pcap2json.call_count))
    print("[Call count] os.rename: " + str(os.rename.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == "abc"
    assert i_num_of_pkt == 0

def test_search_airfunc_4():
    print()
    print("TEST Order: search function call")
    Chk_packet.create_filter=Mock()
    Chk_packet.debug_level =Mock()
    Chk_packet.pcap2json =Mock()
    os.rename =Mock()
    Chk_packet.count_packet =Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = ""
    d_tlv_param={}
    Chk_packet.debug_level.return_value  = 1
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_SUCCESS,"abc"
    Chk_packet.pcap2json.return_value  = COM_DEF.i_RET_SUCCESS
    Chk_packet.count_packet.return_value = 3, COM_DEF.i_RET_TLV_ABNORMAL
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.search(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.debug_level.return_value: " + str(Chk_packet.debug_level))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[In] Chk_packet.pcap2json.return_value: " + str(Chk_packet.pcap2json))
    print("[In] Chk_packet.count_packet.return_value: " + str(Chk_packet.count_packet))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.debug_level: " + str(Chk_packet.debug_level.call_count))
    print("[Call count] Chk_packet.pcap2json: " + str(Chk_packet.pcap2json.call_count))
    print("[Call count] os.rename: " + str(os.rename.call_count))
    print("[Call count] Chk_packet.count_packet: " + str(Chk_packet.count_packet.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == "abc"
    assert i_num_of_pkt == 3

def test_search_airfunc_5():
    print()
    print("TEST Order: search function call")
    Chk_packet.create_filter=Mock()
    Chk_packet.debug_level =Mock()
    Chk_packet.pcap2json =Mock()
    os.rename =Mock()
    Chk_packet.count_packet =Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = ""
    d_tlv_param={}
    Chk_packet.debug_level.return_value  = 1
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_SUCCESS,"abc"
    Chk_packet.pcap2json.return_value  = COM_DEF.i_RET_SUCCESS
    Chk_packet.count_packet.return_value = 3, COM_DEF.i_RET_SUCCESS
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.search(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.debug_level.return_value: " + str(Chk_packet.debug_level))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[In] Chk_packet.pcap2json.return_value: " + str(Chk_packet.pcap2json))
    print("[In] Chk_packet.count_packet.return_value: " + str(Chk_packet.count_packet))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.debug_level: " + str(Chk_packet.debug_level.call_count))
    print("[Call count] Chk_packet.pcap2json: " + str(Chk_packet.pcap2json.call_count))
    print("[Call count] os.rename: " + str(os.rename.call_count))
    print("[Call count] Chk_packet.count_packet: " + str(Chk_packet.count_packet.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert s_filtered_file == "abc"
    assert i_num_of_pkt == 3

def test_get_pkt_num_airfunc_1():
    print()
    print("TEST Order: get_pkt_num function call")
    Chk_packet.create_filter=Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = "abc.pcap"
    d_tlv_param={}
    Chk_packet.create_filter.return_value = ""
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.get_pkt_num(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.create_filter.return_value: " + str(Chk_packet.create_filter))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == ""
    assert i_num_of_pkt == 0

def test_get_pkt_num_airfunc_2():
    print()
    print("TEST Order: get_pkt_num function call")
    Chk_packet.create_filter=Mock()
    Chk_packet.create_filtered_file =Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = "abc.pcap"
    d_tlv_param={}
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_TLV_ABNORMAL,"abc.pcap"   
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.get_pkt_num(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.create_filtered_file: " + str(Chk_packet.create_filtered_file.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == ""
    assert i_num_of_pkt == 0

def test_get_pkt_num_airfunc_3():
    print()
    print("TEST Order: get_pkt_num function call")
    #Mock regis
    Chk_packet.create_filter=Mock()
    Chk_packet.create_filtered_file =Mock()
    Chk_packet.count_packet =Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = "abc.pcap"
    d_tlv_param={}
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_SUCCESS,"abc.pcap"
    Chk_packet.count_packet.return_value = 0,COM_DEF.i_RET_TLV_ABNORMAL
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.get_pkt_num(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[In] Chk_packet.count_packet.return_value: " + str(Chk_packet.count_packet))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.create_filtered_file: " + str(Chk_packet.create_filtered_file.call_count))
    print("[Call count] Chk_packet.count_packet: " + str(Chk_packet.count_packet.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == "abc.pcap"
    assert i_num_of_pkt == 0

def test_get_pkt_num_airfunc_4():
    print()
    print("TEST Order: get_pkt_num function call")
    #Mock regis
    Chk_packet.create_filter=Mock()
    Chk_packet.create_filtered_file =Mock()
    Chk_packet.count_packet=Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = "abc.pcap"
    d_tlv_param={}
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_SUCCESS,"abc.pcap"
    Chk_packet.count_packet.return_value = 4, COM_DEF.i_RET_SUCCESS
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.get_pkt_num(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[In] Chk_packet.count_packet.return_value: " + str(Chk_packet.count_packet))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.create_filtered_file: " + str(Chk_packet.create_filtered_file.call_count))
    print("[Call count] Chk_packet.count_packet: " + str(Chk_packet.count_packet.call_count))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
    assert s_filtered_file == "abc.pcap"
    assert i_num_of_pkt == 4

def test_get_pkt_num_airfunc_5():
    print()
    print("TEST Order: get_pkt_num function call")
    Chk_packet.create_filter=Mock()
    Chk_packet.create_filtered_file =Mock()
    Chk_packet.count_packet=Mock()
    Mock_call()

    i_analyzemsg =""
    s_capturefilename = "abc.pcap"
    d_tlv_param={}
    Chk_packet.create_filtered_file.return_value = COM_DEF.i_RET_SUCCESS,"abc.pcap"
    Chk_packet.count_packet.return_value = 4, COM_DEF.i_RET_TLV_ABNORMAL
    i_ret, s_filtered_file, i_num_of_pkt  = Chk_packet.get_pkt_num(s_capturefilename, i_analyzemsg, d_tlv_param, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] s_capturefilename: " + str(s_capturefilename))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[In] Chk_packet.create_filtered_file.return_value: " + str(Chk_packet.create_filtered_file))
    print("[In] Chk_packet.count_packet.return_value: " + str(Chk_packet.count_packet))
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] s_filtered_file: " + str(s_filtered_file))
    print("[Out] i_num_of_pkt: " + str(i_num_of_pkt))

    print("[Call count] Chk_packet.create_filter: " + str(Chk_packet.create_filter.call_count))
    print("[Call count] Chk_packet.create_filtered_file: " + str(Chk_packet.create_filtered_file.call_count))
    print("[Call count] Chk_packet.count_packet: " + str(Chk_packet.count_packet.call_count))

    Mock_count()
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL
    assert s_filtered_file == "abc.pcap"
    assert i_num_of_pkt == 4

def test_create_addr_filter_airfunc_1():
    print()
    print("TEST Order: create_addr_filter function call")
    Mock_call()

    i_analyzemsg =""
    d_tlv_param={}
    s_filter  = Chk_packet.create_addr_filter(d_tlv_param, i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert s_filter == ""


def test_create_addr_filter_airfunc_3():
    print()
    print("TEST Order: create_addr_filter function call")
    Mock_call()

    i_analyzemsg =""
    d_tlv_param={"TransAddr":"AAA","NumOfLink":2,"DataList":[{"SourceAddr":"1"},{"DestAddr":"1"}]}
    s_filter  = Chk_packet.create_addr_filter(d_tlv_param, i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert "(wlan src 1 or wlan dst 1) or (wlan src 1 or wlan dst 1)" in s_filter

def test_create_addr_filter_airfunc_2():
    print()
    print("TEST Order: create_addr_filter function call")
    Mock_call()

    i_analyzemsg =""
    d_tlv_param={"TransAddr":"AAA","NumOfLink":2,"DataList":[{"DestAddr":"0","SourceAddr":"1"},{"DestAddr":"1","SourceAddr":"2"}]}
    s_filter  = Chk_packet.create_addr_filter(d_tlv_param, i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert "((wlan src 1 and wlan dst 0) or (wlan src 0 and wlan dst 1)) or ((wlan src 2 and wlan dst 1) or (wlan src 1 and wlan dst 2))" in s_filter

def test_create_addr_filter_airfunc_4():
    print()
    print("TEST Order: create_addr_filter function call")
    Mock_call()

    i_analyzemsg =""
    d_tlv_param={"NumOfLink":2,"DataList":[{"SourceAddr":"1","TransAddr":"AAA"},{"DestAddr":"1","TransAddr":"AAA"}]}
    s_filter  = Chk_packet.create_addr_filter(d_tlv_param, i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert "(wlan src 1 or wlan dst 1) or (wlan src 1 or wlan dst 1)" in s_filter


def test_set_pkt_filter_airfunc_1():
    print()
    print("TEST Order: set_pkt_filter function call")
    Mock_call()

    i_analyzemsg = "1"
    s_filter  = Chk_packet.set_pkt_filter(i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert "wlan subtype assoc-req" in s_filter

#for open file function test, have to update file name before test
def test_set_pkt_filter_airfunc_2():
    print()
    print("TEST Order: set_pkt_filter function call")
    Mock_call()

    i_analyzemsg = "1"
    s_filter  = Chk_packet.set_pkt_filter(i_analyzemsg, Control.Logger_GetObj)

    print("[In] i_analyzemsg: " + str(i_analyzemsg))
    print("[Out] s_filter: " + str(s_filter))

    Mock_count()
    assert s_filter == ""


