#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This function encode from user parameter to tlv data.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

from Common_TLVInfo import Common_Get_TLVInfo
from Common_TLVInfo import Common_Get_TypeInfo
from Encode_TypeParam import Encode_TypeParam_RemoveSeparateChar
from Encode_TypeParam import Encode_TypeParam_DataList
from CLS_Define import COM_DEF
from Debug import Debug_GetObj


##
# @brief Format check of encoded result.
# @param s_tlv_type    tlv type
# @param tlv_param    tlv parameter
# @param s_tlv_len    tlv_param length
# @param d_type_info    tlv type information
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval s_return_data    encoded data
# @retval s_return_len    length of encoded data
def Encode_FormatCheck(s_tlv_type, tlv_param, s_tlv_len,
                       d_type_info, i_module_type):

    s_return_data = ""
    s_return_len = ""

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Encode_FormatCheck")

    if ("IpAddress" == s_tlv_type or "NetMask" == s_tlv_type or
            "GateWay" == s_tlv_type) and isinstance(tlv_param, str):
        s_return_data, s_return_len = \
            Encode_TypeParam_RemoveSeparateChar(tlv_param,
                                                i_module_type)

    elif ("MacAddress" == s_tlv_type or "DestAddr" == s_tlv_type or
          "TransAddr" == s_tlv_type or "SourceAddr" == s_tlv_type) and \
            isinstance(tlv_param, str):
        s_return_data = tlv_param.replace(":", "")

        i_tlv_param_len = len(s_return_data) >> 1
        s_return_len = hex(i_tlv_param_len)[2:].zfill(4)

    elif "DataList" == s_tlv_type and isinstance(tlv_param, list):
        s_return_data, s_return_len = Encode_TypeParam_DataList(tlv_param,
                                                                d_type_info,
                                                                i_module_type)
    elif ("Date" == s_tlv_type or
          "Time" == s_tlv_type) and isinstance(tlv_param, str):
        s_return_len = s_tlv_len
        s_return_data = tlv_param

    else:
        if isinstance(tlv_param, str):
            # considere that user parameter is longer than default value
            i_tlv_param_len = len(tlv_param)
            s_return_len = hex(i_tlv_param_len)[2:].zfill(4)

            for s_param in tlv_param:
                s_return_data += hex(ord(s_param))[2:]

        elif isinstance(tlv_param, int):
            # the length value used in Encode_TypeParameter.json
            s_return_len = s_tlv_len
            if tlv_param < 0:
                i_tlv_len = int(s_tlv_len)
                mask = (1 << (i_tlv_len * 8)) - 1
                s_return_data = str(format((tlv_param) & mask, 'x'))
            else:
                s_return_data = hex(tlv_param)[2:].zfill(int(s_tlv_len)*2)
        else:
            # dict data
            pass

    Dbg.log(COM_DEF.TRACE,
            "[E] Encode_FormatCheck")

    return s_return_data, s_return_len


