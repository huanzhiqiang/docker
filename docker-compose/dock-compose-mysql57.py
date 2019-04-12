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
    restart: always
    networks:
      networkapp:
         ipv4_address: 172.19.0.2

networks:
  networkapp:
    ipam:
      config:
        - subnet: 172.19.0.0/16
