# Python for Network Automation (Ep 4): Mastering JSON for Real Network Automation

Modern network devices, APIs, IPAM systems, and cloud controllers all speak **JSON**, not CSV. If you want to automate Cisco Nexus, Meraki Dashboard, NetBox, or REST APIs, you *must* understand JSON.

This episode gives you a **clear, practical, network‑engineer‑friendly guide** to mastering JSON — with real examples, real nested data, and real device configuration use cases.

---

## 🧠 Part 1: Understanding JSON — The "S" Trick (load vs loads)

Python has four functions for working with JSON, and the biggest confusion is knowing which one to use.

### **🔥 The Rule to Remember:**

**The letter `S` stands for *String*.**

| Function       | Reads/Writes | Source Type | Memory Trick    |
| -------------- | ------------ | ----------- | --------------- |
| `json.load()`  | Read         | File        | **No S → File** |
| `json.loads()` | Read         | String      | **S → String**  |
| `json.dump()`  | Write        | File        | **No S → File** |
| `json.dumps()` | Write        | String      | **S → String**  |

### **Real-Life Example**

```python
import json

# Case 1: Loading JSON from an API response string
json_string = '{"hostname": "Router1", "ip": "10.1.1.1"}'
data_from_string = json.loads(json_string)

# Case 2: Loading JSON from a file (e.g., NetBox export)
with open('data.json', 'r') as f:
    data_from_file = json.load(f)
```

---

## 🧩 Part 2: Real Network JSON - Nested Data

Real network APIs send **deeply nested** JSON with lists inside dictionaries inside lists.

Example file: `interface_config.json`.

```json
{
    "hostname": "nyc-core-01",
    "region": "US-East",
    "interfaces": [
        {
            "name": "GigabitEthernet1",
            "description": "MANAGEMENT",
            "enabled": true,
            "ip": "192.168.10.5"
        },
        {
            "name": "GigabitEthernet2",
            "description": "UPLINK-ISP",
            "enabled": false,
            "ip": "172.16.50.2"
        }
    ]
}
```

### **Loading the JSON File**

```python
import json

print("--- Loading JSON File ---")
with open('interface_config.json', 'r') as f:
    device_data = json.load(f)

print(f"Loaded data for: {device_data['hostname']}")
print(f"Type: {type(device_data)}")  # It's a dictionary!
```

---

## 🛠 Part 3: Navigating Nested JSON (Drill Down Method)

Use **keys** for dictionaries and **indexes** for lists.

### Example: Accessing Deep Data

```python
# 1. Top-level key
region = device_data['region']

# 2. Access the interfaces list
interfaces = device_data['interfaces']

# 3. Get the first interfaceirst_int = interfaces[0]
print(f"First Interface: {first_int['name']}")

# 4. One-line drill-down: Get IP of second interface
uplink_ip = device_data['interfaces'][1]['ip']
print(f"Uplink IP: {uplink_ip}")
```

### ⭐ Real-life scenario:

* Checking all DOWN interfaces
* Getting all management IPs
* Validating device regions for compliance

```python
print("\n--- Checking Disabled Interfaces ---")
for intf in device_data['interfaces']:
    if not intf['enabled']:
        print(f"{intf['name']} is DOWN → IP: {intf['ip']}")
```

---

## ✏️ Part 4: Editing JSON (Read → Modify → Write)

JSON files cannot be "edited" directly — you:

1. **Read** file into Python
2. **Modify** dictionary/list in memory
3. **Write** the updated JSON back

### **Scenario:** Enable the ISP uplink interface and update description.

```python
print("\n--- Updating Configuration ---")

for interface in device_data['interfaces']:
    if interface['name'] == 'GigabitEthernet2':
        print(f"Updating {interface['name']}...")

        interface['enabled'] = True
        interface['description'] = "UPLINK-ISP-PRIMARY"
        interface['mtu'] = 1500   # Adding a new field

# Save back to file
with open('interface_config.json', 'w') as f:
    json.dump(device_data, f, indent=4)

print("Update saved!")
```

### 🌐 More Real Automation Use Cases

* Updating interface descriptions using CDP/LLDP data
* Changing BGP neighbor states
* Adding missing SNMP location fields
* Fixing wrong IP addresses in API-driven configs

---

## 🔍 Part 5: Pretty Printing JSON (Debugging Pro Tip)

API responses can look messy.

### Using `json.dumps` for clean output:

```python
print("--- Raw Output ---")
print(device_data)

print("\n--- Pretty JSON ---")
print(json.dumps(device_data, indent=4))
```

### When is this useful?

* Debugging API responses
* Printing clean logs
* Exporting structured info to Slack/Teams bots

---

## 🎯 Summary

By now, you can:

* Use `load`/`loads` and `dump`/`dumps` correctly
* Read and write JSON files safely
* Navigate complex nested structures
* Modify network data programmatically
* Pretty-print JSON for debugging

JSON is the language of modern network automation — and now you speak it.

You now understand:

* Variables (E1)
* Lists & Dictionaries (E2)
* CSV Inventory (E3)
* JSON (E4)

You're ready for Episode 5: **Using Python Libraries (Netmiko, Requests, NAPALM) to automate real devices and APIs!**
