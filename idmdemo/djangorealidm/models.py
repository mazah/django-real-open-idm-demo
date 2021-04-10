from django.db import models
from river.models.fields.state import StateField
from django.db.models import Q

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    surname = models.CharField(max_length=20, unique=False)
    givenname = models.CharField(max_length=20, unique=False)
    description = models.TextField(max_length=500, unique=False)
    externalid = models.CharField(max_length=20, unique=True)
    expirydate = models.DateField()

    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(max_length=256, unique=True)
    groups = models.ManyToManyField(Group)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Grant(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    status = StateField(on_delete=models.CASCADE)

    class Meta:
        unique_together = [["group", "user"], ["role", "user"]]
        constraints = [
            models.CheckConstraint(
                check=Q(group__isnull=False) | Q(role__isnull=False),
                name='not_both_null'
            ),
            models.CheckConstraint(
                check=Q(group__isnull=True) | Q(role__isnull=True),
                name='either_null'
            )
        ]

    def __str__(self):
        if self.group:
            return "g " + self.group.name + ", " + self.user.username
        else:
            return "r " + self.role.name + ", " + self.user.username


