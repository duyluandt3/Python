#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief COM_SOCKET class definition.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-

import socket
import re
import threading
import binascii
from Debug import Debug_GetObj
from CLS_Define import COM_DEF


##
# @brief Define socket related processing
class COM_SOCKET():

    ##
    # @brief Run when instantiating the COM_SOCKET class.
    # @param i_port    port number
    # @param i_bufsize    buffer size
    # @param i_module_type    module number \n
    #                           - COM_DEF.i_MODULE_MC(0) : MC \n
    #                           - COM_DEF.i_MODULE_DUT(1) : DUT \n
    #                           - COM_DEF.i_MODULE_AP(2) : AP \n
    #                           - COM_DEF.i_MODULE_AIRCAP(3) : AIRCAP \n
    #                           - COM_DEF.i_MODULE_NETWORKTOOL(4) : NETWORKTOOL
    # @retval None
    def __init__(self, i_port, i_bufsize, i_module_type):

        # @cond
        self.Dbg = Debug_GetObj(i_module_type)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.o_conn = None
        self.o_address = None
        self.i_bufsize = i_bufsize
        self.SOCKET_SND_LOCK = threading.Semaphore()
        self.SOCKET_RCV_LOCK = threading.Semaphore()
        # @endcond

    ##
    # @brief Socket bind.
    # @param s_host    host address
    # @param i_port    port number
    # @retval None
    def bind(self, s_host, i_port):

        # @cond
        self.sock.bind((s_host, i_port))
        # @endcond

    ##
    # @brief Socket listen.
    # @param i_backlog    maximum queue length
    # @retval None
    def listen(self, i_backlog):

        # @cond
        self.i_backlog = i_backlog
        self.sock.listen(i_backlog)
        # @endcond

    ##
    # @brief Accept of socket.
    # @param None
    # @retval None
    def accept(self):

        # @cond
        self.o_conn, self.o_address = self.sock.accept()
        # @endcond

    ##
    # @brief Socket connection.
    # @param s_host   host address
    # @param i_port   port number
    # @retval None
    def connect(self, s_host, i_port):

        # @cond
        self.sock.connect((s_host, i_port))
        # @endcond

    ##
    # @brief Read the received data of the socket.
    # @param None
    # @retval s_recv    received data
    def read(self):

        if None is self.o_conn:
            recv_binary = self.sock.recv(self.i_bufsize)
        else:
            recv_binary = self.o_conn.recv(self.i_bufsize)

        s_recv = binascii.hexlify(recv_binary).decode()

        if 0 < len(s_recv):

            if "}{" in s_recv:
                s_recv = re.sub("}{", ',', s_recv)
            else:
                pass

        # Receive FIN from MC
        elif not recv_binary:
            self.Dbg.log(COM_DEF.DEBUG,
                         "FIN Receive !!! ")
            if self.o_conn:
                self.o_conn.close()

            self.sock.close()
        else:
            pass

        self.SOCKET_RCV_LOCK.release()

        return s_recv

    ##
    # @brief Write data to the socket.
    # @param send_str    command data
    # @retval i_ret    value of the result \n
    #                      - Success : COM_DEF.i_RET_SUCCESS \n
    #                      - Failure : COM_DEF.i_RET_SYSTEM_ERROR
    def write(self, send_str):

        self.SOCKET_SND_LOCK.acquire()

        send_binary = binascii.unhexlify(send_str)

        i_ret = COM_DEF.i_RET_SUCCESS

        try:
            if None is self.o_conn:
                self.sock.send(send_binary)
            else:
                self.o_conn.send(send_binary)

        except socket.error as e:
            self.Dbg.log(COM_DEF.ERROR,
                         "socket.error : " + str(e))
            i_ret = COM_DEF.i_RET_SYSTEM_ERROR

        self.SOCKET_SND_LOCK.release()

        return i_ret

    ##
    # @brief Socket close.
    # @param None
    # @retval None
    def close(self):

        if self.o_conn:
            self.o_conn.shutdown(socket.SHUT_RDWR)
            self.o_conn.close()

        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except socket.error as e:
            self.Dbg.log(COM_DEF.ERROR,
                         "close error : " + str(e))
