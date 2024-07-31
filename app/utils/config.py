from os import environ

# Business central tenant
TENANT = environ.get('tenant')

# entra application credential
CLIENT_ID = environ.get('client_id')
CLIENT_SECRET = environ.get('client_secret')
SCOPE = environ.get('scope')
GRANT_TYPE = environ.get('grant_type')

# company names
ELATEC_GMBH = environ.get('elatec_gmbh')
ELATEC_SYSTEM_GMBH = environ.get('elatec_system_gmbh')
SESAMSEC_GMBH = environ.get('sesamsec_gmbh')
ELATEC_INC = environ.get('elatec_inc')