import network
import espnow
from machine import Pin, SoftI2C
import ssd1306
import time

# Setup I2C for OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Setup RGB LED
red_rgb = Pin(25, Pin.OUT)
green_rgb = Pin(26, Pin.OUT)
blue_rgb = Pin(27, Pin.OUT)

# Setup Button
button = Pin(13, Pin.IN, Pin.PULL_UP)  # Change pin number as needed

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESPNOW
e = espnow.ESPNow()
e.active(True)

# Replace with the actual MAC address of the traffic light controller
traffic_board_mac = mac  # traffic light's device MAC

# Add peer only if it does not already exist
try:
    e.add_peer(traffic_board_mac)
except Exception as ex:
    if "ESP_ERR_ESPNOW_EXIST" in str(ex):
        print("Peer already exists. Proceeding...")
    else:
        print("Failed to add peer:", ex)

def display_status(message):
    oled.fill(0)  # Clear the display
    oled.text("Traffic Status:", 0, 0)
    oled.text(message.decode(), 0, 20)  # Decode bytes to string
    oled.show()  # Update the OLED display

def update_rgb(status):
    if status == b'GO':
        red_rgb.off()
        green_rgb.on()
        blue_rgb.off()
    elif status == b'GET READY':
        red_rgb.on()
        green_rgb.on()
        blue_rgb.off()
    elif status == b'STOP':
        red_rgb.on()
        green_rgb.off()
        blue_rgb.off()

def receive_status():
    while True:
        host, msg = e.recv()
        if msg:
            print("Received:", msg)
            display_status(msg)
            update_rgb(msg)

def check_button():
    # Simple debounce logic
    button_pressed = False
    while True:
        if not button.value() and not button_pressed:  # Button pressed (active LOW)
            button_pressed = True
            print("Button pressed! Sending STOP to traffic board.")
            e.send(traffic_board_mac, b'STOP')  # Send STOP to traffic board
            update_rgb(b'STOP')  # Update RGB LED status
            display_button_feedback()
        elif button.value():  # Button released
            button_pressed = False

def display_button_feedback():
    oled.fill(0)  # Clear the display
    oled.text("STOP sent!", 0, 0)
    oled.show()  # Update the OLED display
    time.sleep(2)  # Show the message for 2 seconds
    display_status(b'Waiting for status...')  # Return to previous status display

def main():
    from _thread import start_new_thread
    start_new_thread(receive_status, ())  # Start listening for status updates
    start_new_thread(check_button, ())  # Start checking button status
    while True:
        time.sleep(0.1)  # Keep the main loop running

# Run the main function
main()
