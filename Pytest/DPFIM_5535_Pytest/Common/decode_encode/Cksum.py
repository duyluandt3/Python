#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This function used to check whether command is broken or not.
# @author E2N3
# data 2018.11.09

# -*- coding: utf-8 -*-
from Debug import Debug_GetObj
from CLS_Define import COM_DEF


##
# @brief Function for calc checksum
# @param s_data          tlv data
# @param i_module_type   module number
# @retval i_sum_data     cksum result
def Calc_Cksum(s_data, i_module_type):

    i_sum_data = 0

    # Get debug info
    Dbg = Debug_GetObj(i_module_type)

    Dbg.log(COM_DEF.TRACE, "[S] Calc_Cksum")

    # set data to list by separating byte unit
    l_all_data = [(cnt+offset) for (cnt, offset) in zip(s_data[::2],
                                                        s_data[1::2])]
    i_data_len = len(l_all_data)

    # calcurate cksum value
    for i_num in range(0, i_data_len, 2):
        if i_num == i_data_len - 1:
            i_add_data = (int(l_all_data[i_num], 16)) << 8
        else:
            i_add_data = (int(l_all_data[i_num], 16) << 8) + \
                            (int(l_all_data[i_num + 1], 16))
        i_sum_data += i_add_data
        if(i_sum_data >= 65536):
            i_sum_data = i_sum_data - 65535
        else:
            pass

    Dbg.log(COM_DEF.TRACE, "[E] Calc_Cksum")

    return i_sum_data ^ 0xFFFF
