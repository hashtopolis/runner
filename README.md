# Hashtopolis Service Runner

Server background runner for Hashtopolis to run specific services.
The runner is packed into a zip (using `build.sh`) and then placed in `src/inc/runner/` in Hashtopolis. 
It is automatically then activated when the multicast feature gets enabled on the server.

## Prerequisites

This service is running only on Linux and you need to have the multicast enabled on your network device with the following commands:
```
sudo ifconfig <nic> multicast
sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev <nic>
```
Also you need python3 and the following python modules installed:
```
service
mysql-connector
```
 
