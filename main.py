import serial

def try_ports():
    ports = ['/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3', '/dev/ttyS4', 
             'COM0', 'COM1', 'COM2', 'COM3', 'COM4']
    for port in ports:
        try:
            ser = serial.Serial(
                port=port,
                baudrate=250000,  # Default baud rate after communication reset
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            print(f"Successfully connected to {port}")
            return ser
        except serial.SerialException as e:
            print(f"Serial error on port {port}: {e}")
        except Exception as e:
            print(f"General error on port {port}: {e}")

    raise Exception("Could not connect to any port")

def send_read_command(ser):
    # Example command to read cell voltages
    command = bytes([0xC0, 0x02, 0x15, 0x0B])  # Initialize byte, register address, data size
    crc = 0xD2B3.to_bytes(2, byteorder='big')  # CRC value
    full_command = command + crc
    ser.write(full_command)

def stream_data():
    ser = try_ports()
    try:
        send_read_command(ser)
        while True:
            response = ser.read(128)  # Adjust as needed for the expected frame size
            if response:
                print(f"Received data: {response.hex()}")
            else:
                print("No data received")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    stream_data()