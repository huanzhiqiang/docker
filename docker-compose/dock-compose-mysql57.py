version: "3"
services:
  mysq3316:
    build:
      context: ./file
      dockerfile: Dockerfile
    hostname: mysql3316
    container_name: mysql3316-master
    ports:
      - 3316:3306
    environment:
      - MYSQL_DATABASE=eajucloud
      - MYSQL_ROOT_PASSWORD=anbang@123
    volumes:
      - /data/mysql/Mer_DT/3306/data:/var/lib/mysql:rw
      - /etc/localtime:/etc/localtime:ro
      - /data/mysql/Mer_DT/3306/log:/var/log/mysql
    restart_policy:
      condition: on-failure
    networks:
      networkapp:
         ipv4_address: 172.19.0.2

networks:
  networkapp:
    ipam:
      config:
        - subnet: 172.19.0.0/16


		
sed -n 's@IPADD@172.19.0.102@g' /opt/compose/5516/docker-compose.yml 
sed -n 's@NAMES@mysql5516@g' /opt/compose/5516/docker-compose.yml 
sed -n 's@PORT@5516@g' /opt/compose/5516/docker-compose.yml 
sed -n 's@DIR@5516@g' /opt/compose/5516/docker-compose.yml 
mkdir -p /data/mysql/5516/{data,tmp,binlog}
