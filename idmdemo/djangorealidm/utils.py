from ldap3 import Server, Connection, ALL, NTLM, Reader, ObjectDef, SUBTREE
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
from ldap3.extend.microsoft.removeMembersFromGroups import ad_remove_members_from_groups as removeUsersInGroups
from django.conf import settings
from django.utils import timezone


def check_grant_in_effect(grant_obj):
    if grant_obj.not_valid_before and grant_obj.not_valid_after:
        return grant_obj.not_valid_before <= timezone.now() <= grant_obj.not_valid_after
    else:
        return grant_obj.not_valid_before <= timezone.now()


class Sync(object):
    def __init__(self):
        uri = settings.REAL_IDM["LDAP_SERVER"]
        dn = settings.REAL_IDM.get("BIND_USER")
        password = settings.REAL_IDM.get("BIND_PASSWD")
        self.ldap_user_attr = settings.REAL_IDM.get("LDAP_USER_ATTRIBUTE", "sAMAccountName")
        self.search_base = settings.REAL_IDM["SEARCH_BASE"]
        self.conn = self.ldap_begin(uri, dn, password)

    def ldap_begin(self, uri, dn=None, password=None, port=389, use_ssl=False):
        server = Server(uri, get_info=ALL)
        conn = Connection(server, dn, password, auto_bind=True)
        return conn

    def find_userdn_by_username(self, username):
        self.conn.search(
            search_base=self.search_base,
            search_filter="({}={})".format(self.ldap_user_attr, username),
            search_scope=SUBTREE,
            attributes=[self.ldap_user_attr]
        )
        try:
            userDn = self.conn.response[0]["dn"]
        except Exception as e:
            print(e)
            return

        return userDn

    def add_user_to_group(self, username, groupDn):
        userDn = self.find_userdn_by_username(username)
        print("Adding user {} to group {}".format(userDn, groupDn))
        addUsersInGroups(self.conn, userDn, groupDn, raise_error=True)

    def remove_user_from_group(self, username, groupDn):
        userDn = self.find_userdn_by_username(username)
        print("Removing user: '{}' from group '{}'".format(userDn, groupDn))
        removeUsersInGroups(self.conn, userDn, groupDn, fix=True, raise_error=True)

    def sync_users_single_group(self, users, groupDn):
        self.conn.search(
            search_base=self.search_base,
            search_filter="(&(objectCategory=user)(memberOf={}))".format(groupDn),
            search_scope=SUBTREE,
            attributes=[self.ldap_user_attr]
        )
        users_in_group = [str(user[self.ldap_user_attr]) for user in self.conn.entries]
        print("Users in group: '{}': {}".format(groupDn, users_in_group))
        for user in users:
            if user not in users_in_group:
                self.add_user_to_group(user, groupDn)

        group_diff = list(set(users_in_group) - set(users)) # Users in LDAP group that shouldn't be
        for user in group_diff:
            self.remove_user_from_group(user, groupDn)

    def sync_users_groups(self, users, groups=[]):
        for group in groups:
            self.conn.search(
                search_base=self.search_base,
                search_filter="(&(objectClass=group)(cn={}))".format(group),
                search_scope=SUBTREE,
            )
            groupDn = self.conn.response[0]["dn"]

            self.sync_users_single_group(users, groupDn)

        return

