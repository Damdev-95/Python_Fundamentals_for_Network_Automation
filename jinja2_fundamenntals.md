# Jinja2 Basics for Network Automation

Jinja2 is a **template engine** that allows network engineers to generate dynamic configurations using variables, loops, and logic.

Instead of writing repetitive configs manually, you create a **template once** and reuse it with different data.

---

##  Why Jinja2 for Network Engineers?

- ✅ Avoid repetitive CLI configuration
- ✅ Standardize configurations across devices
- ✅ Reduce human errors
- ✅ Scale to hundreds of devices easily

---

##  How Jinja2 Works

Jinja2 uses:
- **Variables** → Dynamic values
- **Conditionals** → Decision making
- **Loops** → Repeat configurations

---

## 📌 1. Variables

Variables are placeholders that get replaced with real values.

### 🧾 Template (`vlantemplate.j2`)
```jinja2
interface {{ interface }}
 description {{ description }}
 switchport mode access
 switchport access vlan {{ vlan }}
 spanning-tree portfast
 no shutdown
 ```

 ```python
 from jinja2 import Template


with open("vlantemplate.j2") as f:
template = Template(f.read())

data = {
    "interface": "GigabitEthernet1/0/1",
    "description": "User-PC",
    "vlan": 10
}

print(template.render(data))
```

## Multiple devices 

```python
from jinja2 import Template

# Load template
with open("vlan_template.j2") as f:
    template = Template(f.read())

devices = [ {"interface": "GigabitEthernet1/0/1","description": "HR-Desktop","vlan": 10},
           {"interface": "GigabitEthernet1/0/2","description": "Finance-Desktop","vlan": 20},
           {"interface": "GigabitEthernet1/0/3","description": "IT-Support","vlan": 30}
]

for device in devices:
    print(template.render(device))
    print("************************************")
```

## Condtionals(if/else)

below is the interfacetemplate.j2 file 
```jinja2
interface {{ interface }}
 description {{ description }}

{% if mode == "access" %}
 switchport mode access
 switchport access vlan {{ vlan }}

{% elif mode == "trunk" %}
 switchport mode trunk
 switchport trunk allowed vlan {{ vlan }}

{% endif %}
 no shutdown
 ```

 ```python
 from jinja2 import Template

# Load template
with open("interface_template.j2") as f:
    template = Template(f.read())

devices = [ {"interface": "GigabitEthernet1/0/1","mode": "access","description": "HR-Desktop","vlan": 10},
           {"interface": "GigabitEthernet1/0/2","mode": "access","description": "Finance-Desktop","vlan": 20},
           {"interface": "GigabitEthernet1/0/3","mode": "access", "description": "IT-Support","vlan": 30},
           {"interface": "GigabitEthernet1/0/48","mode": "trunk", "description": "UPLINK-TO-CORE-SWITCH","vlan": "10,20,30"}
]

for device in devices:
    print(template.render(device))
    print("************************************")
```

Real-Life Use Cases
🔹 Interface configuration automation
🔹 VLAN deployments
🔹 BGP / OSPF config generation
🔹 Customer onboarding templates
🔹 Data center provisioning

 

 
