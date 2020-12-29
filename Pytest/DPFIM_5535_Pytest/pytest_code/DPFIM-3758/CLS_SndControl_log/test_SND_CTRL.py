import queue
import json
import threading
import signal
import sys
import time
import collections
import pytest
import logging

sys.path.append('../../Common/debug/')
sys.path.append('../../Common/decode_encode/')
sys.path.append('../../Common/interface/')
sys.path.append('../../Common/inc/')
sys.path.append('config/')
sys.path.append('scenario/')
sys.path.append('stub/')
sys.path.append('class/')
sys.path.append('class/sub_func/')
from CLS_Log import LOG_CTRL
from Debug import Logger_Init
from CLS_SndControl import SND_CTRL
from CLS_Define import COM_DEF
from mock import Mock
from Decode_ComHdr import Decode_ComHdr
from Decode_TLV import Decode_TLV
import CLS_SndControl
import Debug
import CLS_Log

CLS_SndControl.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
CLS_SndControl.Logger_GetStubMode = Mock(return_value=0)
CLS_Log.Logger_GetObj = Mock(return_value=logging.getLogger('test'))
CLS_Log.Logger_GetStubMode = Mock(return_value=0)


def logger_Mock(snd):
    snd.logger.debug = Mock()
    snd.logger.error = Mock()
    snd.logger.info = Mock()


def print_logger(snd):
    print("[Logger] debug: " + str(snd.logger.debug.call_args_list))
    print("[Logger] error: " + str(snd.logger.error.call_args_list))
    print("[Logger] info: " + str(snd.logger.info.call_args_list))


def test_SND_Update_IpAddress_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    s_Ipaddr = "192.168.0.10"

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] s_Ipaddr: " + s_Ipaddr)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    snd.SND_Update_IpAddress(i_src_id, s_Ipaddr)
    print_logger(snd)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))


def test_SND_Check_IpAddress_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_dst_id = 0x0a01
    s_Ipaddr = "192.168.0.10"
    d_testParam = {"IpAddress": "192.168.0.10"}
    snd.SND_Update_IpAddress = Mock()
    snd.SND_Update_IpAddress.return_value = COM_DEF.i_RET_SUCCESS
    print("[In] i_dst_id: " + hex(i_dst_id))
    print("[In] s_Ipaddr: " + s_Ipaddr)
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Check_IpAddress(i_dst_id, s_Ipaddr, d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Check_IpAddress_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: IPAddress disagreement")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_dst_id = 0x0a01
    s_Ipaddr = "192.168.0.20"
    d_testParam = {"IpAddress": "192.168.0.10"}
    snd.SND_Update_IpAddress = Mock()
    snd.SND_Update_IpAddress.return_value = COM_DEF.i_RET_SUCCESS
    print("[In] i_dst_id: " + hex(i_dst_id))
    print("[In] s_Ipaddr: " + s_Ipaddr)
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Check_IpAddress(i_dst_id, s_Ipaddr, d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Check_IpAddress_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: dst_id disagreement")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_dst_id = 0x0a03
    s_Ipaddr = "192.168.0.10"
    d_testParam = {"IpAddress": "192.168.0.10"}
    snd.SND_Update_IpAddress = Mock()
    snd.SND_Update_IpAddress.return_value = COM_DEF.i_RET_SUCCESS
    print("[In] i_dst_id: " + hex(i_dst_id))
    print("[In] s_Ipaddr: " + s_Ipaddr)
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Check_IpAddress(i_dst_id, s_Ipaddr, d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Delete_IpAddress_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    i_dst_id = 0x0a02
    print("[In] i_dst_id: " + hex(i_dst_id))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    snd.SND_Delete_IpAddress(i_dst_id)
    print_logger(snd)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))


def test_SND_Delete_IpAddress_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: dst_id disagreement")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    i_dst_id = 0x0a03
    print("[In] i_dst_id: " + hex(i_dst_id))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    snd.SND_Delete_IpAddress(i_dst_id)
    print_logger(snd)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))


def test_SND_Initialize_InstanceID_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal com_port")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    print("[In] none")
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    snd.SND_Initialize_InstanceID()
    print_logger(snd)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))