##
# @brief Encode the common header and TLV data of the request command.
# @param s_device_type    device type
# @param i_src_id    source id
# @param s_command    command string
# @param d_User_Param    user parameter
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : Value other than COM_DEF.i_RET_SUCCESS
# @retval i_cmd_id    command id
# @retval i_action    action id
# @retval s_encode_data    encode data
# @retval i_encode_len    encode data length
# @retval i_maxRetryCount    max retry counter
# @retval i_waitRspTimer    wait time for command response
def Encode_TLV_Req(s_device_type, i_src_id, s_command, d_User_Param,
                   i_module_type):

    s_encode_data = ""
    i_encode_len = 0
    l_user_param_type = []

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Encode_TLV_Req")

    # Get mandatory tlv parameter written for each interface
    i_result, d_default_tlv_info = Common_Get_TLVInfo(s_device_type,
                                                      COM_DEF.i_ACTION_REQ,
                                                      COM_DEF.i_ENCODE_FLG,
                                                      i_module_type)
    if COM_DEF.i_RET_SUCCESS != i_result:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "Common_Get_TLVInfo error [ret:%d]" % (i_result))
        return COM_DEF.i_RET_SYSTEM_ERROR, "None", 0, 0, "None", 0, 0
    else:
        pass

    try:
        d_cmd_tlv_info = d_default_tlv_info[s_command]
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "failed to access tlv data")
        Dbg.log(COM_DEF.ERROR,
                err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, "None", 0, 0, "None", 0, 0

    # get default type parameter
    i_result, d_type_info = Common_Get_TypeInfo(i_module_type)
    if i_result:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "Common_Get_TypeInfo error [ret:%d]" % (i_result))
        COM_DEF.i_RET_SYSTEM_ERROR, "None", 0, 0, "None", 0, 0
    else:
        pass

    for s_tlv_type in list(d_cmd_tlv_info):

        if "MaxRetryCount" == s_tlv_type:
            i_maxRetryCount = d_cmd_tlv_info["MaxRetryCount"]
        elif "WaitRspTime" == s_tlv_type:
            i_waitRspTimer = d_cmd_tlv_info["WaitRspTime"]
        elif "CmdId" == s_tlv_type:
            i_cmd_id = d_cmd_tlv_info["CmdId"]
        elif "Action" == s_tlv_type:
            i_action = d_cmd_tlv_info["Action"]
        else:
            s_id = ""
            try:
                s_id = hex(d_type_info[s_tlv_type]["ID"])[2:].zfill(4)
            except Exception as err_info:
                Dbg.log(COM_DEF.ERROR,
                        "[0x%04x] " % i_src_id +
                        "unexpected error (id)")
                Dbg.log(COM_DEF.ERROR,
                        err_info)
                return COM_DEF.i_RET_SYSTEM_ERROR, "None", 0, 0, "None", 0, 0

            s_tlv_len = ""
            try:
                s_tlv_len = hex(d_type_info[s_tlv_type]["Length"])[2:].zfill(4)
            except Exception as err_info:
                Dbg.log(COM_DEF.ERROR,
                        "[0x%04x] " % i_src_id +
                        "unexpected error (tlv length)")
                Dbg.log(COM_DEF.ERROR,
                        err_info)
                return COM_DEF.i_RET_SYSTEM_ERROR, "None", 0, 0, "None", 0, 0

            # check user parameter
            if s_tlv_type in d_User_Param:
                tlv_param = d_User_Param[s_tlv_type]
#                del d_User_Param[s_tlv_type]
                l_user_param_type.append(s_tlv_type)
            else:
                tlv_param = d_type_info[s_tlv_type]["Value"]

            # Format change is needed about a part of string parameter.
            # check and change tlv param in this funcition
            s_tlv_value, s_tlv_len = Encode_FormatCheck(s_tlv_type,
                                                        tlv_param,
                                                        s_tlv_len,
                                                        d_type_info,
                                                        i_module_type)

            if "DataList" == s_tlv_type:
                s_encode_data += s_tlv_value
                i_encode_len += int(s_tlv_len, 16)
            else:
                Dbg.log(COM_DEF.DEBUG,
                        "[0x%04x] " % i_src_id +
                        "TYPE    : 0x%s (%s)" %
                        (s_id, s_tlv_type))

                Dbg.log(COM_DEF.DEBUG,
                        "[0x%04x] " % i_src_id +
                        "LEN     : 0x%s (%d)" %
                        (s_tlv_len, d_type_info[s_tlv_type]["Length"]))

                Dbg.log(COM_DEF.DEBUG,
                        "[0x%04x] " % i_src_id +
                        "VALUE   : 0x%s" % (s_tlv_value))

                s_encode_data += s_id + s_tlv_len + s_tlv_value
                i_encode_len += COM_DEF.i_TLV_Type_Length
                i_encode_len += COM_DEF.i_TLV_Len_Length
                i_encode_len += int(s_tlv_len, 16)

    # for loop end

    if d_User_Param:

        for s_tlv_type in list(d_User_Param):
            if s_tlv_type not in l_user_param_type:
                try:
                    d_tlv_info = d_type_info[s_tlv_type]
                except Exception as err_info:
                    Dbg.log(COM_DEF.ERROR, err_info)
                    return \
                        COM_DEF.i_RET_TLV_ABNORMAL, "None", 0, 0, "None", 0, 0

                s_id = hex(d_tlv_info["ID"])[2:].zfill(4)

                s_tlv_len = hex(d_tlv_info["Length"])[2:].zfill(4)

                tlv_param = d_User_Param[s_tlv_type]

                # Format change is needed about a part of string parameter.
                # check and change tlv param in this funcition
                s_tlv_value, s_tlv_len = Encode_FormatCheck(s_tlv_type,
                                                            tlv_param,
                                                            s_tlv_len,
                                                            d_type_info,
                                                            i_module_type)

                if "DataList" == s_tlv_type:
                    s_encode_data += s_tlv_value
                    i_encode_len += int(s_tlv_len, 16)
                else:
                    Dbg.log(COM_DEF.DEBUG,
                            "[0x%04x] " % i_src_id +
                            "TYPE    : 0x%s (%s)" %
                            (s_id, s_tlv_type))

                    Dbg.log(COM_DEF.DEBUG,
                            "[0x%04x] " % i_src_id +
                            "LEN     : 0x%s (%d)" %
                            (s_tlv_len, d_type_info[s_tlv_type]["Length"]))

                    Dbg.log(COM_DEF.DEBUG,
                            "[0x%04x] " % i_src_id +
                            "VALUE   : 0x%s" % (s_tlv_value))

                    s_encode_data += s_id + s_tlv_len + s_tlv_value
                    i_encode_len += COM_DEF.i_TLV_Type_Length
                    i_encode_len += COM_DEF.i_TLV_Len_Length
                    i_encode_len += int(s_tlv_len, 16)
            else:
                # user parameter already is setted.
                Dbg.log(COM_DEF.TRACE,
                        s_tlv_type + " already is setted !!")
        # for loop end
    else:
        pass

    Dbg.log(COM_DEF.TRACE,
            "[E] Encode_TLV_Req")

    return COM_DEF.i_RET_SUCCESS, i_cmd_id, i_action, s_encode_data, \
        i_encode_len, i_maxRetryCount, i_waitRspTimer


