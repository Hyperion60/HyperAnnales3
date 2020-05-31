class HyperionRouter:
    route_user_app = {'auth', 'contenttypes', 'accounts', 'django', 'sessions', 'admin'}
    route_static_app = {'static_files'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_static_app:
            return 'pdf_ref'
        print(model._meta.app_label)
        if model._meta.app_label in self.route_user_app:
            return 'user_ref'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_static_app:
            return 'pdf_ref'
        if model._meta.app_label in self.route_user_app:
            return 'user_ref'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_static_app or
            obj2._meta.app_label in self.route_user_app
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_static_app:
            return db == 'pdf_ref'
        if app_label in self.route_user_app:
            return db == 'user_ref'
        return None