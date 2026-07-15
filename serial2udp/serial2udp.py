import socket
import sys
import serial

# --- CONFIGURATION ---
SERIAL_PORT = "/dev/ttyUSB0"  # Change to "COM3" on Windows
BAUD_RATE = 115200            # Must match the transmitter speed
UDP_IP = "127.0.0.1"          # Remote target IP address
UDP_PORT = 10000              # Remote target UDP port

def main():
    # 1. Initialize the UDP Socket
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination = (UDP_IP, UDP_PORT)
    except socket.error as msg:
        print(f"Failed to create socket: {msg}")
        sys.exit()

    # 2. Initialize the Serial Port Connection
    try:
        ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=0.1)
        print(f"Streaming {SERIAL_PORT} to udp://{UDP_IP}:{UDP_PORT}...")
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
        sys.exit()

    # 3. Forward loop
    try:
        while True:
            # Read until a newline character is encountered
            if ser.in_waiting > 0:
                data_line = ser.readline()
                
                # Relay raw bytes to minimize transformation overhead
                if data_line:
                    udp_socket.sendto(data_line, destination)
                    print(f"Forwarded: {data_line.strip()}")
                    
    except KeyboardInterrupt:
        print("\nExiting script cleanly...")
    finally:
        ser.close()
        udp_socket.close()

if __name__ == "__main__":
    main()
