

# 🐍 Netmiko Documentation (Python Network Automation)

## Overview

**Netmiko** is a Python library that simplifies SSH connections to network devices such as **Cisco, Juniper, Arista, Huawei, Palo Alto, and more**.
It is widely used for **network automation, configuration management, and operational tasks**.

Netmiko is built on top of **Paramiko** and abstracts vendor-specific SSH behavior.

---

## Key Features

* Simple SSH connection handling
* Vendor-specific device support
* Send show commands
* Push configuration commands
* Supports enable mode
* Ideal for scripting and automation workflows

---

## Installation

```bash
pip install netmiko
```

---

## Supported Device Types (Examples)

| Vendor        | device_type      |
| ------------- | ---------------- |
| Cisco IOS     | `cisco_ios`      |
| Cisco NX-OS   | `cisco_nxos`     |
| Cisco ASA     | `cisco_asa`      |
| Juniper JunOS | `juniper_junos`  |
| Arista EOS    | `arista_eos`     |
| Huawei        | `huawei`         |
| Palo Alto     | `paloalto_panos` |

---

## Basic Connection Example

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "Password"
}

connection = ConnectHandler(**device)
print(connection.find_prompt())
connection.disconnect()
```

---

## Sending Show Commands

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "netadmin",
    "password": "Password123"
}

connection = ConnectHandler(**device)

output = connection.send_command("show ip interface brief")
print(output)

connection.disconnect()
```

---

## Sending Configuration Commands

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "netadmin",
    "password": "Password123"
}

connection = ConnectHandler(**device)

config_commands = [
    "interface Ethernet0/2",
    "description CONFIGURED USING NETMIKO",
    "ip address 10.10.10.1 255.255.255.252",
    "no shutdown"
]

output = connection.send_config_set(config_commands)
print(output)

connection.disconnect()
```

---

## Using Enable Mode (Privileged EXEC)

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "netadmin",
    "password": "Password123",
    "secret": "EnablePassword"
}

connection = ConnectHandler(**device)
connection.enable()

output = connection.send_command("show running-config")
print(output)

connection.disconnect()
```

---

## Running Multiple Commands

```python
commands = [
    "show version",
    "show inventory",
    "show ip route"
]

for cmd in commands:
    print(f"\nRunning: {cmd}")
    print(connection.send_command(cmd))
```

---

## Backing Up Device Configuration

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "netadmin",
    "password": "Password123"
}

connection = ConnectHandler(**device)

running_config = connection.send_command("show running-config")

with open("router_backup.cfg", "w") as file:
    file.write(running_config)

connection.disconnect()
```

---

## Automating Multiple Devices

```python
devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "netadmin",
        "password": "Password123"
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.2",
        "username": "netadmin",
        "password": "Password123"
    }
]

for device in devices:
    connection = ConnectHandler(**device)
    print(f"Connected to {device['host']}")
    print(connection.send_command("show ip interface brief"))
    connection.disconnect()
```

---

## Error Handling (Best Practice)

```python
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

try:
    connection = ConnectHandler(**device)
    print(connection.send_command("show version"))

except NetmikoTimeoutException:
    print("Connection timed out")

except NetmikoAuthenticationException:
    print("Authentication failed")

finally:
    if 'connection' in locals():
        connection.disconnect()
```

---

## Common Use Cases

* Network device provisioning
* Interface configuration
* Backup and restore of configs
* Network audits
* Troubleshooting automation
* Pre-checks and post-checks

---

## Best Practices

* Never hardcode credentials in production
* Use environment variables or vaults
* Always test in lab before production
* Log outputs for auditing
* Use `try/except` for reliability

---

## Useful Netmiko Methods

| Method              | Description          |
| ------------------- | -------------------- |
| `send_command()`    | Run show commands    |
| `send_config_set()` | Push config commands |
| `enable()`          | Enter enable mode    |
| `find_prompt()`     | Get device prompt    |
| `disconnect()`      | Close SSH session    |

---

## References

* Netmiko GitHub Repository
* Official Netmiko Documentation
* Python Network Automation Community

