# **Episode 3: File Handling for Network Automation (Reading & Writing TXT & CSV Files)**

When you store network data inside a Python script — device IPs, hostnames, configs — that data disappears as soon as the script ends. Real network automation requires **persistent data**, stored in real files.

In this episode, you will learn how to:

* Read device IPs from a `.txt` file
* Save router configuration backups into files
* Read and build a **network inventory** using `.csv` files
* Update/edit CSV data using the **read → modify → write** pattern

Let’s begin.

---

# **1. Why Files Matter in Network Automation**

Your Python script needs to interact with the real world. Files are how it does that.

### ✔ Why Files?

* Your script can **receive** data from files (device IPs, credentials, inventory tables)
* Your script can **save** results to files (config backups, reports, logs)

Files act like the **ears and mouth** of your automation.

---

# **The `with open()` Pattern**

This is the safest, cleanest way to work with files.

```python
# Syntax
with open('filename.txt', 'mode') as f:
    # work with file object 'f'
```

### **File Modes You Must Know**

* `'r'` → **Read** (default). Error if file does not exist.
* `'w'` → **Write**. Overwrites the file or creates it if missing.
* `'a'` → **Append**. Adds new lines to the end.

### ✔ Key Takeaway

**Always use `with open()`** — it automatically closes the file and prevents corruption.

---

# **2. Reading & Writing Simple Text Files (.txt)**

TXT files are perfect for storing simple lists such as IP addresses.

---

## **Example 1: Reading Device IPs from `ips.txt`**

### **Sample File: `ips.txt`**

```
10.1.1.1
10.1.1.2
10.1.1.3
```

### **Python Code: Turning TXT Into a Python List**

```python
print("--- Reading device IPs from file ---")

device_ips = []  # empty list

with open('ips.txt', 'r') as f:
    for line in f:
        device_ips.append(line.strip())  # strip removes invisible \n
print(f"Here is our Python list of IPs: {device_ips}")

# Now you can loop through and connect to each device
for ip in device_ips:
    print(f"Connecting to device {ip}...")
```

### ✔ Real-World Use

* Run commands on multiple network devices read from a text file
* Automate backup tasks for each device

---

## **Example 2: Writing a Config Backup to a File**

Let’s simulate saving a router configuration.

```python
print("\n--- Saving config backup ---")

# Simulated config (in real life, you would get this from Netmiko)
config_data = """
!
hostname core-router-01
!
interface GigabitEthernet0/1
 description LINK-TO-SW-01
 ip address 192.168.1.1 255.255.255.0
!
"""

# 'w' overwrites or creates a file
with open('backup_core-router-01.txt', 'w') as f:
    f.write(config_data)

print("Backup file saved!")
```

### ✔ Real-World Use

* Store nightly configuration backups
* Export logs or command outputs

---

# **3. The Power of CSV Files (Network Inventory)**

A `.txt` file stores a simple list.
A `.csv` file stores a **table** (like Excel).

This makes CSV perfect for:

* Network inventories
* VLAN tables
* IPAM data
* Device deployment lists

---

## **Example CSV: `inventory.csv`**

```
hostname,ip_address,model,location
core-rtr-01,10.1.1.1,ASR1002,HQ
dist-sw-01,10.1.2.1,Nexus9K,HQ
access-sw-01,10.1.3.1,Cat3850,Floor1
```

---

## **Reading CSV as a List of Dictionaries**

This is one of the most powerful patterns in automation.

```python
import csv

print("\n--- Reading Inventory from CSV ---")

inventory = []  # We will build a LIST of DICTIONARIES

with open('inventory.csv', 'r') as f:
    reader = csv.DictReader(f)  # Automatically uses header row as keys

    for row in reader:
        inventory.append(row)

print(inventory)
```

### **Why This Is Powerful**

Now you can do this:

```python
print("\n--- Generating configs from CSV data ---")
for device in inventory:
    print(f"--- Config for {device['hostname']} ---")
    print(f"snmp-server location {device['location']}")

    if device['model'] == 'ASR1002':
        print("  This is a router!")

    print("!")
```

### ✔ Key Takeaway

**`csv.DictReader` turns your CSV into a list of dictionaries — the ultimate network automation dataset.**

---

# **4. Editing & Updating Files (The Read → Modify → Write Pattern)**

Files aren’t “edited” directly like a text editor.

Instead:

1. **Read** the file into Python (list or list of dictionaries)
2. **Modify** the data in memory
3. **Write** the updated data back

This is professional-grade automation.

---

## **Example: Update a Router’s Location in CSV**

Assume `inventory` already contains the CSV data.

### **Step 1 & 2 — Modify in Memory**

```python
# Update the first router's location
inventory[0]['location'] = 'HQ-MDF'

print(f"\nUpdated data in memory: {inventory}")
```

---

### **Step 3 — Write the Updated CSV File**

```python
# Get the headers from the dictionary keys
headers = inventory[0].keys()

with open('inventory_updated.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)

    writer.writeheader()  # Write the CSV header row
    writer.writerows(inventory)  # Write all rows from memory

print("Updated inventory saved to 'inventory_updated.csv'")
```

### ✔ Real-World Use

* Correct wrong device information
* Add new fields (OS version, serial numbers)
* Export updated network inventory
* Prepare data for mass configuration deployment

---

# **Conclusion — Your Scripts Can Now Persist Data**

You now understand how to:

* Use `with open()` safely to read and write files
* Read device IPs from `.txt` files
* Save network configuration backups to text files
* Use CSV + `DictReader` to build a powerful network inventory system
* Update/edit files using the read → modify → write automation pattern

With file handling mastered, you're ready for the next big step in network automation.

---

If you'd like, I can now prepare **Episode 4**, or generate:

* GitHub repository structure
* Example folder hierarchy
* Practice labs for Episode 3
* A downloadable sample dataset
