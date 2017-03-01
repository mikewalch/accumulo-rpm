#!/bin/bash

./remove-accumulo.sh

set -e

sudo rpm -i accumulo-2.0.0-1.x86_64.rpm

sudo sed -i -e 's/export HADOOP_PREFIX=.*/export HADOOP_PREFIX=\/opt\/hadoop-2\.7\.3/' /etc/accumulo/accumulo-env.sh
sudo sed -i -e 's/export ZOOKEEPER_HOME=.*/export ZOOKEEPER_HOME=\/opt\/zookeeper-3\.4\.9/' /etc/accumulo/accumulo-env.sh
sudo sed -i -e 's/<value><\/value>/<value>hdfs\:\/\/localhost\:9000\/accumulo<\/value>/' /etc/accumulo/accumulo-site.xml
sudo sed -i -e 's/<\/configuration>/<property>\n<name>tserver\.port\.search<\/name>\n<value>true<\/value>\n<\/property>\n<property>\n<name>replication\.receipt\.service\.port<\/name><value>0<\/value>\n<\/property>\n<\/configuration>/' /etc/accumulo/accumulo-site.xml

/opt/hadoop-2.7.3/bin/hdfs dfs -rm -r /accumulo || true
/opt/hadoop-2.7.3/bin/hdfs dfs -chmod 777 /
sudo -u accumulo accumulo init --clear-instance-name --instance-name "centos" --user "root" --password "secret"

sudo systemctl daemon-reload

sudo systemctl start accumulo-monitor.service accumulo-master.service accumulo-gc.service accumulo-tracer.service
if [ "$1" == "--multi" ]; then
  sudo systemctl start accumulo-multi-tserver-1.service accumulo-multi-tserver-2.service
else
  sudo systemctl start accumulo-tserver.service 
fi
