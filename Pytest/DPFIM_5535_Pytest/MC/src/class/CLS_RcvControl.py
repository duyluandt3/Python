#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief Command Receive Thread. \n
#        Notify SND_CTRL thread to data by using queue \n
#        when command resposne is received.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

# ----- import -----
import threading
from Debug import Debug_GetObj
from rcv_cmd_proc import Decode_RequestData
from Decode_ComHdr import Decode_ComHdr
from CLS_Define import COM_DEF


##
# @brief Define processes related to receive processing.
class RCV_CTRL():

    ##
    # @brief Run when instantiating the RCV_CTRL class.
    # @param s_name    user-defined thread name
    # @param IfCtrl    socket or serial object
    # @param s_DeviceType    device type
    # @retval None
    def __init__(self, s_name, IfCtrl, s_DeviceType):

        # @cond
        # Get logger info
        self.Dbg = Debug_GetObj(COM_DEF.i_MODULE_MC)

        self.Dbg.log(COM_DEF.DEBUG,
                     "Initialize Receive Thread !! " + s_name)

        self.stop_event = threading.Event()
        self.s_name = s_name
        # socket or serial class
        self.IfCtrl = IfCtrl
        self.l_deviceInfo_list = [[]]
        self.i_TestCtrlThread_Count = 0
        self.s_device_type = s_DeviceType
        # @endcond

    ##
    # @brief Set information of test control thread that
    #        uses Socket or Serial port.
    # @param SocLog    socket class for log control thread (class object)
    # @param i_src_id    source id
    # @param QSndRcv    queue class used by this thread and
    #                   receive interface thread (class object)
    # @param SndCtrl    this class object (class object)
    # @retval None
    def RCV_SetRelatedThreadInfo(self, SocLog, i_src_id,
                                 QSndRcv, SndCtrl):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] RCV_SetRelatedThreadInfo")

        self.Dbg.log(COM_DEF.DEBUG,
                     '[%s] SRC ID : 0x%04x COUNTER : %d' %
                     (self.s_name, i_src_id,
                      self.i_TestCtrlThread_Count))

        self.l_deviceInfo_list.append([self.i_TestCtrlThread_Count,
                                       SocLog,
                                       i_src_id,
                                       QSndRcv,
                                       SndCtrl])

        self.i_TestCtrlThread_Count += 1

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] RCV_SetRelatedThreadInfo")

    ##
    # @brief Socket, or Serial port for each port.
    # @param None
    # @retval None
    def RCV_StartThread(self):

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] RCV_StartThread")

        # @cond
        self.ctrlpc_rcv_thread = \
            threading.Thread(target=self.__RCV_CtrlThread,
                             name=self.s_name)
        # @endcond

        self.ctrlpc_rcv_thread.setDaemon(True)
        self.ctrlpc_rcv_thread.start()

        self.Dbg.log(COM_DEF.TRACE,
                     "[E] RCV_StartThread")

    ##
    # @brief send recevie command to control thread or
    #        return ack command to device.
    # @retval None
    def __RCV_CtrlThread(self):

        l_rply_cmd = []
        s_read_data = ""
        s_read_cmd = ""

        self.Dbg.log(COM_DEF.TRACE,
                     "[S] RCV_Thread")
        self.Dbg.log(COM_DEF.INFO,
                     '[%s] start thread [recv] !!' %
                     (self.s_name))

        while not self.stop_event.is_set():

            try:
                s_read_data = self.IfCtrl.read()
            except Exception as err_info:
                self.Dbg.log(COM_DEF.ERROR,
                             err_info)
                s_read_data = ""
                break
            else:
                pass

            if isinstance(s_read_data, str):

                s_read_cmd += s_read_data

                while "" != s_read_cmd:

                    # get common header
                    i_result, i_dst_id, i_src_id, i_cmd_id, i_action, \
                        i_seq_num, i_ack_num, i_tlv_len, s_tlv_data = \
                        Decode_ComHdr(s_read_cmd, COM_DEF.i_MODULE_MC)

                    if COM_DEF.i_RET_SUCCESS == i_result and \
                            COM_DEF.i_CMD_NotifyCaptureLog != i_cmd_id:
                        self.Dbg.log(COM_DEF.DEBUG,
                                     '[%s] rcv cmd : %s' %
                                     (self.s_name, s_read_cmd))
                    else:
                        pass

                    if COM_DEF.i_RET_SUCCESS == i_result or \
                        COM_DEF.i_RET_COMHDR_STARTBIT == i_result or \
                            COM_DEF.i_RET_COMHDR_CKSUM == i_result:
                        i_cnt = 1
                        while i_cnt <= self.i_TestCtrlThread_Count:
                            # check MC thread id

                            if i_dst_id == self.l_deviceInfo_list[i_cnt][2]:
                                # get queue object for sending command
                                QSndRcv = self.l_deviceInfo_list[i_cnt][3]

                                if (i_action & COM_DEF.i_ACTION_UPPERMASK) != \
                                        COM_DEF.i_ACTION_REQ:

                                    # queue put to Test Control Thread()
                                    l_rply_cmd = []
                                    l_rply_cmd.append([i_result,
                                                       i_dst_id,
                                                       i_src_id,
                                                       i_cmd_id,
                                                       i_action,
                                                       i_seq_num,
                                                       i_ack_num,
                                                       i_tlv_len,
                                                       s_tlv_data])
                                    QSndRcv.put(l_rply_cmd)
                                else:
                                    SocLog = \
                                        self.l_deviceInfo_list[i_cnt][1]

                                    SndCtrl = \
                                        self.l_deviceInfo_list[i_cnt][4]

                                    # swap src id and dsc id
                                    Decode_RequestData(SocLog,
                                                       i_result,
                                                       i_src_id,
                                                       i_dst_id,
                                                       i_cmd_id,
                                                       i_action,
                                                       i_seq_num,
                                                       i_tlv_len,
                                                       s_tlv_data,
                                                       QSndRcv,
                                                       SndCtrl,
                                                       self.s_device_type)
                                # instance id found !!
                                break

                            else:
                                # check next list
                                i_cnt += 1
                        else:
                            # can't find match instance id
                            self.Dbg.log(COM_DEF.ERROR,
                                         "[%s] discard command - "
                                         % (self.s_name) +
                                         "DST ID : 0x%04x SRC ID : 0x%04x" %
                                         (i_dst_id, i_src_id))
                        # while loop end
                        if COM_DEF.i_COMHDR_LENGTH + i_tlv_len \
                           < len(s_read_cmd):
                            # musto be length x 2 because data is byte data.
                            i_next_pos = COM_DEF.i_COMHDR_LENGTH * 2 + \
                                i_tlv_len * 2
                            s_read_cmd = s_read_cmd[i_next_pos:]
                        else:
                            pass

                    elif COM_DEF.i_RET_COMHDR_LENGTH == i_result or \
                            COM_DEF.i_RET_WAIT_NEXT_CMD == i_result:
                        self.Dbg.log(COM_DEF.TRACE,
                                     '[%s] wait next command' %
                                     (self.s_name))
                        break
                    else:
                        self.Dbg.log(COM_DEF.TRACE,
                                     '[%s] discard command' %
                                     (self.s_name))
                        s_read_cmd = ""
                        break
                # while loop end
            else:
                pass
        # while loop end

        self.Dbg.log(COM_DEF.INFO,
                     '[%s] exit thread [recv] !!' %
                     (self.s_name))

        self.Dbg.log(COM_DEF.TRACE, "[E] RCV_Thread")
