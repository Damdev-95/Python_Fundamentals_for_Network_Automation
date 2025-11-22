

# **Python for Network Automation – Episode 6**

## **Putting It All Together: Build a Multi-Device Configuration Generator**

In the previous episodes, you learned:

* Variables & data types
* Lists and dictionaries
* Reading/writing files
* CSV parsing
* JSON parsing & nested data
* Decision-making using `if/elif/else`, `continue`, and `break`

Now in **Episode 6**, we combine everything to build a full automation script:

> **A Python Configuration Generator that reads device data from a JSON file and generates CLI configuration files for each device.**

This is your first real automation tool — and it mirrors what engineers build in production environments.

---

# **📌 Part 1 — The Goal of the Configuration Generator**

Our Python script will:

1. Read a list of network devices from a JSON file
2. Generate config for each device based on:

   * Vendor (Cisco, Juniper, Arista)
   * Hostname
   * Loopback IP
   * Interface IPs
3. Use conditionals to choose vendor-specific syntax
4. Create one output file *per device* under a `configs/` directory

---

# **📁 Part 2 — The Device Inventory (JSON File)**

Create a file named: **devices.json**

```json
{
    "devices": [
        {
            "hostname": "core-rtr-01",
            "vendor": "cisco",
            "loopback": "10.10.10.1/32",
            "interfaces": [
                {"name": "GigabitEthernet0/0", "ip": "192.168.10.1/24"},
                {"name": "GigabitEthernet0/1", "ip": "172.16.5.1/30"}
            ]
        },
        {
            "hostname": "edge-sw-01",
            "vendor": "arista",
            "loopback": "10.10.20.1/32",
            "interfaces": [
                {"name": "Ethernet1", "ip": "10.1.1.10/24"},
                {"name": "Ethernet2", "ip": "10.1.2.10/24"}
            ]
        },
        {
            "hostname": "branch-rtr-01",
            "vendor": "juniper",
            "loopback": "10.10.30.1/32",
            "interfaces": [
                {"name": "ge-0/0/0", "ip": "192.168.50.1/24"},
                {"name": "ge-0/0/1", "ip": "192.168.60.1/24"}
            ]
        }
    ]
}
```

This simulates a real network inventory in JSON format.

---

# **📦 Part 3 — Project Structure**

Your working directory should look like:

```
episode6/
│
├── devices.json
├── generate_configs.py
└── configs/
```

Create the `configs/` folder manually:

```bash
mkdir configs
```

---

# **🧠 Part 4 — Vendor-Specific Templates**

Every vendor uses different CLI syntax.
We will create templates directly inside Python as **multi-line strings**.

---

# **🧩 Part 5 — The Full Python Script (Bring Everything Together)**

Save as: **generate_configs.py**

```python
import json
import os

print("=== Network Configuration Generator (Episode 6) ===")

# -------------------------------
# Load JSON inventory
# -------------------------------
with open("devices.json", "r") as f:
    inventory = json.load(f)

devices = inventory["devices"]
print(f"Loaded {len(devices)} devices from JSON.\n")


# -------------------------------
# Vendor Templates
# -------------------------------
def generate_cisco_config(device):
    config = f"""
!
hostname {device['hostname']}
!
interface Loopback0
 ip address {device['loopback']}
!
"""
    for intf in device["interfaces"]:
        config += f"""
interface {intf['name']}
 ip address {intf['ip']}
 no shutdown
!
"""
    return config


def generate_arista_config(device):
    config = f"""
!
hostname {device['hostname']}
!
interface Loopback0
   ip address {device['loopback']}
!
"""
    for intf in device["interfaces"]:
        config += f"""
interface {intf['name']}
   ip address {intf['ip']}
   no shutdown
!
"""
    return config


def generate_juniper_config(device):
    config = f"""
set system host-name {device['hostname']}
set interfaces lo0 unit 0 family inet address {device['loopback']}
"""
    for intf in device["interfaces"]:
        config += f"set interfaces {intf['name']} unit 0 family inet address {intf['ip']}\n"
    return config


# -------------------------------
# Main Logic: Loop Through Devices
# -------------------------------
for device in devices:
    print(f"Generating config for {device['hostname']} ({device['vendor']})")

    vendor = device["vendor"].lower()

    # Decision-making logic
    if vendor == "cisco":
        final_config = generate_cisco_config(device)

    elif vendor == "arista":
        final_config = generate_arista_config(device)

    elif vendor == "juniper":
        final_config = generate_juniper_config(device)

    else:
        print(f"Unknown vendor {vendor}, skipping...")
        continue   # Skip unsupported vendors

    # Write to file
    filename = f"configs/{device['hostname']}.cfg"

    with open(filename, "w") as f:
        f.write(final_config)

    print(f"✔ Saved: {filename}\n")

print("=== All device configs generated successfully! ===")
```

---

# **🧪 Part 6 — Run the Script**

```bash
python3 generate_configs.py
```

You should see output like:

```
Generating config for core-rtr-01 (cisco)
✔ Saved: configs/core-rtr-01.cfg

Generating config for edge-sw-01 (arista)
✔ Saved: configs/edge-sw-01.cfg

Generating config for branch-rtr-01 (juniper)
✔ Saved: configs/branch-rtr-01.cfg
```

---

# **📄 Part 7 — Example of Generated Config Files**

### **Cisco Output (core-rtr-01.cfg)**

```
!
hostname core-rtr-01
!
interface Loopback0
 ip address 10.10.10.1/32
!
interface GigabitEthernet0/0
 ip address 192.168.10.1/24
 no shutdown
!
interface GigabitEthernet0/1
 ip address 172.16.5.1/30
 no shutdown
!
```

---

### **Arista Output (edge-sw-01.cfg)**

```
!
hostname edge-sw-01
!
interface Loopback0
   ip address 10.10.20.1/32
!
interface Ethernet1
   ip address 10.1.1.10/24
   no shutdown
!
interface Ethernet2
   ip address 10.1.2.10/24
   no shutdown
!
```

---

### **Juniper Output (branch-rtr-01.cfg)**

```
set system host-name branch-rtr-01
set interfaces lo0 unit 0 family inet address 10.10.30.1/32
set interfaces ge-0/0/0 unit 0 family inet address 192.168.50.1/24
set interfaces ge-0/0/1 unit 0 family inet address 192.168.60.1/24
```

---

# **📌 Part 8 — What You Just Learned**

You now understand how to combine:

* JSON parsing (`json.load`)
* Dictionaries & lists
* Nested data navigation
* Conditionals (`if / elif / else`)
* Loop control (`continue`)
* Dynamic template generation
* Writing output files


