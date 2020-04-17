from ._commands import PostgresCommand


class Command(PostgresCommand):
    def handle(self, *args, **options):
        self.init(**options)
        self.drop_foreign_key_constraints()
        self.drop_unique_constraints()
        # self.drop_primary_key_constraints()

    def drop_foreign_key_constraints(self):
        for model in self.get_models():
            db_table = model._meta.db_table
            sql = """
SELECT conname
FROM pg_constraint
WHERE connamespace::regnamespace::text=current_schema AND conrelid::regclass::text='%s' AND contype='f'
            """ % db_table
            self.cursor.execute(sql)
            for r in self.cursor.fetchall():
                fk_conname = r[0]
                sql = """
ALTER TABLE ONLY public.%s
    DROP CONSTRAINT %s;""" % (db_table,fk_conname)
                print(sql.strip())
                self.cursor.execute(sql)

    def drop_unique_constraints(self):
        for model in self.get_models():
            db_table = model._meta.db_table
            sql = """
SELECT conname
FROM pg_constraint
WHERE connamespace::regnamespace::text=current_schema AND conrelid::regclass::text='%s' AND contype='u'
            """ % db_table
            self.cursor.execute(sql)
            for r in self.cursor.fetchall():
                u_conname = r[0]
                sql = """
ALTER TABLE ONLY public.%s
    DROP CONSTRAINT %s;""" % (db_table,u_conname)
                print(sql.strip())
                self.cursor.execute(sql)

    def drop_primary_key_constraints(self):
        for model in self.get_models():
            db_table = model._meta.db_table
            sql = """
SELECT conname
FROM pg_constraint
WHERE connamespace::regnamespace::text=current_schema AND conrelid::regclass::text='%s' AND contype='p'
            """ % db_table
            self.cursor.execute(sql)
            for r in self.cursor.fetchall():
                pk_conname = r[0]
                sql = """
ALTER TABLE ONLY public.%s
    DROP CONSTRAINT %s;""" % (db_table,pk_conname)
                print(sql.strip())
                self.cursor.execute(sql)
