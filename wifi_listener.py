import platform
import subprocess
import os
import netifaces
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Define global variables
observed_mac_addresses = {}
last_cleanup_time = time.time()

# Load the configuration from the JSON file
with open("config.json", 'r') as config_file:
    config = json.load(config_file)

# Initialize Spotipy with your credentials and specify the required scope
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['client_id'],
                                               client_secret=config['client_secret'],
                                               redirect_uri=config['redirect_uri'],
                                               scope='user-library-read user-modify-playback-state user-read-playback-state'))

# This will open the browser wher the user must copy the url into the console
sp.auth_manager.get_authorization_code()

# Function to get the current network interface
def get_current_network_interface():
    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                # Use a meaningful variable name
                return f"\\Device\\NPF_{interface}"
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Function to add the Tshark folder to the PATH environment variable
def add_tshark_to_path_variable():
    try:
        tshark_folder = "C:\\Program Files\\Wireshark"
        current_path = os.environ.get('Path', '')
        new_path = f"{current_path};{tshark_folder}"
        os.environ['Path'] = new_path
    except subprocess.CalledProcessError:
        print("Failed to add the Tshark folder to the PATH environment variable")

# Function to check if Tshark is installed
def is_tshark_installed():
    try:
        add_tshark_to_path_variable()
        subprocess.check_call(["tshark", "--version"])
        return True
    except FileNotFoundError:
        print("Tshark (part of Wireshark) is not installed.")
        return False
    except subprocess.CalledProcessError:
        print("Error: Failed to run Tshark.")
        return False

# Function to install Wireshark (Tshark)
def install_wireshark():
    print("Wireshark (which includes Tshark) is not installed. Please follow these steps to install it:")
    print("1. Download Wireshark from https://www.wireshark.org/download.html")
    print("2. Run the Wireshark installer and select the option to install Wireshark.")
    print("3. Make sure to add Wireshark to your system PATH during installation.")
    print("4. Restart your computer if necessary.")
    print("5. Run this script again after installation.")

# Function to parse MAC addresses from a line
def parse_mac_address(line):
    parts = line.strip().split()
    if len(parts) > 0:
        return parts[0]
    else:
        return None

# Function to cleanup devices that have not been observed for 15min
def cleanup_devices(current_time, timeout):
    global last_cleanup_time
    for mac, timestamp in list(observed_mac_addresses.items()):
        if current_time - timestamp > timeout:
            print(f"Device disconnected - MAC address: {mac}")
            del observed_mac_addresses[mac]
    last_cleanup_time = current_time
    
# Function to start the network listener
def start_network_listener(interface, timeout=3600): # 15 min
    if not is_tshark_installed():
        install_wireshark()
        return

    try:
        command = [
            "tshark",
            "-i", interface,
            "-T", "fields",
            "-e", "wlan.sa",
            "-e", "wlan.fc",
            "-e", "eth.src",
            "-q",  # Use quiet mode to avoid packet storage
        ]

        tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(f"Listening for network devices on interface {interface} (Ctrl+C to stop):")

        for line in tshark_process.stdout:
            mac_address = parse_mac_address(line)
            if mac_address:
                current_time = time.time()
                if mac_address not in observed_mac_addresses:
                    print(f"New device connected - MAC address: {mac_address}, Total devices: {len(observed_mac_addresses) + 1}")
                    play_song_on_device(sp, mac_address)
                    
                observed_mac_addresses[mac_address] = current_time

                if current_time - last_cleanup_time >= 300:  #Run an cleanup every 300 seconds = 5 minutes
                    current_total = len(observed_mac_addresses)
                    cleanup_devices(current_time, timeout)
                    print(f"Total MAC addresses after cleanup: {len(observed_mac_addresses)}. Removed {current_total - len(observed_mac_addresses)} devices")

    except subprocess.CalledProcessError:
        print("\nError.")
    except Exception as e:
        print(str(e))

def find_device_song_by_mac(mac):
    for device in config['user_devices']:
        if device['mac_address'].lower() == mac:
            return device['song_uri']  # Return the device song if a match is found
    return None  # Return None if no matching device is found

def find_device_id_by_name(device_name):
   # Get a list of your Spotify devices
    devices = sp.devices()
    if not devices['devices']:
        print(f"No devices found to play the song on.")
        return None

    # Find the specified device by name
    for device in devices['devices']:
        if device['name'] == device_name:
            return device['id']
    
    return None

# Function to play a song on a selected device
def play_song_on_device(sp, mac_address):
    song = find_device_song_by_mac(mac_address)
    if song is None:
        return
    
    try:
        device_name = config['spotify_device_name']
        device_id = find_device_id_by_name(device_name)
        if not device_id:
            print(f"Could not found the device id for device {device_name}.")
            return
        
        # Add the song to the queue
        track = sp.track(song)
        sp.add_to_queue(uri=song, device_id=device_id)

        # Skip to the next track in the queue
        sp.next_track(device_id=device_id)
        print(f"Playing {track['name']} on device '{mac_address}'.")
            
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    if platform.system() == "Windows":
        current_connected_interface = get_current_network_interface()
        start_network_listener(current_connected_interface)
    else:
        print("This script is intended for Windows only.")
