# -*- coding: utf-8 -*-
from typing import Any, List
from serial2udp import server

espA = "USB\\VID_303A&PID_1001&MI_00\\6&21011EDD&0&0000"
espB = "USB\\VID_303A&PID_1001&MI_00\\6&328677DC&0&0000"

def main():
    print(f"Detected Port: {server.get_all_esp32_com_ports()}")
    print(f"Detected Port espA: {server.get_com_port(espA)}")
    print(f"Detected Port espB: {server.get_com_port(espB)}")
    server.start(server.get_com_port(espA))

if __name__ == "__main__":
  main()
