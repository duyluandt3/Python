#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This function decoded from tlv information to command.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

from Common_TLVInfo import Common_Get_TLVInfo
from Common_TLVInfo import Common_Get_TypeInfo
from Common_TLVInfo import Common_Get_TypeReverseInfo
from CLS_Define import COM_DEF
from Debug import Debug_GetObj
from collections import OrderedDict


##
# @brief Format check of decoded result.
# @param i_src_id    source id
# @param s_tlv_type    tlv type
# @param i_tlv_len    tlv data length
# @param s_tlv_form    tlv data type form
# @param i_pos    tlv pointer position
# @param l_tlv_data    tlv byte data
# @param d_type_info    tlv type information
# @param l_tlv_id_list    mandatory parameter id list
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : Value other than COM_DEF.i_RET_SUCCESS
# @retval tlv_data    tlv data (dict/str/int) \n
#                         - "DataList" : dict \n
#                         - string parameter : string \n
#                         - other : integer
def Decode_FormatCheck(i_src_id, s_tlv_type, i_tlv_len, s_tlv_form,
                       i_pos, l_tlv_data, d_type_info, l_tlv_id_list,
                       i_module_type):

    i_cnt = 0
    i_dec_cnt = 0
    s_separator_chr = ""

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Decode_FormatCheck")

    if ("IpAddress" == s_tlv_type or "NetMask" == s_tlv_type or
        "GateWay" == s_tlv_type) and \
            s_tlv_form == "Str":
                s_separator_chr = "."

    elif ("MacAddress" == s_tlv_type or
          "DestAddr" == s_tlv_type or
          "TransAddr" == s_tlv_type or
          "SourceAddr" == s_tlv_type) and s_tlv_form == "Str":
            s_separator_chr = ":"

    elif "DataList" == s_tlv_type:
        d_data_list = OrderedDict()

        while i_cnt < i_tlv_len:

            i_tlv_id = (int(l_tlv_data[i_pos+i_cnt], 16) << 8) + \
                (int(l_tlv_data[i_pos+i_cnt + 1], 16))
            l_tlv_id_list.append(i_tlv_id)
            i_cnt += 2

            s_type = d_type_info[str(i_tlv_id)]["Type"]
            Dbg.log(COM_DEF.DEBUG,
                    "[0x%04x] " % i_src_id +
                    "TYPE    : %s (0x%04x)" % (s_type, i_tlv_id))

            i_tlv_sublen = (int(l_tlv_data[i_pos+i_cnt], 16) << 8) + \
                (int(l_tlv_data[i_pos+i_cnt + 1], 16))
            i_cnt += 2

            if d_type_info[str(i_tlv_id)]["Length"] != 0 and \
                    i_tlv_sublen != d_type_info[str(i_tlv_id)]["Length"]:
                Dbg.log(COM_DEF.ERROR,
                        "[0x%04x] " % i_src_id +
                        "length mismatch : %d" % (i_tlv_sublen))
                return COM_DEF.i_RET_TLV_ABNORMAL, {}
            else:
                pass

            Dbg.log(COM_DEF.DEBUG,
                    "[0x%04x] " % i_src_id +
                    "LEN     : %d" % (i_tlv_sublen))

            i_ret, d_data_list[s_type] = \
                Decode_FormatCheck(i_src_id, s_type, i_tlv_sublen,
                                   d_type_info[str(i_tlv_id)]["Form"],
                                   i_pos+i_cnt, l_tlv_data, d_type_info,
                                   l_tlv_id_list, i_module_type)
            if COM_DEF.i_RET_SUCCESS != i_ret:
                Dbg.log(COM_DEF.ERROR,
                        "Decode_FormatCheck error [ret:%d]" %
                        (i_ret))
                return i_ret, {}
            else:
                i_cnt += i_tlv_sublen
        # while end

        return COM_DEF.i_RET_SUCCESS, d_data_list
    else:
        pass

    if "Str" == s_tlv_form:
        s_tlv_data = ""

        while i_cnt < i_tlv_len:
            if ":" == s_separator_chr:
                s_tlv_data += l_tlv_data[i_pos+i_cnt]
            elif "." == s_separator_chr:
                s_tlv_data += str(int(l_tlv_data[i_pos+i_cnt], 16))
            else:
                s_tlv_data += chr(int(l_tlv_data[i_pos+i_cnt], 16))

            i_cnt += 1
            if i_cnt < i_tlv_len:
                s_tlv_data += s_separator_chr
            else:
                pass
        else:
            pass

        Dbg.log(COM_DEF.DEBUG,
                "[0x%04x] " % i_src_id +
                "VALUE   : %s" % (s_tlv_data))

        Dbg.log(COM_DEF.TRACE, "[E] Decode_FormatCheck")

        return COM_DEF.i_RET_SUCCESS, s_tlv_data
    else:
        i_tlv_data = 0
        i_dec_cnt = i_tlv_len
        while 0 != i_dec_cnt:
            i_tlv_data += int(l_tlv_data[i_pos+i_cnt], 16) << (i_dec_cnt-1)*8
            i_dec_cnt -= 1
            i_cnt += 1
        else:
            pass

        Dbg.log(COM_DEF.DEBUG,
                "[0x%04x] " % i_src_id +
                "VALUE   : " + hex(i_tlv_data))

        Dbg.log(COM_DEF.TRACE, "[E] Decode_FormatCheck")

        return COM_DEF.i_RET_SUCCESS, i_tlv_data