def test_SND_Initialize_InstanceID_2():
    snd2 = SND_CTRL("DUT2", 0x0102, "DUT", "", "192.168.0.20", 5010)
    print()
    print("Test Objective: Normal host and port")
    logger_Mock(snd2)
    
    snd2.d_instance_id_list.clear()
    snd2.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd2.d_instance_id_list[0x0102] = {
            "Con_info": ('192.168.0.20', 5010),
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    print("[In] none")
    print("d_instance_id_list: " + str(snd2.d_instance_id_list))

    snd2.SND_Initialize_InstanceID()
    print_logger(snd2)
    print("d_instance_id_list: " + str(snd2.d_instance_id_list))


def test_SND_Initialize_InstanceID_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: com_port mismatch")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "(192.168.0.20, 5010)",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB2",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    print("[In] none")
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    snd.SND_Initialize_InstanceID()
    print_logger(snd)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))


def test_SND_Update_InstanceID_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")

    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a00,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a00,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_rply_tlv = {
        "Result": 0,
        "NumOfIf": 1,
        "DataList": [
            {
                0: {
                    "SrcId": 0x0102
                },
                1: {
                    "DstId": 0x01
                }
            }
        ]
    }

    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    i_ret = snd.SND_Update_InstanceID(d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_InstanceID_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: NumOfIf is none")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_rply_tlv = {
        "Result": 0,
        "DataList": [
            {
                0: {
                    "SrcId": 0x0102
                },
                1: {
                    "DstId": 0x01
                }
            }
        ]
    }

    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    i_ret = snd.SND_Update_InstanceID(d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Update_InstanceID_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: DataList is none")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_rply_tlv = {
        "Result": 0,
        "NumOfIf": 1
    }

    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    i_ret = snd.SND_Update_InstanceID(d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Update_InstanceID_4():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: DataList num is unmatch")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_rply_tlv = {
        "Result": 0,
        "NumOfIf": 2,
        "DataList": [
            {
                0: {
                    "SrcId": 0x0102,
                },
                1: {
                    "DstId": 0x01
                }
            }
        ]
    }

    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    i_ret = snd.SND_Update_InstanceID(d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Update_InstanceID_5():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SrcId and DstId none")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_rply_tlv = {
        "Result": 0,
        "NumOfIf": 1,
        "DataList": [
            {
                0: {
                    "test_SrcId": 0x0102
                },
                1: {
                    "test_DstId": 0x01
                }
            }
        ]
    }

    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    i_ret = snd.SND_Update_InstanceID(d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_Dhcpd_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "AP",
            "Ipaddr": "192.168.0.60"
        }

    i_src_id = 0x0102
    d_testParam = {}
    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    snd.SND_Set_Dhcpd_Command(i_src_id, d_testParam)
    print_logger(snd)
    print("[Out] d_testParam: " + str(d_testParam))


def test_SND_Set_Dhcpd_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Do not set parameters")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "AP",
            "Ipaddr": "192.168.0.60"
        }

    i_src_id = 0x0102
    d_testParam = {
        "IpAddress": "192.168.0.100",
        "NetMask": "255.255.254.0",
        "GateWay": "192.168.0.1",
        "AssignNum": 25,
        "LeaseTime": 3600
    }
    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))

    snd.SND_Set_Dhcpd_Command(i_src_id, d_testParam)
    print_logger(snd)
    print("[Out] d_testParam: " + str(d_testParam))


