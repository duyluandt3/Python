#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control common procedure
# @author E2N3
# @date 2019.05.28

# -*- coding: utf-8 -*-

from CLS_Define import COM_DEF
from tx_snd import snd_req_cmd


class CTRL_DBG():

    ##
    # @brief Run when instantiating the DBG_FUNC class.
    # @param cls_soc    socket used for sending response command to \n
    #                   MC (class object)
    # @retval None
    def __init__(self, cls_soc, debug):
        self.sock = cls_soc
        self.debug = debug

    ##
    # @brief send to debug loggg
    # @param l_com_hdr     header info
    # @param s_dbg_str    debug string
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Success : COM_DEF.i_RET_SUCCESS \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def dbg_info(self, l_com_hdr, s_dbg_str):
        self.debug.debug(s_dbg_str)
        snd_req_cmd(l_com_hdr,
                    s_dbg_str,
                    self.sock,
                    COM_DEF.i_MODULE_AP)

    ##
    # @brief send to error info
    # @param l_com_hdr     header info
    # @param s_dbg_str    debug string
    # @param i_ret    value of the result
    # @retval d_rply_tlv    response data \n
    #                         ["Result"] value of the result \n
    #                           - Failure : Value other than
    #                                       COM_DEF.i_RET_SUCCESS
    def error_info(self, l_com_hdr, s_dbg_str, i_ret):
        self.debug.error(s_dbg_str)
        d_rply_tlv = {}
        snd_req_cmd(l_com_hdr,
                    s_dbg_str,
                    self.sock,
                    COM_DEF.i_MODULE_AP)
        d_rply_tlv["Result"] = i_ret
        return d_rply_tlv
