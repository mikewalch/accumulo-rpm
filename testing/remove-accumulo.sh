#!/bin/bash

sudo systemctl stop accumulo-monitor.service accumulo-tserver.service accumulo-master.service accumulo-gc.service accumulo-tracer.service accumulo-multi-tserver-1.service accumulo-multi-tserver-2.service

sudo rpm -e accumulo-2.0.0-1.x86_64

sudo rm -f /var/log/accumulo/*
sudo rm -f /etc/accumulo/*
