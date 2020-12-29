#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Log Management module. \n
#        Write log data received from device to log file.
# @author E2N3
# @date 2019.12.24

# -*- coding: utf-8 -*-

import copy
import datetime
import threading
import select
import json
import sys
import re
from CLS_Socket import COM_SOCKET
from Debug import Debug_Init
from Debug import Debug_GetObj
from CLS_Define import COM_DEF


##
# @brief Define log related processing.
class LOG_CTRL():

    ##
    # @brief Run when instantiating the LOG_CTRL class.
    # @param None
    # @retval None
    def __init__(self):
        """
        Constructor for initializing object variables
        """
        # @cond
        # Get logger info
        self.Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

        # set stop thread event
        self.EwaitStop = threading.Event()
        self.Sockets = []
        self.d_logSocketInfo = {}
        self.i_local_port = 50000
        self.d_base_time = {}
        self.cls_dut_base_time = 0
        self.l_identifier_list = []
        self.s_LogFileName = ""
        # @endcond

    ##
    # @brief Register socket information in list of log class.
    # @param s_DeviceId    peer device name in procesing
    # @retval None
    def GenerateSocket(self, s_DeviceId):
        """
        generate socket used by each threads.
        """
        self.Dbg.log(COM_DEF.TRACE, "[S] GenerateSocket")

        i_bufsize = 4096

        # @cond
        self.d_logSocketInfo[s_DeviceId] = {}

        SocCtrl = COM_SOCKET(self.i_local_port,
                             i_bufsize,
                             COM_DEF.i_MODULE_MC)
        self.Sockets.append(SocCtrl.sock)

        self.d_logSocketInfo[s_DeviceId]["Socket"] = SocCtrl
        self.d_logSocketInfo[s_DeviceId]["Port"] = self.i_local_port
        self.i_local_port += 1
        self.l_identifier_list.append(s_DeviceId)
        # @endcond

        self.Dbg.log(COM_DEF.DEBUG,
                     '%s: local port : %d' %
                     (s_DeviceId,
                      self.d_logSocketInfo[s_DeviceId]["Port"]))

        self.Dbg.log(COM_DEF.TRACE, "[E] GenerateSocket")

    ##
    # @brief Return port number for each device to communicate with
    #        log control thread.
    # @param s_DeviceId    peer device name in procesing
    # @retval d_logSocketInfo[s_DeviceId]["Port"]    port number (int)
    def GetPortNumber(self, s_DeviceId):
        """
        return socket port number generated bu GenerateSocket method
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] GetPortNumber")

        self.Dbg.log(COM_DEF.DEBUG,
                     "port number [%s] : %d" %
                     (s_DeviceId,
                      self.d_logSocketInfo[s_DeviceId]["Port"]))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] GetPortNumber")

        return self.d_logSocketInfo[s_DeviceId]["Port"]

    ##
    # @brief Set base time to list when SetCurrentTime command is sent.
    # @param i_src_id    source id
    # @param s_DeviceType    device type
    # @retval s_date    year、month、day
    # @retval s_time    hours, minutes, and seconds
    def SetBaseTime(self, i_src_id, s_DeviceType):
        """
        Set the base time for time synchronization.
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] SetBaseTime")

        i_dummy = 0

        # Set base time for each source id.
        try:
            Now = datetime.datetime.today()
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "Failed to get date time")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            sys.exit(1)

        self.d_base_time[hex(i_src_id)] = Now
        if "WIRELESS_DEVICE" == s_DeviceType:
            self.cls_dut_base_time = Now
        else:
            pass

        s_dbg_str = "SRC ID {} base time : {:.6f}"
        self.Dbg.log(COM_DEF.DEBUG,
                     s_dbg_str.format(i_src_id,
                                      self.d_base_time[hex(i_src_id)]))

        s_date = (hex(Now.year)[2:].zfill(4) +
                  hex(Now.month)[2:].zfill(2) +
                  hex(Now.day)[2:].zfill(2))

        s_time = (hex(Now.hour)[2:].zfill(2) +
                  hex(Now.minute)[2:].zfill(2) +
                  hex(Now.second)[2:].zfill(2) +
                  hex(i_dummy)[2:].zfill(2))

        self.Dbg.log(COM_DEF.TRACE,
                     "date : %s / time : %s" %
                     (s_date, s_time))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] SetBaseTime")

        return s_date, s_time

    ##
    # @brief Generate a file to write the log for each test.
    # @param s_TestName    test number
    # @retval i_result  Success  0 \
    #                   Failed   others
    def GenerateLogFile(self, s_TestName):
        """
        generate log file
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] GenerateLogFile")

        s_TestName = s_TestName.replace(' ', '_')

        Now = datetime.datetime.today()
        s_LogFileName = str(Now)
        s_LogFileName = re.sub(r"[-:. ]", "", s_LogFileName)
        s_LogFileName = s_TestName + "_" + s_LogFileName + ".txt"
        # @cond
        self.s_LogFileName = copy.deepcopy(s_LogFileName)
        s_write_file_name = "%s/LOG/%s" % (COM_DEF.s_TOPDIR, s_LogFileName)
        # @endcond
        s_write_log = \
            "[" + str(Now) + "]" + " log capture start... %s" % \
            (s_write_file_name)

        i_result = Debug_Init(COM_DEF.i_MODULE_LOGCTRL, s_write_file_name)
        if COM_DEF.i_RET_SUCCESS != i_result:
            print("failed to initialize debug...")
        else:
            self.NotifiedLog = Debug_GetObj(COM_DEF.i_MODULE_LOGCTRL)
            self.NotifiedLog.log(COM_DEF.INFO, s_write_log)

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] GenerateLogFile")

        return i_result

    ##
    # @brief Start the log control resident thread.
    # @param Qlog    log control queue (Queue class object)
    # @retval None
    def StartThread(self, Qlog):
        """
        start log ctrl thread
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] StartThread")

        # @cond
        self.LogCtrlThread = \
            threading.Thread(target=self.__LOG_CtrlThread,
                             args=(Qlog,),
                             name="LOG_THREAD")
        # @endcond

        self.LogCtrlThread.setDaemon(True)
        self.LogCtrlThread.start()

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] StartThread")

    ##
    # @brief Stop log control thread.
    # @param None
    # @retval None
    def StopThread(self):
        """
        Stop Log Thread
        """
        self.Dbg.log(COM_DEF.TRACE, "[S] StopThread")

        self.EwaitStop.set()
        for soc_tmp in self.Sockets:
            soc_tmp.close()

        self.Dbg.log(COM_DEF.TRACE, "[E] StopThread")

    ##
    # @brief Receive a log write request from each device and
    #        write it to a file.
    # @param Qlog    log control queue (Queue class object)
    # @retval None
    def __LOG_CtrlThread(self, Qlog):
        """
        Thread to write the log to be notified.
        """
        i_bufsize = 4096

        d_rcv_data = {}
        i_backlog = len(self.d_logSocketInfo.keys())

        self.Dbg.log(COM_DEF.TRACE, "[S] __LOG_Thread")

        for s_DeviceId in self.l_identifier_list:
            SocCtrl = self.d_logSocketInfo[s_DeviceId]["Socket"]
            SocCtrl.bind(COM_DEF.s_LOCAL_HOST,
                         self.d_logSocketInfo[s_DeviceId]["Port"])
            SocCtrl.listen(i_backlog)
        # for loop end

        readfds = list(self.Sockets)

        """
        Robotframework process is waiting to response from LOG Thread.
        Robotframework process restart procedure by receiving "OK" context.
        """
        Qlog.put(COM_DEF.i_RET_SUCCESS)

        while not self.EwaitStop.is_set():

            # recv data
            l_soc_rReady, l_soc_wReady, l_soc_xReady = \
                select.select(readfds, [], [])
            for soc_tmp in l_soc_rReady:
                if soc_tmp in self.Sockets:
                    for s_DeviceId in self.l_identifier_list:
                        SocCtrl = self.d_logSocketInfo[s_DeviceId]["Socket"]
                        if SocCtrl.sock == soc_tmp:
                            SocCtrl.accept()
                            readfds.append(SocCtrl.o_conn)
                        else:
                            pass
                    # for loop end

                else:
                    for s_DeviceId in self.l_identifier_list:
                        SocCtrl = self.d_logSocketInfo[s_DeviceId]["Socket"]
                        if SocCtrl.o_conn == soc_tmp:
                            recv_str = SocCtrl.o_conn.recv(i_bufsize)

                            # Receive FIN
                            if not recv_str:
                                self.Dbg.log(COM_DEF.ERROR, "FIN Receive")
                                return
                            else:
                                pass

                            try:
                                d_rcv_data = \
                                    json.loads(recv_str.decode('utf-8'))
                            except Exception as err_info:
                                self.Dbg.log(COM_DEF.ERROR, err_info)
                                self.Dbg.log(COM_DEF.ERROR, recv_str)
                                d_rcv_data = ""
                            break
                        else:
                            pass
                    # for loop end

                    # -------- write log file --------

                    if "" == d_rcv_data or "" == self.s_LogFileName:
                        pass
                    else:
                        # Get Destination ID
                        i_dst_id = d_rcv_data["DstId"]
                        s_dst_id = "[DST:" + hex(i_dst_id) + "]"

                        # Get Source ID
                        i_src_id = d_rcv_data["SrcId"]
                        s_src_id = "[SRC:" + hex(i_src_id) + "]"

                        # Get Offset Time
                        if "" != d_rcv_data['Time']:
                            if hex(i_src_id) in self.d_base_time:
                                base_time = \
                                    self.d_base_time[hex(i_src_id)]
                            elif ((i_dst_id & 0xff00) == 0x0a00):
                                base_time = \
                                    self.cls_dut_base_time
                            else:
                                pass

                            s_offset_time = d_rcv_data['Time']
                            s_log_time = "     "
                            s_log_time += \
                                self.__culcurate_datetime(
                                    base_time,
                                    s_offset_time)

                            self.Dbg.log(COM_DEF.TRACE,
                                         "[SRC ID:0x%04x] " % (i_src_id) +
                                         "log time : %s offset time : %s" %
                                         (s_log_time, s_offset_time))

                        else:
                            # If SetCurrentTime is not used, get current time.
                            # Set "[CP]" tag at top of time data
                            s_log_time = "[CP] "
                            Now = datetime.datetime.today()
                            s_log_time += str(Now)

                        # Get LOG data
                        s_dbglog = " " + d_rcv_data["Log"].rstrip("\r")
                        s_dbglog = " " + d_rcv_data["Log"].rstrip("\n")
                        s_write_log = \
                            s_src_id + s_dst_id + " " + s_log_time + \
                            s_dbglog

                        self.NotifiedLog.log(COM_DEF.INFO, s_write_log)

                    # The thread that requested to write the log
                    # is waiting for an "OK" response.
                    s_return_val = 'OK'
                    SocCtrl.o_conn.send(s_return_val.encode('utf-8'))
        # while loop end

        self.Dbg.log(COM_DEF.INFO, "Delete Log thread")

        self.Dbg.log(COM_DEF.TRACE, "[E] __LOG_Thread")

    ##
    # @brief calcurate date time by using offsettime notified from device.
    # @param base_time    datetime data (class object) \n
    #                       ex) YYYY-MM-DD HH:MM:SS.ffff
    # @param s_offset    offset time calculated from base time
    # @retval date_time    current time calculated from offset time &
    #                      base time (str)
    def __culcurate_datetime(self, base_time, s_offset):
        """
        calcurate date time by using offsettime notified from device.
        """
        # change from usec offset to msec offset
        f_offset = int(s_offset, 16) // 1000
        f_microsec_offset = int(s_offset, 16) % 1000
        date_time = datetime.datetime.strptime(str(base_time),
                                               "%Y-%m-%d %H:%M:%S.%f")
        date_time += datetime.timedelta(
                        microseconds=int(f_microsec_offset),
                        milliseconds=int(f_offset))

        return str(date_time)
