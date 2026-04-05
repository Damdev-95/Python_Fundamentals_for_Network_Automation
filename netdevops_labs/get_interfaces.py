import csv
from netmiko import ConnectHandler

def get_interface_status(device):
    connection = ConnectHandler(**device)
    output = connection.send_command("show ip interface brief")
    connection.disconnect()
    return output

def main():
    with open("devices.csv") as f:
        reader = csv.DictReader(f)
        for device in reader:
            print(f"\nConnecting to {device['ip']}...\n")
            try:
                output = get_interface_status(device)
                print(output)
            except Exception as e:
                print(f"Failed for {device['ip']}: {e}")

if __name__ == "__main__":
    main()
