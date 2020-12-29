#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Accept Keywords from Robotframework and control testing.
# @author E2N3
# @date 2019.12.24

# -*- coding: utf-8 -*-#

# ----- import -----
import datetime
import json
import queue
import threading
import sys
from collections import OrderedDict
from CLS_Serial import COM_SERIAL
from CLS_Socket import COM_SOCKET
from CLS_Log import LOG_CTRL
from CLS_SndControl import SND_CTRL
from CLS_RcvControl import RCV_CTRL
from CLS_Define import COM_DEF
from Debug import Debug_GetObj
from Debug import Debug_Init

# @cond
# store the device information.
d_DeviceInfo = {}
# store the current device information used by next test.
d_old_DeviceInfo = {}
# @endcond


class TEST_CTRL:
    """Provides some methods for handling commands
    from robotframework I/F
    `- __init__`
    `- init_env`
    `- start_capture_log`
    `- stop_capture_log`
    `- run_testcmd`
    `- register_testcmd`
    `- flush_testcmd`
    """
    def __init__(self):
        """
        Constructor for initializing object variables.
        """
        self.Qmain = queue.Queue()
        self.Cmain = threading.Condition()
        s_log_filename = \
            COM_DEF.s_TOPDIR + \
            "/LOG/MC" + \
            "_" + \
            datetime.datetime.today().strftime('%Y%m%d%H%M%S') + \
            ".txt"
        i_result = Debug_Init(COM_DEF.i_MODULE_MC, s_log_filename)
        if COM_DEF.i_RET_SUCCESS != i_result:
            print("failed to initialize debug")
        else:
            pass
        self.Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

    def init_env(self, s_DevConfigName):
        """
        Public method for Initializing the test environment.
        - read device info file
        - generate LOG_CTRL based on DeviceId in device information files.
        - generate SND_CTRL based on DeviceId in device information files.
        - generate RCV_CTRL based on port parameter in device information files
        """
        global d_DeviceInfo
        global d_old_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] init_env")

        d_rt_params = {"Result": COM_DEF.i_RET_SUCCESS}

        if d_DeviceInfo:
            d_old_DeviceInfo = d_DeviceInfo
        else:
            pass

        # read device information file
        i_result, d_readDeviceInfo = \
            self.__Read_DeviceConfigFile(s_DevConfigName)
        if i_result:
            d_rt_params["Result"] = i_result
            return d_rt_params
        else:
            pass

        if {} == d_DeviceInfo:
            d_DeviceInfo = d_readDeviceInfo
        elif d_DeviceInfo == d_old_DeviceInfo:
            pass
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "The device info file was changed during testing.")
            sys.exit(1)

        if d_DeviceInfo == d_old_DeviceInfo:
            for s_DeviceId in d_DeviceInfo:
                SndCtrl = d_DeviceInfo[s_DeviceId]["SNDCTRL"]

                if "SOCKET" in d_DeviceInfo[s_DeviceId]:
                    s_host = \
                        d_DeviceInfo[s_DeviceId]["SOCKET"]["HOST"]
                    i_port = \
                        d_DeviceInfo[s_DeviceId]["SOCKET"]["PORT"]
                    d_connect_info = (s_host, i_port)
                else:
                    s_com_port = \
                        d_DeviceInfo[s_DeviceId]["SERIAL"]["COMPORT"]
                    d_connect_info = s_com_port

                # update instance id information
                SndCtrl.Update_NodeId(d_connect_info)
                SndCtrl.Generate_PeerDeviceInfoList(d_connect_info)
            # for end

        else:
            # generate LOG_CTRL object
            i_result = self.__Generate_LogCtrl()
            if i_result:
                d_rt_params["Result"] = i_result
                return d_rt_params
            else:
                pass

            # generate RCV_CTRL & SND_CTRL object
            i_result = self.__Generate_SndCtrl_RcvCtrl()
            if i_result:
                d_rt_params["Result"] = i_result
                return d_rt_params
            else:
                pass

        # Request_test_ready_to
        d_rt_params = self.__Run_request_test_ready()

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] init_env")

        return d_rt_params

    def start_capture_log(self, s_TestName):
        """
        Public method for starting retrieve logs
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] start_capture_log")

        d_rt_params = {}

        i_result = self.LogCtrl.GenerateLogFile(s_TestName)
        if i_result:
            pass
        else:
            self.Dbg.log(COM_DEF.INFO,
                         "related log name : %s" %
                         self.LogCtrl.s_LogFileName)

        d_rt_params["Result"] = i_result

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] start_capture_log")

        return d_rt_params

    def stop_capture_log(self):
        """
        Public method for stopping retrieve logs
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] start_capture_log")

        d_rt_params = {"Result": COM_DEF.i_RET_SUCCESS}

        self.LogCtrl.s_LogFileName = ""

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] start_capture_log")

        return d_rt_params

    def run_testcmd(self, s_DeviceId, s_CmdName, d_TestParams):
        """
        Public method for executing command immediately notified
        by robotframework
        """
        global d_DeviceInfo

        d_rt_params = {}

        d_req_cmd_data = {}
        d_req_cmd_data['command'] = s_CmdName
        d_req_cmd_data['params'] = d_TestParams

        SndCtrl = d_DeviceInfo[s_DeviceId]["SNDCTRL"]
        d_rt_params = SndCtrl.Run_Command(d_req_cmd_data)
        if d_rt_params['Result']:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s: Run_Command failed [%d]"
                         % (s_DeviceId, d_rt_params['Result']))
        else:
            pass

        return d_rt_params

    def register_testcmd(self, s_DeviceId, s_CmdName, d_TestParams):
        """
        Public method for queueing command notified by robotframework
        """
        global d_DeviceInfo

        d_rt_params = {}

        d_req_cmd_data = {}
        d_req_cmd_data['command'] = s_CmdName
        d_req_cmd_data['params'] = d_TestParams

        SndCtrl = d_DeviceInfo[s_DeviceId]["SNDCTRL"]
        d_rt_params = SndCtrl.Register_Command(d_req_cmd_data)
        if d_rt_params['Result']:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s: Register_Command failed [%d]"
                         % (s_DeviceId, d_rt_params['Result']))
        else:
            pass

        return d_rt_params

    def flush_testcmd(self):
        """
        Public method for executing commands stacked on the list
        """
        global d_DeviceInfo

        d_rt_params = {}
        l_rt_reg_data_list = []
        l_response_device_list = []

        # get the number of the registered commands
        for s_DeviceId in d_DeviceInfo.keys():
            SndCtrl = d_DeviceInfo[s_DeviceId]["SNDCTRL"]
            i_counter = len(SndCtrl.l_command_list)
            if i_counter:
                # append the object that command is registed to list
                l_response_device_list.append(s_DeviceId)
            else:
                pass
        # for loop end

        i_wait_response_device_num = len(l_response_device_list)

        self.Dbg.log(COM_DEF.DEBUG,
                     "the num of threads waiting to respond [%d]" %
                     (i_wait_response_device_num))

        # send cond signal
        with self.Cmain:
            self.Cmain.notify_all()

        # wait for result
        i_cnt = 0
        while i_cnt < i_wait_response_device_num:

            try:
                s_DeviceId = self.Qmain.get()

            except Exception as err_info:
                self.Dbg.log(COM_DEF.ERROR,
                             "failed to get data in queue")
                self.Dbg.log(COM_DEF.ERROR, err_info)
                d_rt_params["Result"] = COM_DEF.i_RET_SYSTEM_ERROR
                return d_rt_params

            SndCtrl = d_DeviceInfo[s_DeviceId]["SNDCTRL"]
            l_rt_reg_data_list.extend(SndCtrl.l_rt_params_list)
            SndCtrl.l_command_list = []
            i_cnt += 1
        # while loop end

        self.Dbg.log(COM_DEF.DEBUG,
                     "result list : %s" % str(l_rt_reg_data_list))

        return l_rt_reg_data_list

    def __Read_DeviceConfigFile(self, s_DevConfigName):
        """
        read device information file
        """
        global d_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Read_device_config_file")

        decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

        try:
            with open(s_DevConfigName, "r", encoding='utf-8-sig') as fp:
                d_deviceInfo = decoder.decode(fp.read())
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "can't read %s" % s_DevConfigName)
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return COM_DEF.i_RET_SYSTEM_ERROR

        self.Dbg.log(COM_DEF.DEBUG,
                     "device info file : %s" % str(d_DeviceInfo))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Read_device_config_file")

        return COM_DEF.i_RET_SUCCESS, d_deviceInfo

    def __Generate_LogCtrl(self):
        """
        generate LogCtrl object.
        """
        global d_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Generate_LogCtrl")

        """ generate queue used by MC and LogCtrl """
        Qlog = queue.Queue()

        """ generate log control object """
        self.LogCtrl = LOG_CTRL()

        """
        generate socket used by LogCtrl and SndCtrl
        from device info file
        """
        for s_DeviceId in list(d_DeviceInfo):
            self.LogCtrl.GenerateSocket(s_DeviceId)

        """
        the socket of TestCtrl object separatelly be generated
        because TestCtrl is not included in d_DeviceInfo
        """
        self.LogCtrl.GenerateSocket("MC")
        self.LogCtrl.StartThread(Qlog)

        """
        Wait for thread startup to complete
        """
        i_result = Qlog.get()

        self.Dbg.log(COM_DEF.DEBUG,
                     "get result data " +
                     "whether log thread is started or not [ret:%d]" %
                     (i_result))

        if COM_DEF.i_RET_SUCCESS != i_result:
            self.LogCtrl = ""
        else:
            self.SockLog = self.__Generate_ConnectionWithLogThread("MC")
            if self.SockLog:
                pass
            else:
                return COM_DEF.i_RET_SYSTEM_ERROR

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Generate_LogCtrl")

        return COM_DEF.i_RET_SUCCESS

    def __Generate_SndCtrl_RcvCtrl(self):
        """
        create SndCtrl object from each device id.
        create RcvCtrl object from each port number.
        """
        global d_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Generate_SndCtrl_RcvCtrl")

        """
        initialize local variable
        """
        i_src_node_id = COM_DEF.i_NODE_MC
        i_src_instance_id = 0x01
        s_com_port = ""    # comport name
        s_host = ""        # host ip address
        i_port = ""        # port number

        """
        generate SndCtrl object for each device id.
        """
        for s_DeviceId in list(d_DeviceInfo):

            # generate the SRC ID associated with Device Id
            i_src_id = (i_src_node_id << 8) + i_src_instance_id
            self.Dbg.log(COM_DEF.INFO,
                         "SRC ID : 0x%04x" % (i_src_id))

            s_DeviceType = d_DeviceInfo[s_DeviceId]["DeviceType"]

            # generate socket connection used by SndCtrl and LogCtrl thread
            SockLog = self.__Generate_ConnectionWithLogThread(s_DeviceId)
            if self.SockLog:
                pass
            else:
                return COM_DEF.i_RET_SYSTEM_ERROR

            # generate RCV_CTRL object for a socket or serial
            if "SOCKET" in d_DeviceInfo[s_DeviceId]:
                i_result = \
                    self.__Generate_SocketRcvCtrl(s_DeviceId, s_DeviceType)
                if i_result:
                    return COM_DEF.i_RET_SYSTEM_ERROR
                else:
                    s_host = \
                        d_DeviceInfo[s_DeviceId]["SOCKET"]["HOST"]
                    i_port = \
                        d_DeviceInfo[s_DeviceId]["SOCKET"]["PORT"]
                    d_connect_info = (s_host, i_port)
                    self.Dbg.log(COM_DEF.INFO,
                                 "%s: HOST - %s PORT - %d" %
                                 (s_DeviceId, s_host, i_port))
            else:
                i_result = \
                    self.__Generate_SerialRcvCtrl(s_DeviceId, s_DeviceType)
                if i_result:
                    return COM_DEF.i_RET_SYSTEM_ERROR
                else:
                    s_com_port = \
                        d_DeviceInfo[s_DeviceId]["SERIAL"]["COMPORT"]
                    d_connect_info = s_com_port
                    self.Dbg.log(COM_DEF.INFO,
                                 "%s: COMPORT - %s" %
                                 (s_DeviceId, s_com_port))

            # generate queue used by SndCtrl and RcvCtrl
            QSndRcv = queue.Queue()

            # generate SndCtrl object
            SndCtrl = SND_CTRL(s_DeviceId, i_src_id, s_DeviceType,
                               s_com_port, s_host, i_port)
            d_DeviceInfo[s_DeviceId]["SndCtrl"] = SndCtrl

            # set parameters to receive thread.
            RcvCtrl = d_DeviceInfo[s_DeviceId]["RCVCTRL"]
            RcvCtrl.RCV_SetRelatedThreadInfo(SockLog, i_src_id,
                                             QSndRcv, SndCtrl)

            # update instance id information
            SndCtrl.Update_NodeId(d_connect_info)
            SndCtrl.Generate_PeerDeviceInfoList(d_connect_info)

            # start SndCtrl thread
            SndCtrl.StartThread(self.Qmain,
                                QSndRcv,
                                self.Cmain,
                                RcvCtrl.IfCtrl,
                                self.LogCtrl)

            d_DeviceInfo[s_DeviceId]['SNDCTRL'] = SndCtrl

            i_src_instance_id += 1

        # for loop end

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Generate_SndCtrl_RcvCtrl")

        return COM_DEF.i_RET_SUCCESS

    def __Generate_ConnectionWithLogThread(self, s_DeviceId):
        """
        get port number used by each devices and
        Log Control thread.
        """
        i_bufsize = 4096

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Generate_ConnectionWithLogThread")

        i_log_port = self.LogCtrl.GetPortNumber(s_DeviceId)

        SockLog = COM_SOCKET(i_log_port,
                             i_bufsize,
                             COM_DEF.i_MODULE_MC)
        try:
            SockLog.connect(COM_DEF.s_LOCAL_HOST, i_log_port)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "can't connect Log Ctrl Thread [%d]" % i_log_port)
            self.Dbg.log(COM_DEF.ERROR,
                         err_info)
            return ""

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Generate_ConnectionWithLogThread")

        return SockLog

    def __Generate_SocketRcvCtrl(self, s_DeviceId, s_DeviceType):
        """
        generate RCV_CTRL oject to receive socket data
        """
        global d_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Generate_SocketRcvCtrl")

        if "HOST" in d_DeviceInfo[s_DeviceId]["SOCKET"]:
            s_host = d_DeviceInfo[s_DeviceId]["SOCKET"]["HOST"]
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s :Host is not setted !!" % s_DeviceId)
            return COM_DEF.i_RET_SYSTEM_ERROR

        if "PORT" in d_DeviceInfo[s_DeviceId]["SOCKET"]:
            i_device_port = \
                d_DeviceInfo[s_DeviceId]["SOCKET"]["PORT"]
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s :Port is not setted !!" % s_DeviceId)
            return COM_DEF.i_RET_SYSTEM_ERROR

        if "BUFSIZE" in d_DeviceInfo[s_DeviceId]["SOCKET"]:
            i_bufsize = \
                d_DeviceInfo[s_DeviceId]["SOCKET"]["BUFSIZE"]
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "%s :BufSize is not setted !!" % s_DeviceId)
            return COM_DEF.i_RET_SYSTEM_ERROR

        # generate socket used by SndCtrl and RcvCtrl
        SocCtrl = COM_SOCKET(i_device_port, i_bufsize, COM_DEF.i_MODULE_MC)
        try:
            SocCtrl.connect(s_host, i_device_port)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "failed to connect : %s/%d" %
                         (s_host, i_device_port))
            self.Dbg.log(COM_DEF.ERROR, err_info)
            return COM_DEF.i_RET_SYSTEM_ERROR

        RcvCtrl = RCV_CTRL("RCV_" + str(i_device_port), SocCtrl, s_DeviceType)
        RcvCtrl.RCV_StartThread()

        d_DeviceInfo[s_DeviceId]["RCVCTRL"] = RcvCtrl
        d_DeviceInfo[s_DeviceId]["IFCTRL"] = SocCtrl

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Generate_SocketRcvCtrl")

        return COM_DEF.i_RET_SUCCESS

    def __Generate_SerialRcvCtrl(self, s_DeviceId, s_DeviceType):
        """
        generate RCV_CTRL oject to receive serial data
        """
        global d_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Generate_SerialRcvCtrl")

        i_result = self.__Check_SameComport(s_DeviceId)
        if COM_DEF.i_RET_SUCCESS < i_result:
            # RCV_CTRL object already be generated
            return COM_DEF.i_RET_SUCCESS
        else:

            if "BAUDRATE" in d_DeviceInfo[s_DeviceId]["SERIAL"]:
                i_baudrate = \
                    d_DeviceInfo[s_DeviceId]["SERIAL"]["BAUDRATE"]
            else:
                # can't get parameter from DeviceInfo.json
                self.Dbg.log(COM_DEF.ERROR,
                             "%s: baudrate is not setted !!" % s_DeviceId)
                return COM_DEF.i_RET_SYSTEM_ERROR

            if "USER" in d_DeviceInfo[s_DeviceId]["SERIAL"]:
                s_user = d_DeviceInfo[s_DeviceId]["SERIAL"]["USER"]
            else:
                # can't get parameter from device info file
                # this parameter is option.
                s_user = ""

            if "PASSWORD" in d_DeviceInfo[s_DeviceId]["SERIAL"]:
                s_password = \
                    d_DeviceInfo[s_DeviceId]["SERIAL"]["PASSWORD"]
            else:
                # can't get parameter from DeviceInfo.json
                # this parameter is option.
                s_password = ""

            s_comport = d_DeviceInfo[s_DeviceId]["SERIAL"]["COMPORT"]
            SerCtrl = COM_SERIAL(s_comport, i_baudrate, s_user, s_password,
                                 True, COM_DEF.i_MODULE_MC)

            # get the state of the serial port
            b_connect = SerCtrl.isConnected()
            if not b_connect:
                self.Dbg.log(COM_DEF.ERROR,
                             "%s: failed to open serial port." %
                             (s_DeviceId))
                return COM_DEF.i_RET_SYSTEM_ERROR
            else:
                pass

            RcvCtrl = RCV_CTRL("RCV_" + s_comport, SerCtrl, s_DeviceType)
            RcvCtrl.RCV_StartThread()

            d_DeviceInfo[s_DeviceId]["RCVCTRL"] = RcvCtrl
            d_DeviceInfo[s_DeviceId]["IFCTRL"] = SerCtrl

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Generate_SerialRcvCtrl")

        return COM_DEF.i_RET_SUCCESS

    def __Check_SameComport(self, s_DeviceId):
        """
        this serial class obj is possible to use multiple interface thread.
        check whether same port number is or not.
        True already be same port number.
        """
        global d_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Check_SameComport")

        if "COMPORT" in d_DeviceInfo[s_DeviceId]["SERIAL"]:
            s_comport = d_DeviceInfo[s_DeviceId]["SERIAL"]["COMPORT"]
        else:
            self.Dbg.log(COM_DEF.ERROR, "comport is not setted !!")
            return COM_DEF.i_RET_SYSTEM_ERROR

        for s_DeviceId_In_List in list(d_DeviceInfo):
            if s_DeviceId_In_List != s_DeviceId and \
                    "SERIAL" in d_DeviceInfo[s_DeviceId_In_List]:

                s_comport_in_list = \
                    d_DeviceInfo[s_DeviceId_In_List]["SERIAL"]["COMPORT"]
                if s_comport == s_comport_in_list and \
                        "RCVCTRL" in d_DeviceInfo[s_DeviceId_In_List]:

                    self.Dbg.log(COM_DEF.DEBUG, "find same port !!")
                    d_DeviceInfo[s_DeviceId]["RCVCTRL"] = \
                        d_DeviceInfo[s_DeviceId_In_List]["RCVCTRL"]
                    self.Dbg.log(COM_DEF.TRACE,
                                 "[E] __Check_SameComport")
                    return COM_DEF.i_RET_SUCCESS + 1
                else:
                    pass
            else:
                pass
        else:
            self.Dbg.log(COM_DEF.INFO,
                         "%s: not found same comport - %s" %
                         (s_DeviceId, s_comport))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Check_SameComport")

        return COM_DEF.i_RET_SUCCESS

    def __Run_request_test_ready(self):
        """
        generate request_test_ready command
        """
        global d_DeviceInfo

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Run_request_test_ready")

        s_CmdName = 'Request_test_ready'

        # generate request_test_ready
        l_coninfo = []
        for s_DeviceId in list(d_DeviceInfo):
            if "SOCKET" in d_DeviceInfo[s_DeviceId]:
                s_host = d_DeviceInfo[s_DeviceId]["SOCKET"]["HOST"]
                i_port = d_DeviceInfo[s_DeviceId]["SOCKET"]["PORT"]
                tpl_if_key = (s_host, i_port)
            else:
                s_com_port = \
                    d_DeviceInfo[s_DeviceId]["SERIAL"]["COMPORT"]
                tpl_if_key = s_com_port

            if tpl_if_key in l_coninfo:
                self.Dbg.log(COM_DEF.TRACE,
                             "skip duplicate info")
            else:
                l_coninfo.append(tpl_if_key)

                d_req_cmd_data = {}
                d_req_cmd_data['command'] = s_CmdName
                d_req_cmd_data['params'] = {}

                SndCtrl = d_DeviceInfo[s_DeviceId]["SNDCTRL"]
                d_rt_params = SndCtrl.Run_Command(d_req_cmd_data)
                if d_rt_params['Result']:
                    self.Dbg.log(COM_DEF.ERROR,
                                 "%s: Request_test_ready faid [%d]" %
                                 (s_DeviceId, d_rt_params['Result']))
                    break
                else:
                    pass
        # for loop end

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Run_request_test_ready")

        return d_rt_params