##
# @brief Encode the common header and TLV data of the ack command.
# @param i_dst_id    destination id
# @param i_src_id    source id
# @param i_cmd_id    command id
# @param i_result_value    ack command result value
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_result    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
# @retval i_tlv_all_len    length of encoded data
# @retval s_tlv_data    encoded data
def Encode_TLV_Ack(i_dst_id, i_src_id, i_cmd_id, i_result_value,
                   i_module_type):

    # ID + length parameter length
    i_tlv_def_len = 4

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Encode_TLV_Ack")

    # get default type parameter
    i_result, d_type_info = Common_Get_TypeInfo(i_module_type)
    if i_result:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "Common_Get_TypeInfo error [ret:%d]" % (i_result))
        return COM_DEF.i_RET_SYSTEM_ERROR, 0, "None"
    else:
        pass

    i_id = d_type_info["Result"]["ID"]
    s_tlv_data = hex(i_id)[2:].zfill(4)

    Dbg.log(COM_DEF.DEBUG,
            "[0x%04x] " % i_src_id +
            "TYPE    : 0x%s (Result)" % (s_tlv_data))

    i_tlv_len = d_type_info["Result"]["Length"]
    s_tlv_data += hex(i_tlv_len)[2:].zfill(4)

    Dbg.log(COM_DEF.DEBUG,
            "[0x%04x] " % i_src_id +
            "LEN     : 0x%s" % (s_tlv_data[4:]))

    # Set Result tlv
    s_tlv_data += '{:02x}'.format(i_result_value & 0xffff).zfill(4)

    Dbg.log(COM_DEF.DEBUG,
            "[0x%04x] " % i_src_id +
            "VALUE   : 0x%s" % (s_tlv_data[8:]))

    i_tlv_all_len = i_tlv_def_len + i_tlv_len

    Dbg.log(COM_DEF.TRACE,
            "[E] Encode_TLV_Ack")

    return COM_DEF.i_RET_SUCCESS, i_tlv_all_len, s_tlv_data


