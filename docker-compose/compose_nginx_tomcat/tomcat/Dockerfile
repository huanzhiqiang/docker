FROM centos:6
MAINTAINER huanzhiqiang 
ADD jdk-8u45-linux-x64.tar.gz /usr/local
ENV JAVA_HOME /usr/local/jdk1.8.0_45
ADD apache-tomcat-8.0.46.tar.gz /usr/local
COPY server.xml /usr/local/apache-tomcat-8.0.46/conf

EXPOSE 8080
ENTRYPOINT ["/usr/local/apache-tomcat-8.0.46/bin/catalina.sh", "run"]
