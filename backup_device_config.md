# Automate Network Device Backups with Python & Netmiko (Step-by-Step)

## Overview

This guide walks you through automating network device configuration backups using Python and Netmiko.
The script connects to devices via SSH, retrieves the running configuration, and saves it in a timestamped folder.

 ## Prerequisites

Before you start, ensure you have:

- Python installed (3.x)
- Netmiko installed
- A CSV file containing device details
- SSH access to your network devices


* Step 1: Install Required Library
pip install netmiko

* Step 2: Create Device Inventory (CSV)

Create a file named devices.csv:

```csv
name,device_type,host_ip
R1,cisco_ios,192.168.1.1
R2,cisco_ios,192.168.1.2
```

* Step 3: Generate Timestamp for Backup Folder

We use Python’s datetime module to create a unique folder for each run.
```python
import datetime

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
```

* Step 4: Create Backup Folder
  
```pythonn
import os

backup_dir = f"device_backup_{timestamp}"
os.makedirs(backup_dir, exist_ok=True)
```

* Step 5: Collect User Credentials Securely

```python
import getpass

USERNAME = input("Enter username: ")
PASSWORD = getpass.getpass("Enter Password: ")
```

* Step 6: Read Device Inventory
```python
import csv

with open("devices.csv", "r") as file:
    data = csv.DictReader(file)
```

* Step 7: Connect to Devices Using Netmiko
```python
from netmiko import ConnectHandler

for device in data:
    device_info = {
        "device_type": device["device_type"],
        "host": device["host_ip"],
        "username": USERNAME,
        "password": PASSWORD
    }
```

* Step 8: Execute Command and Fetch Configuration
  
```python
with ConnectHandler(**device_info) as device_connect:
    device_config = device_connect.send_command("show running-config")
```

* Step 9: Save Configuration to File

```python
filename = f"{device['name']}_{device['host_ip']}_{timestamp}.config"
filepath = os.path.join(backup_dir, filename)

with open(filepath, "w") as backup_file:
    backup_file.write(device_config)
```
 
* Step 10: Add Error Handling

```python
try:
    # connection and backup logic
except Exception as e:
    print(f"Failed to connect to {device['host_ip']}: {e}")
```

## Full CodeBase

```python
from netmiko import ConnectHandler
import csv
import datetime
import getpass
import os

# Step 1: Create timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Step 2: Create backup folder
backup_dir = f"device_backup_{timestamp}"
os.makedirs(backup_dir, exist_ok=True)

# Step 3: Get credentials
USERNAME = input("Enter username: ")
PASSWORD = getpass.getpass("Enter Password: ")

# Step 4: Read inventory
with open("devices.csv", "r") as file:
    data = csv.DictReader(file)

    for device in data:
        device_info = {
            "device_type": device["device_type"],
            "host": device["host_ip"],
            "username": USERNAME,
            "password": PASSWORD
        }

        try:
            print(f"Connecting to {device['name']} ({device['host_ip']})")

            with ConnectHandler(**device_info) as device_connect:
                device_config = device_connect.send_command("show running-config")

                filename = f"{device['name']}_{device['host_ip']}_{timestamp}.config"
                filepath = os.path.join(backup_dir, filename)

                with open(filepath, "w") as backup_file:
                    backup_file.write(device_config)

                print(f"Backup saved for {device['name']}")

        except Exception as e:
            print(f"Failed to connect to {device['host_ip']}: {e}")
```
