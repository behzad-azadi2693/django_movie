class MovieDb:
    route_app_labels = {'auth','sessions','contenttypes','admin', 'accounts'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'movie_db'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'movie_db'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'movie_db'
        return None

class MessageDb:
    route_app_labels = {'movie'} 

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'message_db'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'message_db'
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'message_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
            return True
        return None