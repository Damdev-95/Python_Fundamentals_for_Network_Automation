# Python Network Automation: Automating OSPF with Jinja2 & CSV (Step-by-Step Project)

In this episode of our Intermediate Python for Network Automation series, we take things a step further—from simple scripts to real-world, scalable automation.


In this project, you’ll learn how to build a data-driven network automation workflow using a CSV file as your source of truth, combined with Jinja2 to dynamically generate clean and reusable OSPF configurations. We’ll then push those configs to devices using Netmiko.


## Tools
- Python 3.10
- Jinja2
- Netmiko
- CSV
- getpass
- Cisco Routers

## Folder structure

<img width="589" height="178" alt="image" src="https://github.com/user-attachments/assets/04b61ed4-381e-4945-9b80-d9f1848ea850" />

- devices.csv

```csv
host,loopback_ip,physical_subnets
172.16.29.130,2.2.2.2,192.168.23.0
172.16.29.131,3.3.3.3,192.168.23.0;192.168.34.0
172.16.29.132,4.4.4.4,192.168.34.0
```

- config_template.j2

```jinja
interface Loopback0
  description Router ID
  ip address {{ loopback_ip }} 255.255.255.255

router ospf 1
  router-id {{ loopback_ip }}
  network {{ loopback_ip }} 0.0.0.0 area 0
  {% for subnet in physical_subnets %}
  network {{ subnet }} 0.0.0.255 area 0
  {% endfor %}
```

- deploy_ospf.py

```python
import csv
import getpass
from netmiko import ConnectHandler
from jinja2 import Template

# Standard Credentials
USERNAME = input("Enter username: ")
PASSWORD = getpass.getpass(f"Enter Password for {USERNAME}: ")

with open("config_template.j2") as f:
    ospf_template = Template(f.read())

def deploy_ospf():
    with open("devices.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Handle the multiple subnets
            subnet_list = row['physical_subnets'].split(";")
            
            # Generate the config
            config_text = ospf_template.render(
                loopback_ip=row['loopback_ip'],
                physical_subnets=subnet_list
            )

            device = {
                "device_type": "cisco_ios",
                "host": row['host'],
                "username": USERNAME,
                "password": PASSWORD,
            }

            try:
                with ConnectHandler(**device) as net_connect:
                    print(f"[*] Pushing OSPF to {row['host']}...")
                    print("Preview Config Below...")
                    print(config_text.splitlines())
                    net_connect.send_config_set(config_text.splitlines())
                    print(f"Configured: {row['host']} is now routing for {subnet_list}")
            except Exception as e:
                print(f"Error on {row['host']}: {e}")

if __name__ == "__main__":
    deploy_ospf()
```

## Execute the following commands to run
Ensure your router hosts and credentials are valid

`pip install netmiko jinja getpass csv`

`python deploy_ospf`