##
# @brief Encode the common header and TLV data of the response command.
# @param s_device_type    device type
# @param i_src_id    source id
# @param i_cmd_id    command id
# @param i_action    action id
# @param d_User_Param    user parameter
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_result    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : Value other than COM_DEF.i_RET_SUCCESS
# @retval s_encode_data    encoded data
# @retval i_encode_len    length of encoded data
def Encode_TLV_Rsp(s_device_type, i_src_id, i_cmd_id, i_action, d_User_Param,
                   i_module_type):

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Encode_TLV_Rsp")

    # Get mandatory tlv parameter written for each interface
    i_result, d_default_tlv_info = Common_Get_TLVInfo(s_device_type,
                                                      COM_DEF.i_ACTION_RSP,
                                                      COM_DEF.i_ENCODE_FLG,
                                                      i_module_type)

    if COM_DEF.i_RET_SUCCESS != i_result:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "Common_Get_TLVInfo error [ret:%d]" % (i_result))
        return COM_DEF.i_RET_SYSTEM_ERROR, "None", 0
    else:
        pass

    # get mandatory tlv to match command response
    try:
        d_cmd_tlv_all_info = d_default_tlv_info[i_cmd_id]
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "failed to access tlv data")
        Dbg.log(COM_DEF.ERROR,
                err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, "None", 0

    if i_action & COM_DEF.i_ACTION_LOWERMASK:
        # Mandatory SET parameter
        d_cmd_tlv_info = d_cmd_tlv_all_info[str(i_cmd_id)]["SET"]
    else:
        d_cmd_tlv_info = d_cmd_tlv_all_info[str(i_cmd_id)]["GET"]

    # get default type parameter
    i_result, d_type_info = Common_Get_TypeInfo(i_module_type)
    if i_result:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "Common_Get_TypeInfo error [ret:%d]" % (i_result))
        return COM_DEF.i_RET_SYSTEM_ERROR, "None", 0
    else:
        pass

    l_mandatory_list = d_cmd_tlv_info["Mandatory"]
    i_encode_len = 0
    s_encode_data = ""
    for s_mandatory_tlv in l_mandatory_list:
        d_tlv_info = d_type_info[s_mandatory_tlv]

        # ID
        s_id = hex(d_tlv_info["ID"])[2:].zfill(4)

        # Length
        s_tlv_len = hex(d_tlv_info["Length"])[2:].zfill(4)

        if s_mandatory_tlv in d_User_Param:
            tlv_param = d_User_Param[s_mandatory_tlv]
            del d_User_Param[s_mandatory_tlv]
        else:
            tlv_param = d_tlv_info["Value"]

        # Format change is needed about a part of string parameter.
        # check and change tlv param in this funcition
        s_tlv_value, s_tlv_len = Encode_FormatCheck(s_mandatory_tlv,
                                                    tlv_param, s_tlv_len,
                                                    d_type_info,
                                                    i_module_type)

        if "DataList" == s_mandatory_tlv:
            s_encode_data += s_tlv_value
            i_encode_len += int(s_tlv_len, 16)
        else:
            Dbg.log(COM_DEF.DEBUG,
                    "[0x%04x] " % i_src_id +
                    "TYPE    : 0x%s (%s)" %
                    (s_id, s_mandatory_tlv))

            Dbg.log(COM_DEF.DEBUG,
                    "[0x%04x] " % i_src_id +
                    "LEN     : 0x%s (%d)" %
                    (s_tlv_len, d_tlv_info["Length"]))

            Dbg.log(COM_DEF.DEBUG,
                    "[0x%04x] " % i_src_id +
                    "VALUE   : 0x%s" % (s_tlv_value))

            s_encode_data += s_id + s_tlv_len + s_tlv_value

            # add ID and Length size (2 byte + 2 byte) to data length
            i_encode_len += COM_DEF.i_TLV_Type_Length
            i_encode_len += COM_DEF.i_TLV_Len_Length
            i_encode_len += int(s_tlv_len, 16)

    # for loop end

    if d_User_Param:

        for s_tlv_type in list(d_User_Param):
            try:
                d_tlv_info = d_type_info[s_tlv_type]
            except Exception as err_info:
                Dbg.error(err_info)
                return COM_DEF.i_RET_TLV_ABNORMAL, "None", 0
            # ID
            s_id = hex(d_tlv_info["ID"])[2:].zfill(4)

            # Length
            s_tlv_len = hex(d_tlv_info["Length"])[2:].zfill(4)

            tlv_param = d_User_Param[s_tlv_type]
            del d_User_Param[s_tlv_type]

            # Format change is needed about a part of string parameter.
            # check and change tlv param in this funcition
            s_tlv_value, s_tlv_len = Encode_FormatCheck(s_tlv_type,
                                                        tlv_param, s_tlv_len,
                                                        d_type_info,
                                                        i_module_type)

            if "DataList" == s_tlv_type:
                s_encode_data += s_tlv_value
                i_encode_len += int(s_tlv_len, 16)
            else:
                Dbg.log(COM_DEF.DEBUG,
                        "[0x%04x] " % i_src_id +
                        "TYPE    : 0x%s (%s)" %
                        (s_id, s_tlv_type))

                Dbg.log(COM_DEF.DEBUG,
                        "[0x%04x] " % i_src_id +
                        "LEN     : 0x%s (%d)" %
                        (s_tlv_len, d_tlv_info["Length"]))

                Dbg.log(COM_DEF.DEBUG,
                        "[0x%04x] " % i_src_id +
                        "VALUE   : 0x%s" % (s_tlv_value))

                s_encode_data += s_id + s_tlv_len + s_tlv_value

                # add ID and Length size (2 byte + 2 byte) to data length
                i_encode_len += COM_DEF.i_TLV_Type_Length
                i_encode_len += COM_DEF.i_TLV_Len_Length
                i_encode_len += int(s_tlv_len, 16)
        # for loop end
    else:
        pass

    Dbg.log(COM_DEF.TRACE,
            "[E] Encode_TLV_Rsp")

    return COM_DEF.i_RET_SUCCESS, s_encode_data, i_encode_len
