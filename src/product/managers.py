from django.db.models import Manager


# create model manager


class CategoryManager(Manager):
    def active(self):
        return self.filter(status=True)


class ProductManager(Manager):
    def publish(self):
        return self.filter(status="pub")
