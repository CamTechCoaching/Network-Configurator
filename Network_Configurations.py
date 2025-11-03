import csv
import os

# ----- Function to read devices from CSV ----- #
def read_devices(file_path):
    """
    Reads devices from a CSV file.
    Expects CSV headers: hostname, ip
    Returns a list of dictionaries for each device.
    """
    devices = []
    try:
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # ensure at least 'hostname' and 'ip' exist
                if 'hostname' in row and 'ip' in row:
                    devices.append(row)
                else:
                    print(f"Skipping invalid row: {row}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"Error reading device file: {e}")
    return devices

# ----- Function to simulate device configuration ----- #
def simulate_config(device):
    """
    Returns a simulated Cisco-style configuration for a device.
    """
    hostname = device.get('hostname', 'TestDevice')
    ip_address = device.get('ip', '192.168.1.1')
    return f"""!
version 15.2
hostname {hostname}
!
interface GigabitEthernet0/0
 ip address {ip_address} 255.255.255.0
 no shutdown
!
line vty 0 4
 login local
 transport input ssh
!
end
"""

# ----- Function to gather configs for all devices ----- #
def gather_configs(devices, output_file):
    """
    Writes simulated configs for all devices to a single output file.
    """
    if not devices:
        print("No devices provided.")
        return

    with open(output_file, 'w') as out:
        for device in devices:
            ip = device.get('ip', 'UnknownIP')
            hostname = device.get('hostname', 'UnknownHost')
            try:
                print(f"Simulating config for {hostname} ({ip})...")
                config = simulate_config(device)
                out.write(f"\n---- Config for {hostname} ({ip}) ----\n")
                out.write(config + "\n")
                print(f"Config written for {hostname} ({ip})")
            except Exception as e:
                print(f"Error simulating config for {hostname} ({ip}): {e}")

# ----- Main execution ----- #
if __name__ == '__main__':
    csv_file = 'devices.csv'
    output_file = 'output_configs.txt'

    # Read devices from CSV
    devices_list = read_devices(csv_file)
    if devices_list:
        gather_configs(devices_list, output_file)
        print(f"\nAll simulated configs written to {output_file}")
    else:
        print("No devices found to simulate.")
