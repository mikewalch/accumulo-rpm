#!/bin/bash

sudo yum install wget vim java-1.8.0-openjdk-devel

if ! grep -q "JAVA_HOME" ~/.bashrc; then
  cat <<EOF >> ~/.bashrc
export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk"
alias ssh="ssh -A"
EOF
fi
source ~/.bashrc

wget -c http://apache.claz.org/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz
wget -c http://apache.claz.org/zookeeper/zookeeper-3.4.9/zookeeper-3.4.9.tar.gz

HADOOP_PREFIX=/opt/hadoop-2.7.3
ZOOKEEPER_HOME=/opt/zookeeper-3.4.9

pkill -f hadoop\\.hdfs
pkill -f QuorumPeerMain

sudo chmod 777 /opt/
rm -rf $HADOOP_PREFIX
rm -rf $ZOOKEEPER_HOME

tar xzf zookeeper-3.4.9.tar.gz -C /opt/
cp $ZOOKEEPER_HOME/conf/zoo_sample.cfg $ZOOKEEPER_HOME/conf/zoo.cfg
$ZOOKEEPER_HOME/bin/zkServer.sh start

tar xzf hadoop-2.7.3.tar.gz -C /opt/

cat <<EOF > $HADOOP_PREFIX/etc/hadoop/core-site.xml
<configuration>
  <property>
    <name>fs.defaultFS</name> 
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
EOF

cat <<EOF > $HADOOP_PREFIX/etc/hadoop/hdfs-site.xml
<configuration>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///opt/data/hadoop/name</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///opt/data/hadoop/data</value>
  </property>
</configuration>
EOF

$HADOOP_PREFIX/bin/hdfs namenode -format
$HADOOP_PREFIX/sbin/start-dfs.sh