def test_SND_Get_IpAddress_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_testParam = {
        "DestDeviceInfoKey": "DUT1"
    }

    print("[In] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Get_IpAddress(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Get_IpAddress_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Get from the second of the list ")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.11"
        }

    d_testParam = {
        "DestDeviceInfoKey": "DUT1"
    }

    print("[In] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Get_IpAddress(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Get_IpAddress_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: DestIpAddress description ")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_testParam = {
        "DestDeviceInfoKey": "DUT1",
        "DestIpAddress": "192.168.0.20"
    }

    print("[In] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Get_IpAddress(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Get_IpAddress_4():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: No description of DestDeviceInfoKey ")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_testParam = {
        "DeviceInfoKey": "DUT1"
    }

    print("[In] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Get_IpAddress(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Get_IpAddress_5():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: I can't find a match DestDeviceInfoKey. ")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": "192.168.0.10"
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "dev/ttyUSB1",
            "Dst_id": 0x0a02,
            "Device_info": "DUT2",
            "Ipaddr": "192.168.0.11"
        }

    d_testParam = {
        "DestDeviceInfoKey": "DUT"
    }

    print("[In] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Get_IpAddress(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_Ping_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    d_testParam = {"DestIpAddress": "192.168.0.10"}

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Ping_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testPram: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Set_Ping_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: DestDeviceInfokey Delete")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    d_testParam = {
        "DestIpAddress": "192.168.0.10",
        "DestDeviceInfoKey": "ENDPOINT"
        }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Ping_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testPram: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Set_Ping_Command_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Get_IpAddress error")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_TLV_ABNORMAL)

    d_testParam = {
        "DestIpAddress": "192.168.0.10",
        "DestDeviceinfoKey": "ENDPOINT"
        }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Ping_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testPram: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_Iperf_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: client")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    d_testParam = {
        "IperfModeType": 2,
        "IperfCmdString": "-t90 -i1",
        "DestIpAddress": "192.168.0.10",
        'DestDeviceInfoKey': 'ENDPOINT'
        }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Iperf_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Set_Iperf_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: server")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    d_testParam = {
        "IperfModeType": 1,
        "IperfCmdString": "-i1",
        "DestDeviceInfoKey": "ENDPOINT"
        }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Iperf_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Set_Iperf_Command_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: IperfModeType none")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    d_testParam = {
        "IperfCmdString": "-t90 -i1",
        "DestIpAddress": "192.168.0.10"
        }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Iperf_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_Iperf_Command_4():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test SND_Get_IpAddress error")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_TLV_ABNORMAL)

    d_testParam = {
        "IperfModeType": 2,
        "IperfCmdString": "-t90 -i1",
        "DestIpAddress": "192.168.0.10"
        }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Iperf_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_Iperf_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Not DestIpAddress and DestDeviceInfoKey")
    logger_Mock(snd)

    snd.SND_Get_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    d_testParam = {
        "IperfModeType": 1,
        "IperfCmdString": "-i1"
        }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Set_Iperf_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Set_Time_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    i_src_id = 0x0101
    d_testParam = {}
    cls_log = LOG_CTRL()
    cls_log.LOG_SetBaseTime = Mock()
    cls_log.LOG_SetBaseTime.return_value = "20181221", "090001"

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + str(cls_log))
    snd.SND_Set_Time_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] d_testParam: " + str(d_testParam))


