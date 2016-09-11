# django-softdelete-it


Add soft-delete functionality to desired models.

### Quick start

Follow steps mentioned below to add `soft-delete` feature in any model of your django app.

1. Add "soft_delete_it" to your INSTALLED_APPS setting like this:
        ```
        INSTALLED_APPS = [
          ...
          'soft_delete_it',
         ]
         ```
2. Import `SoftDeleteModel` from soft_delete app to your model file like this:
      from soft_delete_it import SoftDeleteModel
3. Inherit `SoftDeleteModel` class to your model class. It will add following features:
    - `objects` manager's behavior will change such that:
        - `delete()` method which will soft delete instances
        - will always return  return only 'non soft deleted' objects
        - `hard_delete()` method to hard delete the objects
    - `all_objects` manager:
        - will always return both soft deleted and non soft deleted objects
        - `hard_delete()` method to hard delete the objects
        - `only_deleted()` method to return only soft deleted objects
        - `undelete()` method to un-delete soft-deleted objects


### Example
```
from django.db import models
from soft_delete_it.models import SoftDeleteModel


class Author(SoftDeleteModel):
    name = models.CharField(max_length=50)
    dob = models.DateField()


class Article(SoftDeleteModel):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')


a1 = Author.objects.create(name='Bob', dob='2000-1-2')
a2 = Author.objects.create(name='John', dob='1990-10-15')

Author.objects.all() # return QuerySet with 2 objects
a1.delete() # a1 is soft-deleted
Author.objects.all() # return QuerySet with 1 object, a2
Author.all_objects.all() # return QuerySet with 2 object, a1 and a2
a1.undelete() # un-deletes a1 object
Author.objects.all() # return QuerySet with 2 objects

article1 = Article.objects.create(title='Bob The Builder')
article1.author = a1
Article.objects.all() # return QuerySet with 1 object, article1

a1.delete() # soft-deletes both a1 and article1 as Article's author field is on_delete_cascade and it Inherits SoftDeleteModel

Article.all_objects.all() # returns QuerySet containing article objects both soft-deleted and unsoft-deleted
Article.all_objects.get(title='Bob The Builder').undelete()
```
