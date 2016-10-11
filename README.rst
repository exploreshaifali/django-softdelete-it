***********************
django-softdelete-it
***********************

Add soft-delete functionality to desired models.

Quick start
############

Follow steps mentioned below to add ``soft-delete`` feature in any model of your django app.

1. ``pip install django-softdelete-it``
2. Add ``soft_delete_it`` to your INSTALLED_APPS setting like this: ::

        INSTALLED_APPS = [
          ...
          'soft_delete_it',
         ]
3. Import ``SoftDeleteModel`` from soft_delete_it app to your model file like this: ::

      from soft_delete_it import SoftDeleteModel

4. Inherit ``SoftDeleteModel`` class to your model class. It will add following features:
    - ``objects`` manager's behavior will change such that:
        - ``delete()`` method which will soft delete instances
        - will always return only 'non soft deleted' objects
        - ``hard_delete()``` method to hard delete the objects
    - ``all_objects`` manager:
        - will always return both soft deleted and non soft deleted objects
        - ``hard_delete()`` method to hard delete the objects
        - ``only_deleted()`` method to return only soft deleted objects
        - ``undelete()`` method to un-delete soft-deleted objects

Example
**************
::

    from django.db import models
    from soft_delete_it.models import SoftDeleteModel


    class Author(SoftDeleteModel):
        name = models.CharField(max_length=50)
        dob = models.DateField()


    class Article(SoftDeleteModel):
        title = models.CharField(max_length=50)
        body = models.TextField(null=True)
        author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')


    Bob = Author.objects.create(name='bob', dob='2000-12-12')
    John = Author.objects.create(name='john', dob='1990-10-12')

    Author.objects.all() # return QuerySet with 2 objects
    Bob.delete() # Bob is soft-deleted
    Author.objects.all() # return QuerySet with 1 object, John
    Author.all_objects.all() # return QuerySet with 2 object, Bob and John
    Bob.undelete() # un-deletes Bob object
    Author.objects.all() # return QuerySet with 2 objects


    article1 = Article(title='Bob The Builder', body='')
    article1.author = Bob
    article1.save()

    Article.objects.all() # return QuerySet with 1 object, article1

    Bob.delete() # soft-deletes both Bob and article1 as Article's author field is on_delete_cascade and it Inherits SoftDeleteModel


If you are implementing a new ``Manager``  for a model, simply inherit ``SoftDeleteManager`` as well along with other Managers.

If you are implementing a new ``QuerySet`` for a model, you will need to do following:
    1. Inherit ``SoftDeleteQuerySet``
    2. Write Manager inheriting ``SoftDeleteManager`` which defines soft-delete functionality in it's ``__init__()`` method(as in the example) and override ``get_queryset()`` method(as in the example)
    3. Write model class inheriting ``SoftDeleteModel`` and uses above new defined ``Manager`` method(as in the example)


Example with QuerySet
*****************************

Lets create a QuerySet for Article such that if no author is provided while creating a new article, one default author will be added in object.
::

    #Creating a default author object first
    default_author = Author.objects.create(name='default')

    #Implementing QuerySet
    from soft_delete_it.models import SoftDeleteModel, SoftDeleteQuerySet, SoftDeleteManager

    class ArticleQuerySet(SoftDeleteQuerySet):

        def create(self, **kwargs):
            try:
                author = kwargs['author']
            except KeyError:
                kwargs['author'] = Author.objects.get(name='default')
            article = super(ArticleQuerySet, self).create(**kwargs)
            return article

    class ArticleManager(SoftDeleteManager):

        def __init__(self, *args, **kwargs):
            self.deleted_also = kwargs.get('deleted_also', False)
            super(ArticleManager, self).__init__(*args, **kwargs)

        def get_queryset(self):
            '''return all unsoft-deleted objects'''
            if self.deleted_also:
                return ArticleQuerySet(self.model)
            return ArticleQuerySet(self.model).filter(deleted=None)

    class Article(SoftDeleteModel):
        title = models.CharField(max_length=50)
        body = models.TextField(null=True)
        author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')

        objects = ArticleManager.from_queryset(ArticleQuerySet)()
        all_objects = ArticleManager.from_queryset(ArticleQuerySet)(deleted_also=True)


How soft-deletion functionality is implemented:
*****************************************************

1. Create a new soft_delete app, whole code for soft-deletion functionality is implemented in its models.py file.
2. Added an abstract ``SoftDeleteModel`` which contains a ``deleted`` attribute which is a ``UUIDField``. It will hold ``None`` for undeleted object and a new ``uuid4`` for deleted objects.
3. Implemented a ``SoftDeleteQuerySet`` to override default django's ``delete`` method to ``soft-delete`` objects instead of hard deleting them.
4. ``undelete()``, ``hard_delete()``, ``only_deleted()`` methods are implemented in same QuerySet class to provide extra features.
5. ``SoftDeleteManger`` implemented to use above QuerySet by overriding ``get_queryset()`` method.
6. QuerySet's delete method is necessary to override to support ``bulk_delete`` feature.
7. Call pre_delete and post_delete signals before and after the definition of above delete method.
8. Use NestedObjects from django admin utils to soft-delete all related objects.
9. Two managers, ``objects`` and ``all_objects`` to return undeleted, all objects are implemented.