def test_SND_Set_InitWLAN_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "NumOfIf": 1,
        "DataList": {
            0: {
                "Role": 1
            }
        }
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Set_InitWLAN_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: NumOfIf none")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "DataList": {
            0: {
                "Role": 1
            }
        }
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_InitWLAN_Command_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Number of DataList !=number of src_id list")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "NumOfIf": 2,
        "DataList": {
            0: {
                "Role": 1
            },
            1: {
                "Role": 2
            }
        }
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_InitWLAN_Command_4():
    snd2 = SND_CTRL("DUT1", 0x0101, "DUT1", "", "192.168.0.20", 5010)
    print()
    print("Test Objective: Normal port and host")
    logger_Mock(snd2)

    snd2.d_instance_id_list.clear()
    snd2.d_instance_id_list[0x0101] = {
            "Con_info": ("192.168.0.20", 5010),
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd2.d_instance_id_list[0x0102] = {
            "Con_info": ("192.168.0.20", 5010),
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "NumOfIf": 1,
        "DataList": {
            0: {
                "Role": 1
            }
        }
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd2.d_instance_id_list))
    i_ret = snd2.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd2)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd2.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Set_InitWLAN_Command_5():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: com_port mismatch")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB3",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB3",
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "NumOfIf": 1,
        "DataList": {
            0: {
                "Role": 1
            }
        }
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_InitWLAN_Command_6():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: NumOfIf != DataList")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "NumOfIf": 2,
        "DataList": {
            0: {
                "Role": 1
            }
        }
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_InitWLAN_Command_7():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Not DataList")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }
    snd.d_instance_id_list[0x0102] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT2",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "NumOfIf": 2
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_InitWLAN_Command_8():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: self.i_src_id == i_src_key")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    snd.d_instance_id_list[0x0101] = {
            "Con_info": "/dev/ttyUSB0",
            "Dst_id": 0x0a01,
            "Device_info": "DUT1",
            "Ipaddr": ""
        }

    i_src_id = 0x0101
    d_testParam = {
        "NumOfIf": 1,
        "DataList": {
            0: {
                "Role": 1
            }
        }
    }
    cls_log = ""

    print("[In] i_src_id: " + hex(i_src_id))
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] cls_log: " + cls_log)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    i_ret = snd.SND_Set_InitWLAN_Command(i_src_id, d_testParam, cls_log)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    print("[Out] d_testParam: " + str(d_testParam))
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Check_ConnectAp_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    d_testCriteria = {
        "AbnormalTest": 1,
        "ExpectResult": COM_DEF.i_RET_SUCCESS
    }
    d_rply_tlv = {
        "Result": COM_DEF.i_RET_SUCCESS
    }

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_ConnectAp(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Check_ConnectAp_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: unmatch result")
    logger_Mock(snd)

    d_testCriteria = {
        "AbnormalTest": 1,
        "ExpectResult": COM_DEF.i_RET_SUCCESS
    }
    d_rply_tlv = {
        "Result": COM_DEF.i_RET_TLV_ABNORMAL
    }

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_ConnectAp(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Check_ConnectAp_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Not AbnormalTest")
    logger_Mock(snd)

    d_testCriteria = {
        "ExpectResult": COM_DEF.i_RET_SUCCESS
    }
    d_rply_tlv = {
        "Result": COM_DEF.i_RET_SUCCESS
    }

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_ConnectAp(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Check_ConnectAp_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: AbnormalTest none")
    logger_Mock(snd)

    d_testCriteria = {
        "ExpectResult": COM_DEF.i_RET_SUCCESS
    }
    d_rply_tlv = {
        "Result": COM_DEF.i_RET_SUCCESS
    }

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_ConnectAp(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Check_Apchannel_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    d_testCriteria = {
        "ExpectChannel": 1
    }
    d_rply_tlv = {
        "Channel": 1
    }

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_Apchannel(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Check_Apchannel_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: unmatch channel")
    logger_Mock(snd)

    d_testCriteria = {
        "ExpectChannel": 1
    }
    d_rply_tlv = {
        "Channel": 2
    }

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_Apchannel(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Check_Apchannel_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Channel None")
    logger_Mock(snd)

    d_testCriteria = {
        "ExpectChannel": 1
    }
    d_rply_tlv = {}

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_Apchannel(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Check_Apchannel_4():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: ExpectChannel None")
    logger_Mock(snd)

    d_testCriteria = {}
    d_rply_tlv = {
        "Channel": 1
    }

    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    i_ret = snd.SND_Check_Apchannel(d_testCriteria, d_rply_tlv)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Wait_Event_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    d_testParam = {
        "EventNum": COM_DEF.i_RET_SUCCESS
    }
    que_dev = queue.Queue()
    que_dev.get = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    i_ret = snd.SND_Wait_Event_Command(d_testParam, que_dev)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_WAIT_NEXT_CMD


def test_SND_Wait_Event_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Event Timeout")
    logger_Mock(snd)

    d_testParam = {
        "EventNum": 1
    }
    que_dev = queue.Queue()
    que_dev.get = Mock(return_value=COM_DEF.i_RET_TIMEOUT)

    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    i_ret = snd.SND_Wait_Event_Command(d_testParam, que_dev)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TIMEOUT


def test_SND_Run_Wait_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal TimeSec")
    logger_Mock(snd)

    d_testParam = {
        "TimeSec": 5
    }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Wait_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_WAIT_NEXT_CMD


def test_SND_Run_Wait_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal TimeMsec")
    logger_Mock(snd)

    d_testParam = {
        "TimeMsec": 5
    }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Wait_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_WAIT_NEXT_CMD


def test_SND_Run_Wait_Command_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test none Timesec and TimeMsec")
    logger_Mock(snd)

    d_testParam = {
        "Time": 5
    }

    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Wait_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Run_Continue_Command_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    d_testParam = {
        "ContinueTimes": 5,
        "ContinueOrder": 2
    }

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TEST_CONTINUE


def test_SND_Run_Continue_Command_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: 2call")
    logger_Mock(snd)
    snd.i_continue_ena = 0

    d_testParam = {
        "ContinueTimes": 5,
        "ContinueOrder": 2
    }

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TEST_CONTINUE

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TEST_CONTINUE


def test_SND_Run_Continue_Command_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: i_continue_count > i_continue_max_count")
    logger_Mock(snd)
    snd.i_continue_ena = 1
    snd.i_continue_count = 1
    snd.i_continue_max_count = 0
    d_testParam = {
        "ContinueTimes": 5,
        "ContinueOrder": 2
    }

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_WAIT_NEXT_CMD


def test_SND_Run_Continue_Command_4():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: i_continue_count = i_continue_max_count")
    logger_Mock(snd)
    snd.i_continue_ena = 1
    snd.i_continue_count = 1
    snd.i_continue_max_count = 1
    d_testParam = {
        "ContinueTimes": 5,
        "ContinueOrder": 2
    }

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_WAIT_NEXT_CMD


def test_SND_Run_Continue_Command_5():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: i_continue_count < i_continue_max_count")
    logger_Mock(snd)
    snd.i_continue_ena = 1
    snd.i_continue_count = 1
    snd.i_continue_max_count = 2
    d_testParam = {
        "ContinueTimes": 5,
        "ContinueOrder": 2
    }

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TEST_CONTINUE


def test_SND_Run_Continue_Command_6():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: ContinueTimes none")
    logger_Mock(snd)
    snd.i_continue_ena = 0
    d_testParam = {
        "ContinueOrder": 2
    }

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Run_Continue_Command_7():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: ContinueOrder none")
    logger_Mock(snd)
    snd.i_continue_ena = 0
    d_testParam = {
        "ContinueTimes": 2
    }

    print("i_continue_ena: " + str(snd.i_continue_ena))
    print("i_continue_count: " + str(snd.i_continue_count))
    print("i_continue_max_count: " + str(snd.i_continue_max_count))
    print("[In] d_testParam: " + str(d_testParam))
    i_ret = snd.SND_Run_Continue_Command(d_testParam)
    print_logger(snd)
    print("[Out] i_ret: " + str(i_ret))
    assert i_ret == COM_DEF.i_RET_TLV_ABNORMAL


def test_SND_Set_InstanceID_List_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: Normal")
    logger_Mock(snd)

    snd.d_instance_id_list.clear()
    d_connect_info = "/dev/ttyUSB0"
    s_PeerDevName = "DUT"
    snd.d_instance_id_list.clear()

    print("[In] d_connect_info: " + str(d_connect_info))
    print("[In] s_testParam: " + s_PeerDevName)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))
    snd.SND_Set_InstanceID_List(d_connect_info, s_PeerDevName)
    print_logger(snd)
    print("d_instance_id_list: " + str(snd.d_instance_id_list))


def test_SND_Set_InstanceID_List_2():
    snd2 = SND_CTRL("DUT2", 0x0101, "DUT", "", "192.168.0.20", 5010)
    print()
    print("Test Objective: host and port")
    logger_Mock(snd2)
    
    snd2.d_instance_id_list.clear()
    d_connect_info = (snd2.s_host, snd2.i_port)
    s_PeerDevName = "DUT"
    snd2.d_instance_id_list.clear()

    print("[In] d_connect_info: " + str(d_connect_info))
    print("[In] s_testParam: " + s_PeerDevName)
    print("d_instance_id_list: " + str(snd2.d_instance_id_list))
    snd2.SND_Set_InstanceID_List(d_connect_info, s_PeerDevName)
    print_logger(snd2)
    print("d_instance_id_list: " + str(snd2.d_instance_id_list))


def test_SND_Update_Test_Info_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Check_ConnectAp function call")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "ConnectAp"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Check_Apchannel function call")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "GetApInfo"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Update_InstanceID function call")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "InitWLAN"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_4():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Initialize_InstanceID function call")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "TerminateWLAN"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_5():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Check_IpAddress function call")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "SetIpInfo"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {"IpAddress": "192.168.0.10"}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_6():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Update_IpAddress function call(getipinfo)")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "GetIpInfo"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {"IpAddress": "192.168.0.10"}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_7():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Update_IpAddress function call(startdhcpc)")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "StartDhcpc"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {"IpAddress": "192.168.0.10"}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_8():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Delete_IpAddress function call")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "DisconnectAp"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Update_Test_Info_9():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: No function call")
    logger_Mock(snd)

    snd.SND_Check_ConnectAp = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_Apchannel = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Initialize_InstanceID = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Check_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Update_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Delete_IpAddress = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_retry_cnt = 0
    s_cmd = "StartIperf"
    d_testParam = {}
    d_testCriteria = {}
    d_rply_tlv = {}
    cls_log = 0

    print("[In] i_retry_cnt: " + str(i_retry_cnt))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testCriteria: " + str(d_testCriteria))
    print("[In] d_rply_tlv: " + str(d_rply_tlv))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Update_Test_Info(i_retry_cnt, s_cmd, d_testParam,
                                     d_testCriteria, d_rply_tlv, cls_log)
    print_logger(snd)
    print("[Call count] SND_Check_ConnectAp: " +
          str(snd.SND_Check_ConnectAp.call_count))
    print("[Call count] SND_Check_Apchannel: " +
          str(snd.SND_Check_Apchannel.call_count))
    print("[Call count] SND_Update_InstanceID: " +
          str(snd.SND_Update_InstanceID.call_count))
    print("[Call count] SND_Initialize_InstanceID: " +
          str(snd.SND_Initialize_InstanceID.call_count))
    print("[Call count] SND_Check_IpAddress: " +
          str(snd.SND_Check_IpAddress.call_count))
    print("[Call count] SND_Update_IpAddress: " +
          str(snd.SND_Update_IpAddress.call_count))
    print("[Call count] SND_Delete_IpAddress: " +
          str(snd.SND_Delete_IpAddress.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_1():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Set_InitWLAN_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "InitWLAN"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_2():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Set_Time_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "SetCurrentTime"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_3():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Wait_Event_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "Event"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_4():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Run_Wait_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "Wait"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_5():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Run_Continue_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "Continue"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_6():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Set_Dhcpd_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "StartDhcpd"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_7():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Set_Ping_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "StartPing"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_8():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Set_Iperf_Command function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "StartIperf"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_9():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: SND_Set_Time_Command function call Pattern2")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "ConfirmDevStat"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS


def test_SND_Prepare_Test_Param_10():
    snd = SND_CTRL("DUT1", 0x0101, "DUT", "/dev/ttyUSB0", "", "")
    print()
    print("Test Objective: No function call")
    logger_Mock(snd)

    snd.SND_Set_InitWLAN_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Time_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Wait_Event_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Wait_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Run_Continue_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Dhcpd_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Ping_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)
    snd.SND_Set_Iperf_Command = Mock(return_value=COM_DEF.i_RET_SUCCESS)

    i_src_id = 0x0101
    s_cmd = "DisconnectAp"
    d_testParam = {}
    que_dev = ""
    cls_log = ""

    print("[In] i_src_id: " + str(i_src_id))
    print("[In] s_cmd: " + s_cmd)
    print("[In] d_testParam: " + str(d_testParam))
    print("[In] que_dev: " + str(que_dev))
    print("[In] cls_log: " + str(cls_log))
    i_ret = snd.SND_Prepare_Test_Param(i_src_id, s_cmd, d_testParam,
                                       que_dev, cls_log)
    print_logger(snd)
    print("[Call count] SND_Set_InitWLAN_Command: " +
          str(snd.SND_Set_InitWLAN_Command.call_count))
    print("[Call count] SND_Set_Time_Command: " +
          str(snd.SND_Set_Time_Command.call_count))
    print("[Call count] SND_Wait_Event_Command: " +
          str(snd.SND_Wait_Event_Command.call_count))
    print("[Call count] SND_Run_Wait_Command: " +
          str(snd.SND_Run_Wait_Command.call_count))
    print("[Call count] SND_Run_Continue_Command: " +
          str(snd.SND_Run_Continue_Command.call_count))
    print("[Call count] SND_Set_Dhcpd_Command: " +
          str(snd.SND_Set_Dhcpd_Command.call_count))
    print("[Call count] SND_Set_Ping_Command: " +
          str(snd.SND_Set_Ping_Command.call_count))
    print("[Call count] SND_Set_Iperf_Command: " +
          str(snd.SND_Set_Iperf_Command.call_count))

    assert i_ret == COM_DEF.i_RET_SUCCESS
