import platform
import subprocess
import re

def is_tshark_installed():
    try:
        subprocess.check_call(["tshark", "--version"])
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
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


def start_wifi_listener(interface):
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
            "-Y", "wlan",  # Filter for Wi-Fi packets
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
        wifi_interface = "wlan0"  # Replace with your Wi-Fi interface
        start_wifi_listener(wifi_interface)
    else:
        print("This script is intended for Windows only.")
