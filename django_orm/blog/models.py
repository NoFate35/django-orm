#from django.db import models
'''

class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(TimestampedModel):
    name = models.CharField(max_length=30)


class Post(TimestampedModel):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)
    views = models.DecimalField(max_digits=10, decimal_places=2)
    '''
from django.db import models, transaction


class Project(models.Model):
    name = models.CharField(max_length=200)

    @classmethod
    def reorganize(cls, assignments):
        # BEGIN (write your solution here)
        from django.core.exceptions import ObjectDoesNotExist
        with transaction.atomic():
            for candidat, project_val in assignments.items():
                try:
                    worker = Worker.objects.get(id=candidat)
                    reorganize_project = Project.objects.get(id=project_val)
                except: ObjectDoesNotExist("несуществующий проект!")
                print('worker:', worker, 'project:', reorganize_project)
                worker.project = reorganize_project
                worker.save()
            print('assigment keys', assignments.keys())
            not_workers = Worker.objects.exclude(id__in=assignments.keys())
        # END
        return None

class Worker(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(
        Project,
        null=True,
        on_delete=models.SET_NULL,
    )
