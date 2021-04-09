from django.test import TestCase
from .models import User, Group, Grant
from river.models import State
import django.contrib.auth.models as authModels

class SiteTests(TestCase):
    fixtures = ['newfixtures']

    def setUp(self):
        self.testUser = authModels.User.objects.create(username="testuser")
        self.approver_group = authModels.Group.objects.get(name="approver")
        self.testUser.groups.add(self.approver_group)
        self.state1 = State.objects.get(slug="needs-approval")
        self.user1 = User.objects.get(pk=1)
        self.group1 = Group.objects.get(pk=1)
        self.grant1 = Grant.objects.create(group_id=self.group1.id, user_id=self.user1.id, status=self.state1)

    def testFixtureLoadedUserExists(self):
        self.user1 = User.objects.get(pk=1)
        self.assertEquals(self.user1.username, 'user1')

    def testFixtureLoadedGroupExists(self):
        self.group1 = Group.objects.get(pk=1)
        self.assertEquals(self.group1.name, 'group1')

    def testFixtureState1Exists(self):
        self.state1 = State.objects.get(slug="needs-approval")

    def testGrantNeedsApproval(self):
        approvals = Grant.river.status.get_available_approvals(as_user=self.testUser)
        print(approvals)
        self.assertEqual(approvals[0].groups.all()[0], self.approver_group)
