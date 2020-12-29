# @cond
#
# Copyright (C) 2017 Murata Manufacturing Co.,Ltd.
#

##
# @brief Common Define Class.
# @author E2N3
# @date 2018.11.09

# -*- coding: utf-8 -*-


##
# @brief This class include definition value
class DEF():

    def __init__(self):

        # -------------------------------------------------------------
        #  module type value
        # -------------------------------------------------------------
        self.i_MODULE_MC = 0
        self.i_MODULE_DUT = 1
        self.i_MODULE_AP = 2
        self.i_MODULE_AIRCAP = 3
        self.i_MODULE_NETWORKTOOL = 4
        self.i_MODULE_LOGCTRL = 5

        # -------------------------------------------------------------
        #  top folder path
        # -------------------------------------------------------------
        self.s_TOPDIR = "/home/murata/autoEva/prototype"

        # -------------------------------------------------------------
        #  log folder path
        # -------------------------------------------------------------
        self.s_LOG_FOLDER = self.s_TOPDIR + "/LOG/"

        # -------------------------------------------------------------
        #  log size & roatation count
        # -------------------------------------------------------------
        self.i_LOGSIZE = 0x100000
        self.i_BACKUPCOUNT = 256

        # -------------------------------------------------------------
        #  external return value
        # -------------------------------------------------------------
        self.i_RET_SUCCESS = 0
        self.i_RET_COMHDR_ABNORMAL = -1
        self.i_RET_COMHDR_UNSUPPORTED = -2
        self.i_RET_TLV_ABNORMAL = -3
        self.i_RET_NO_READY = -4
        self.i_RET_WLAN_ERROR = -5
        self.i_RET_SUP_ERROR = -6
        self.i_RET_NETSTACK_ERROR = -7
        self.i_RET_SYSTEM_ERROR = -8
        self.i_RET_BUSY = -9
        self.i_RET_ABNORMAL_TIMEOUT = -10
        self.i_RET_CMD_TIMEOUT = -11

        # -----------------------------
        # MC internal result value
        # -----------------------------
        self.i_RET_COMHDR_STARTBIT = -11
        self.i_RET_COMHDR_CKSUM = -12
        self.i_RET_COMHDR_LENGTH = -13
        self.i_RET_WAIT_NEXT_CMD = -14
        self.i_RET_TEST_CONTINUE = -15
        self.i_RET_NODE_CHK_ERROR = -21
        self.i_RET_TIME_SYNC_ERROR = -22

        # -----------------------------
        #  debug level
        # -----------------------------
        self.DEBUG = 10
        self.INFO = 20
        self.WARNING = 30
        self.ERROR = 40
        self.CRITICAL = 50
        self.TRACE = self.DEBUG - 1

        # ----------------------------
        # The number of retry
        # ----------------------------
        self.i_MAX_TEST_RETRY = 3

        # Interface parameter
        # ----------------------------
        self.s_LOCAL_HOST = "localhost"    # For interface thread

        # -------------------------------------------------------------
        #  Common header
        # -------------------------------------------------------------
        self.i_COMHDR_LENGTH = 16

        '''
        DST ID
        '''
        self.i_DSTID_MASK = 0xf0
        self.i_NODEID_MASK = 0xff00
        self.i_INSTANCEID_MASK = 0x00ff

        '''
        Action parameter
        (Set/Get)
        '''
        self.i_ACTION_GET = 0
        self.i_ACTION_SET = 1
        self.i_ACTION_LOWERMASK = 0xf0

        '''
        Action parameter
        (Type)
        '''
        self.i_ACTION_REQ = 0x1
        self.i_ACTION_ACK = 0x2
        self.i_ACTION_RSP = 0x3
        self.i_ACTION_UPPERMASK = 0x0f

        # -------------------------------------------------------------
        # Encode / Decode
        # -------------------------------------------------------------
        self.i_DECODE_FLG = 0x0
        self.i_ENCODE_FLG = 0x1

        # -------------------------------------------------------------
        # Node ID
        # -------------------------------------------------------------
        self.i_NODE_MC = 1
        self.i_NODE_DUT_START = 10
        self.i_NODE_DUT_END = 59
        self.i_NODE_AP_START = 60
        self.i_NODE_AP_END = 109
        self.i_NODE_AIRCAP_START = 110
        self.i_NODE_AIRCAP_END = 129
        self.i_NODE_NETWORKTOOL_START = 130
        self.i_NODE_NETWORKTOOL_END = 149
        self.i_NODE_MEASURING_START = 150
        self.i_NODE_MEASURING_END = 169

        # -------------------------------------------------------------
        # Command number
        # -------------------------------------------------------------
        self.i_CMD_ResetDUT = 0x0001
        self.i_CMD_SetCurrentTime = 0x0003
        self.i_CMD_InitWLAN = 0x0004
        self.i_CMD_Attach = 0x0004
        self.i_CMD_TerminateWLAN = 0x0006
        self.i_CMD_Detach = 0x0006
        self.i_CMD_SetCountryCode = 0x0007
        self.i_CMD_GetCountryCode = 0x0007
        self.i_CMD_GetRssi = 0x0008
        self.i_CMD_GetMacAddr = 0x0009
        self.i_CMD_SetIpInfo = 0x000a
        self.i_CMD_GetIpInfo = 0x000a
        self.i_CMD_StartPing = 0x000b
        self.i_CMD_StartIperf = 0x000c
        self.i_CMD_FinishIperfServerProcess = 0x000d
        self.i_CMD_SetDhcpIpInfo = 0x000e
        self.i_CMD_StartDhcpd = 0x000f
        self.i_CMD_SetChannel = 0x0010
        self.i_CMD_GetChannel = 0x0010
        self.i_CMD_GetChanlist = 0x0011
        self.i_CMD_GetRate = 0x0012
        self.i_CMD_SetBwcap = 0x0013
        self.i_CMD_GetBwcap = 0x0013
        self.i_CMD_GetVersion = 0x0014
        self.i_CMD_GetPacketCount = 0x0015
        self.i_CMD_SetBand = 0x0016
        self.i_CMD_GetBand = 0x0016
        self.i_CMD_SetFrameburst = 0x0017
        self.i_CMD_GetFrameburst = 0x0017
        self.i_CMD_SetMpc = 0x0018
        self.i_CMD_GetMpc = 0x0018
        self.i_CMD_SetSpect = 0x0019
        self.i_CMD_GetSpect = 0x0019
        self.i_CMD_GetChaninfo = 0x001a
        self.i_CMD_Set11ac = 0x001b
        self.i_CMD_Get11ac = 0x001b
        self.i_CMD_Set11n = 0x001c
        self.i_CMD_Get11n = 0x001c
        self.i_CMD_Scan = 0x0020
        self.i_CMD_GetScanList = 0x0020
        self.i_CMD_ConnectAp = 0x0021
        self.i_CMD_GetApInfo = 0x0021
        self.i_CMD_DisconnectAp = 0x0022
        self.i_CMD_SetPowersaveMode = 0x0023
        self.i_CMD_GetPowersaveMode = 0x0023
        self.i_CMD_SetSsid = 0x0040
        self.i_CMD_SetSecurity = 0x0041
        self.i_CMD_SetStealthMode = 0x0045
        self.i_CMD_SetRadioOutput = 0x0046
        self.i_CMD_GetStaList = 0x0047
        self.i_CMD_SetConnectionLimit = 0x0048
        self.i_CMD_SetDeauth = 0x0049
        self.i_CMD_StartAirCapture = 0x0060
        self.i_CMD_StopAirCapture = 0x0061
        self.i_CMD_DecryptAirLog = 0x0062
        self.i_CMD_CheckAirLog = 0x0063
        self.i_CMD_GetAirLog = 0x0064
        self.i_CMD_CheckMsgNum = 0x0065
        self.i_CMD_NotifyCaptureLog = 0x0070
        self.i_CMD_NotifyEvent = 0x0072
        self.i_CMD_ResetAtt = 0x0090
        self.i_CMD_AttControl = 0x0091
        self.i_CMD_TestReady = 0x0099

        # -------------------------------------------------------------
        # TLV parameter
        # -------------------------------------------------------------
        self.i_TLV_Type_Length = 2
        self.i_TLV_Len_Length = 2

        # -------------------------------------------------------------
        # Type Number
        # -------------------------------------------------------------
        self.i_TYPE_DataList = 0x0000
        self.i_TYPE_Result = 0x0001
        self.i_TYPE_OnOffFlg = 0x0002
        # length range of i_TYPE_OnOffFlg
        self.i_Disabled = 0x0
        self.i_Enabled = 0x1
        self.i_TYPE_Date = 0x0003
        self.i_TYPE_Time = 0x0004
        self.i_TYPE_Role = 0x0005
        self.i_TYPE_User = 0x0006
        self.i_TYPE_Password = 0x0007
        self.i_TYPE_OffsetTime = 0x0008
        self.i_TYPE_LogData = 0x0009
        self.i_TYPE_Ssid = 0x000a
        # length range of self.i_TYPE_Ssid
        self.i_Ssid_Length_Min = 1
        self.i_Ssid_Length_Max = 32

        self.i_TYPE_Bssid = 0x000b
        self.i_TYPE_WepKey = 0x000c
        # length range of i_TYPE_WepKey
        self.i_WepKey_Hex64_Length = 10
        self.i_WepKey_Hex128_Length = 26
        self.i_WepKey_Ascii64_Length = 5
        self.i_WepKey_Ascii128_Length = 13

        self.i_TYPE_WpaPassphrase = 0x000d
        # length range of i_TYPE_WpaPassphrase
        self.i_WpaPassphrase_Length_Min = 8
        self.i_WpaPassphrase_Length_Max = 64
        self.i_TYPE_KeyLength = 0x000e
        self.i_TYPE_Channel = 0x000f

        self.i_TYPE_Bandwidth = 0x0010
        # value of i_TYPE_Bandwidth
        self.i_Bandwidth_20MHz = 0x0
        self.i_Bandwidth_40MHz = 0x1
        self.i_Bandwidth_80MHz = 0x2
        self.i_Bandwidth_80_80MHz = 0x3
        self.i_Bandwidth_160MHz = 0x4
        self.i_Bandwidth_RangeErr = 0x5

        self.i_TYPE_Sideband = 0x0011
        # value of i_TYPE_Sideband
        self.i_Sideband_upper = 0x1
        self.i_Sideband_lower = 0x2

        self.i_TYPE_SrcId = 0x0012
        self.i_TYPE_DstId = 0x0013
        self.i_TYPE_LogName = 0x0014
        self.i_TYPE_LogType = 0x0015
        self.i_TYPE_LogLevel = 0x0016
        self.i_TYPE_NumOfIf = 0x0017
        self.i_TYPE_IfType = 0x0018

        self.i_TYPE_Band = 0x0019
        # value of i_TYPE_BandType
        self.i_BandType_AUTO = 0
        self.i_BandType_24GHz = 1
        self.i_BandType_5GHz = 2
        self.i_BandType_BOTH = 3

        self.i_TYPE_CountryCode = 0x1001
        self.i_TYPE_RevisionCode = 0x1002
        self.i_TYPE_Rssi = 0x1003

        self.i_TYPE_AuthFlg = 0x1004
        # value of i_TYPE_AuthFlg
        self.i_AuthFlg_Open = 0x0
        self.i_AuthFlg_Shared = 0x1
        self.i_AuthFlg_RangeErr = 0x2

        self.i_TYPE_KeyIdx = 0x1005
        # value of i_TYPE_keyIdx
        self.i_KeyIdx_MIN = 0
        self.i_KeyIdx_MAX = 3

        self.i_TYPE_KeyMgmt = 0x1006
        # value of i_TYPE_KeyMgmt
        self.i_KeyMgmt_PSK = 0x0
        self.i_KeyMgmt_EAP = 0x1
        self.i_KeyMgmt_SAE = 0x2
        self.i_KeyMgmt_PSK_SAE_MIX = 0x3
        self.i_KeyMgmt_RangeErr = 0x4

        self.i_TYPE_WpaType = 0x1007
        # value of i_TYPE_WpaType
        self.i_WpaType_WPA = 0x0
        self.i_WpaType_RSN = 0x1
        self.i_WpaType_MIX = 0x2
        self.i_WpaType_RangeErr = 0x3

        self.i_TYPE_WpaPairwise = 0x1008
        # value of i_TYPE_WpaPairwise
        self.i_WpaPairwise_TKIP = 0x0
        self.i_WpaPairwise_CCMP = 0x1
        self.i_WpaPairwise_MIX = 0x2
        self.i_WpaPairwise_RangeErr = 0x3

        self.i_TYPE_Pmf = 0x1009
        # value of i_TYPE_Pmf
        self.i_Pmf_Disabled = 0
        self.i_Pmf_Enabled = 1
        self.i_PmfSettings = 0x100a
        # value of i_TYPE_PmfSettings
        self.i_PmfSettings_Disable = 0x0
        self.i_PmfSettings_Enable = 0x1
        self.i_PmfSettings_Required = 0x2
        self.i_PmfSettings_RangeErr = 0x3

        self.i_TYPE_PowerSaveMode = 0x100b
        self.i_TYPE_Rate = 0x100c
        self.i_TYPE_Rxdfrmucast = 0x100d
        self.i_TYPE_Rxdfrmocast = 0x100e
        self.i_TYPE_Rxdfrmmcast = 0x100f
        self.i_TYPE_ReasonCode = 0x1010
        self.i_TYPE_SpectType = 0x1011

        self.i_TYPE_ScanType = 0x2001
        self.i_TYPE_NumOfAP = 0x2002

        self.i_TYPE_SecurityType = 0x2003
        # value of i_TYPE_SecurityType
        self.i_SecurityType_Open = 0x00
        self.i_SecurityType_Wep = 0x01
        self.i_SecurityType_Wpa = 0x02

        self.i_TYPE_SecurityString = 0x2004
        self.i_TYPE_NumOfChannel = 0x2005
        self.i_TYPE_EventNum = 0x2006
        self.i_TYPE_Pktengrxducast = 0x2007
        self.i_TYPE_Pktengrxdmcast = 0x2008
        self.i_TYPE_ChannelStatus = 0x2009
        self.i_TYPE_ChannelMinutes = 0x200a
        self.i_TYPE_IeFlg = 0x200b
        self.i_TYPE_VersionType = 0x200c
        self.i_TYPE_VersionString = 0x200d
        self.i_TYPE_ApiTest = 0x200e
        self.i_TYPE_ScanResultNum = 0x200f

        self.i_TYPE_MaxAssoc = 0x3001
        self.i_TYPE_NumOfSta = 0x3002
        self.i_TYPE_WlanId = 0x3003
        self.i_TYPE_Location = 0x3004
        self.i_TYPE_ProfileName = 0x3005

        self.i_TYPE_IpAddress = 0x4001
        self.i_TYPE_NetMask = 0x4002
        self.i_TYPE_GateWay = 0x4003
        self.i_TYPE_Interval = 0x4004
        self.i_TYPE_TotalTime = 0x4005
        self.i_TYPE_PacketNum = 0x4006
        self.i_TYPE_PacketSize = 0x4007

        self.i_TYPE_IperfModeType = 0x4008
        # value of i_TYPE_IperfModeType
        self.i_IperfModeType_Server = 0x1
        self.i_IperfModeType_Client = 0x2

        self.i_TYPE_IperfCmdString = 0x4009
        self.i_TYPE_AssignNum = 0x400a
        self.i_TYPE_LeaseTime = 0x400b

        self.i_TYPE_CaptureFileName = 0x5001
        self.i_TYPE_ControlFreq = 0x5002  	# Reserved
        self.i_TYPE_CenterFreq = 0x5003		# Reserved

        self.i_TYPE_AnalyzeMsg = 0x5004
        # value of i_TYPE_AnalyzeMsg
        self.i_AnalyzeMsg_AssocReq = 0x1
        self.i_AnalyzeMsg_AssocRsp = 0x2
        self.i_AnalyzeMsg_ReAssocReq = 0x3
        self.i_AnalyzeMsg_ReAssocRsp = 0x4
        self.i_AnalyzeMsg_ProbeReq = 0x5
        self.i_AnalyzeMsg_ProbeRsp = 0x6
        self.i_AnalyzeMsg_Disconnect = 0x7
        self.i_AnalyzeMsg_Auth = 0x8
        self.i_AnalyzeMsg_Deauth = 0x9
        self.i_AnalyzeMsg_Qos = 0xa
        self.i_AnalyzeMsg_1_4way = 0xb
        self.i_AnalyzeMsg_2_4way = 0xc
        self.i_AnalyzeMsg_3_4way = 0xd
        self.i_AnalyzeMsg_4_4way = 0xe
        self.i_AnalyzeMsg_Beacon = 0xf
        self.i_AnalyzeMsg_WPS_all = 0x10
        self.i_AnalyzeMsg_Req_Identify = 0x11
        self.i_AnalyzeMsg_Rsp_Identify = 0x12
        self.i_AnalyzeMsg_WSC_Start = 0x13
        self.i_AnalyzeMsg_WPS_M1 = 0x14
        self.i_AnalyzeMsg_WPS_M2 = 0x15
        self.i_AnalyzeMsg_WPS_M3 = 0x16
        self.i_AnalyzeMsg_WPS_M4 = 0x17
        self.i_AnalyzeMsg_WPS_M5 = 0x18
        self.i_AnalyzeMsg_WPS_M6 = 0x19
        self.i_AnalyzeMsg_WPS_M7 = 0x1a
        self.i_AnalyzeMsg_WPS_M8 = 0x1b
        self.i_AnalyzeMsg_WPS_WSC_DONE = 0x1c
        self.i_AnalyzeMsg_WPS_failure = 0x1d
        self.i_AnalyzeMsg_WPS_M2D = 0x1e
        self.i_AnalyzeMsg_WPS_WSC_ACK = 0x1f
        self.i_AnalyzeMsg_WPS_WSC_NACK = 0x20
        #  0x21 - 0xdf  Reserved
        self.i_AnalyzeMsg_DHCP_all = 0xe0
        self.i_AnalyzeMsg_DHCP_Discover = 0xe1
        self.i_AnalyzeMsg_DHCP_Offer = 0xe2
        self.i_AnalyzeMsg_DHCP_Request = 0xe3
        self.i_AnalyzeMsg_DHCP_Ack = 0xe4

        self.i_TYPE_CaptureStartTime = 0x5005  # Reserved
        self.i_TYPE_CaptureEndTime = 0x5006		# Reserved
        self.i_TYPE_NumOfMsg = 0x5007
        self.i_TYPE_TimeList = 0x5008
        self.i_TYPE_RadioTapList = 0x5009
        self.i_TYPE_IeList = 0x500a
        self.i_TYPE_DestAddr = 0x500b
        self.i_TYPE_TransAddr = 0x500c
        self.i_TYPE_SourceAddr = 0x500d
        self.i_TYPE_NumOfLink = 0x500e
        self.i_TYPE_AircapIfId = 0x500f
        # value of i_TYPE_AircapIfId
        self.i_IfId_Aircap1 = 0x0
        self.i_IfId_Aircap2 = 0x1
        self.i_IfId_Aircap3 = 0x2
        self.i_IfId_Aircap4 = 0x3

        self.i_TYPE_TriggerMsg = 0x5010
        self.i_TYPE_Direction = 0x5011
        # value of i_TYPE_Direction
        self.i_Direction_Fwd = 0x0
        self.i_Direction_Back = 0x1
        self.i_Direction_Both = 0x2

        self.i_TYPE_ReferenceData = 0x5012
        self.i_TYPE_NumOfPkt = 0x5013
        self.i_TYPE_ChkResult = 0x5014
        # value of i_TYPE_ChkResult
        self.i_PktChkOk = 0x0
        self.i_PktChkNg = 0x1

        self.i_TYPE_NgReason = 0x5015
        # value of i_TYPE_NgReason
        self.i_NoMsg = 0x0
        self.i_IeNotMatch = 0x1
        self.i_NoIe = 0x2
        self.i_NoCapfile = 0x3
        self.i_NoReffile = 0x4
        self.i_OtherErr = 0xff

        self.i_TYPE_NgIeName = 0x5016
        self.i_TYPE_NgIeValueLen = 0x5017
        self.i_TYPE_NgIeValue = 0x5018
        self.i_TYPE_NumOfNg = 0x5019


COM_DEF = DEF()

# @endcond
