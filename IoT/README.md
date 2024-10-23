# Traffic Light System for Persons with Disabilities (PWD)

This project consists of two ESP32 devices working together to create a traffic control system designed for persons with disabilities (PWD). The system is split into two components: one for the traffic light control and the other for PWDs to interact with the system. The communication between the two devices is facilitated using the ESPNOW protocol.

## Project Components

### 1. PWD's Device
The PWD device allows a user to interact with the traffic light system. It features an OLED display, an RGB LED to show traffic status, and a button to request a stop signal at the traffic light.

#### Features:
- **OLED Display**: Shows the current status of the traffic light (`GO`, `GET READY`, or `STOP`).
- **RGB LED**: Provides visual feedback corresponding to the traffic light status.
- **Button**: Allows the user to send a `STOP` request to the traffic light.
- **ESPNOW Communication**: Sends and receives traffic light status updates.

#### Code Components:
- **I2C setup for OLED**: Displays the current traffic status.
- **RGB LED control**: Shows the traffic light status with color indication.
- **Button functionality**: Debounces the button input and sends a `STOP` signal.
- **Receive Status**: Continuously listens for updates from the traffic light and updates the OLED and RGB LEDs accordingly.

#### Hardware Components:
- ESP32
- RGB LED
- OLED Display (SSD1306)
- Push button

### 2. Traffic Light Control Device
The traffic light control device handles the sequencing of traffic lights (`GO`, `GET READY`, and `STOP`). It also communicates with the PWD's device via ESPNOW and interacts with an external API to process data received from the PWD's device.

#### Features:
- **LED Traffic Light Control**: Red, yellow, and green LEDs control the traffic light sequence.
- **Wi-Fi Connectivity**: Connects to an external API for additional traffic data processing.
- **ESPNOW Communication**: Sends status updates to the PWD's device and receives commands (such as `STOP`).
- **API Call**: Fetches relevant traffic data for the PWD based on the received MAC address.

#### Code Components:
- **Wi-Fi Connection**: Connects the ESP32 to a specified Wi-Fi network.
- **Traffic Light Sequence**: Manages the traffic light operations based on normal or stop mode.
- **Receive Requests**: Listens for `STOP` commands and API requests from the PWD's device.
- **API Integration**: Sends an HTTP request to an API to fetch traffic-related data.

#### Hardware Components:
- ESP32
- Red, yellow, and green LEDs

## How it Works
1. The PWD's device listens for traffic light status updates using ESPNOW.
2. The current traffic light status is displayed on the OLED screen and indicated via the RGB LED.
3. When the PWD presses the button, a `STOP` request is sent to the Traffic Light Controller.
4. The Traffic Light Controller receives the `STOP` request and halts the traffic by turning on the red light.
5. The Traffic Light Controller can also connect to a specified API to fetch additional traffic information based on the PWD's device MAC address.
6. Both devices maintain real-time communication to keep traffic light information updated.

## Requirements
- MicroPython installed on ESP32 devices
- External modules:
  - `espnow` for communication between devices
  - `network` for Wi-Fi connection
  - `urequests` for HTTP requests to the API (on the traffic controller device)
  - `ssd1306` for OLED display control

## Usage
1. Flash both MicroPython scripts to their respective ESP32 devices.
2. Power up the Traffic Light Controller device and ensure it's connected to the specified Wi-Fi network.
3. Power up the PWD's device. It will automatically connect to the Traffic Light Controller via ESPNOW.
4. The PWD's device will display the current traffic status and allow the user to request a stop using the button.
5. Monitor the serial output of both devices to debug or observe the system's behavior.

## File Structure
PWD Device Code (pwd_device.py)
Traffic Light Controller Code (traffic_device.py)
README.md 

## Future Enhancements
- Implement voice commands for persons with disabilities to interact with the system.
- Integrate a backup power solution to ensure continuous operation during power outages.
