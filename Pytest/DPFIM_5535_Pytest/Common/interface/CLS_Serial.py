#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief COM_SOCKET class definition.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import sys
import serial
import binascii
import time
import threading
from serial.tools import list_ports
from Debug import Debug_GetObj
from CLS_Define import COM_DEF


##
# @brief Define serial related processing
class COM_SERIAL():

    ##
    # @brief Run when instantiating the COM_SERIAL class.
    # @param s_COMPORT    Comport Number string
    # @param i_BAUDRATE    baudrate
    # @param s_USER    loggin user id
    # @param s_PASSWORD    loggin password
    # @param b_chg_flg    true - changed from string to byte \n
    #                     false - not changed
    # @param i_module_type    module number
    #                           - COM_DEF.i_MODULE_MC(0) : MC \n
    #                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
    #                           - COM_DEF.i_MODULE_AP(2) : AP \n
    #                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
    #                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
    # @retval None
    def __init__(self, s_COMPORT, i_BAUDRATE, s_USER, s_PASSWORD,
                 b_chg_flg, i_module_type):

        # @cond
        self.Dbg = Debug_GetObj(i_module_type)
        self.comport = serial.Serial(timeout=10)
        self.portNo = s_COMPORT
        self.comport.baudrate = i_BAUDRATE
        if COM_DEF.i_MODULE_DUT == i_module_type:
            self.comport.rtscts = True
        else:
            self.comport.rtscts = False
        self.b_chg_flg = b_chg_flg
        self.i_module_type = i_module_type
        self.SERIAL_SND_LOCK = threading.Semaphore()
        self.SERIAL_RCV_LOCK = threading.Semaphore()

        l_list_ports = list_ports.comports()

        devices = []

        for info in l_list_ports:
            devices.append(info.device)

        if len(devices) == 0:
            self.Dbg.log(COM_DEF.DEBUG, "device not found")
            sys.exit(0)
        else:
            for i in range(len(devices)):
                self.Dbg.log(COM_DEF.DEBUG, "input : " + str(i) +
                             ": open " + devices[i])
                if s_COMPORT == devices[i]:
                    self.comport.port = devices[i]
                else:
                    pass
            # for loop end

        try:
            self.comport.open()
            # comport open
            self.Dbg.log(COM_DEF.DEBUG, "open : " + str(self.comport.port))

            if s_USER != "" and s_PASSWORD != "":
                s_snd_cmd = s_USER
                if not s_snd_cmd.endswith("\r\n"):
                    s_snd_cmd = s_snd_cmd + "\r\n"
                else:
                    pass
                self.Dbg.log(COM_DEF.DEBUG, "User : " + s_snd_cmd)
                self.write(s_snd_cmd)

                time.sleep(1)

                s_snd_cmd = s_PASSWORD
                if not s_snd_cmd.endswith("\r\n"):
                    s_snd_cmd = s_snd_cmd + "\r\n"
                else:
                    pass
                self.Dbg.log(COM_DEF.DEBUG, "Password : " + s_snd_cmd)
                self.write(s_snd_cmd)
            else:
                pass
        except Exception as err_info:
            self.Dbg.log(COM_DEF.ERROR,
                         "already open : " + str(self.comport.port))
            self.Dbg.log(COM_DEF.ERROR, err_info)

        # @endcond

    ##
    # @brief Get the state of the serial port, whether it’s open.
    # @param None
    # @retval b_connect    value of the result \n
    #                      - True : serial port open \n
    #                      - False : serial port not open
    def isConnected(self):
        try:
            return self.comport.isOpen()
        except:
            return False

    ##
    # @brief Read the received data of the serial.
    # @param None
    # @retval rsp_data    received data
    def read(self):

        while self.comport.is_open:
            self.SERIAL_RCV_LOCK.acquire()

            try:
                b_command = self.comport.read(1)
                i_rcvSize = self.comport.inWaiting()
            except Exception as err_info:
                self.Dbg.log(COM_DEF.ERROR, err_info)
                self.SERIAL_RCV_LOCK.release()
                return ""

            if i_rcvSize:
                b_command += self.comport.read(i_rcvSize)
            else:
                pass

#                if self.b_chg_flg:
            rsp_data = binascii.hexlify(b_command).decode()
#                else:
#                    rsp_data = rsp_data.decode('utf-8')

            self.SERIAL_RCV_LOCK.release()

            return rsp_data
        else:
            # DEBUG
            self.Dbg.log(COM_DEF.DEBUG, "comport is not opened !!")
            sys.exit(1)

    ##
    # @brief Write data to the socket.
    # @param s_command    command data
    # @retval i_ret    value of the result \n
    #                      - Success : COM_DEF.i_RET_SUCCESS \n
    #                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
    def write(self, s_command):

        i_ret = COM_DEF.i_RET_SUCCESS

        if self.comport.is_open:

            self.SERIAL_SND_LOCK.acquire()

            if self.b_chg_flg:
                try:
                    self.comport.write(binascii.unhexlify(s_command))
                except Exception as err_info:
                    self.Dbg.log(COM_DEF.ERROR, s_command)
                    self.Dbg.log(COM_DEF.ERROR, err_info)
                    i_ret = COM_DEF.i_RET_SYSTEM_ERROR
            else:
                if not s_command.endswith("\r\n"):
                    s_command = s_command + "\r\n"
                else:
                    pass
                self.comport.write(s_command.encode('utf-8'))

            self.comport.flush()

            self.SERIAL_SND_LOCK.release()

        else:
            # DEBUG
            self.Dbg.log(COM_DEF.ERROR, "comport is not opened !!")
            i_ret = COM_DEF.i_RET_SYSTEM_ERROR

        return i_ret

    ##
    # @brief Serial close.
    # @param None
    # @retval None
    def detach(self):

        self.comport.close()
