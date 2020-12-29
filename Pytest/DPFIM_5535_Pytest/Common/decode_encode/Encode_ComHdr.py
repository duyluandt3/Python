#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This function encode from user parameter to common header.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

from Cksum import Calc_Cksum
from CLS_Define import COM_DEF
from Debug import Debug_GetObj


##
# @brief Encoding of common header.
# @param i_dst_id    destination id
# @param i_src_id    source id
# @param i_cmd_id    command id
# @param i_action    action id
# @param i_seq_num    sequence number
# @param i_ack_num    acknowledge number
# @param i_tlv_len    the all tlv length of command
# @param s_tlv_data    tlv data
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval s_comhdr    common header
def Encode_ComHdr(i_dst_id, i_src_id, i_cmd_id, i_action, i_seq_num,
                  i_ack_num, i_tlv_len, s_tlv_data, i_module_type):

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Encode_ComHdr")

    Dbg.log(COM_DEF.DEBUG,
            "DST ID  : 0x%04x" % i_dst_id)
    Dbg.log(COM_DEF.DEBUG,
            "SRC ID  : 0x%04x" % i_src_id)
    Dbg.log(COM_DEF.DEBUG,
            "COMMAND : 0x%04x" % i_cmd_id)
    Dbg.log(COM_DEF.DEBUG,
            "ACTION  : 0x%02x" % i_action)
    Dbg.log(COM_DEF.DEBUG,
            "SEQ NO  : 0x%02x" % i_seq_num)
    Dbg.log(COM_DEF.DEBUG,
            "ACK NO  : 0x%02x" % i_ack_num)
    Dbg.log(COM_DEF.DEBUG,
            "TLV LEN : 0x%04x" % i_tlv_len)
    Dbg.log(COM_DEF.DEBUG,
            "TLV     : %s" % s_tlv_data)

    # Create common header
    # - start bit
    i_start_bit_len = 2
    s_comhdr = hex(65534)[2:].zfill(i_start_bit_len*2)

    # - destination id
    i_dst_id_len = 2
    s_comhdr += hex(i_dst_id)[2:].zfill(i_dst_id_len*2)

    # - source id
    i_src_id_len = 2
    s_comhdr += hex(i_src_id)[2:].zfill(i_src_id_len*2)

    # - command
    i_cmd_id_len = 2
    s_comhdr += hex(i_cmd_id)[2:].zfill(i_cmd_id_len*2)

    # - action
    i_action_len = 1
    s_comhdr += hex(i_action)[2:].zfill(i_action_len*2)

    # - sequence number
    i_seq_num_len = 1
    s_comhdr += hex(i_seq_num)[2:].zfill(i_seq_num_len*2)

    # - acknowledge number
    i_ack_num_len = 1
    s_comhdr += hex(i_ack_num)[2:].zfill(i_ack_num_len*2)

    # - reserved
    i_reserved_len = 1
    i_reserved = 0x00
    s_comhdr += hex(i_reserved)[2:].zfill(i_reserved_len*2)

    # - data length
    i_data_len = 2
    s_comhdr += hex(i_tlv_len)[2:].zfill(i_data_len*2)

    # - chksum
    i_cksum_len = 2
    i_cksum = Calc_Cksum(s_comhdr + s_tlv_data, i_module_type)
    s_comhdr += hex(i_cksum)[2:].zfill(i_cksum_len*2)

    Dbg.log(COM_DEF.DEBUG,
            "CHK SUM : 0x%04x" % i_cksum)
    Dbg.log(COM_DEF.DEBUG,
            "HEADER  : %s" % s_comhdr)

    Dbg.log(COM_DEF.TRACE, "[E] Encode_ComHdr")

    return s_comhdr
