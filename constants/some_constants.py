import os

from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('HHRU_CLIENT_ID')
CLIENT_SECRET = os.getenv('HHRU_CLIENT_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
USER_ACCESS_TOKEN = os.getenv('USER_ACCESS_TOKEN')

group_id = '-1002424181660'
dev_id = 2091023767
admins_id = [dev_id]
