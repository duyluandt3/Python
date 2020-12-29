#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief Decode_ComHdr sub function.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

from Cksum import Calc_Cksum
from CLS_Define import COM_DEF
from Debug import Debug_GetObj


##
# @brief Decode common header and check each data.
# @param s_command   module number
# @param i_module_type    module number \n
#                           - COM_DEF.i_MODULE_MC(0) : MC \n
#                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
#                           - COM_DEF.i_MODULE_AP(2) : AP \n
#                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
#                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
# @retval i_result    Values of check result of common header
# @retval i_dst_id    instance id of MC thread
# @retval i_src_id    instance id of Device
# @retval i_cmd_id    command id
# @retval i_action    notified action parameter
# @retval i_seq_num    notified sequence number
# @retval i_ack_num    notified acknowledge number
# @retval i_tlv_len    tlv data length
# @retval s_tlv_data    tlv data decoded
def Decode_ComHdr(s_command, i_module_type):

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE,
            "[S] Decode_ComHdr")

    # set data to list by separating byte unit
    l_cmd_data_list = [(cnt+offset) for (cnt, offset)
                       in zip(s_command[::2], s_command[1::2])]

    if COM_DEF.i_COMHDR_LENGTH <= len(l_cmd_data_list):
        # received data is longer than header length
        pass
    else:
        Dbg.log(COM_DEF.TRACE,
                "received data is shorter than header length")
        return COM_DEF.i_RET_COMHDR_LENGTH, 0, 0, 0, 0, 0, 0, 0, "None"

    # start bit
    if 'ff' == l_cmd_data_list[0] and 'fe' == l_cmd_data_list[1]:
        pass
    else:
        Dbg.log(COM_DEF.TRACE, "start bit error !!")

        # find 'ff' or fe' from the string, add it to key list.
        l_ff_idx_list = \
            [cnt for cnt, x in enumerate(l_cmd_data_list) if x == 'ff']
        l_fe_idx_list = \
            [cnt for cnt, x in enumerate(l_cmd_data_list) if x == 'fe']

        if len(l_ff_idx_list) and len(l_fe_idx_list):
            b_found = False
            for ff_key_idx in l_ff_idx_list:
                for fe_key_idx in l_fe_idx_list:
                    if ff_key_idx + 1 == fe_key_idx:
                        Dbg.log(COM_DEF.TRACE,
                                "found start bit in command")
                        # find 'fffe' from the string and
                        # remove the characters up to 'fffe'.
                        del l_cmd_data_list[:ff_key_idx]
                        b_found = True
                        break
                    else:
                        pass
                # for loop
                if b_found:
                    break
                else:
                    pass
            # for loop

            if b_found:
                if COM_DEF.i_COMHDR_LENGTH <= len(l_cmd_data_list):
                    # received data is longer than header length
                    pass
                else:
                    Dbg.log(COM_DEF.TRACE,
                            "received data is shorter than header length")
                    return \
                        COM_DEF.i_RET_COMHDR_LENGTH, \
                        0, 0, 0, 0, 0, 0, 0, "None"
            else:
                Dbg.log(COM_DEF.ERROR,
                        "failed to find start bit")
                return \
                    COM_DEF.i_RET_COMHDR_STARTBIT, 0, 0, 0, 0, 0, 0, 0, "None"
        else:
            Dbg.log(COM_DEF.ERROR,
                    "failed to find start bit")
            return \
                COM_DEF.i_RET_COMHDR_STARTBIT, 0, 0, 0, 0, 0, 0, 0, "None"

    # data length
    i_tlv_len = (int(l_cmd_data_list[12], 16) << 8) + \
        (int(l_cmd_data_list[13], 16))
    if (COM_DEF.i_COMHDR_LENGTH + i_tlv_len) > len(l_cmd_data_list):
        Dbg.log(COM_DEF.TRACE,
                "received data is shorter than tlv length")
        return COM_DEF.i_RET_WAIT_NEXT_CMD, 0, 0, 0, 0, 0, 0, 0, "None"
    else:
        pass

    # cksum
    i_cksum = \
        (int(l_cmd_data_list[14], 16) << 8) + (int(l_cmd_data_list[15], 16))
    l_cmd_data_list[14] = '00'
    l_cmd_data_list[15] = '00'

    # check whether tlv data is or not
    s_comhdr = ''.join((l_cmd_data_list[0:COM_DEF.i_COMHDR_LENGTH]))
    if COM_DEF.i_COMHDR_LENGTH < len(l_cmd_data_list):
        # remove cksum from received command
        i_last_data_pos = COM_DEF.i_COMHDR_LENGTH + i_tlv_len
        s_tlv_data = \
            ''.join(l_cmd_data_list[COM_DEF.i_COMHDR_LENGTH:i_last_data_pos])
        s_decode_data = s_comhdr + s_tlv_data
    else:
        s_tlv_data = ""
        s_decode_data = s_comhdr

    Dbg.log(COM_DEF.DEBUG,
            "DECODE DATA : %s" % s_decode_data)

    i_calc_cksum = Calc_Cksum(s_decode_data, i_module_type)
    if i_cksum != i_calc_cksum:
        Dbg.log(COM_DEF.ERROR,
                "cksum error : [Notified] %d (0x%04x) " %
                (i_cksum, i_cksum) +
                "[Expected] %d (0x%04x)" % (i_calc_cksum, i_calc_cksum))
        return COM_DEF.i_RET_COMHDR_CKSUM, 0, 0, 0, 0, 0, 0, 0, "None"
    else:
        pass

    # dst id
    i_dst_id = (int(l_cmd_data_list[2], 16) << 8) + \
        (int(l_cmd_data_list[3], 16))
    Dbg.log(COM_DEF.DEBUG,
            "DST ID  : 0x%04x" % i_dst_id)

    # src id
    i_src_id = (int(l_cmd_data_list[4], 16) << 8) + \
        (int(l_cmd_data_list[5], 16))
    Dbg.log(COM_DEF.DEBUG,
            "SRC ID  : 0x%04x" % i_src_id)

    # cmd id
    i_cmd_id = (int(l_cmd_data_list[6], 16) << 8) + \
        (int(l_cmd_data_list[7], 16))
    Dbg.log(COM_DEF.DEBUG,
            "COMMAND : 0x%04x" % i_cmd_id)

    # action
    i_action = (int(l_cmd_data_list[8], 16))
    Dbg.log(COM_DEF.DEBUG,
            "ACTION  : 0x%02x" % i_action)

    # sequence number
    i_seq_num = (int(l_cmd_data_list[9], 16))
    Dbg.log(COM_DEF.DEBUG,
            "SEQ NO  : 0x%02x" % i_seq_num)

    # acknowledge number
    i_ack_num = (int(l_cmd_data_list[10], 16))
    Dbg.log(COM_DEF.DEBUG,
            "ACK NO  : 0x%02x" % i_ack_num)

    # tlv len
    Dbg.log(COM_DEF.DEBUG,
            "TLV LEN : 0x%04x" % i_tlv_len)

    # tlv data
    Dbg.log(COM_DEF.DEBUG,
            "TLV     : %s" % s_tlv_data)

    Dbg.log(COM_DEF.TRACE,
            "[E] Decode_ComHdr")

    return COM_DEF.i_RET_SUCCESS, \
        i_dst_id, i_src_id, i_cmd_id, i_action, i_seq_num, i_ack_num, \
        i_tlv_len, s_tlv_data
