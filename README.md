Welcome to this project.

There is currently no description on what this project is.

If you are not able to run this project after a clone here are the reasons :

* This project is based on LXD(Linux Container) : There are 3 container instance running :
- One running Django, nginx and uwsgi and celery ( a Juju machine)
- One running Postgresql(JujuCharm)
- One running RabbitMQ(JujuCharm).

# The django database settings are in environment variables.
