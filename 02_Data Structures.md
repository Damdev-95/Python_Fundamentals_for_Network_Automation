# Episode 2: Python for Network Automation — Data Structures Fundamentals

In network automation, data is everything — IP addresses, device names, VLAN lists, interface information, configuration templates, logs, and more. Python’s built‑in data structures make it easy to organize, parse, and manipulate this data so you can automate real network tasks.

This episode covers the **three essential data structures** every network automation engineer uses daily:

* **Strings**
* **Lists**
* **Dictionaries**

Understanding these concepts early will enable you to build powerful automation scripts with clean, readable, and scalable code.

---

## 🔤 1. Variables and Basic Data Types

Variables act as containers for storing different types of data. Python automatically detects the type based on what you assign.

### **Common Data Types Used in Networking**

* **String (`str`)** – Device names, IP addresses, usernames
* **Integer (`int`)** – VLAN IDs, port numbers
* **Float (`float`)** – Interface speeds, bandwidth values
* **Boolean (`bool`)** – Interface state, feature enabled/disabled

### **Example:**

```python
# String (Text)
hostname = "core-router-01"

# Integer (Whole Number)
vlan_id = 100

# Float (Decimal)
interface_speed = 10.5  # e.g., 10.5 Gbps

# Boolean (True/False)
is_interface_up = True

print(f"Device: {hostname} is of type {type(hostname)}")
print(f"VLAN: {vlan_id} is of type {type(vlan_id)}")
print(f"Status: {is_interface_up} is of type {type(is_interface_up)}")
```

### **Key Insight**

Using descriptive variable names like `vlan_id`, `hostname`, or `is_interface_up` improves clarity and reduces errors.

---

## 🧵 2. Working With Strings

Strings represent text, which is the foundation of CLI commands and show‑command outputs.

### **2.1 Building Configuration Lines (f‑Strings)**

F‑strings allow you to embed variables directly inside text.

```python
interface_name = "GigabitEthernet0/1"
description = "User-Data-VLAN-100"

config_line_1 = f"interface {interface_name}"
config_line_2 = f" description {description}"
config_line_3 = f" switchport access vlan 100"

print(config_line_1)
print(config_line_2)
print(config_line_3)
```

### **2.2 Parsing and Cleaning Text (String Methods)**

Real network outputs are often messy. Python provides tools to format and clean them.

```python
# .split() - Break a string into parts
log_message = "ERROR:Interface_Gi0/1:is_down"
log_parts = log_message.split(':')
print(log_parts)                  # ['ERROR', 'Interface_Gi0/1', 'is_down']
print(log_parts[1])               # Interface_Gi0/1

# .strip() - Remove whitespace
raw_hostname = "   core-router-01   "
cleaned = raw_hostname.strip()
print(f"'{raw_hostname}' -> '{cleaned}'")

# .lower() - Standardize case
iface = "Gig0/1"
print(iface.lower())              # gig0/1
```

### **Why Strings Matter in Automation**

You will use strings to:

* Build CLI commands
* Parse show command outputs
* Clean logs
* Normalize data for comparisons

---

## 📦 3. Working With Lists

A **list** stores multiple items in a specific order. Lists are perfect for collections of similar items such as:

* Device IP addresses
* VLAN numbers
* NTP servers
* Interfaces

### **Example:**

```python
# List of NTP servers
ntp_servers = ["1.1.1.1", "8.8.8.8", "132.163.96.5"]

# VLANs to configure
vlans_to_configure = [10, 20, 30, 100, 200]

# Accessing the first item (index 0)
primary_ntp = ntp_servers[0]
print(f"Primary NTP server: {primary_ntp}")

# Adding a new server
ntp_servers.append("4.2.2.2")
print(f"Updated NTP servers: {ntp_servers}")

# Looping through a list
print("
--- NTP Configuration Commands ---")
for server in ntp_servers:
    print(f"ntp server {server}")

print("
--- VLAN Configuration Commands ---")
for vlan in vlans_to_configure:
    print(f"vlan {vlan}")
    print(f" name VLAN-{vlan}-DATA")
```

### **Why Lists Matter**

Loops operate naturally on lists, making them ideal for:

* Iterating through device inventories
* Applying configs to multiple VLANs
* Validating or testing multiple IP addresses

---

## 🗂 4. Working With Dictionaries

A **dictionary** stores key‑value pairs and is the most important data structure for network automation.

Use dictionaries to model real network objects such as:

* Devices
* Interfaces
* BGP neighbors
* User accounts

### **4.1 Example: Representing a Network Device**

```python
router1 = {
    "hostname": "core-router-01",
    "model": "Cisco ASR1002",
    "management_ip": "10.1.1.1",
    "location": "HQ-Datacenter",
    "is_virtual": False,
    "bgp_as": 65001
}

# Accessing values
print(f"Hostname: {router1['hostname']}")
print(f"Management IP: {router1['management_ip']}")

# Updating a value
router1['location'] = "HQ-MDF"
print(f"Updated location: {router1['location']}")

# Adding new information
router1['serial_number'] = "ABC123456"
print(f"Serial Number: {router1['serial_number']}")
```

### **4.2 Using a Dictionary to Generate Configuration**

```python
config = f"""
hostname {router1['hostname']}
ip address {router1['management_ip']} 255.255.255.0
snmp-server location {router1['location']}
!
router bgp {router1['bgp_as']}
"""

print("--- Device Configuration ---")
print(config)
```

### **Where Dictionaries Are Used in Automation**

* Device inventory (list of dictionaries)
* YAML/JSON data models
* Interface details
* API responses

---

## 🎯 Final Thoughts

In this episode, you learned:

* Variables store different types of network data
* Strings build and parse configuration text
* Lists store multiple ordered items like IPs or VLANs
* Dictionaries represent network objects with key‑value attributes

Stay consistent — your automation skills are growing rapidly! 🚀
