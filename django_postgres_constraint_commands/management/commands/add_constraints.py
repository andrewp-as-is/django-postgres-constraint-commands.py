from django.db import models

from ._commands import PostgresCommand
from ._utils import getmd5

ON_DELETE = {
    models.CASCADE:'CASCADE',
    models.SET_NULL:'SET NULL',
    models.PROTECT:'RESTRICT',
    models.DO_NOTHING:'NO ACTION'
}


class Command(PostgresCommand):
    def handle(self, *args, **options):
        self.app_labels = self.get_app_labels()
        if args:
            self.app_labels = list(map(lambda app_label:app_label.lower().split('.')[-1],args))
        # self.add_primary_key_constraints()
        self.add_unique_constraints()
        self.add_foreign_key_constraints()

    def add_primary_key_constraints(self):
        for model in self.get_models():
            app_label = model._meta.app_label.lower()
            db_table = model._meta.db_table
            pk_conname = '%s_pkey' % db_table
            for f in filter(lambda f:f.primary_key,model._meta.fields):
                sql = """
ALTER TABLE ONLY public.%s
    ADD CONSTRAINT %s PRIMARY KEY (%s);""" % (db_table,pk_conname,f.attname)
                if self.has_table(db_table) and not self.has_constraint(db_table,pk_conname):
                    self.cursor.execute(sql)

    def add_unique_constraints(self):
        for model in self.get_models():
            db_table = model._meta.db_table
            for f in filter(lambda f:f.unique and not f.primary_key,model._meta.fields):
                u_conname = '%s_%s_key' % (db_table,f.name) # index, must be unique
                sql = """
ALTER TABLE ONLY public.%s
    ADD CONSTRAINT %s UNIQUE (%s);""" % (db_table,u_conname,f.attname)
                if self.has_table(db_table) and not self.has_constraint(db_table,u_conname):
                    self.cursor.execute(sql)
            if not model._meta.unique_together:
                continue
            unique_together = model._meta.unique_together
            if not any(isinstance(el, (list,tuple)) for el in model._meta.unique_together):
                unique_together = [model._meta.unique_together]
            for fieldnames in unique_together:
                attnames = list(map(
                    lambda f:model._meta.get_field(f).attname,fieldnames
                ))
                conname = '%s_%s_uniq' % (db_table,'_'.join(attnames))
                if len(conname)>63:
                    conname = '%s_%s_uniq' % (db_table,getmd5(','.join(attnames)))
                sql = """
ALTER TABLE ONLY public.%s
    ADD CONSTRAINT %s UNIQUE (%s);""" % (db_table,conname,','.join(attnames))
                if self.has_table(db_table) and not self.has_constraint(db_table,conname):
                    print(sql.strip())
                    self.cursor.execute(sql)

    def add_foreign_key_constraints(self):
        for model in self.get_models():
            db_table = model._meta.db_table
            for f in filter(lambda f:f.remote_field,model._meta.fields):
                fk_conname = '%s_fk_%s_id' % (f.attname,f.remote_field.model._meta.db_table)
                on_delete = ON_DELETE[f.remote_field.on_delete]
                sql = """
ALTER TABLE ONLY public.%s
    ADD CONSTRAINT %s
    FOREIGN KEY (%s) REFERENCES %s(id) ON DELETE %s DEFERRABLE INITIALLY DEFERRED;""" % (db_table,fk_conname,f.attname,f.remote_field.model._meta.db_table,on_delete)
                if self.has_table(db_table) and not self.has_constraint(db_table,fk_conname):
                    print(sql.strip())
                    self.cursor.execute(sql)


"""
python manage.py add_constraints
python manage.py drop_constraints
"""
