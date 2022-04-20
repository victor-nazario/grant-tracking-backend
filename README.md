# grant-tracking-backend

It's important that developers or administrators trying to test or dploy the project follow the 
steps outlined before, as the application comprises various containers communicating between them.

# How to create a network for the containers to communicate in the same space
* Make sure [Docker](https://docs.docker.com/get-docker/) is installed in your system.
&nbsp; 

* Execute ```$ docker network create --subnet=172.20.128.0/16 gtb-net``` 
* In the case there is already an overlaping pool on the address space, change it on the 
command and in the docker-compose.


#Instructions on Setting Postgresql and pgAdmin for Development Environments

* On the terminal, mv to the project root. Once in the root
execute ``$ docker-compose up`` this will download necessary dependencies and set up the containers as needed 
for the application to work.
&nbsp; 

  
* Once the containers are running (verify with ``$ docker ps``) on a web browser visit 
[http://localhost:5050/](http://localhost:5050/) and login with username ``admin@admin.com`` and password ``root``.
&nbsp; 

  
* Right click on ``Servers`` and then select ``Create > Server``, in the screen name the db as desired and then select 
``connection`` from the tabs. In the connections window, provide your Postgres container name as hostname. 
(Can be found by copying the value from ``NAME`` after executing ``$ docker ps``). Provide ``root`` as 
both password and username.
