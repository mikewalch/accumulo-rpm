

## Build test release while version is SNAPSHOT

        cd /path/to/repo/accumulo/
        grep -rl 2.0.0-SNAPSHOT . | xargs sed -i 's/2\.0\.0\-SNAPSHOT/2\.0\.0/g'
        mvn clean package -DskipTests
