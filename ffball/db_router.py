from django.conf import settings
 
class DbRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read yahoo info, read from mongo_db.
        """
        try:
            return settings.DATABASE_APP_MAPPING[model._meta.app_label]
        except KeyError:
            return None;
        
    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        try:
            return settings.DATABASE_APP_MAPPING[model._meta.app_label]
        except KeyError:
            return None;


    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        ffball_obj = settings.DATABASE_APP_MAPPING.get(obj1._meta.app_label)
        yahoo_obj = settings.DATABASE_APP_MAPPING.get(obj2._meta.app_label)
        if yahoo_obj and ffball_obj:
            return yahoo_obj == ffball_obj
        return None


    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db in settings.DATABASE_APP_MAPPING.values():
            return settings.DATABASE_APP_MAPPING.get(model._meta.app_label) == db
        elif settings.DATABASE_APP_MAPPING.has_key(model._meta.app_label):
            return False
        return None
