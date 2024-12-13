#pyserial code to send data to the arduino
import serial
from time import sleep

def setup_arduino_connection(port, baudrate):
    """
    Set up the connection to the Arduino.
    Args:
        port (str): The port the Arduino is connected to.
        baudrate (int): The baudrate of the connection.
    Returns:
        Serial: The serial connection to the Arduino.
    """
    arduino = serial.Serial(port, baudrate)
    return arduino

def send_message_to_arduino(arduino, message):
    """
    Send a message to the Arduino.
    Args:
        arduino (Serial): The serial connection to the Arduino.
        message (str): The message to send to the Arduino.
    """

    arduino.write(str(message).encode())
    # print((message+"\n").encode())
    print(f"Sent message to Arduino: {message}")

def main():
    # Set up the connection to the Arduino
    port = "/dev/cu.usbmodem1101"  # This is the port the Arduino is connected to
    baudrate = 9600
    arduino = setup_arduino_connection(port, baudrate)
    sleep(5)
    # Send an integer to the Arduino
    t = 5
    send_message_to_arduino(arduino, t)
    
    #wait for the arduino to finish for the specified time
    delay_because_arduino_code_is_slow = 1.5
    sleep(delay_because_arduino_code_is_slow)
    while t > 0:
        print(f"Waiting for {t} seconds...")
        t -= 1
        sleep(1)
    # Close the connection to the Arduino
    arduino.close()
    
    

if __name__ == "__main__":
    main()