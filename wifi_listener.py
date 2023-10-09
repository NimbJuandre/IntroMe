import platform
import subprocess
import re
import os
import netifaces

def get_current_network_interface():
    try:
        # Get a list of all network interfaces
        interfaces = netifaces.interfaces()
        
        # Iterate through the interfaces and find the one with an IP address (assuming it's connected)
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                return interface 
        
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

def parse_packet(packet):
    # Extract source MAC address from the packet
    mac_address_match = re.search(r"Source: ([\w:]+)", packet)
    if mac_address_match:
        return mac_address_match.group(1)
    return None


def start_network_listener(interface):
    if not is_tshark_installed():
        install_wireshark()
        return

    try:
        # Run tshark to capture wireless network traffic and print it to stdout
        command = [
            "tshark",
            "-i", interface,  # Specify the network interface (e.g., "wlan0" for Wi-Fi)
            "-T", "fields",  # Output fields, one per line
            "-e", "frame.time",  # Timestamp of the packet
            "-e", "wlan.sa",  # Source MAC address
            # "-Y", "wlan",  # Filter for Wi-Fi packets
        ]

        # Start tshark as a subprocess, capturing and parsing packets continuously
        tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

        print("Listening for network devices (Ctrl+C to stop):")

        for line in tshark_process.stdout:
            mac_address = parse_packet(line)
            if mac_address:
                print(f"Device MAC address: {mac_address}")

    except KeyboardInterrupt:
        print("\nListener stopped by the user.")
    except subprocess.CalledProcessError:
        print("\nError.")

if __name__ == "__main__":
    if platform.system() == "Windows":
        # current_connected_interface = get_current_network_interface()
        current_connected_interface = r"\Device\NPF_{D487526C-FDB1-44C9-B484-72BF575A2138}"
        start_network_listener(current_connected_interface)
    else:
        print("This script is intended for Windows only.")
