##1.
FROM centos:7
RUN yum -y install gcc gcc-c++ make automake cmake wget
RUN groupadd mysql; useradd -r -M -u 39 -s /sbin/nologin -g mysql mysql
RUN mkdir /usr/local/mysql; mkdir /data/mysql/db -p
RUN yum install gcc gcc-c++ ncurses-devel bison bison-devel -y
RUN wget http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.29.tar.gz
RUN tar zxf mysql-5.6.29.tar.gz -C /usr/src/
WORKDIR /usr/src/mysql-5.6.29
RUN cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DMYSQL_DATADIR=/data/mysql/db -DSYSCONFDIR=/etc -DMYSQL_TCP_PORT=3306 -DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_MYISAM_STORAGE_ENGINE=1 -DENABLED_LOCAL_INFILE=1 -DWITH_PARTITION_STORAGE_ENGINE=1 -DDEFAULT_CHARSET=utf8 -DEXTRA_CHARSETS=all -DDEFAULT_COLLATION=utf8_general_ci -DWITH-MYSQLD-LDFLAGS=-all-static -DWITH-CLIENT-LD-FLAGS=-all-static -DWITH_DEBUG=0 && gmake && gmake install
RUN chown -R root:mysql /usr/local/mysql/ && chown -R mysql:mysql /data/mysql/db/
RUN chmod 775 /usr/src/mysql-5.6.29/scripts/mysql_install_db.sh
RUN /usr/src/mysql-5.6.29/scripts/mysql_install_db.sh --basedir=/usr/local/mysql --datadir=/data/mysql/db --no-defaults --user=mysql
RUN cp /usr/src/mysql-5.6.29/support-files/my-default.cnf /etc/my.cnf
RUN cp /usr/src/mysql-5.6.29/support-files/mysql.server /etc/init.d/mysqld
RUN chmod -R 775 /etc/init.d/mysqld && /etc/init.d/mysqld start
RUN echo -e '#!/bin/bash\nexport PATH=$PATH:/usr/local/mysql/bin' >/etc/profile.d/mysql.sh
RUN source /etc/profile





#2.	
FROM harbor.nedy.com/atlas/centos7.5-base:7.5.1804	
MAINTAINER lv "lvtong@live.com"	# update source	# yum update -y	# Install mysql5.7.17	
RUN mkdir /apps/ && cd /apps && curl -O -s download.nedy.com/mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz && tar xf mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz && mv mysql-5.7.17-linux-glibc2.5-x86_64 mysql# #Add mysql.service	
ADD mysql.service /usr/lib/systemd/system/mysql.service	
RUN systemctl enable mysql.service	
# Expose ports	
EXPOSE 3306	
# Define default command	
#ENTRYPOINT  mysql.service status	
RUN systemctl status mysql.service



#3.
FROM centos:7
MAINTAINER huanzhiqiang
RUN yum install libaio numactl net-tools vim -y
RUN groupadd mysql && useradd -r -g mysql -M -s /bin/false mysql
RUN mkdir -p /data/mysql/{data,binlog,tmp} && chown -R mysql:mysql /data/mysql 
ADD mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz /usr/local
RUN ln -s /usr/local/mysql-5.7.24-linux-glibc2.12-x86_64 /usr/local/mysql && chown -R mysql:mysql /usr/local/mysql
COPY my.cnf /etc
RUN echo export PATH='${PATH}':/usr/local/mysql/bin > /etc/profile.d/mysql.sh && source /etc/profile.d/mysql.sh
RUN /usr/local/mysql/bin/mysqld --initialize-insecure --basedir=/usr/local/mysql --datadir=/data/mysql/data --user=mysql && /usr/local/mysql/bin/mysqld_safe --defaults-file=/etc/my.cnf &
EXPOSE 3306
CMD /usr/sbin/init




###############宿主机创建目录；
mkdir -p /data/mysql/{data,tmp,binlog}
##################
/usr/local/mysql/bin/mysqld --initialize-insecure --basedir=/usr/local/mysql --datadir=/data/mysql/data --user=mysql
/usr/local/mysql/bin/mysqld_safe --defaults-file=/etc/my.cnf &