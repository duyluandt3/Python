#
# Copyright (C) 2020 Murata Manufacturing Co.,Ltd.
#

##
# @brief This class control a function get log from AirCap PC
# @author E2N3
# @date 2020.06.09

# -*- coding: utf-8 -*-

import glob
import os
import time
import json
import subprocess

from CLS_Define import COM_DEF
from Debug import Debug_GetObj
from collections import OrderedDict


##
# @brief Define AIRCAP related processing.
class AIR_LOG_COLLECT_FUNC():
    ##
    #  @brief Run when finish AIRCAP class.
    #  @param self      instance of AIRCAP_FUNC class
    #  @param cls_soc   socket used for sending response command to MC
    #  @param s_host     MC IP Address
    def __init__(self, dbg):
        # read environment file
        try:
            env_file = "./device/AIRCAP/sub/env.json"
            fr = open(str(env_file), 'r')
            d_aircap_data = json.load(fr)
            fr.close()
        except Exception as err_info:
            print(err_info)

        # @cond
        # Get debug info
        self.Dbg = dbg
        self.ref_data_path = d_aircap_data["RefDataPath"]
        self.d_cp_info = {}
        self.d_cp_info["host"] = d_aircap_data["CpHost"]
        self.d_cp_info["id"] = d_aircap_data["CpID"]
        self.d_cp_info["passwd"] = d_aircap_data["CpPWD"]
        self.d_cp_info["path"] = d_aircap_data["CpRefDtPath"]
        self.d_cp_info["LogPath"] = d_aircap_data["CpLogPath"]

    ##
    #  @brief get log from Aircap PC, send to MC PC
    #  @param self      instance of AIRCAP_FUNC class
    #  @param air_log_name    log name from main thread
    #      **["Result"]**    the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_TLV_ABNORMAL \n
    #      - i_RET_SYSTEM_ERROR \n
    def get_log_file(self, air_log_name):

        self.Dbg.log(COM_DEF.TRACE, "[S] get_log_file")
        i_ret = COM_DEF.i_RET_SUCCESS

        s_dst_file = "%s@%s:%s" % (self.d_cp_info["id"],
                                   self.d_cp_info["host"],
                                   self.d_cp_info["path"])
        s_passwd = self.d_cp_info["passwd"]

        # Check Log and send to MC
        if ' ' == air_log_name:
            i_ret = COM_DEF.i_RET_SYSTEM_ERROR
            return i_ret
        else:
            l_cmd_data = ["sshpass", "-p", s_passwd, "scp", "-o",
                          "StrictHostKeyCHecking=no",
                          "-r", air_log_name, s_dst_file]
            self.Dbg.log(COM_DEF.INFO, ' '.join(l_cmd_data))
            i_ret = self.__runcommand(l_cmd_data)
            if i_ret == COM_DEF.i_RET_SUCCESS:
                pass
            else:
                return i_ret

        self.Dbg.log(COM_DEF.TRACE, "[E] Tranfer AirCap Log")

        return i_ret

    ##
    #  @brief run l_cmd_data command
    #  @param self          instance of AIRCAP_FUNC class
    #  @param l_cmd_data    run command
    #      **["Result"]**   the value of the result (int) \n
    #      - i_RET_SUCCESS \n
    #      - i_RET_TLV_ABNORMAL \n
    #      - i_RET_SYSTEM_ERROR \n
    #      .
    def __runcommand(self, l_cmd_data):
        i_ret = COM_DEF.i_RET_SUCCESS
        try:
            subprocess.call(l_cmd_data)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "subprocess.check_output error")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            i_ret = COM_DEF.i_RET_SYSTEM_ERROR
        return i_ret
