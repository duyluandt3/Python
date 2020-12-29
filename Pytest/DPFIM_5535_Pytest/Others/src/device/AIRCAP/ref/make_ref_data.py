#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief This is sub-function to check the packet capture log
# @author E2N3
# @date 2018.11.13

# -*- coding: utf-8 -*-

import csv
import json
from collections import OrderedDict
from collections import defaultdict

##
#  @brief convert the file to "json" from "CSV"
#  @param s_file_path    the directory path of the "CSV" file
#  @param s_file_name    the file name of "CSV" file
#  @retval d_ref_data    the reference data of the "json" format
def csv2json(s_file_path, s_file_name):
    d_ref_data = OrderedDict()
    d_tmp_dict = defaultdict(list)
    l_tmp_key_lst = []
    l_key_lst = []
    s_csv_file = s_file_path + s_file_name + ".csv"
    s_json_file = s_file_path + s_file_name + ".json"

    with open(s_csv_file, "r") as fr_csv:
        reader = csv.reader(fr_csv)
        header = next(reader)

        # read 1 line from csv
        for row in reader:
            s_raw_line = (row[1]).replace(" ", "").replace(
                "\":\"", ": ").replace("\"", "").split(": ")
            print(s_raw_line)

            if 1 < len(s_raw_line):
                l_key = [
                    item for item in s_raw_line if s_raw_line.index(item) == 0]
                l_val = [
                    item for item in s_raw_line if s_raw_line.index(item) == 1]

                if l_key[0] == "frame.time_epoch":
                    pass
                else:
                    l_tmp_key_lst.extend(l_key)

                d_tmp_dict[l_key[0]].append(l_val[0])
            else:
                pass

    # remove duplicate key from key list
    l_key_lst = sorted(set(l_tmp_key_lst), key=l_tmp_key_lst.index)

    for key in l_key_lst:
        if len(d_tmp_dict[key]) > 1:
            d_ref_data[key] = ','.join(d_tmp_dict[key])
        elif len(d_tmp_dict[key]) == 1:
            d_ref_data[key] = d_tmp_dict[key][0]
        else:
            pass

    # create json file for reference data from dict data
    try:
        with open(s_json_file, "w") as fw_json:
            # print(json.dumps(d_ref_data, indent=4)) # for debug
            json.dump(d_ref_data, fw_json, indent=4)
    except Exception as err_info:
        print(err_info)

    return


if __name__ == "__main__":

    s_file_path = "./"
    s_file_name = ""

    print('Input pcap file name ')
    s_file_name = input('>>>  ')
    print('file name is ' + s_file_name)

    csv2json(s_file_path, s_file_name)
    print("End.")
