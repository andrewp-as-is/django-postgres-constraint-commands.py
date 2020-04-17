<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-postgres-constraint-commands.svg?longCache=True)](https://pypi.org/project/django-postgres-constraint-commands/)
[![](https://img.shields.io/pypi/v/django-postgres-constraint-commands.svg?maxAge=3600)](https://pypi.org/project/django-postgres-constraint-commands/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-postgres-constraint-commands.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-postgres-constraint-commands.py/)

#### Installation
```bash
$ [sudo] pip install django-postgres-constraint-commands
```

#### Pros
designed for Django projects with a large number of models:

+   no need `makemigrations` and `migrate`
+   no migration conflicts
+   integrity checks - drop and create constraints again
+   define tables with raw SQL (optional)

#### How it works
define models foreign and unique keys, run command

#### Settings
```python
INSTALLED_APPS = [
    ...
    'django_postgres_constraint_commands',
    ...
]
```

#### Examples
dev
```bash
$ python manage.py add_constraints # manage.py add_constraints app1 app2 ...
$ python manage.py drop_constraints # manage.py drop_constraints app1 app2 ...
```

prod
```bash
$ ssh user@hostname sudo docker run --env-file .env image python manage.py add_constraints
$ ssh user@hostname sudo docker run --env-file .env image python manage.py drop_constraints
```

`models.py`

```python
class Model1(models.Model):
    name = models.TextField(unique=True)
    obj = models.ForeignKey('Obj',related_name='+',on_delete=models.SET_NULL)

    class Meta:
        db_table = '<db_table>'
        managed=False

class Model2(models.Model):
    user = models.ForeignKey('User',related_name='+',on_delete=models.SET_NULL)
    obj = models.ForeignKey('Obj',related_name='+',on_delete=models.SET_NULL)

    class Meta:
        db_table = '<db_table>'
        managed=False
        unique_together = [('user', 'obj',)]
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>