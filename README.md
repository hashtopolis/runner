# Hashtopolis Service Runner

[![CodeFactor](https://www.codefactor.io/repository/github/s3inlc/hashtopolis-runner/badge)](https://www.codefactor.io/repository/github/s3inlc/hashtopolis-runner)
[![LoC](https://tokei.rs/b1/github/s3inlc/Hashtopolis-Runner?category=code)](https://github.com/s3inlc/Hashtopolis-Runner)
[![Test Status](https://travis-ci.org/s3inlc/hashtopolis-runner.svg?branch=master)](https://travis-ci.org/s3inlc/hashtopolis-runner)

Server background runner for Hashtopolis to run specific services.
The runner is packed into a zip (using `build.sh`) and then placed in `src/inc/runner/` in Hashtopolis. 
It is automatically then activated when the multicast feature gets enabled on the server.

## Prerequisites

This service is running only on Linux and you need to have the multicast enabled on your network device (Server & Agents!) with the following commands:
```
sudo ifconfig <nic> multicast
sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev <nic>
```
Also you need python3 and the following python modules installed:
```
service
mysql-connector
```
It's important that the network is able to run with multicast and that there are no devices attached which could slow down the process.
 
