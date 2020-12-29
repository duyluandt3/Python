
class TEST_INFO():
    '''
    I/F thread parameter is managed by this table.
    '''
    def __init__(self, d_deviceInfo):
        self.d_test_info = {}

        # Initialization
        for s_ifname in list(d_deviceInfo):
            self.d_test_info[s_ifname] = {}
            self.d_test_info[s_ifname]["Ssid"] = ""
            self.d_test_info[s_ifname]["Channel"] = 0
            self.d_test_info[s_ifname]["Bandwidth"] = 0
            self.d_test_info[s_ifname]["PeerDeviceKey"] = ""
            # Security
            self.d_test_info[s_ifname]["SecurityType"] = 0
            self.d_test_info[s_ifname]["AuthFlg"] = 0
            self.d_test_info[s_ifname]["KeyIdx"] = 0
            self.d_test_info[s_ifname]["WepKey"] = 0
            self.d_test_info[s_ifname]["Pmf"] = 0
            self.d_test_info[s_ifname]["PmfSettings"] = 0
            self.d_test_info[s_ifname]["KyeMgmt"] = 0
            self.d_test_info[s_ifname]["WpaType"] = 0
            self.d_test_info[s_ifname]["WpaPairwise"] = 0
            self.d_test_info[s_ifname]["WpaPassphrase"] = ""
            self.d_test_info[s_ifname]["KeyLength"] = 0
            # WPS
            self.d_test_info[s_ifname]["device_name"] = ""
            self.d_test_info[s_ifname]["manufacturer"] = ""
            self.d_test_info[s_ifname]["model_name"] = ""
            self.d_test_info[s_ifname]["model_number"] = ""
            self.d_test_info[s_ifname]["serial_number"] = ""
            self.d_test_info[s_ifname]["device_type"] = ""
            self.d_test_info[s_ifname]["os_version"] = ""
            self.d_test_info[s_ifname]["config_methods"] = ""
            # P2P
            self.d_test_info[s_ifname]["P2pDevAddr"] = ""
            self.d_test_info[s_ifname]["P2pListenChannel"] = ""
            self.d_test_info[s_ifname]["P2pOperChannel"] = ""
            self.d_test_info[s_ifname]["PinNumber"] = ""


    def Set_TestInfo(self, s_ifname, s_command, d_testParam):
        if "SetOpenSecurity" == s_command:
            self.d_test_info[s_ifname]["SecurityType"] = 0
        elif "SetWepSecurity" == s_command:
            self.d_test_info[s_ifname]["SecurityType"] = 1
        elif "SetWpaSecurity" == s_command:
            self.d_test_info[s_ifname]["SecurityType"] = 2
        else:
            pass

        if "SetSsid" == s_command or \
            "SetOpenSecurity" == s_command or \
            "SetWepSecurity" == s_command or \
            "SetWpaSecurity" == s_command or \
            "SetChannel" == s_command or \
            "SetIpInfo" == s_command:
            if d_testParam:
                for s_key_param in list(d_testParam):
                    self.d_test_info[s_ifname][s_key_param] = d_testParam[s_key_param]
                else:
                    pass
            else:
                pass
        else:
            pass

    def Get_TestInfo(self, s_ifname, s_key_param):
        return self.d_test_info[s_ifname][s_key_param]
