# --------------------------------------------------------------------
# AutoEva - Automatic Evaluation System for Wi-Fi
#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# Encode_TLV sub function.
##

# -*- coding: utf-8 -*-
import re
from Debug import Debug_GetObj
from CLS_Define import COM_DEF


##
# @brief Remove separater in test parameter
# @param s_tlv_param    tlv parameter
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : Value other than COM_DEF.i_RET_SUCCESS
# @retval s_encode_data    encode data
# @retval i_encode_len    encode data length
def Encode_TypeParam_RemoveSeparateChar(s_tlv_param, i_module_type):

    i_cnt = 0
    s_return_data = ""

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Encode_TypeParam_RemoveSeparateChar")

    map_int_param = map(int, re.split('[.]', s_tlv_param))
    for i_data in map_int_param:
        s_return_data += hex(i_data)[2:].zfill(2)
        i_cnt += 1

    s_return_len = hex(i_cnt)[2:].zfill(4)

    Dbg.log(COM_DEF.TRACE,
            "[E] Encode_TypeParam_RemoveSeparateChar")

    return s_return_data, s_return_len


##
# @brief Encode Datalist parameter
# @param d_tlv_param    tlv parameter
# @param d_type_info    tlv type info
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : Value other than COM_DEF.i_RET_SUCCESS
# @retval s_encode_data    encode data
# @retval i_encode_len    encode data length
def Encode_TypeParam_DataList(d_tlv_param, d_type_info, i_module_type):

    s_encode_data = ""
    i_encode_data_len = 0
    s_encode_parts = ""
    i_encode_parts_len = 0

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Encode_TypeParam_DataList")

    i_cnt = 0
    i_list_num = len(d_tlv_param)
    while i_cnt < i_list_num:

        key_list = d_tlv_param[i_cnt].keys()
        for s_tlv_type in key_list:

            s_id = ""
            try:
                s_id = hex(d_type_info[s_tlv_type]["ID"])[2:].zfill(4)
                i_encode_parts_len += 2
            except Exception as err_info:
                Dbg.log(COM_DEF.ERROR,
                        "unexpected error (id)")
                Dbg.log(COM_DEF.ERROR,
                        err_info)
                return "", 0

            s_tlv_len = ""
            try:
                s_tlv_len = hex(d_type_info[s_tlv_type]["Length"])[2:].zfill(4)
                i_encode_parts_len += 2
            except Exception as err_info:
                Dbg.log(COM_DEF.ERROR,
                        "unexpected error (tlv length)")
                Dbg.log(COM_DEF.ERROR,
                        err_info)
                return "", 0

            tlv_param = d_tlv_param[i_cnt][s_tlv_type]

            s_tlv_data = ""
            if ("IpAddress" == s_tlv_type or "NetMask" == s_tlv_type or
                    "GateWay" == s_tlv_type) and isinstance(tlv_param, str):
                        s_tlv_data, s_tlv_len = \
                            Encode_TypeParam_RemoveSeparateChar(tlv_param,
                                                                i_module_type)
            elif ("MacAddress" == s_tlv_type or "DestAddr" == s_tlv_type or
                  "TransAddr" == s_tlv_type or
                  "SourceAddr" == s_tlv_type) and isinstance(tlv_param, str):
                s_tlv_data = tlv_param.replace(":", "")

                i_tlv_param_len = len(s_tlv_data) >> 1
                s_tlv_len = str(6).zfill(4)
            else:
                if isinstance(tlv_param, str):
                    # considere that user parameter is longer than
                    # default value
                    i_tlv_param_len = len(tlv_param)
                    s_tlv_len = hex(i_tlv_param_len)[2:].zfill(4)

                    for s_param in tlv_param:
                        s_tlv_data += hex(ord(s_param))[2:]
                elif isinstance(tlv_param, int):
                    # the length value used in Encode_TypeParameter.json
                    s_tlv_len = s_tlv_len
                    if tlv_param < 0:
                        i_tlv_len = int(s_tlv_len)
                        mask = (1 << (i_tlv_len * 8)) - 1
                        s_tlv_data = str(format((tlv_param - 1) & mask, 'x'))
                    else:
                        s_tlv_data = hex(tlv_param)[2:].zfill(int(s_tlv_len)*2)
                else:
                    pass

            i_encode_parts_len += int(s_tlv_len, 16)

            Dbg.log(COM_DEF.DEBUG,
                    "TYPE    : 0x%s (%s)"
                    % (s_id, s_tlv_type))

            Dbg.log(COM_DEF.DEBUG,
                    "LEN     : 0x%s (%d)"
                    % (s_tlv_len, d_type_info[s_tlv_type]["Length"]))

            Dbg.log(COM_DEF.DEBUG,
                    "VALUE   : 0x%s" % (s_tlv_data))

            s_encode_parts += s_id
            s_encode_parts += s_tlv_len
            s_encode_parts += s_tlv_data
        # for loop end

        s_encode_data += str(COM_DEF.i_TYPE_DataList).zfill(4)
        i_encode_data_len += 2
        s_encode_data += hex(i_encode_parts_len)[2:].zfill(4)
        i_encode_data_len += 2
        s_encode_data += s_encode_parts
        i_encode_data_len += i_encode_parts_len

        s_encode_parts = ""
        i_encode_parts_len = 0

        i_cnt += 1

    # while loop end

    Dbg.log(COM_DEF.TRACE,
            "[E] Encode_TypeParam_DataList")

    return s_encode_data, hex(i_encode_data_len)[2:].zfill(4)
