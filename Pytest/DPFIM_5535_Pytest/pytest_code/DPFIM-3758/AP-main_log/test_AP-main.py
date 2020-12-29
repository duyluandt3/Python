# -*- coding: utf-8 -*-
import time
import json
import sys
import pytest
from mock import Mock
sys.path.append("./device/AP/Cisco/")
sys.path.append('../../Common/debug/')
sys.path.append('../../Common/decode_encode/')
sys.path.append('../../Common/interface')
sys.path.append('../../Common/inc')
sys.path.append('./common')
import json
import sys
import threading
from Debug import Logger_GetObj
from CLS_Define import COM_DEF
from tx_snd import snd_rsp_cmd
import Control
import logging
import AP_main
from AP_main import call_apfunc
from Control import AP_FUNC


AP_main.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
AP_main.Logger_GetStubMode = Mock(return_value=0)
Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
Control.Logger_GetStubMode = Mock(return_value=0)

cls_ap_func = AP_FUNC(1)


def Mock_call():
    cls_ap_func.attach = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.date = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.ssid = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.open = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.wep = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.wpa = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    cls_ap_func.channel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.country = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.stealth = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.controlbss = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.stalist = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.control11n = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.detach = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.confirm_stat = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.dhcpd = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    cls_ap_func.setipinfo = Mock(return_value=COM_DEF.i_RET_SUCCESS)


def Mock_count():
    print("[Call count] cls_ap_func.attach: " +
          str(cls_ap_func.attach.call_count))
    print("[Call count] cls_ap_func.date: " +
          str(cls_ap_func.date.call_count))
    print("[Call count] cls_ap_func.ssid: " +
          str(cls_ap_func.ssid.call_count))
    print("[Call count] cls_ap_func.open: " +
          str(cls_ap_func.open.call_count))
    print("[Call count] cls_ap_func.wep: " + str(cls_ap_func.wep.call_count))
    print("[Call count] cls_ap_func.wpa: " + str(cls_ap_func.wpa.call_count))
    print("[Call count] cls_ap_func.channel: " +
          str(cls_ap_func.channel.call_count))
    print("[Call count] cls_ap_func.country: " +
          str(cls_ap_func.country.call_count))
    print("[Call count] cls_ap_func.stealth: " +
          str(cls_ap_func.stealth.call_count))
    print("[Call count] cls_ap_func.controlbss: " +
          str(cls_ap_func.controlbss.call_count))
    print("[Call count] cls_ap_func.stalist: " +
          str(cls_ap_func.stalist.call_count))
    print("[Call count] cls_ap_func.control11n: " +
          str(cls_ap_func.control11n.call_count))
    print("[Call count] cls_ap_func.detach: " +
          str(cls_ap_func.detach.call_count))
    print("[Call count] cls_ap_func.confirm_stat: " +
          str(cls_ap_func.confirm_stat.call_count))
    print("[Call count] cls_ap_func.dhcpd: " +
          str(cls_ap_func.dhcpd.call_count))
    print("[Call count] cls_ap_func.setipinfo: " +
          str(cls_ap_func.setipinfo.call_count))


def test_call_apfunc_1():
    print()
    print("TEST Order: dhcpd function call")
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_StartDhcpd]]
    d_tlv_param = ""

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    i_ret = call_apfunc(cls_ap_func, l_com_hdr_info, d_tlv_param)
    print("[Out] i_ret: " + str(i_ret))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_call_apfunc_2():
    print()
    print("TEST Order: setipinfo function call")
    Mock_call()

    l_com_hdr_info = [["test", "test2", COM_DEF.i_CMD_SetIpInfo]]
    d_tlv_param = ""

    print("[In] l_com_hdr_info: " + str(l_com_hdr_info))
    print("[In] d_tlv_param: " + str(d_tlv_param))
    i_ret = call_apfunc(cls_ap_func, l_com_hdr_info, d_tlv_param)
    print("[Out] i_ret: " + str(i_ret))
    Mock_count()
    assert i_ret == COM_DEF.i_RET_SUCCESS
