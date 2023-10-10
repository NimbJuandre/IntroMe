import platform
import subprocess
import re
import os
import netifaces
import time

observed_mac_addresses = {}
# Store the last time the code for removing devices ran
last_cleanup_time = 0

def get_current_network_interface():
    try:
        # Get a list of all network interfaces
        interfaces = netifaces.interfaces()
        
        # Iterate through the interfaces and find the one with an IP address (assuming it's connected)
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                # Format the interface name as "\Device\NPF_{GUID}"
                return f"\\Device\\NPF_{interface}"
        
        # If no connected interface found, return None
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
def add_tshark_to_path_variable():
    try:
        tshark_folder = "C:\\Program Files\\Wireshark"
        current_path = os.environ.get('Path', '')
        new_path = f"{current_path};{tshark_folder}"
        os.environ['Path'] = new_path
        
    except subprocess.CalledProcessError:
        print("Failed to add the tshark folder to the PATH environment variable")

def is_tshark_installed():
    try:
        add_tshark_to_path_variable()
        subprocess.check_call(["tshark", "--version"])
        return True
    except FileNotFoundError:
        print("FileNotFoundError")
        return False
    except subprocess.CalledProcessError:
        print("CalledProcessError")
        return False

def install_wireshark():
    print("Wireshark (which includes tshark) is not installed. Please follow these steps to install it:")
    print("1. Download Wireshark from https://www.wireshark.org/download.html")
    print("2. Run the Wireshark installer and select the option to install Wireshark.")
    print("3. Make sure to add Wireshark to your system PATH during installation.")
    print("4. Restart your computer if necessary.")
    print("5. Run this script again after installation.")

def parse_mac_address(line):
    # Parse the MAC addresses from the captured line based on the provided data format
    # Assuming the MAC addresses are separated by spaces
    parts = line.strip().split()
    if len(parts) > 0:
            return parts[0]
    else:
        return None

def cleanup_devices(current_time, timeout):
    for mac, timestamp in list(observed_mac_addresses.items()):
        if current_time - timestamp > timeout:
            print(f"Device disconnected - MAC address: {mac}")
            del observed_mac_addresses[mac]

def start_network_listener(interface, timeout=3600):
    global last_cleanup_time

    if not is_tshark_installed():
        install_wireshark()
        return

    try:
        command = [
            "tshark",
            "-i", interface,          # Specify the network interface (e.g., "wlan0" for Wi-Fi)
            "-T", "fields",           # Output fields, one per line
            "-e", "wlan.sa",          # Source MAC address
            "-e", "wlan.fc",  
            "-e", "eth.src",
        ]

        # Start tshark as a subprocess, capturing and parsing packets continuously
        tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

        print(f"Listening for network devices on interface {interface} (Ctrl+C to stop):")
        for line in tshark_process.stdout:
            # Extract the MAC address from the captured line
            mac_address = parse_mac_address(line)

            if mac_address:
                current_time = time.time()

                if mac_address not in observed_mac_addresses:
                    print(f"MAC addresses added: {mac_address}")
                    print(f"Total MAC addresses: {len(observed_mac_addresses)}")

                # Update the timestamp for the existing MAC address or add it if not present
                observed_mac_addresses[mac_address] = current_time

                # Check if 5 minutes have elapsed since the last cleanup
                if current_time - last_cleanup_time >= 300:  # 300 seconds = 5 minutes
                    current_total = len(observed_mac_addresses)
                    cleanup_devices(current_time, timeout)
                    last_cleanup_time = current_time  # Update the last cleanup time
                    print(f"Total MAC addresses after cleanup: {len(observed_mac_addresses)}. Removed {current_total - len(observed_mac_addresses)} devices")

    except KeyboardInterrupt:
        print("\nListener stopped by the user.")
    except subprocess.CalledProcessError:
        print("\nError.")

if __name__ == "__main__":
    if platform.system() == "Windows":
        current_connected_interface = get_current_network_interface()
        start_network_listener(current_connected_interface)
    else:
        print("This script is intended for Windows only.")
