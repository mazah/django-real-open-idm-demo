from django.test import TestCase
from .models import User, Group

class SiteTests(TestCase):
    fixtures = ['djangorealidm']

    def testFixtureLoadedUserExists(self):
        s = User.objects.get(pk=1)
        self.assertEquals(s.username, 'user1')

    def testFixtureLoadedGroupExists(self):
        s = Group.objects.get(pk=1)
        self.assertEquals(s.name, 'group1')
