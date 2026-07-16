import socket
import sys
import time
import serial
import re
import wmi

BAUD_RATE = 115200            # Must match the transmitter speed
UDP_IP = "127.0.0.1"          # Remote target IP address
UDP_PORT = 5000              # Remote target UDP port

def get_all_esp32_com_ports():
    c = wmi.WMI()
    espCOM = []
    for device in c.Win32_PnPEntity():
        if device.DeviceID.startswith("USB\\VID_303A&PID_1001"):
            friendly_name = device.Caption
            if friendly_name:
                match = re.search(r"COM\d+", friendly_name)
                if match:
                    espCOM.append(match.group(0))
    
    return espCOM

def get_com_port(instance_id: str):
    # Connect to the local Windows Management Instrumentation service
    c = wmi.WMI()
    # Query for the specific Plug and Play device using its Device ID
    # DeviceID=instance_id
    for device in c.Win32_PnPEntity():
        if device.DeviceID == instance_id:
            friendly_name = device.Caption
            if friendly_name:
                match = re.search(r"COM\d+", friendly_name)
                if match:
                    return match.group(0)
    
    return None

def start(com_port: str):
    # 1. Initialize the UDP Socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            destination = (UDP_IP, UDP_PORT)
            while True:
                try:
                    with serial.Serial(port=com_port, baudrate=BAUD_RATE, timeout=0.1) as ser:
                        print(f"Connected! Streaming {com_port} to udp://{UDP_IP}:{UDP_PORT}...")
                        while True:
                            # Read until a newline character is encountered
                            if ser.in_waiting > 0:
                                data_line = ser.readline()
                                
                                # Relay raw bytes to minimize transformation overhead
                                if data_line:
                                    udp_socket.sendto(data_line, destination)
                                    print(f"Forwarded: {data_line.decode('utf-8').strip()}")
                except serial.SerialException as e:
                    print(f"Failed to open serial port: {e}")
                    time.sleep(2)
                finally:
                    print(f"Closing {ser.port}...")
                    ser.close()
    except socket.error as msg:
        print(f"Failed to create socket: {msg}")
        sys.exit()
    except KeyboardInterrupt:
        print("Exiting script cleanly...")
        sys.exit()
    finally:
        print(f"Closing UDP server on port {UDP_PORT}...")
        udp_socket.close()

    
