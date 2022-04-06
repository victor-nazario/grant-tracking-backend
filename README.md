# grant-tracking-backend


#Instructions on Setting Postgresql and pgAdmin for Development Environments
* Make sure [Docker](https://docs.docker.com/get-docker/) is installed in your system.
&nbsp; 

  
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
