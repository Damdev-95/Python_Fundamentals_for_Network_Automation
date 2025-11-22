# Config Generator
We are going to build a Configuration Generator. Imagine you have a spreadsheet with 50 new switches. You need to configure all of them. Doing it by hand takes hours. Today, we will write a script that reads that spreadsheet and generates 50 perfect, individual configuration files in less than 1 second. Let's code."


# Step 1: The Input Data (The CSV)
Concept: Every automation script needs a "Source of Truth." We will use a CSV file. Action: Create a file named inventory.csv. Explanation: "Notice we have different device types ('switch' and 'router') and different data for each (VLANs vs. IP addresses)."

```csv
hostname,type,site,mgmt_ip,access_vlan
nyc-core-01,router,NYC,10.1.1.1,N/A
nyc-acc-01,switch,NYC,10.1.1.11,10
nyc-acc-02,switch,NYC,10.1.1.12,10
nyc-acc-03,switch,NYC,10.1.1.13,20
nyc-acc-04,switch,NYC,10.1.1.14,20
lon-core-01,router,LON,10.2.1.1,N/A
lon-acc-01,switch,LON,10.2.1.11,100
lon-acc-02,switch,LON,10.2.1.12,100
lon-acc-03,switch,LON,10.2.1.13,200
lon-acc-04,switch,LON,10.2.1.14,200
tok-core-01,router,TOK,10.3.1.1,N/A
tok-acc-01,switch,TOK,10.3.1.11,50
tok-acc-02,switch,TOK,10.3.1.12,50
tok-acc-03,switch,TOK,10.3.1.13,60
tok-acc-04,switch,TOK,10.3.1.14,60
sin-core-01,router,SIN,10.4.1.1,N/A
sin-acc-01,switch,SIN,10.4.1.11,99
sin-acc-02,switch,SIN,10.4.1.12,99
sin-acc-03,switch,SIN,10.4.1.13,99
sin-acc-04,switch,SIN,10.4.1.14,99
```

# Step 2: The Setup (Imports & Directory)
Concept: Setting up the environment. Real-World Tip: "We don't want to clutter our main folder. Let's make Python create a specific folder just for our configs."

```python
import csv
import os  # New Module! Used for talking to the Operating System

# 1. Create a folder to store our configs
output_folder = "generated_configs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created folder: {output_folder}")
```

# Step 3: The Loop (Reading the Data)
Concept: Combining with open (Ep 3) and csv.DictReader (Ep 3). Explanation: "We are turning our spreadsheet into a List of Dictionaries so Python can understand it."

```python
# 2. Open the CSV file
print("--- Starting Configuration Generation ---")

with open('inventory.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    # Loop through every device in the CSV
    for device in reader:
        hostname = device['hostname']
        print(f"Processing {hostname}...")
```

# Step 4: The Logic (The "Brain")
Concept: Using if/else (Ep 5) to decide what config to build. Explanation: "A router needs different commands than a switch. We use an if statement to check the type column from our CSV and build the configuration string (config_text) dynamically."

```python
# ... inside the loop ...
        
        # 3. Create the Base Configuration (Applied to ALL devices)
        # We use f-strings (Ep 2) to insert data
        config_text = f"""!
hostname {hostname}
ip domain-name {device['site'].lower()}.company.com
!
username admin privilege 15 secret cisco123
!
"""

        # 4. Add Specific Configuration based on Type (Logic from Ep 5)
        if device['type'] == 'router':
            config_text += f"""interface GigabitEthernet1
 description WAN-UPLINK
 ip address {device['mgmt_ip']} 255.255.255.0
 no shut
!
router bgp 65001
 network {device['mgmt_ip']} mask 255.255.255.0
!
"""
        elif device['type'] == 'switch':
            config_text += f"""vlan {device['access_vlan']}
 name ACCESS-DATA
!
interface Vlan{device['access_vlan']}
 description MANAGEMENT
 ip address {device['mgmt_ip']} 255.255.255.0
 no shut
!
"""
```

# Step 5: The Output (Saving Files)
Concept: Writing to a file using dynamic filenames (Ep 3). Explanation: "We don't just want to print this to the screen. We want to save it. We'll use the hostname to name the file so we know which config belongs to which device."

```python
# ... still inside the loop ...

        # 5. Write the config to a file
        # We save it INSIDE the 'generated_configs' folder
        filename = f"{output_folder}/{hostname}.cfg"
        
        with open(filename, 'w') as config_file:
            config_file.write(config_text)
            
        print(f"  -> Saved config to {filename}")

print("--- Job Complete! ---")
```

## Full code for Reference

```python
import csv
import os

# Create output directory
output_folder = "generated_configs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("--- Starting Configuration Generation ---")

with open('inventory.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    for device in reader:
        hostname = device['hostname']
        print(f"Processing {hostname}...")

        # Base Config
        config_text = f"""!
hostname {hostname}
ip domain-name {device['site'].lower()}.company.com
!
"""

        # Logic for Routers vs Switches
        if device['type'] == 'router':
            config_text += f"""interface Gi1
 description WAN-UPLINK
 ip address {device['mgmt_ip']} 255.255.255.0
!
"""
        elif device['type'] == 'switch':
            config_text += f"""vlan {device['access_vlan']}
 name ACCESS_DATA
!
interface Vlan{device['access_vlan']}
 ip address {device['mgmt_ip']} 255.255.255.0
!
"""

        # Save to file
        filename = f"{output_folder}/{hostname}.cfg"
        with open(filename, 'w') as config_file:
            config_file.write(config_text)
            
        print(f"  -> Saved {filename}")

print("--- Job Complete! ---")
```

"And there you have it. We just generated 20 unique configurations in milliseconds. If that CSV had 1,000 rows, it would have taken the exact same amount of effort.

This is the power of Python. We didn't just type commands; we built a system to generate commands for us.

What's Next? You might be asking, 'Okay, I have the text files... but how do I push them to the routers?' That requires a connection. In the next series, we will leave the 'Beginner's Guide' and start the 'Intermediate Network Automation' series, where we will install Netmiko and Napalm to actually log into devices and push these configs automatically.



