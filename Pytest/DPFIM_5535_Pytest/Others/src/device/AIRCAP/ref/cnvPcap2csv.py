#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This is sub-function to check the packet capture log
# @author E2N3
# @date 2018.11.13

# -*- coding: utf-8 -*-

import shlex
import subprocess

##
#  @brief convert the file to "json" from "CSV"
#  @param s_file_path    the directory path of the "pcap" file
#  @param s_file_name    the file name of "pcap" file
#  @param s_frame_num    the frame number in pcap file
#  @retval s_csv_file    the reference data of the "csv" format
def pcap2csv(s_file_path, s_file_name, s_frame_num):

    s_cap_file = s_file_path + s_file_name + ".pcap"
    s_csv_file = s_file_path + s_file_name + ".csv"
    s_cmd_str = ["tshark", "-r", s_cap_file, "-T", "json"]
    s_filter_str = "\'-Y frame.number == " + s_frame_num + "\'"
    s_cmd_str.extend(shlex.split(s_filter_str))
    # print(s_cmd_str)  # for debug

    try:
        # decode command response data from "byte" data to "str" data
        s_json_data = subprocess.check_output(
            s_cmd_str).decode('utf-8')
        s_json_data = s_json_data.replace("  {", "[\n  {")
        s_json_data = s_json_data.replace("  }\n\n", "  }\n]")
        s_json_data = s_json_data.replace("  }\r\n\r\n", "  }\n]")
        s_json_data = s_json_data.replace("  ,", ",")
        s_json_data = s_json_data.replace("]]", "]\n]")
        # print(s_json_data)  # for debug
    except Exception as err_info:
        print(err_info)
        return

    lines = s_json_data.split('\n')
    try:
        with open(s_csv_file, 'w', newline='', encoding='UTF-8',
                  errors='ignore') as fw_csv:
            # read line one by one
            for line in lines:
                # print(line)  # for debug
                row = "{},{}\n".format("", line)
                fw_csv.write(row)
    except Exception as err_info:
        print(err_info)

    return


if __name__ == "__main__":

    s_file_path = "./"
    s_file_name = "AssocReq-wps"
    s_frame_num = ""

    print('Input pcap file name ')
    s_file_name = input('>>>  ')
    print('file name is ' + s_file_name)

    print('Input frame number in pcap file')
    s_frame_num = input('>>>  ')
    if s_frame_num == "":
        s_frame_num = "1"
    print('frame number is ' + s_frame_num)

    pcap2csv(s_file_path, s_file_name, s_frame_num)
    print("End.")