##
# @brief Decode command data, get common header and TLV data,
#        and check parameters.
# @param i_dst_id    destination id
# @param i_src_id    source id
# @param i_cmd_id    command id
# @param i_action    action id
# @param i_all_tlv_len    the all tlv length of command
# @param s_tlv_data    tlv data
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @param s_device_type    device type
# @retval i_ret_result    value of the result \n
#                           - Success : COM_DEF.i_RET_SUCCESS \n
#                           - Failure : Value other than COM_DEF.i_RET_SUCCESS
# @retval d_return_data    decode data
def Decode_TLV(i_dst_id, i_src_id, i_cmd_id, i_action, i_all_tlv_len,
               s_tlv_data, i_module_type, s_device_type):

    d_return_data = {}
    i_ret_result = 1  # result tlv value is less than 0

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE, "[S] Decode_TLV")

    # Get mandatory tlv parameter written for each interface
    i_result, d_default_tlv_info = Common_Get_TLVInfo(s_device_type,
                                                      i_action,
                                                      COM_DEF.i_DECODE_FLG,
                                                      i_module_type)
    if COM_DEF.i_RET_SUCCESS != i_result:
        Dbg.log(COM_DEF.DEBUG,
                "[0x%04x] " % i_src_id +
                "failed to open tlv json")
        return COM_DEF.i_RET_SYSTEM_ERROR, {}
    else:
        pass

    # get mandatory tlv to match command response
    try:
        d_cmd_tlv_all_info = d_default_tlv_info[i_cmd_id]
        if i_action & COM_DEF.i_ACTION_LOWERMASK:
            # Mandatory SET parameter
            d_cmd_tlv_info = d_cmd_tlv_all_info[str(i_cmd_id)]["SET"]
        else:
            d_cmd_tlv_info = d_cmd_tlv_all_info[str(i_cmd_id)]["GET"]
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "[0x%04x] " % i_src_id +
                "failed to find tlv : 0x%04x" % (i_cmd_id))
        Dbg.log(COM_DEF.ERROR,
                err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, {}

    # get command name
    d_return_data["Command"] = d_cmd_tlv_info["Name"]

    # set data to list by separating byte unit
    l_tlv_data_list = \
        [(cnt+offset) for (cnt, offset) in zip(s_tlv_data[::2],
                                               s_tlv_data[1::2])]

    # get the reversed info of tlv
    i_result, d_type_info = Common_Get_TypeReverseInfo(i_module_type)
    if i_result:
        Dbg.log(COM_DEF.DEBUG,
                "[0x%04x] " % i_src_id +
                "Common_Get_TypeReverseInfo error [ret:%d]" %
                (i_result))
        return COM_DEF.i_RET_SYSTEM_ERROR, {}
    else:
        pass

    i_cnt = 0
    l_tlv_id_list = []
    while i_cnt < i_all_tlv_len:

        i_tlv_id = (int(l_tlv_data_list[i_cnt], 16) << 8) + \
                (int(l_tlv_data_list[i_cnt + 1], 16))
        l_tlv_id_list.append(i_tlv_id)
        i_cnt += COM_DEF.i_TLV_Type_Length

        s_type = d_type_info[str(i_tlv_id)]["Type"]
        Dbg.log(COM_DEF.DEBUG,
                "[0x%04x] " % i_src_id +
                "TYPE    : %s (0x%04x)" %
                (s_type, i_tlv_id))

        i_tlv_len = (int(l_tlv_data_list[i_cnt], 16) << 8) + \
            (int(l_tlv_data_list[i_cnt + 1], 16))
        i_cnt += COM_DEF.i_TLV_Len_Length

        # get length value
        if d_type_info[str(i_tlv_id)]["Length"] != 0 and \
                i_tlv_len != d_type_info[str(i_tlv_id)]["Length"]:
                    Dbg.log(COM_DEF.ERROR,
                            "[0x%04x] " % i_src_id +
                            "length mismatch : %d" % (i_tlv_len))
                    return COM_DEF.i_RET_TLV_ABNORMAL, {}
        else:
            pass

        Dbg.log(COM_DEF.DEBUG,
                "[0x%04x] " % i_src_id +
                "LEN     : %d" % (i_tlv_len))

        if "DataList" == s_type:

            d_return_list = OrderedDict()
            i_ret, d_return_list[s_type] = \
                Decode_FormatCheck(i_src_id, s_type, i_tlv_len,
                                   d_type_info[str(i_tlv_id)]["Form"],
                                   i_cnt, l_tlv_data_list, d_type_info,
                                   l_tlv_id_list, i_module_type)

            d_return_data.setdefault(s_type, []).append(d_return_list[s_type])
        else:
            i_ret, d_return_data[s_type] = \
                Decode_FormatCheck(i_src_id, s_type, i_tlv_len,
                                   d_type_info[str(i_tlv_id)]["Form"],
                                   i_cnt, l_tlv_data_list, d_type_info,
                                   l_tlv_id_list, i_module_type)

        if i_ret:
            Dbg.log(COM_DEF.DEBUG,
                    "Decode_FormatCheck error [ret:%d]" % i_ret)
        else:
            pass

        i_cnt += i_tlv_len
    # while loop end

    # Reverses the sign of the "Result" parameter
    if (i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_REQ:
        pass
    else:
        if COM_DEF.i_RET_SUCCESS != d_return_data["Result"]:
            d_return_data["Result"] = d_return_data["Result"] - 0x0001 - 0xffff
            return d_return_data["Result"], d_return_data
        else:
            pass

    # ack command
    if (i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_ACK:

        Dbg.log(COM_DEF.TRACE, "[E] Decode_TLV")

        return COM_DEF.i_RET_SUCCESS, d_return_data
    else:
        pass

    # Get tlv info
    i_ret_result, d_type_info = Common_Get_TypeInfo(i_module_type)
    if COM_DEF.i_RET_SUCCESS != i_ret_result:
        return i_ret_result, {}
    else:
        pass

    # check mandatory parameter
    l_mandatory_list = d_cmd_tlv_info["Mandatory"]

    for s_mandatory_tlv in l_mandatory_list:
        d_tlv_info = d_type_info[s_mandatory_tlv]

        # ID
        i_mandatory_id = d_tlv_info["ID"]

        for i_tlv_id in l_tlv_id_list:
            if i_mandatory_id == i_tlv_id:
                # mandatory parameter is set
                break
            else:
                pass
        else:
            Dbg.log(COM_DEF.ERROR,
                    "[0x%04x] " % i_src_id +
                    "failed to find [%s]" % s_mandatory_tlv)
            i_ret_result = COM_DEF.i_RET_TLV_ABNORMAL
    # for loop end

    Dbg.log(COM_DEF.TRACE, "[E] Decode_TLV")

    return i_ret_result, d_return_data
