#
# Copyright (C) 2019 Murata Manufacturing Co.,Ltd.
#

##
# @brief Control command procedure.
# @author E2N3
# @date 2019.12.24

# -*- coding: utf-8 -*-

# ----- import -----
import threading
from time import sleep
from snd_cmd_proc import ctrl_snd_cmd
from seq_num import CreateSeqList
from Debug import Debug_GetObj
from CLS_Define import COM_DEF


##
# @brief Start timer thread when timeout happen.
# @param QSndRcv    queue class used by this thread and
#                   receive interface thread
# @retval None
def EvtTimerThread(QSndRcv):

    # Get logger info
    Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

    Dbg.log(COM_DEF.TRACE,
            "[S] EvtTimerThread")

    Dbg.log(COM_DEF.ERROR,
            "TIMEOUT !!")

    QSndRcv.put(COM_DEF.i_RET_ABNORMAL_TIMEOUT)

    Dbg.log(COM_DEF.TRACE,
            "[E] EvtTimerThread")


##
# @brief The processing class of the sending thread
#        corresponding to each device
class SND_CTRL():

    ##
    # @brief d_instance_id_list    Instance ID management variable
    d_instance_id_list = {}

    ##
    # @brief d_dst_node_id_list    Management variable of payout number of
    #                              Destination ID
    d_dst_node_id_list = {}

    # @cond
    # (starting number of setting range) - 1
    d_dst_node_id_list["WIRELESS_DEVICE"] = 9
    d_dst_node_id_list["AP"] = 59
    d_dst_node_id_list["AIRCAP"] = 109
    d_dst_node_id_list["NETWORKTOOL"] = 129
    # @endcond

    ##
    # @brief Run when instantiating the SND_CTRL class.
    # @param s_DeviceId    peer device name
    # @param i_src_id    source id
    # @param s_DeviceType    device type
    # @param s_com_port    com port of the opposite device
    # @param s_host    host of the opposite device
    # @param i_port    port of the opposite device
    # @retval None
    def __init__(self, s_DeviceId, i_src_id, s_DeviceType,
                 s_com_port, s_host, i_port):
        """
        initialize local variable
        """
        # @cond
        # Get logger info
        self.Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

        self.s_DeviceId = s_DeviceId
        self.i_src_id = i_src_id
        self.s_DeviceType = s_DeviceType
        self.s_com_port = s_com_port
        self.s_host = s_host
        self.i_port = i_port

        self.EwaitStop = threading.Event()
        self.l_command_list = []
        self.i_repeat_max = COM_DEF.i_MAX_TEST_RETRY
        self.i_test_num = 0
        self.i_evt_wait_flg = 0
        self.i_evt_rcvd_flg = False
        self.i_evt_rcvd_num = 0
        self.s_old_LogFileName = ""
        # @endcond

        CreateSeqList(self.s_DeviceType)

    ##
    # @brief Set the latest number of node id in destination id.
    # @param d_connect_info    connect information \n
    #                            - (s_host, i_port) : host name, port number \n
    #                            - s_com_port : COM port
    # @retval None
    def Update_NodeId(self, d_connect_info):
        """
        update node id
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] Update_NodeId")

        # setting of instance id information list.
        for i_src_key, v_instance in SND_CTRL.d_instance_id_list.items():
            if v_instance["DEVINFO"] == d_connect_info:
                self.Dbg.log(COM_DEF.DEBUG,
                             "device info already exist")
                return
            else:
                pass

        SND_CTRL.d_dst_node_id_list[self.s_DeviceType] += 1

        self.Dbg.log(COM_DEF.DEBUG,
                     '[%s] NODE ID : 0x%02x' %
                     (self.s_DeviceType,
                      SND_CTRL.d_dst_node_id_list[self.s_DeviceType]))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] Update_NodeId")

        return

    ##
    # @brief Set instance id to management list.
    # @param d_connect_info    connect information \n
    #                            - (s_host, i_port) : host name, port number \n
    #                            - s_com_port : COM port
    # @retval None
    def Generate_PeerDeviceInfoList(self, d_connect_info):
        """
        generate peer device information list
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] Generate_PeerDeviceInfoList")

        d_interface_info = {}
        d_dst_id = {}
        d_device_info = {}
        d_ip_addr = {}
        i_dst_instance_id = 0x00

        d_interface_info["DEVINFO"] = d_connect_info

        i_node_id = SND_CTRL.d_dst_node_id_list[self.s_DeviceType]

        self.Dbg.log(COM_DEF.TRACE,
                     '[%s] NODE ID : 0x%02x' %
                     (self.s_DeviceId, i_node_id))

        i_dst_id = (i_node_id << 8) + i_dst_instance_id
        d_dst_id["DstId"] = i_dst_id

        self.Dbg.log(COM_DEF.DEBUG,
                     '[%s] DST ID : 0x%04x' %
                     (self.s_DeviceId, d_dst_id["DstId"]))

        d_device_info["DEVID"] = self.s_DeviceId
        d_ip_addr["IPADDR"] = ""

        d_device_info.update(d_ip_addr)
        d_dst_id.update(d_device_info)
        d_interface_info.update(d_dst_id)

        # @cond
        SND_CTRL.d_instance_id_list[self.i_src_id] = d_interface_info
        # @endcond

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] Generate_PeerDeviceInfoList")

    ##
    # @brief Register command data for each transmission thread.
    # @param d_req_cmd_data command data info
    # @retval d_rt_params    value of the result \n
    #                           - COM_DEF.i_RET_SUCCESS
    def Register_Command(self, d_req_cmd_data):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] Register_Command")
        d_rt_params = {"Result": COM_DEF.i_RET_SUCCESS}

        try:
            self.l_command_list.append(d_req_cmd_data)
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR, "failed to register command")
            self.Dbg.log(COM_DEF.ERROR, err_info)
            d_rt_params['Result'] = COM_DEF.i_RET_SYSTEM_ERROR

        self.Dbg.log(COM_DEF.DEBUG, "%s" % str(self.l_command_list))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] Register_Command")

        return d_rt_params

    ##
    # @brief run the command data.
    # @param d_req_cmd_data command data info
    # @retval l_rt_params_list TLV result list
    def Run_Command(self, d_req_cmd_data):

        s_CmdName = d_req_cmd_data["command"]
        d_TestParam = d_req_cmd_data["params"]

        return self.__tx_proc(s_CmdName, d_TestParam)

    ##
    # @brief Get the state of the event wait flag for each transmission thread
    # @param None
    # @retval b_ret    value of the result \n
    #                    - True \n
    #                    - False
    def Get_EventStatus(self, event_number):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] Get_EventStatus")
        self.Dbg.log(COM_DEF.TRACE,
                     "event number : " + str(event_number))
        self.Dbg.log(COM_DEF.DEBUG,
                     "wait event status : %s"
                     % "enabled"
                     if self.i_evt_wait_flg == 1 else "disabled")

        if 1 == self.i_evt_wait_flg:
            # wait event
            b_ret = True
        else:
            # already received event.
            self.i_evt_rcvd_flg = True
            self.i_evt_rcvd_num = event_number
            b_ret = False

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] Get_EventStatus")

        return b_ret

    ##
    # @brief Start test control thread.
    # @param Qmain    queue class used by main and interface thread
    #                      (class object)
    # @param QSndRcv    queue class used by this thread and
    #                   receive interface thread (class object)
    # @param Cmain    threading.Condition class. wait notify_all signal
    #                       (class object)
    # @param IfCtrl    socket or serial object (class object)
    # @param LogCtrl    log class (class object)
    # @retval None
    def StartThread(self, Qmain, QSndRcv, Cmain, IfCtrl,
                    LogCtrl):
        """
        start snd ctrl thread
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] StartThread")

        self.QSndRcv = QSndRcv
        self.LogCtrl = LogCtrl
        self.IfCtrl = IfCtrl

        # @cond
        self.SndCtrlThread = \
            threading.Thread(target=self.__SND_CtrlThread,
                             args=(Qmain,
                                   Cmain,),
                             name=self.s_DeviceId)
        # @endcond

        self.SndCtrlThread.setDaemon(True)
        self.SndCtrlThread.start()

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] StartThread")

    ##
    # @brief Command transmission and reception processing is
    #        performed to the opposite device
    # @param Qmain    queue class used by main and interface thread
    #                      (class object)
    # @param Cmain    threading.Condition class. wait notify_all signal
    #                       (class object)
    # @retval None
    def __SND_CtrlThread(self, Qmain, Cmain):
        """
        control to manage some registered command
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __SND_CtrlThread")

        self.Dbg.log(COM_DEF.INFO,
                     "start [%s] thread" %
                     (self.s_DeviceId))

        while not self.EwaitStop.is_set():

            # wait start send procedure
            self.Dbg.log(COM_DEF.TRACE,
                         '%s: condition wait...' %
                         self.s_DeviceId)

            """
            wait notify_all from robotframework process
            """
            with Cmain:
                Cmain.wait()

            self.l_rt_params_list = []

            # count start from 1 because array 0 is empty.
            i_cnt = 0
            i_reg_testNum = len(self.l_command_list)

            self.Dbg.log(COM_DEF.DEBUG,
                         "[%s] start flush command [registered : %d]" %
                         (self.s_DeviceId, i_reg_testNum))

            # @cond
            # Control command is executed when test number is matched
            while i_cnt < i_reg_testNum:

                # get command info
                d_req_cmd_data = self.l_command_list[i_cnt]

                s_CmdName = d_req_cmd_data["command"]
                d_TestParam = d_req_cmd_data["params"]

                self.Dbg.log(COM_DEF.DEBUG,
                             "command [%d] : %s" % (i_cnt, s_CmdName))
                self.Dbg.log(COM_DEF.DEBUG,
                             "params  [%d] : %s" % (i_cnt, str(d_TestParam)))

                d_rslt_data = \
                    self.__tx_proc(s_CmdName, d_TestParam)

                d_rt_params = {self.s_DeviceId: {s_CmdName: {}}}
                d_rt_params[self.s_DeviceId][s_CmdName].update(d_rslt_data)

                self.l_rt_params_list.append(d_rt_params)

                if COM_DEF.i_RET_WAIT_NEXT_CMD == d_rslt_data['Result']:
                    self.Dbg.log(COM_DEF.DEBUG, "execute next command...")
                else:
                    if COM_DEF.i_RET_SUCCESS != d_rslt_data['Result']:
                        self.Dbg.log(COM_DEF.ERROR,
                                     '[%s] %s failed' %
                                     (self.s_DeviceId, s_CmdName))
                        break
                    else:
                        pass

                i_cnt += 1
            # while loop end
            # @endcond

            if i_reg_testNum:
                self.Dbg.log(COM_DEF.DEBUG,
                             "[%s] finish flush command" % self.s_DeviceId)
                Qmain.put(self.s_DeviceId)
            else:
                pass
        # while loop

        self.Dbg.log(COM_DEF.INFO,
                     '[%s] exit thread [main]' %
                     (self.s_DeviceId))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] SND_CtrlThread")

    def __tx_proc(self, s_CmdName, d_TestParam):
        """
        common procedure for send control
        """
        d_rt_params = {}

        """
        Add or change the required parameters for each command.
        """
        i_result = self.__check_TestParam(s_CmdName,
                                          d_TestParam)

        if COM_DEF.i_RET_WAIT_NEXT_CMD == i_result or \
                COM_DEF.i_RET_SUCCESS != i_result:
            d_rt_params['Result'] = i_result
        else:
            i_dst_id = \
                SND_CTRL.d_instance_id_list[self.i_src_id]["DstId"]
            i_result, d_rt_params, i_rcv_dst_id = \
                ctrl_snd_cmd(self.IfCtrl,
                             i_dst_id,
                             self.i_src_id,
                             s_CmdName,
                             d_TestParam,
                             self.QSndRcv,
                             self.s_DeviceType)

            if COM_DEF.i_RET_SUCCESS != i_result:
                self.Dbg.log(COM_DEF.ERROR,
                             '[%s] ctrl_snd_cmd ' %
                             (self.s_DeviceId) +
                             'error [ret:%d]' %
                             (i_result))
                d_rt_params['Result'] = i_result
            else:
                self.Dbg.log(COM_DEF.TRACE,
                             '[%s] DST ID : 0x%04x' %
                             (self.s_DeviceId,
                              i_rcv_dst_id))

                i_result = self.__update_TestInfo(
                                i_rcv_dst_id,
                                s_CmdName,
                                d_TestParam,
                                d_rt_params)
                if COM_DEF.i_RET_SUCCESS != i_result:
                    self.Dbg.log(COM_DEF.ERROR,
                                 '[%s] __update_TestInfo' %
                                 (self.s_DeviceId) +
                                 ' error [ret:%d]' %
                                 (i_result))
                else:
                    pass

        if i_result and COM_DEF.i_RET_SUCCESS == d_rt_params['Result']:
            d_rt_params['Result'] = i_result
        else:
            pass

        return d_rt_params

    ##
    # @brief Set test parameter by following environment.
    # @param i_src_id    source id
    # @param s_CmdName    command name
    # @param d_TestParam    test parameter
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __check_TestParam(self, s_CmdName, d_TestParam):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __check_TestParam")
        self.Dbg.log(COM_DEF.TRACE,
                     "Command Name : " + s_CmdName)

        i_result = COM_DEF.i_RET_SUCCESS

        # @cond
        if 'WIRELESS_DEVICE' == self.s_DeviceType:
            if "Request_initialization_to" == s_CmdName:
                i_result = \
                    self.__check_InitializationParams(d_TestParam)
            elif "Request_scan_to" == s_CmdName or \
                 "Request_connection_to" == s_CmdName:
                self.i_evt_rcvd_flg = False
                self.i_evt_rcvd_num = 0
            else:
                pass
        else:
            if "Request_initialization_to" == s_CmdName:
                self.__set_LogNameType(d_TestParam)
            else:
                pass

        if "Request_test_ready" == s_CmdName:
            self.__get_CurrentTime(d_TestParam)
        elif "Request_event_wait_to" == s_CmdName:
            i_result = self.__wait_EventNotification(d_TestParam)
        elif "Request_ping_to" == s_CmdName:
            i_result = self.__update_PeerIpAddress(d_TestParam)
        elif "Request_iperf_to" == s_CmdName:
            i_result = self.__update_IperfParams(d_TestParam)
        elif "Request_sleep_to" == s_CmdName:
            i_result = self.__sleep_Thread(d_TestParam)
        else:
            pass

        # @endcond

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __check_TestParam")

        return i_result

    ##
    # @brief Set parameters for Srcid and Dstid.
    # @param i_src_id    source id
    # @param d_TestParam    test parameter \n
    #                         ["NumOfIf"] Number of interface to generate \n
    #                         ["DataList"] Multiple TLV data
    # @param LogCtrl    log class (class object)
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __check_InitializationParams(self, d_TestParam):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __check_InitializationParams")

        i_result = COM_DEF.i_RET_SUCCESS
        l_src_id = []

        # instance id is guranteeded
        if "NumOfIf" in d_TestParam:
            i_if_num = d_TestParam["NumOfIf"]
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "The required parameter does not exist : NumOfIf")
            return COM_DEF.i_RET_TLV_ABNORMAL

        if "DataList" in d_TestParam:
            if i_if_num == len(d_TestParam["DataList"]):

                if self.s_com_port != "":
                    self.Dbg.log(COM_DEF.TRACE,
                                 "COM PORT : " + self.s_com_port)
                    d_connect_info = self.s_com_port
                else:
                    self.Dbg.log(COM_DEF.TRACE,
                                 "HOST IP  : " + self.s_host)
                    self.Dbg.log(COM_DEF.TRACE,
                                 "PORT     : " + str(self.i_port))
                    d_connect_info = (self.s_host, self.i_port)

                # get source id with same connection information
                for i_src_key, v_instance in \
                        SND_CTRL.d_instance_id_list.items():

                    if self.i_src_id != i_src_key and \
                            v_instance["DEVINFO"] == d_connect_info:

                        self.Dbg.log(COM_DEF.DEBUG,
                                     "multiple instances exist " +
                                     "in the same connection " +
                                     "(registered:0x%04x/new:%04x)" %
                                     (self.i_src_id, i_src_key))
                        l_src_id.append(i_src_key)
                    else:
                        pass
                # for loop end

                l_src_id.sort()
                self.Dbg.log(COM_DEF.TRACE,
                             "SRC ID list : " + str(l_src_id))

                if len(d_TestParam["DataList"]) != len(l_src_id):
                    self.Dbg.log(COM_DEF.ERROR,
                                 "number of DataList (%d)" %
                                 (len(d_TestParam["DataList"])) +
                                 " != number of SRC ID list (%d)" %
                                 (len(l_src_id)))
                    return COM_DEF.i_RET_TLV_ABNORMAL
                else:
                    pass

                i_cnt = 0
                while i_cnt < i_if_num:
                    d_tmp_list = {}
                    d_tmp_list["SrcId"] = l_src_id[i_cnt]
                    d_tmp_list["DstId"] = \
                        SND_CTRL.d_instance_id_list[l_src_id[i_cnt]]["DstId"]
                    d_TestParam["DataList"][i_cnt].update(d_tmp_list)
                    i_cnt += 1
                # for loop end
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "the number of interface is unmatch " +
                             "(expect:%d/result:%d)" %
                             (i_if_num, len(d_TestParam["DataList"])))
                return COM_DEF.i_RET_TLV_ABNORMAL
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "DataList is none !!")
            return COM_DEF.i_RET_TLV_ABNORMAL

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __check_InitializationParams")

        return i_result

    ##
    # @brief Create LogName test parameter
    # @param d_TestParam  test parameter
    # @retval None
    def __set_LogNameType(self, d_TestParam):
        """
        Set LogName Type parameter to Request_initialization_to command
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __set_LogNameType")

        if self.s_old_LogFileName == \
                self.LogCtrl.s_LogFileName:
            self.LogCtrl.GenerateLogFile('Temp')
        else:
            pass

        d_TestParam["LogName"] = self.LogCtrl.s_LogFileName
        self.s_old_LogFileName = self.LogCtrl.s_LogFileName

        self.Dbg.log(COM_DEF.DEBUG,
                     "[%s] Type : LogName Value : %s" %
                     (self.s_DeviceId, d_TestParam["LogName"]))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __set_LogNameType")

    ##
    # @brief Set the parameters required to set the time.
    # @param i_src_id    source id
    # @param d_TestParam    test parameter
    # @param LogCtrl    log class (class object)
    # @retval None
    def __get_CurrentTime(self, d_TestParam):
        """
        Set base time to peer devices for time sync.
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __get_CurrentTime")

        # Set log base time
        s_date, s_time = \
            self.LogCtrl.SetBaseTime(self.i_src_id, self.s_DeviceType)
        d_TestParam["Date"] = s_date
        d_TestParam["Time"] = s_time

        self.Dbg.log(COM_DEF.DEBUG,
                     "DATE [%s] TIME [%s]" %
                     (d_TestParam["Date"], d_TestParam["Time"]))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __get_CurrentTime")

    ##
    # @brief Wait for the event.
    # @param d_TestParam    test parameter
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_WAIT_NEXT_CMD \n
    #                    - Failure : Value other than
    #                                COM_DEF.i_RET_WAIT_NEXT_CMD
    def __wait_EventNotification(self, d_TestParam):
        """
        wait for event notification
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __wait_EventNotification")

        i_result = COM_DEF.i_RET_SUCCESS

        if self.i_evt_rcvd_flg is True:
            self.Dbg.log(COM_DEF.INFO,
                         "already received: %d" %
                         (self.i_evt_rcvd_num))
            if self.i_evt_rcvd_num == d_TestParam["EventNum"]:
                self.i_evt_rcvd_flg = False
                self.i_evt_rcvd_num = 0

                self.Dbg.log(COM_DEF.TRACE,
                             "[E] __wait_EventNotification")

                return COM_DEF.i_RET_WAIT_NEXT_CMD
        else:
            pass

        self.i_evt_wait_flg = 1
        i_evt_num = -1

        th_tim = threading.Timer(60, EvtTimerThread,
                                 args=(self.QSndRcv,),)
        th_tim.setDaemon(True)
        th_tim.start()

        while (i_evt_num != d_TestParam["EventNum"]):
            self.Dbg.log(COM_DEF.DEBUG,
                         "wait event : %d" %
                         (d_TestParam["EventNum"]))
            i_evt_num = self.QSndRcv.get()
            self.i_evt_wait_flg = 0
            if i_evt_num == COM_DEF.i_RET_ABNORMAL_TIMEOUT:
                i_result = COM_DEF.i_RET_ABNORMAL_TIMEOUT
                break
            else:
                th_tim.cancel()
                self.Dbg.log(COM_DEF.INFO,
                             "event received : %d" %
                             (i_evt_num))

        # while loop end
        self.Dbg.log(COM_DEF.TRACE,
                     "wait event loop end")

        del th_tim

        if COM_DEF.i_RET_ABNORMAL_TIMEOUT != i_result:
            i_result = COM_DEF.i_RET_WAIT_NEXT_CMD
        else:
            pass

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __wait_EventNotification")

        return i_result

    ##
    # @brief Set parameters for sending the Startiperf command.
    # @param d_TestParam test parameter \n
    #                         ["IperfModeType"] iperf type specification
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __update_IperfParams(self, d_TestParam):
        """
        Update iperf parameter
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __update_IperfParams")

        i_result = COM_DEF.i_RET_SUCCESS

        if "IperfModeType" not in d_TestParam:
            self.Dbg.log(COM_DEF.ERROR,
                         "IperfModeType is none")
            return COM_DEF.i_RET_TLV_ABNORMAL
        else:
            pass

        if d_TestParam["IperfModeType"] == 0x01:
            d_TestParam["IperfCmdString"] = "-s " + \
                                            d_TestParam["IperfCmdString"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "iperf server command : " +
                         d_TestParam["IperfCmdString"])
        else:
            i_result = self.__update_PeerIpAddress(d_TestParam)
            if i_result == COM_DEF.i_RET_SUCCESS:

                d_TestParam["IperfCmdString"] = \
                    "-c " \
                    + d_TestParam["IpAddress"] \
                    + " " \
                    + d_TestParam["IperfCmdString"]

                self.Dbg.log(COM_DEF.DEBUG,
                             "iperf client command : %s" %
                             (d_TestParam["IperfCmdString"]))

                if "IpAddress" in d_TestParam:
                    del d_TestParam["IpAddress"]
                    self.Dbg.log(COM_DEF.DEBUG,
                                 "Remove DestIpAddress in d_testParam")
                else:
                    pass

            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "__update_PeerIpAddress error [ret:%d]" %
                             (i_result))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __update_IperfParams")

        return i_result

    ##
    # @brief Set parameters for sending the Startping command.
    # @param d_TestParam test parameter
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __update_PeerIpAddress(self, d_TestParam):
        """
        Update ip address parameter
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __update_PeerIpAddress")

        i_result = COM_DEF.i_RET_SUCCESS

        i_result = self.__get_IpAddr(d_TestParam)
        if i_result == COM_DEF.i_RET_SUCCESS:
            if "DestIpAddress" in d_TestParam:
                d_TestParam["IpAddress"] = d_TestParam["DestIpAddress"]
                del d_TestParam["DestIpAddress"]
                self.Dbg.log(COM_DEF.DEBUG,
                             "changed from DestIpAddress to " +
                             "IpAddress %s" % d_TestParam["IpAddress"])
                if 0 == len(d_TestParam["IpAddress"]):
                    self.Dbg.log(COM_DEF.ERROR,
                                 "IpAddress is not found !!")
                    return COM_DEF.i_RET_TLV_ABNORMAL
                else:
                    pass
            else:
                pass

            if "DestDeviceInfoKey" in d_TestParam:
                del d_TestParam["DestDeviceInfoKey"]
                self.Dbg.log(COM_DEF.DEBUG,
                             "removed DestDeviceInfoKey " +
                             "in command")
            else:
                pass

        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "SND_Get_IpAddress error [ret:%d]" %
                         (i_result))

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __update_PeerIpAddress")

        return i_result

    ##
    # @brief Get an IPaddress from the instance id list.
    # @param d_TestParam test parameter
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __get_IpAddr(self, d_TestParam):
        """
        check ip params and update IP Address from DestDeviceInfoKey.
        If DestIpAddress is included, give priority to DestIpAddress.
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __get_IpAddr")

        i_result = COM_DEF.i_RET_SUCCESS

        if "DestIpAddress" in d_TestParam:
            self.Dbg.log(COM_DEF.TRACE,
                         "DestIpAddress is included (%s)" %
                         (d_TestParam["DestIpAddress"]))

        elif "DestDeviceInfoKey" in d_TestParam:
            for i_check_src_id in SND_CTRL.d_instance_id_list:
                if d_TestParam["DestDeviceInfoKey"] == \
                   SND_CTRL.d_instance_id_list[i_check_src_id]["DEVID"]:
                    d_TestParam["DestIpAddress"] = \
                        SND_CTRL.d_instance_id_list[i_check_src_id]["IPADDR"]
                    break
                else:
                    pass
            # for loop end

            if "DestIpAddress" in d_TestParam:
                pass
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "can't find DestDeviceInfoKey type : %s" %
                             (d_TestParam["DestDeviceInfoKey"]))
                return COM_DEF.i_RET_TLV_ABNORMAL
        else:
            if "IpAddress" in d_TestParam:
                # this root is used in case of the 'Continue' command.
                # The reason 'DestDeviceKeyInfo' or 'DestIpAddress' to
                # 'IpAddress was changed from
                # beacuse Request_ping_to or
                # Request_iperf_to command already be executed.
                pass
            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "Neither DestIpAddress nor " +
                             "DestDeviceInfoKey are included.")
                return COM_DEF.i_RET_TLV_ABNORMAL

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __get_IpAddr")

        return i_result

    ##
    # @brief sleep thread
    # @param d_TestParam test parameter
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __sleep_Thread(self, d_TestParam):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __sleep_Thread")

        if "TimeMsec" in d_TestParam:
            wait_time = d_TestParam["TimeMsec"] / 1000
        elif "TimeSec" in d_TestParam:
            wait_time = d_TestParam["TimeSec"]
        else:
            return COM_DEF.i_RET_TLV_ABNORMAL

        self.Dbg.log(COM_DEF.INFO,
                     "[%s] wait %d sec" %
                     (self.s_DeviceId, wait_time))

        # sleep thread
        sleep(wait_time)

        self.Dbg.log(COM_DEF.INFO, "[%s] wake up" % self.s_DeviceId)

        i_ret = COM_DEF.i_RET_WAIT_NEXT_CMD

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __sleep_Thread")

        return i_ret

    ##
    # @brief Update test info by test command result.
    # @param i_dst_id     peer device id
    # @param s_CmdName    command name
    # @param d_TestParam    test parameter
    # @param d_rt_params    response tlv until prev command
    # @retval i_result    value of the result \n
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __update_TestInfo(self, i_dst_id, s_CmdName, d_TestParam,
                          d_rt_params):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __update_TestInfo")
        self.Dbg.log(COM_DEF.TRACE,
                     "Command Name : " + s_CmdName)

        i_result = COM_DEF.i_RET_SUCCESS

        # WIRELESS_DEVICE command
        if "WIRELESS_DEVICE" == self.s_DeviceType:
            if "Request_initialization_to" == s_CmdName:
                # destination id update
                self.__Update_DestinationId(i_dst_id)
                i_result = self.__update_PeerDeviceInfoList(d_rt_params)
            elif "Request_termination_to" == s_CmdName:
                self.__clear_DestinationId()
            elif "Set_ip_to" == s_CmdName or \
                    "Get_ip_from" == s_CmdName or \
                    "Set_ip_by_dhcp_to" == s_CmdName:
                self.__update_IpAddress(d_rt_params["IpAddress"])
            elif "Request_disconnection_to" == s_CmdName:
                self.__delete_IpAddress()
            else:
                pass
        else:
            if "Request_initialization_to" == s_CmdName:
                self.__Update_DestinationId(i_dst_id)
            elif "Request_test_ready" == s_CmdName and \
                    "IpAddress" in d_rt_params:
                self.__update_IpAddress(d_rt_params["IpAddress"])
            else:
                pass

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __update_TestInfo")

        return i_result

    ##
    # @brief Update the destination id of the instance id management list.
    # @param i_dst_id    destination id
    # @retval None
    def __Update_DestinationId(self, i_dst_id):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __Update_DestinationId")

        # @cond
        # setting destination id
        SND_CTRL.d_instance_id_list[self.i_src_id]["DstId"] = i_dst_id
        # @endcond

        self.Dbg.log(COM_DEF.DEBUG,
                     "SRC ID : 0x%04x " % self.i_src_id +
                     " DST ID : 0x%04x"
                     % SND_CTRL.d_instance_id_list[self.i_src_id]["DstId"])

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __Update_DestinationId")

    ##
    # @brief Set the destination id in the Instance id list.
    # @param d_rt_params    response tlv until prev command
    # @retval i_result    value of the result \n
    #                         ["NumOfIf"] Number of interface to generate \n
    #                         ["DataList"] Multiple TLV data \n
    #                         ["SrcId"] source id \n
    #                         ["DstId"] destination id
    #                    - Success : COM_DEF.i_RET_SUCCESS \n
    #                    - Failure : Value other than COM_DEF.i_RET_SUCCESS
    def __update_PeerDeviceInfoList(self, d_rt_params):
        """
        Update destination id info from Request_initialization_to response
        """
        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __update_PeerDeviceInfoList")

        # instance id is guranteeded
        if "NumOfIf" in d_rt_params:
            i_if_num = d_rt_params["NumOfIf"]
            self.Dbg.log(COM_DEF.DEBUG,
                         "the number of interfaces : %d" %
                         (i_if_num))
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "InitWLAN response: NumOfIf is none")
            return COM_DEF.i_RET_TLV_ABNORMAL

        if "DataList" in d_rt_params:
            if i_if_num == len(d_rt_params["DataList"]):
                i_cnt = 0
                while i_cnt < i_if_num:
                    i_dst_id = 0
                    i_src_id = 0

                    # get the pair of srcid and dstid included in DataList.
                    d_list_parts = d_rt_params["DataList"][i_cnt]

                    if "SrcId" in d_list_parts:
                        i_src_id = d_list_parts["SrcId"]
                        self.Dbg.log(COM_DEF.INFO,
                                     "SRC ID : 0x%04x" % (i_src_id))
                    else:
                        self.Dbg.log(COM_DEF.ERROR,
                                     "InitWLAN response : SRC ID is none")
                        return COM_DEF.i_RET_TLV_ABNORMAL

                    if "DstId" in d_list_parts:
                        i_dst_id = d_list_parts["DstId"]
                        self.Dbg.log(COM_DEF.INFO,
                                     "DST ID : 0x%04x" % (i_dst_id))
                    else:
                        self.Dbg.log(COM_DEF.ERROR,
                                     "InitWLAN response : " +
                                     "DST ID is none !!")
                        return COM_DEF.i_RET_TLV_ABNORMAL

                    # register dst id in srcid list.
                    if i_dst_id in SND_CTRL.d_instance_id_list:
                        SND_CTRL.d_instance_id_list[i_dst_id]["DstId"] = \
                            i_src_id
                    else:
                        self.Dbg.log(COM_DEF.ERROR,
                                     "InitWLAN response : " +
                                     "unexpected DST ID : 0x%04x" %
                                     (i_dst_id))
                        return COM_DEF.i_RET_TLV_ABNORMAL

                    i_cnt += 1

                # while end

            else:
                self.Dbg.log(COM_DEF.ERROR,
                             "the number of DataList is unmatch " +
                             "(NumOfIf:%d/num of DataList:%d" %
                             (i_if_num, len(d_rt_params["DataList"])))
                return COM_DEF.i_RET_TLV_ABNORMAL
        else:
            self.Dbg.log(COM_DEF.ERROR,
                         "InitWLAN response : DataList is none !!")
            return COM_DEF.i_RET_TLV_ABNORMAL

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __update_PeerDeviceInfoList")

        return COM_DEF.i_RET_SUCCESS

    ##
    # @brief Update the IPAddress of the instance id management list.
    # @param s_IpAddr    IPAddress
    # @retval None
    def __update_IpAddress(self, s_IpAddr):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __update_IpAddress")

        old_ip_addr = \
            SND_CTRL.d_instance_id_list[self.i_src_id]["IPADDR"]
        self.Dbg.log(COM_DEF.DEBUG,
                     "SRC ID : 0x%04x " % self.i_src_id +
                     "old IP Address : %s" % old_ip_addr)

        SND_CTRL.d_instance_id_list[self.i_src_id]["IPADDR"] = s_IpAddr

        self.Dbg.log(COM_DEF.INFO,
                     "SRC ID : 0x%04x " % self.i_src_id +
                     "Update IP Address : %s" % s_IpAddr)

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __update_IpAddress")

    ##
    # @brief Delete an IPaddress that is registered in the instance id list.
    # @retval None
    def __delete_IpAddress(self):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __delete_IpAddress")

        for i_check_src_id in SND_CTRL.d_instance_id_list:
            i_dst_id = \
                SND_CTRL.d_instance_id_list[i_check_src_id]["DstId"]
            if self.i_src_id != i_dst_id:
                pass
            else:
                SND_CTRL.d_instance_id_list[i_check_src_id]["IPADDR"] = ""

                self.Dbg.log(COM_DEF.INFO,
                             '[0x%04x] Delete IP address : %s' %
                             (i_check_src_id,
                              SND_CTRL.d_instance_id_list[
                                  i_check_src_id]["IPADDR"]))
                break
        # for loop end

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __delete_IpAddress")

    ##
    # @brief Initializes the instance id at terminate execution.
    # @retval None
    def __clear_DestinationId(self):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] __clear_DestinationId")

        if self.s_com_port != "":
            self.Dbg.log(COM_DEF.TRACE,
                         "COM PORT : " + self.s_com_port)
            d_connect_info = self.s_com_port
        else:
            self.Dbg.log(COM_DEF.TRACE,
                         "HOST IP  : " + self.s_host)
            self.Dbg.log(COM_DEF.TRACE,
                         "PORT     : " + str(self.i_port))
            d_connect_info = (self.s_host, self.i_port)

        for i_src_key, v_instance in SND_CTRL.d_instance_id_list.items():
            if v_instance["DEVINFO"] == d_connect_info:
                i_dst_id = \
                    SND_CTRL.d_instance_id_list[i_src_key]["DstId"]
                i_dst_id = i_dst_id & COM_DEF.i_NODEID_MASK
                self.Dbg.log(COM_DEF.DEBUG,
                             '[0x%04x] DST ID : 0x%04x' %
                             (i_src_key, i_dst_id))
            else:
                pass
        # for loop end

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] __clear_DestinationId")
