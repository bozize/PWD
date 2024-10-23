import network
import espnow
import time
from machine import Pin
import urequests  # Ensure this library is available for HTTP requests

# Setup LED Pins for Traffic Light
red_led = Pin(25, Pin.OUT)
yellow_led = Pin(26, Pin.OUT)
green_led = Pin(27, Pin.OUT)

# Wi-Fi Connection Details
SSID = "ssid" #Wi-Fi SSID
PASSWORD = "password"  #Wi-Fi password

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)  # Set ESP32 to station mode
wlan.active(True)

# Initialize ESPNOW
e = espnow.ESPNow()
e.active(True)

# Replace with the actual MAC address of the OLED display board
oled_board_mac = mac  # pwd's debice  MAC adddress

# Timing configuration (in seconds)
green_light_duration = 5  # Duration for green light
yellow_light_duration = 2  # Duration for yellow light
red_light_duration = 5     # Duration for red light

# State to control traffic light operations
operating_state = True  # True means operating normally, False means stopped

# Function to connect to Wi-Fi
def connect_to_wifi():
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to Wi-Fi, IP Address:", wlan.ifconfig()[0])

# Function to add OLED board as a peer
def add_peer():
    try:
        e.add_peer(oled_board_mac)  # Add the OLED board as a peer
        print("Peer added:", oled_board_mac)
    except Exception as ex:
        print("Failed to add peer:", ex)

def get_traffic_data(mac_address):
    # Prepare the URL using the MAC address in hex format
    url = f"https://39f7-197-232-150-13.ngrok-free.app/api/pwd/{mac_address}"  # Use original MAC with colons
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            response_data = response.json()  # Parse the JSON response
            print("Response from API:", response_data)
            return response_data  # Return the parsed response data
        else:
            print("Error in API call:", response.status_code)
            return None
    except Exception as e:
        print("Exception during API call:", e)
        return None

def broadcast_status(status):
    print("Broadcasting status:", status)
    e.send(oled_board_mac, status)  # Send the status to the OLED display

def traffic_light_sequence():
    global operating_state  # Declare operating_state as global
    while True:
        if operating_state:  # Check if operating normally
            # Green Light (GO)
            green_led.on()
            red_led.off()
            yellow_led.off()
            broadcast_status(b'GO')
            print("Green light ON")
            time.sleep(green_light_duration)

            # Yellow Light (GET READY)
            green_led.off()
            yellow_led.on()
            broadcast_status(b'GET READY')
            print("Yellow light ON")
            time.sleep(yellow_light_duration)

            # Red Light (STOP)
            yellow_led.off()
            red_led.on()
            broadcast_status(b'STOP')
            print("Red light ON")
            time.sleep(red_light_duration)
        else:
            # If in STOP state, keep the red light on
            red_led.on()
            yellow_led.off()
            green_led.off()
            print("Red light ON (STOP state)")
            time.sleep(30)  # Keep red light on for 30 seconds
            operating_state = True  # Return to normal operation

def receive_requests():
    global operating_state  # Allow function to modify the operating state
    while True:
        host, msg = e.recv()
        if msg:  # Check if there's a message
            try:
                received_mac = msg.decode()  # Decode the received message to get the MAC address
                print(f"Received request for MAC Address: {received_mac}")
                
                if received_mac == 'STOP1':  # Check for STOP command
                    print("STOP command received. Setting traffic light to STOP.")
                    operating_state = False  # Set operating state to STOP
                    broadcast_status(b'STOP1')  # Send STOP status to OLED
                    continue  # Skip to the next iteration

                # Call the API and get the traffic data based on the MAC address received
                traffic_data = get_traffic_data(received_mac)
                if traffic_data and traffic_data.get("message") == "yes":  # Check if the message field is "yes"
                    # Prepare the actual traffic data to be sent
                    traffic_info = "Traffic data here"  # Replace this with the actual data you want to send
                    broadcast_status(traffic_info.encode())  # Broadcast traffic data to OLED
                else:
                    print("Access denied. Response not valid.")
            except Exception as e:
                print("Error processing message:", e)

# Main loop
def main():
    connect_to_wifi()  # Connect to Wi-Fi
    print("Starting traffic light sequence...")
    add_peer()  # Add the OLED display as a peer
    # Start a thread or separate function for receiving requests
    from _thread import start_new_thread
    start_new_thread(receive_requests, ())
    
    traffic_light_sequence()  # Start the traffic light sequence

main()
