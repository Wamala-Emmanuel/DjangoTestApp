# import ldap
# import logging

# import environ

# env = environ.Env()
# environ.Env.read_env()

# LDAP = 'ldap://ug.sbicdirectory.com/'

# def ldap_authentication(sap_number, password):
#     connection = ldap.initialize(LDAP)

#     try:

#         connection.simple_bind_s(
#             '%s@ug.sbicdirectory.com' % sap_number,
#             password
#         )
#         return {
#             "status": True,
#             "message": "Success"
#         }

#     except ldap.SERVER_DOWN:
#         logging.error('LDAP server is not reachable')
#         return {
#             "status": False,
#             "error": "Server is not reachable"
#         }

#     except ldap.INVALID_CREDENTIALS:
#         logging.debug('Invalid LDAP credentials')
#         return {
#             "status": False,
#             "error": "Invalid User Credentials"
#         }

#     finally:
#         connection.unbind() 