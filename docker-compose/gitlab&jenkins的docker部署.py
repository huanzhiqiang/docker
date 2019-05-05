#1.安装docker,docker-compose工具；
mkdir /storage
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum list docker-ce --showduplicates | sort -r
yum install docker-ce-18.06.3.ce -y

#docker目录位置更改；
mkdir /etc/docker
cat > /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": ["https://ejburpg5.mirror.aliyuncs.com"],
  "graph": "/storage/docker"
}
EOF
mkdir /storage/docker
systemctl restart docker

#安装docker-compose工具；
curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version

############2.安装gitlab
mkdir /storage/{compose,apps}
mkdir /storage/apps/{config,logs,data} -p
cat >/storage/compose/gitlab_compose.yml <<EOF
version: '3'
services:
  gitlab:
    container_name: gitlab
	hostname: gitlab
    image: gitlab/gitlab-ce:latest
    restart: always
    environment:
      GITLAB_OMNIBUS_CONFIG: |
            external_url 'http://172.19.0.2'
    ports:
      - '9090:80'
      - '4443:443'
      - '2222:22'
    volumes:
      - '/storage/apps/gitlab/config:/etc/gitlab'
      - '/storage/apps/gitlab/logs:/var/log/gitlab'
      - '/storage/apps/gitlab/data:/var/opt/gitlab'
    networks:
      networkapp:
         ipv4_address: 172.19.0.2
networks:
  networkapp:
    ipam:
      config:
        - subnet: 172.19.0.0/16
EOF

##启动 
docker-compose -f gitlab_compose.yml up
##后台启动
docker-compose -f gitlab_compose.yml build up -d

#检查
docker images
dockers ps -a

################################jenkins部署
cd /storage/apps/tomcat
|-- apache-tomcat-8.5.37.tar.gz
|-- catalina.sh
|-- Dockerfile
|-- jdk-8u201-linux-x64.tar.gz
|-- jenkins.war
`-- server.xml
#Dockerfile的tomcat
[root@VM_0_5_centos tomcat]# cat Dockerfile 
FROM centos:7
MAINTAINER huanzhiqiang 
ADD jdk-8u201-linux-x64.tar.gz /usr/local
ADD apache-tomcat-8.5.37.tar.gz /usr/local
ENV JAVA_HOME /usr/local/jdk1.8.0_201
ENV CATALINA_HOME /usr/local/apache-tomcat-8.5.37
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/bin
RUN rm -fr /usr/local/apache-tomcat-8.5.37/webapps/*
COPY server.xml /usr/local/apache-tomcat-8.5.37/conf
COPY jenkins.war /usr/local/apache-tomcat-8.5.37/webapps
COPY catalina.sh /usr/local/apache-tomcat-8.5.37/bin
RUN chmod 777 /usr/local/apache-tomcat-8.5.37/bin/catalina.sh

EXPOSE 8080
ENTRYPOINT ["/usr/local/apache-tomcat-8.5.37/bin/catalina.sh", "run"]
#创建目录编排compose; 
mkdir -p /storage/apps/jenkins/{data,logs}

cat >/storage/compose/jenkins_compose.yml <<EOF
version: '3'
services:
  jenkins:
    restart: always
    hostname: jenkins
    container_name: jenkins
    build: ../apps/tomcat
    ports:
      - '8888:8080'
    volumes:
      - '/storage/apps/jenkins/data:/root/.jenkins'
      - '/storage/apps/jenkins/logs:/usr/local/apache-tomcat-8.5.37/logs'
      - '/etc/localtime:/etc/localtime:ro'
    networks:
      compose_networkapp:
        ipv4_address: 172.19.0.3
networks:
  compose_networkapp:
    external: true
EOF

#启动；
docker-compose -f jenkins_compose.yml build up -d

#####访问；
http://XXXX:8888/jenkins/     admin/QWE@1XXXXm
http://XXXX:9090/   root/QWE@1XXXXm