Homework6   My URL application deployment is: http://52.33.235.189
Availiable registered users:
username/password:
Summer/123
David/123
Sara/123


1.I choose AWS EC2 as server to deploy my grumblr project.
First, I create a ubuntu instance and obtain the key-pair.Then launching a EC2 instance.
Then I login the aws sever which launched just now.
Then install the apache2, django,pip and python-ev.
Then change the apache's site configuration file whose path is in /etc/apache2/sites-available/.

2.I choose the mysql as the database.
First, install the mysql-server and python-mysqldb.
Then login the mysql and create a database.
Then change the setting.py file about the database configuration.
Finally Synchronize the database.

3.I also implement the functionality of sending email.When you click forget passwaord and enter a valid email.Then you will receive a 
link in your email.Then clicking the link,you could change your password.
