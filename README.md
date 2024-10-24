# apache-guacd-installation
## Machine - AWS Ubuntu image
```
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.5 LTS
Release:	22.04
Codename:	jammy
```
### System Update:
1. `sudo apt update -y`
2. `sudo apt install -y build-essential libcairo2-dev libjpeg-turbo8-dev     libpng-dev libtool-bin libossp-uuid-dev libvncserver-dev     freerdp2-dev libssh2-1-dev libtelnet-dev libwebsockets-dev     libpulse-dev libvorbis-dev libwebp-dev libssl-dev     libpango1.0-dev libswscale-dev libavcodec-dev libavutil-dev     libavformat-dev`
### Install Apache Guacamole:
3. `wget https://downloads.apache.org/guacamole/1.5.5/source/guacamole-server-1.5.5.tar.gz`
4. `tar -xvf guacamole-server-1.5.5.tar.gz`
5. `cd guacamole-server-1.5.5`
6. `sudo ./configure --with-init-dir=/etc/init.d --enable-allow-freerdp-snapshots`
7. `sudo make`
8. `sudo make install`
9. `sudo ldconfig`
10. `sudo systemctl daemon-reload`
11 `sudo systemctl start guacd`
12 `sudo systemctl enable guacd`
13. `sudo mkdir -p /etc/guacamole/extensions`
14. `sudo mkdir -p /etc/guacamole/lib`

### Install Apache Guacamole Web App:
* `sudo apt install -y tomcat9 tomcat9-admin tomcat9-common tomcat9-user`
* `wget https://downloads.apache.org/guacamole/1.5.5/binary/guacamole-1.5.5.war`
* `sudo mv guacamole-1.5.5.war /var/lib/tomcat9/webapps/guacamole.war`
* `sudo systemctl restart tomcat9 guacd`   
NOTE: As of this, tomcat10 was not supported by Guacamole 1.5.5. 

### Setup Datbase:
* `sudo apt install mariadb-server`
* `sudo mysql_secure_installation`
    * follow the prompts
* `sudo mysql`
* ``` 
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
    CREATE DATABASE guacamole_db;
    CREATE USER 'guacamole_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT,INSERT,UPDATE,DELETE ON guacamole_db.* TO 'guacamole_user'@'localhost';
    FLUSH PRIVILEGES;

### Setup db extensions and libraries
* `wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.26.tar.gz`
* `tar -xf mysql-connector-java-8.0.26.tar.gz`
* `sudo cp mysql-connector-java-8.0.26/mysql-connector-java-8.0.26.jar /etc/guacamole/lib/`
* `wget https://downloads.apache.org/guacamole/1.5.5/binary/guacamole-auth-jdbc-1.5.5.tar.gz`
* `tar -xf guacamole-auth-jdbc-1.5.5.tar.gz`
* `sudo mv guacamole-auth-jdbc-1.5.5/mysql/guacamole-auth-jdbc-mysql-1.5.5.jar /etc/guacamole/extensions/`
* `cd guacamole-auth-jdbc-1.5.5/mysql/schema`
* `cat *.sql | mysql -u root -p guacamole_db`
* `sudo vim /etc/guacamole/guacamole.properties`
* ```
    # MySQL properties
    mysql-hostname: 127.0.0.1
    mysql-port: 3306
    mysql-database: guacamole_db
    mysql-username: guacamole_user
    mysql-password: [password]
* `sudo systemctl restart tomcat9 guacd mysql`

### Make Ubuntu ssh login password enabled
* `sudo adduser ea-user`
    * follow the prompts
* `sudo vim /etc/ssh/sshd_config`
    - Comment out the line containing: `Include /etc/ssh/sshd_config.d/*.conf`
    - Uncomment the line: `PasswordAuthenticaltion yes`
* `sudo service sshd restart`

### Browser Operations:
* `http://<server-ip>:8080/guacamole`
* In the username and password - enter `guacadmin` `guacadmin` which are default.
* Go to settings --> connection --> New Conection
* Give the connection name
* Network parameters:
    * Hostname should be internal-ip as its hosted on AWS
    * Port 22
* Save the connection
* Go to the User icon on top right and click Home
* Connect to the recently created connection.
* There you go.

NOTE: Haven't been able to use the pem file to login yet.