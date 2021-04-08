from django.db import models
from river.models.fields.state import StateField

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.username


class Grant(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = StateField(on_delete=models.CASCADE)

    class Meta:
        unique_together = ("group", "user")

    def __str__(self):
        return self.group.name + ", " + self.user.username


class LDAPSettings(models.Model):
    uri = models.CharField(max_length=256, unique=True, help_text="LDAP uri including protocol in the form of 'host:port', for example example.com")
    dn = models.CharField(max_length=256, blank=True)
    password = models.CharField(max_length=256, blank=True)
    usersOU = models.CharField(max_length=256)
    groupsOU = models.CharField(max_length=256)
