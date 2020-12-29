#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief Common_TLVInfo sub function.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import json
from Debug import Debug_GetObj
from CLS_Define import COM_DEF

##
#   @brief List containing encoder information for request command.
REQUEST_ENCODER_LIST = {}

##
#  @brief List containing decoder information for request command.
REQUEST_DECODER_LIST = {}

##
#   @brief List containing encoder information for response command.
RESPONSE_ENCODER_LIST = {}

##
#   @brief List containing decoder information for response command.
RESPONSE_DECODER_LIST = {}

##
#   @brief List containing default values of TLV format.
d_TYPE_PARAM = {}

##
#   @brief List containing TLV format information corresponding to command ID.
d_TYPE_REVERSE_PARAM = {}


##
# @brief Open the file specified at argv1 (s_file_name)
#        and read the decoded or encoded information.
# @param s_file_name   json file name
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
# @retval d_data_info    Read data of "Common/decode_encode/json/*.json"
def Common_OpenFile(s_file_name, i_module_type):

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Common_OpenFile")

    try:
        # tlv file that mandatory paramter is written
        with open(COM_DEF.s_TOPDIR +
                  "/Common/decode_encode/json/" +
                  s_file_name, "r",
                  encoding='utf-8-sig') as f_data:
            d_data_info = json.load(f_data)
    except Exception as err_info:
        Dbg.log(COM_DEF.ERROR,
                "failed to read " + s_file_name)
        Dbg.log(COM_DEF.ERROR,
                err_info)
        return COM_DEF.i_RET_SYSTEM_ERROR, 0

    Dbg.log(COM_DEF.TRACE,
            "[E] Common_OpenFile")

    return COM_DEF.i_RET_SUCCESS, d_data_info


