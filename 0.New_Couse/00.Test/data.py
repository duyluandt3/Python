import os
import time
import json
from data import GET_DATA

class AIRCAP_FUNC(GET_DATA):
    ##
    #  @brief Run when instantiating the AIRCAP_FUNC class.
    #  @param self      instance of AIRCAP_FUNC class
    #  @param cls_soc   socket used for sending response command to MC
    #  @param s_host     MC IP Address
    def __init__(self, cls_soc, s_host):
        # read environment file
        try:
            env_file = "./env.json"
            fr = open(str(env_file), 'r')
            d_aircap_data = json.load(fr)
            fr.close()
        except Exception as err_info:
            print(err_info)

        # @cond
        # Get debug info
        self.cap_file_path = d_aircap_data["CaptureFilePath"]
        self.filename_extension = d_aircap_data["FilenameExtension"]
        self.file_size_max = d_aircap_data["FileSizeMax"]
        self.ref_data_path = d_aircap_data["RefDataPath"]
        self.ref_file_extension = d_aircap_data["RefFileExtension"]
        self.d_cp_info = {}
        if "CpHost" in d_aircap_data:
            self.d_cp_info["host"] = d_aircap_data["CpHost"]
        else:
            self.d_cp_info["host"] = s_host
        self.d_cp_info["id"] = d_aircap_data["CpID"]
        self.d_cp_info["passwd"] = d_aircap_data["CpPWD"]
        self.d_cp_info["path"] = d_aircap_data["CpRefDtPath"]
        self.d_cp_info["LogPath"] = d_aircap_data["CpLogPath"]

        self.wlan_ifname = d_aircap_data["WlanIf"]
        self.eth_ifname = d_aircap_data["EthIf"]

    def print_data(self):
        print(self.cap_file_path)


data = AIRCAP_FUNC("","")
data.print_data()
