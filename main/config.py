import os

PRODUCTION = os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Eng')
DEBUG = DEVELOPMENT = not PRODUCTION

FACEBOOK_APP_ID = "764417813716475"
FACEBOOK_APP_SECRET = "1f2a1f6f9a172fc9f5eff7cf3273c92d"
FACEBOOK_PAGE_ID = "103122593543457"
FACEBOOK_PAGE_ACCESS_TOKEN = "EAAK3OZBQZCHfsBAGsrDxuRrz4IlnlZBtNB7ObBUpKqZCf2fteWgr0AcaJPtSkRAiGUHY5XnBMI4S4THZAbo7yYgAelKxsZAcFrNDE1nl1TRqzNYX7RITivlZAKaUu3gNeFIZCZAeQRZAYkCtOZB9FTyfYB3H29Ev300fqYq9iMBMGXigDv0D6QKPoZAv"
FACEBOOK_WEBHOOK_VERIFY_TOKEN = "I_am_da_maaan!"
FACEBOOK_BOT_NAME = "jjmdev_utw"
