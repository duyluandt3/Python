#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief This module enable debug function.
# @author E2N3
# @date 2019.12.24

# -*- coding: utf-8 -*-

# ----- import -----
import json
import logging
import logging.handlers
from CLS_Define import COM_DEF
d_Debug_INFO = {}


##
# @brief read configuration file debug information is written
# @param i_module_type    module number
# @retval Success         COM_DEF.i_RET_SUCCESS
# @retval s_json_name     name of configuration file
# @retval s_log_name      log name
def __debug_GetFileName(i_module_type):

    s_json_name = ""
    s_log_name = ""

    if COM_DEF.i_MODULE_MC == i_module_type:
        s_json_name = \
            COM_DEF.s_TOPDIR + "/Common/debug/json/DebugInfo_MC.json"
        s_log_name = 'MC'
    elif COM_DEF.i_MODULE_DUT == i_module_type:
        s_json_name = \
            COM_DEF.s_TOPDIR + "/Common/debug/json/DebugInfo_DUT.json"
        s_log_name = 'DUT'
    elif COM_DEF.i_MODULE_AP == i_module_type:
        s_json_name = \
            COM_DEF.s_TOPDIR + "/Common/debug/json/DebugInfo_AP.json"
        s_log_name = 'AP'
    elif COM_DEF.i_MODULE_AIRCAP == i_module_type:
        s_json_name = \
            COM_DEF.s_TOPDIR + "/Common/debug/json/DebugInfo_AIRCAP.json"
        s_log_name = 'AIRCAP'
    elif COM_DEF.i_MODULE_NETWORKTOOL == i_module_type:
        s_json_name = \
            COM_DEF.s_TOPDIR + "/Common/debug/json/DebugInfo_NETWORKTOOL.json"
        s_log_name = 'NETWORKTOOL'
    elif COM_DEF.i_MODULE_LOGCTRL == i_module_type:
        s_json_name = \
            COM_DEF.s_TOPDIR + "/Common/debug/json/DebugInfo_LOGCTRL.json"
        s_log_name = 'LOG'
    else:
        pass

    return COM_DEF.i_RET_SUCCESS, s_json_name, s_log_name


##
# @brief debug initialization
# @param i_module_type     module number
# @param s_log_file_name   debug file name
# @retval i_ret            valur od the result \n
#                           - Success : COM_DEF.i_RET_SUCCESS \n
#                           - Failure : COM_DEF.i_RET_SYSTEM_ERROR
def Debug_Init(i_module_type, s_log_file_name):

    global d_Debug_INFO

    # debug dictionary
    #  debug - module debug class
    i_result, s_json_name, s_log_name = \
        __debug_GetFileName(i_module_type)
    if i_result:
        print("can't get file name")
        return COM_DEF.i_RET_SYSTEM_ERROR
    else:
        pass

    if s_log_name in d_Debug_INFO:
        d_Debug_INFO[s_log_name].handlers.clear()
    else:
        pass

    # tlv file that mandatory paramter is written
    with open(s_json_name, "r",
              encoding='utf-8-sig') as f_data:
        try:
            d_debugInfo = json.load(f_data)
        except Exception as err_info:
            print(err_info)
            print("can't open debug file")
            return COM_DEF.i_RET_SYSTEM_ERROR

    i_DebugLevel = d_debugInfo["DebugLevel"]
    i_ShowLog = d_debugInfo["ShowLog"]

    # create debug
    debug = logging.getLogger(s_log_name)

    # set log level
    #   0 - output more than info level
    #   1 - output more than info debug
    #   2 - output all
    if 1 == i_DebugLevel:
        i_level = logging.DEBUG
        debug.setLevel(logging.DEBUG)
    elif 2 == i_DebugLevel:
        i_level = logging.DEBUG - 1
        logging.addLevelName(i_level, 'TRACE')
    else:
        i_level = logging.INFO

    debug.setLevel(i_level)

    formatter = \
        logging.Formatter("[%(levelname)-5s] %(asctime)s " +
                          "[%(threadName)-15s]" +
                          "[%(filename)-20s:L.%(lineno)-4s] " +
                          "%(message)s")
    if i_ShowLog != 0:
        sh = logging.StreamHandler()
        sh.setLevel(i_level)
        if COM_DEF.i_MODULE_LOGCTRL != i_module_type:
            sh.setFormatter(formatter)
        else:
            pass
        debug.addHandler(sh)
    else:
        pass

    # add Rotating File Hander to logging handlers
    file_handler = \
        logging.handlers.RotatingFileHandler(s_log_file_name,
                                             mode='a',
                                             maxBytes=COM_DEF.i_LOGSIZE,
                                             backupCount=COM_DEF.i_BACKUPCOUNT)
    file_handler.setLevel(i_level)
    if COM_DEF.i_MODULE_LOGCTRL != i_module_type:
        file_handler.setFormatter(formatter)
    else:
        pass

    debug.addHandler(file_handler)

    d_Debug_INFO[s_log_name] = debug

    return COM_DEF.i_RET_SUCCESS


def Debug_GetObj(i_module_type):
    global d_Debug_INFO

    i_result, s_json_name, s_log_name = \
        __debug_GetFileName(i_module_type)
    if i_result:
        print("can't get file name")
        return COM_DEF.i_RET_SYSTEM_ERROR
    else:
        pass

    debug = d_Debug_INFO[s_log_name]

    return debug
