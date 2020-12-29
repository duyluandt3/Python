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
from CLS_Define import COM_DEF
from CLS_Serial import COM_SERIAL
from Control import AP_FUNC
import Control
import logging


def logger_Mock(snd):
    snd.logger.debug = Mock()
    snd.logger.error = Mock()
    snd.logger.info = Mock()


def print_logger(snd):
    print("[Logger] debug: " + str(snd.logger.debug.call_args_list))
    print("[Logger] error: " + str(snd.logger.error.call_args_list))
    print("[Logger] info: " + str(snd.logger.info.call_args_list))


def test_dhcpd_1():
    # 先頭に改行を入れることで関数名の後に続けて結果が表示されることを防ぐ
    print()
    print("Test Objective: Normal")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    # 引数の設定
    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS


def test_dhcpd_2():
    print()
    print("Test Objective: not WlanId")
    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_TLV_ABNORMAL


def test_dhcpd_3():
    print()
    print("Test Objective: except OSError")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0.10",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_4():
    print()
    print("Test Objective: except IpAddressValueerror")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10.60",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_5():
    print()
    print("Test Objective: i_available_num < i_assign_num")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.206",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_6():
    print()
    print("Test Objective: i_available_num = i_assign_num")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.205",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS


def test_dhcpd_7():
    print()
    print("Test Objective: i_available_num > i_assign_num")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.204",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS


def test_dhcpd_8():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 1/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_9():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 2/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_10():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 3/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_11():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 4/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_12():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 5/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_13():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 6/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_14():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 7/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_15():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 8/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_16():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 9/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_17():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 10/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_18():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 11/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_dhcpd_19():
    print()
    print("Test Objective: static_snd_rcv_cmd error(count 12/12)")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_param = {"WlanId": 9,
                   "IpAddress": "192.168.0.10",
                   "NetMask": "255.255.255.0",
                   "GateWay": "192.168.0.25",
                   "AssignNum": 50,
                   "LeaseTime": 86400}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.side_effect = [(COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SUCCESS, ""),
                                              (COM_DEF.i_RET_SYSTEM_ERROR, "")]
    ap.ser = 0
    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_param : " + str(d_tlv_param))

    i_ret = ap.dhcpd(l_com_hdr_info, d_tlv_param)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR


def test_setipinfo_1():
    print()
    print("Test Objective: Normal")
    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_data = {"IpAddress": "192.168.0.60",
                  "NetMask": "255.255.255.0",
                  "GateWay": "192.168.0.60"}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SUCCESS, ""
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_data : " + str(d_tlv_data))

    i_ret = ap.setipinfo(l_com_hdr_info, d_tlv_data)
    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS, i_ret


def test_setipinfo_2():
    print()
    print("static_snd_rcv_cmd Result error: send config")
    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_data = {"IpAddress": "192.168.0.60",
                  "NetMask": "255.255.255.0",
                  "GateWay": "192.168.0.60"}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock()
    Control.static_snd_rcv_cmd.return_value = COM_DEF.i_RET_SYSTEM_ERROR, ""
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_data : " + str(d_tlv_data))

    i_ret = ap.setipinfo(l_com_hdr_info, d_tlv_data)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_WLAN_ERROR


def test_setipinfo_3():
    print()
    print("static_snd_rcv_cmd Result error: send show")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = "test"
    d_tlv_data = {"IpAddress": "192.168.0.60",
                  "NetMask": "255.255.255.0",
                  "GateWay": "192.168.0.60"}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    Control.static_snd_rcv_cmd = Mock(side_effect=[(COM_DEF.i_RET_SUCCESS, ""),
                                                   (COM_DEF.i_RET_SYSTEM_ERROR,
                                                    "")])
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_data : " + str(d_tlv_data))

    i_ret = ap.setipinfo(l_com_hdr_info, d_tlv_data)

    print_logger(ap)
    print("[Call list] static_snd_rcv_cmd: " +
          str(Control.static_snd_rcv_cmd.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_WLAN_ERROR


def test_confirm_stat_1():
    print()
    print("Test Order: Nomal")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = [[0x3c01]]
    d_tlv_data = {"IpAddress": "192.168.0.60",
                  "NetMask": "255.255.255.0",
                  "GateWay": "192.168.0.60"}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    d_rply_tlv = {"Result": COM_DEF.i_RET_SUCCESS}
    ap.attach = Mock(return_value=d_rply_tlv)
    ap.date = Mock(return_value=d_rply_tlv)
    ap.setipinfo = Mock(return_value=d_rply_tlv)
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_data : " + str(d_tlv_data))

    i_ret = ap.confirm_stat(l_com_hdr_info, d_tlv_data)
    print_logger(ap)
    print("[Call list] setipinfo : " + str(ap.setipinfo.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SUCCESS


def test_confirm_stat_2():
    print()
    print("Test Order: not call setipinfo")

    Control.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
    Control.Logger_GetStubMode = Mock(return_value=0)

    l_com_hdr_info = [[0x3c02]]
    d_tlv_data = {"IpAddress": "192.168.0.60",
                  "NetMask": "255.255.255.0",
                  "GateWay": "192.168.0.60"}

    ap = AP_FUNC(1)
    logger_Mock(ap)
    Control.snd_req_cmd = Mock()
    d_rply_tlv = {"Result": COM_DEF.i_RET_SUCCESS}
    d_rply_tlv_error = {"Result": COM_DEF.i_RET_SYSTEM_ERROR}
    ap.attach = Mock(return_value=d_rply_tlv)
    ap.date = Mock(return_value=d_rply_tlv_error)
    ap.setipinfo = Mock(return_value=d_rply_tlv)
    ap.ser = 0

    print("[In] l_com_hdr_info : " + str(l_com_hdr_info))
    print("[In] d_tlv_data : " + str(d_tlv_data))

    i_ret = ap.confirm_stat(l_com_hdr_info, d_tlv_data)
    print_logger(ap)
    print("[Call list] setipinfo : " + str(ap.setipinfo.call_args_list))
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret["Result"] == COM_DEF.i_RET_SYSTEM_ERROR
