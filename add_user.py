import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'noguelle'
user.email = 'noguelle@gmail.com'
user.password = 'Fender1580'
user.superuser = True
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()