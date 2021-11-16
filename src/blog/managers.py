from django.db.models import Manager


# create manager


class CategoryManager(Manager):
    def active(self):
        return self.filter(status=True)


class BlogManager(Manager):
    def get_published_post(self):
        return self.filter(status="p")
