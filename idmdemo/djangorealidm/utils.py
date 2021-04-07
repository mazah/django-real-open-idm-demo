from ldap3 import Server, Connection, ALL


def ldap_sync(uri, dn=None, password=None):
    server = Server(uri, get_info=ALL)
    conn = Connection(server, dn,password, auto_bind=True)
    conn.search('dc=demo1,dc=freeipa,dc=org', '(objectclass=person)')
