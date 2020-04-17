from django.apps import apps
from django.db import connection
from django.core.management.base import BaseCommand


DJANGO_APPS_LABELS = [
    'admin',
    'auth',
    'contenttypes',
    'django',
    'sessions',
    'sites'
]


class PostgresCommand(BaseCommand):
    cursor = None
    app_labels = None

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.cursor = connection.cursor()

    def add_arguments(self, parser):
        super(PostgresCommand, self).add_arguments(parser)
        parser.add_argument('app_label', nargs='*', help='app_label')

    def init(self,**options):
        self.app_labels = self.get_app_labels()
        if 'app_label' in options and options.get('app_label'):
            self.app_labels = list(map(
                lambda a:a.lower().split('.')[-1],
                options.get('app_label')
            ))


    def is_matview(self,model):
        db_table = model._meta.db_table
        sql = """
SELECT oid
FROM pg_class
WHERE relnamespace::regnamespace::text=current_schema AND relname='%s' AND relkind='m'""" % db_table
        self.cursor.execute(sql)
        return bool(self.cursor.fetchall())

    def get_app_labels(self):
        app_labels = []
        for model in apps.get_models():
            app_labels+= [model._meta.app_label.lower()]
        return list(sorted(set(app_labels)))

    def get_models(self):
        for model in apps.get_models():
            app_label = model._meta.app_label.lower()
            if app_label in self.app_labels and app_label not in DJANGO_APPS_LABELS and not self.is_matview(model):
                yield model

    def has_table(self,db_table):
        sql = """
SELECT oid
FROM pg_class
WHERE relnamespace::regnamespace::text=current_schema AND relname='%s' AND relkind='r'
        """ % db_table
        self.cursor.execute(sql)
        return bool(self.cursor.fetchall())

    def has_constraint(self,db_table,conname):
        sql = """
SELECT oid
FROM pg_constraint
WHERE connamespace::regnamespace::text=current_schema AND conrelid::regclass::text='%s' AND conname='%s'""" % (db_table,conname)
        self.cursor.execute(sql)
        return bool(self.cursor.fetchall())

    def execute_sql(self,sql):
        print(sql.strip())
        self.cursor.execute(sql)
