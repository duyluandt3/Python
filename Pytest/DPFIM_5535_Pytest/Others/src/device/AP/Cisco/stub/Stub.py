import time
import queue
from Com_def import *
QUEUE_STUB = 0

def Stub_Write(s_cmd):
    global QUEUE_STUB

    print("[STUB] Stub_Write : " + s_cmd)

    if "admin" == s_cmd or "a1B2c3" == s_cmd:
        pass
    else:
        QUEUE_STUB.put(s_cmd)
    return i_RET_SUCCESS


def Stub_Readline(s_portno):
    global QUEUE_STUB

    print("[STUB] Stub_Readline")

    s_cmd = QUEUE_STUB.get()

    print("[STUB] read data : " + s_cmd)

    if "show client summary" == s_cmd:
        recv_str = "Number of Clients................................ 2\nNumber of PMIPV6 Clients......................... 0\nGLAN/\nRLAN/\nMAC Address AP Name Slot Status WLAN Auth Protocol Port Wired PMIPV6 Role\n----------------- ----------------- ---- ------------- ----- ---- ---------------- ---- ----- ------- ----------------\n3c:a9:f4:56:01:24 FW30-1702I 1 Associated 1 Yes 802.11n(5 GHz) 1 No No Local\n5c:e0:c5:71:9a:df FW30-1702I 1 Associated 1 Yes 802.11ac(5 GHz) 1 No No Local"
        return recv_str
    elif "y" == s_cmd or "logout" == s_cmd:
        return s_cmd
    else:
        return "\(Cisco Controller\) >"


def Stub_Init():
    global QUEUE_STUB

    print("[STUB] Stub_Init")
    QUEUE_STUB = queue.Queue()
