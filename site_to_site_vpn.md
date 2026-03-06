## Stop Overpaying for Cloud Networking: Building a Single-IP Egress over Site-to-Site VPN with StrongSwan

Cloud-native doesn’t always mean cloud-managed. Managed gateways promise a “set-and-forget” experience, but they often fall short when you need fine-grained control for complex site-to-site integrations.

By combining Linux networking with StrongSwan IPsec, you can build a custom egress point that performs Source Network Address Translation (SNAT) before encryption. This approach not only reduces costs—it also gives you the visibility and control that managed services usually hide.

## The "Hidden" Cost of Cloud Networking
Cloud providers like AWS and Azure make it easy to start, but "Managed" services come with a heavy tax:

- Managed Private NAT Gateway: ~$32/month + $0.045 per GB processed.

- VPN Gateway: ~$36/month + Data transfer fees.

The Problem: If you have 50 instances in a private subnet, the partner network on the other side of the VPN usually doesn't want to whitelist 50 different IP addresses. They want only one trusted IP.

## Archittecture diagram





Local Network
Component	Value
Ubuntu VPN Gateway	172.16.3.5
Local LAN	172.16.10.0/24
NAT Source IP	172.16.3.5
Public IP	5.5.5.5


Remote Network
Component	Value
Remote Gateway	35.156.227.84
Remote LAN	192.168.100.0/24

## Solution

Deploying a StrongSwan IPsec Site-to-Site VPN on Ubuntu Server with Private NAT ensuring that all internal hosts communicate with the remote network using a single source IP address.

By using a single Ubuntu instance as your gateway, you can "masquerade" your entire internal network. To the partner, every request looks like it’s coming from a single ip address

- Systemn Requirements
Ubuntu Server 20.04 / 22.04 / 24.04
Static Public IP address
Mininum of 2 vCPU, 4G RAM Server spec
Mininimum of 20 GB Storage

-  Install StrongSwan
sudo apt update
sudo apt upgrade -y
sudo apt install strongswan

Verify installation:
ipsec version

- Enable IP Forwarding
  The server must route traffic between Local network and VPN

- Configure StrongSwan
edit IPsec Configuration using the following commands;

sudo nano /etc/ipsec.conf


- Configure Pre-Shared Key
edit secrets file:

```
sudo nano /etc/ipsec.secrets
41.223.145.225 35.156.227.84 : PSK "StrongSharedSecretKey"
```

- Configure NAT for Single Source IP

The system will translate all LAN hosts to one IP address before entering the tunnel.

Add SNAT Rule
```
sudo iptables -t nat -A POSTROUTING \
-s 192.168.10.0/24 \
-d 10.50.0.0/16 \
-j SNAT --to-source 192.168.10.1
```

Verify iptables rules:
sudo iptables -t nat -L -v

- Start StrongSwan

Restart service:
sudo systemctl restart strongswan

Enable auto start:
sudo systemctl enable strongswan

- Verify VPN Tunnel

Check tunnel status:
sudo ipsec statusall

Testing Connectivity
From a LAN host:     
ping 10.50.1.10

Check NAT translation:
sudo iptables -t nat -L -v
