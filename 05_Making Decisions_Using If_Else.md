

# Python for Network Automation – Episode 5

Making Decisions **(If, Else, Elif, Break, Continue)**

Automation becomes powerful when your script can **make decisions**—just like a real network engineer who checks device types, interface states, VLAN assignments, BGP sessions, and more.

In this episode, we explore **control flow**:

* `if`
* `elif`
* `else`
* `continue`
* `break`

These concepts allow your Python code to act dynamically, validate conditions, prevent bad changes, and stop faulty loops—critical skills for real automation.

---

## **Part 1: The Basics — `if` and `else`**

### **Concept**

Python asks a question → If True, do one thing → else, do another.

### **Real Network Example: Checking if a VLAN exists before configuration**

```python
vlan_id = 100
allowed_vlans = [10, 20, 30, 40, 50]

print(f"Checking VLAN {vlan_id}...")

if vlan_id in allowed_vlans:
    print(f"VLAN {vlan_id} already exists. Skipping creation.")
else:
    print(f"VLAN {vlan_id} not found. Creating VLAN {vlan_id}...")
```

### **Key Takeaway**

The `else` block catches everything that doesn’t meet the `if` condition — it's your fallback/safety path.

---

## **Part 2: Handling Multiple Options — `elif`**

### **Concept**

Networks have multiple OS types and logic branches.
`elif` lets you test several conditions, in order.

### **Real Network Example: Vendor-specific command sets**

```python
device_os = "junos"

if device_os == "ios":
    print("Cisco IOS detected")
    command = "show ip interface brief"

elif device_os == "nxos":
    print("Cisco NX-OS detected")
    command = "show interface brief"

elif device_os == "eos":
    print("Arista EOS detected")
    command = "show ip interface brief"

elif device_os == "junos":
    print("Juniper JunOS detected")
    command = "show interface terse"

else:
    print("Unknown OS! Cannot determine command.")
    command = None

print(f"Final command selected → {command}")
```

### **Key Takeaway**

Python only runs **the first matching condition**.
Use `elif` to handle multiple vendors, interface states, routing protocols, etc.

---

## **Part 3: Skipping Items in a Loop — `continue`**

### **Concept**

Inside a loop, `continue` says:

> “Skip everything below and jump to the next item.”

### **Why It Matters in Networking**

Great for filtering:

* Skip UP interfaces
* Skip management VLANs
* Skip Loopbacks
* Skip shutdown BGP peers
* Skip devices with failed ping tests

### **Real Network Example: Skip interfaces that are already UP**

```python
interfaces = [
    {"name": "Gi1/0/1", "status": "up"},
    {"name": "Gi1/0/2", "status": "down"},
    {"name": "Gi1/0/3", "status": "up"},
    {"name": "Gi1/0/4", "status": "down"}
]

print("\n--- Interface Remediation Start ---")

for intf in interfaces:
    if intf["status"] == "up":
        print(f"Skipping {intf['name']} (already UP)")
        continue   # jump to next interface

    print(f"Bringing {intf['name']} UP → sending 'no shut'")
```

### **Real Example: Skip unreachable devices before SSH automation**

```python
devices = [
    {"ip": "10.10.1.1", "reachable": True},
    {"ip": "10.10.1.2", "reachable": False},
    {"ip": "10.10.1.3", "reachable": True},
]

for dev in devices:
    if not dev["reachable"]:
        print(f"Skipping {dev['ip']} — ping failed!")
        continue

    print(f"Connecting to {dev['ip']} via SSH...")
```

### **Key Takeaway**

`continue` acts like a **filter**.
It protects your code from acting on devices/interfaces you don't want to modify.

---

## **Part 4: Stopping a Loop Completely — `break`**

### **Concept**

`break` instantly stops the loop — nothing else runs.

### **Why It Matters in Networking**

Use it when:

* You find a specific MAC address in a huge table
* You locate a target IP in ARP
* You detect a critical failure
* You find the active device in an HA pair
* You locate the primary BGP neighbor

### **Real Network Example: Searching for an IP**

```python
target_ip = "192.168.100.10"
ip_list = [
    "192.168.100.1",
    "192.168.100.2",
    "192.168.100.10",
    "192.168.100.20"
]

print(f"Searching for {target_ip}...\n")

for ip in ip_list:
    print(f"Checking {ip}...")
    if ip == target_ip:
        print(f"FOUND {target_ip}! Stopping search.")
        break

print("\nSearch complete.")
```

### **Real Example: Stop scanning once you find the active firewall**

```python
fw_nodes = [
    {"hostname": "fw01", "state": "standby"},
    {"hostname": "fw02", "state": "active"},
    {"hostname": "fw03", "state": "standby"}
]

for fw in fw_nodes:
    print(f"Checking {fw['hostname']}...")
    if fw["state"] == "active":
        print(f"Active firewall found → {fw['hostname']}")
        break
```

### **Key Takeaway**

Once your automation finds what it needs, **stop immediately** and save processing time.

---

## **Part 5: Combining `if`, `continue`, and `break` — Real Network Use Case**

### **Scenario**

Your script reads device health, and:

* Skip devices that fail ping tests
* Stop everything if a device is in “CRITICAL” state
* Continue with SSH automation for healthy devices

```python
devices = [
    {"ip": "10.1.1.1", "reachable": True,  "state": "OK"},
    {"ip": "10.1.1.2", "reachable": False, "state": "UNKNOWN"},
    {"ip": "10.1.1.3", "reachable": True,  "state": "CRITICAL"},
    {"ip": "10.1.1.4", "reachable": True,  "state": "OK"}
]

for dev in devices:

    # Skip unreachable devices
    if not dev["reachable"]:
        print(f"Skipping {dev['ip']} — Ping failed.")
        continue

    # Stop everything on a critical alert
    if dev["state"] == "CRITICAL":
        print(f"CRITICAL ALERT on {dev['ip']} — Aborting automation!")
        break

    print(f"Connecting to {dev['ip']} via SSH...")
```

This is real-world automation logic you’ll use daily.

---

## **Summary**

### **You Learned:**

| Concept        | Purpose                | Real Use Case                         |
| -------------- | ---------------------- | ------------------------------------- |
| `if` / `else`  | Basic decision making  | Check VLANs, check interface state    |
| `elif`         | Multiple options       | Vendor-specific commands              |
| `continue`     | Skip current loop item | Skip UP interfaces, skip failed pings |
| `break`        | Exit loop entirely     | Stop when MAC/IP is found             |
| Combined logic | Intelligent automation | Health checks, filtering, early exit  |

---