##
# @brief Get tlv information from encode or decode file as following. \n
#     ex) \n
#     - DUT_request_encorder.json \n
#     - DUT_response_encorder.json \n
#     - DUT_request_decorder.json \n
#     - DUT_response_decorder.json \n
#     If tlv information already be read, return data in the global area.
# @param s_dev_type   device type
# @param i_action   action id
# @param i_dcdenc_flg   decode/encode type \n
#                           - 0 : decode \n
#                           - 1 : encode
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
# @retval decode/encode_list     decode/encode list of tlv command list \n
#             - Request decode : REQUEST_DECODER_LIST \n
#             - Request encode : REQUEST_ENCODER_LIST \n
#             - Response decode : RESPONSE_DECODER_LIST \n
#             - Response encode : RESPONSE_ENCODER_LIST
def Common_Get_TLVInfo(s_dev_type, i_action, i_dcdenc_flg, i_module_type):

    global REQUEST_ENCODER_LIST
    global REQUEST_DECODER_LIST
    global RESPONSE_ENCODER_LIST
    global RESPONSE_DECODER_LIST

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE, "[S] Common_Get_TLVInfo")

    # get request or response key
    if (i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_REQ and \
            (COM_DEF.i_ENCODE_FLG == i_dcdenc_flg):
        # check whether tlv info already is getted or not
        if s_dev_type in REQUEST_ENCODER_LIST:
            Dbg.log(COM_DEF.TRACE,
                    "already open %s_request_encoder.json" % s_dev_type)
            i_result = COM_DEF.i_RET_SUCCESS
        else:
            i_result, REQUEST_ENCODER_LIST[s_dev_type] = \
                Common_OpenFile(s_dev_type + "_request_encoder.json",
                                i_module_type)

        Dbg.log(COM_DEF.TRACE, "[E] Common_Get_TLVInfo")

        return i_result, REQUEST_ENCODER_LIST[s_dev_type]

    elif (i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_REQ and \
            (COM_DEF.i_DECODE_FLG == i_dcdenc_flg):
        # check whether tlv info already is getted or not
        if s_dev_type in REQUEST_DECODER_LIST:
            Dbg.log(COM_DEF.TRACE,
                    "already open %s_request_decoder.json" % s_dev_type)
            i_result = COM_DEF.i_RET_SUCCESS
        else:
            i_result, REQUEST_DECODER_LIST[s_dev_type] = \
                Common_OpenFile(s_dev_type + "_request_decoder.json",
                                i_module_type)

        Dbg.log(COM_DEF.TRACE, "[E] Common_Get_TLVInfo")

        return i_result, REQUEST_DECODER_LIST[s_dev_type]

    elif (((i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_RSP) or
            ((i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_ACK))\
            and (COM_DEF.i_DECODE_FLG == i_dcdenc_flg):
        # check whether tlv info already is getted or not
        if s_dev_type in RESPONSE_DECODER_LIST:
            Dbg.log(COM_DEF.TRACE,
                    "already open %s_response_decoder.json" % s_dev_type)
            i_result = COM_DEF.i_RET_SUCCESS
        else:
            i_result, RESPONSE_DECODER_LIST[s_dev_type] = \
                Common_OpenFile(s_dev_type + "_response_decoder.json",
                                i_module_type)

        Dbg.log(COM_DEF.TRACE, "[E] Common_Get_TLVInfo")

        return i_result, RESPONSE_DECODER_LIST[s_dev_type]

    elif (((i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_RSP) or
            ((i_action & COM_DEF.i_ACTION_UPPERMASK) == COM_DEF.i_ACTION_ACK))\
            and (COM_DEF.i_ENCODE_FLG == i_dcdenc_flg):
        # check whether tlv info already is getted or not
        if s_dev_type in RESPONSE_ENCODER_LIST:
            Dbg.log(COM_DEF.TRACE,
                    "already open %s_response_encoder.json" % s_dev_type)
            i_result = COM_DEF.i_RET_SUCCESS
        else:
            i_result, RESPONSE_ENCODER_LIST[s_dev_type] = \
                Common_OpenFile(s_dev_type + "_response_encoder.json",
                                i_module_type)

        Dbg.log(COM_DEF.TRACE, "[E] Common_Get_TLVInfo")

        return i_result, RESPONSE_ENCODER_LIST[s_dev_type]

    else:
        Dbg.log(COM_DEF.ERROR,
                "unexpected parameter : \n" +
                "DEVICE TYPE   : %s\n" % s_dev_type +
                "ACTION        : 0x%02x\n" % i_action +
                "ENCODE/DECODE : %s" %
                "Encode"
                if COM_DEF.i_ENCODE_FLG == i_dcdenc_flg else "Decode")

        return COM_DEF.i_RET_SYSTEM_ERROR, 0


##
# @brief Read type id information. \n
#        If type id information already be read,
#        return data in the global area.
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
# @retval d_TYPE_PARAM    Read data of "TypeParam.json"
def Common_Get_TypeInfo(i_module_type):

    global d_TYPE_PARAM

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Common_Get_TypeInfo")

    if d_TYPE_PARAM:
        Dbg.log(COM_DEF.TRACE, "already has type info")
    else:
        i_result, d_TYPE_PARAM = \
                Common_OpenFile("TypeParam.json", i_module_type)
        if i_result:
            Dbg.log(COM_DEF.ERROR,
                    "failed to read TypeParam.json")
            return COM_DEF.i_RET_SYSTEM_ERROR, 0
        else:
            pass

    Dbg.log(COM_DEF.TRACE,
            "[E] Common_Get_TypeInfo")

    return COM_DEF.i_RET_SUCCESS, d_TYPE_PARAM


##
# @brief Read type id information from command data. \n
#        if type id information already be read,
#        return data in the global area.
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_ret    value of the result \n
#                      - Success : COM_DEF.i_RET_SUCCESS \n
#                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
# @retval d_TYPE_REVERSE_PARAM    Read data of "TypeReverseParam.json"
def Common_Get_TypeReverseInfo(i_module_type):

    global d_TYPE_REVERSE_PARAM

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Common_Get_TypeReverseInfo")

    if d_TYPE_REVERSE_PARAM:
        Dbg.log(COM_DEF.TRACE, "already has type info")
    else:
        i_result, d_TYPE_REVERSE_PARAM = \
            Common_OpenFile("TypeReverseParam.json", i_module_type)
        if i_result:
            Dbg.log(COM_DEF.ERROR,
                    "failed to read TypeReverseParam.json")
            return COM_DEF.i_RET_SYSTEM_ERROR, 0
        else:
            pass

    Dbg.log(COM_DEF.TRACE,
            "[E] Common_Get_TypeReverseInfo")

    return COM_DEF.i_RET_SUCCESS, d_TYPE_REVERSE_PARAM
