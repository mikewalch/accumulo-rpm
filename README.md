# Accumulo RPM

This project creates an Accumulo RPM using a binary tarball release of Accumulo.

Currently, the RPM has been tested to work with following versions of Accumulo & Linux:

* Accumulo: 2.0.0-SNAPSHOT
* Linux: CentOS 7

## Build RPM

1. Install rpmbuild

	      sudo yum install rpm-build

2. Build a non-snapshot version of Accumulo and copy to 

        cd /path/to/repo/accumulo/
        grep -rl "2.0.0-SNAPSHOT" . | xargs sed -i 's/2\.0\.0\-SNAPSHOT/2\.0\.0/g'
        mvn clean package -DskipTests

3. Copy the RPM to your accumulo-rpm repo and use it to build the RPM.
	
        cp assemble/target/accumulo-2.0.0-bin.tar.gz /path/to/accumulo-rpm
        cd /path/to/accumulo-rpm
        ./build.sh accumulo-2.0.0-bin.tar.gz

4. The will be placed in testing/

## Test RPM

1. Launch a test CentOS 7 VM

2. Copy the build RPM and test scripts to the VM.

        scp ./testing/* centos@1.2.3.4:~/

3. Install and set up Accumulo's dependencies

        ./setup-deps.sh

4. Set up Accumulo using the command below or by following the installation instructions
   in the next section. Add `--multi` to command to set up multiple tablet servers.

        ./setup-accumulo.sh

## Installation Instructions 

1. Install Accumulo RPM

        sudo rpm -i accumulo-2.0.0-1.x86_64.rpm

2. Copy and edit configuration files. Make sure to set `HADOOP_PREFIX` and `ZOOKEEPER_HOME`
   in accumulo.conf:

        sudo -u accumulo cp /etc/accumulo/examples/accumulo.conf /etc/accumulo
        sudo -u accumulo cp /etc/accumulo/examples/accumulo-site.xml /etc/accumulo-site.xml
        vim /etc/accumulo/accumulo.conf

3. Initialize Accumulo

        sudo -u accumulo accumulo init

4. Start Accumulo services

        sudo systemctl start accumulo-monitor.service accumulo-tserver.service accumulo-master.service accumulo-gc.service accumulo-tracer.service

   The command above does not provide feedback as to if the process started. Use `systemctl`
   to check status and `journalctl` to view sytstemd logs. Accumulo services will log to
   `/var/log/accumulo` when started.

5. (Optional) Configure Accumulo to start automatically when the system boots up.

        sudo systemctl daemon-reload
        sudo systemctl enable accumulo-monitor.service accumulo-tserver.service accumulo-master.service accumulo-gc.service accumulo-tracer.service

# Start multiple tablet servers

1. Add the following to accumulo-site.xml

        <property>
          <name>tserver.port.search</name>
          <value>true</value>
        </property>
        <property>
          <name>replication.receipt.service.port</name>
          <value>0</value>
        </property>

2. Use `accumulo-multi-tserver-*` service to start multiple tservers

        sudo systemctl start accumulo-multi-tserver-1.service accumulo-multi-tserver-2.service

# Enable NUMA control on tablet servers

1. Install NUMA control

        sudo yum install numactl

2. Configure NUMA control policy in SystemD unit files. The configuration depends on your
   hardware. To execute each tablet server on its own processer core, add the following to 
   `/usr/lib/systemd/system/accumulo-multi-tserver-1.service`:

      Environment="ACCUMULO_JAVA_PREFIX=numactl --physcpubind 0"

   And add the following to `/usr/lib/systemd/system/accumulo-multi-tserver-2.service`

      Environment="ACCUMULO_JAVA_PREFIX=numactl --physcpubind 1"
