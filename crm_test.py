import os
from dotenv import load_dotenv

from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
from zcrmsdk.src.com.zoho.api.authenticator.store.file_store import FileStore
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zcrmsdk.src.com.zoho.crm.api.record.record_operations import RecordOperations

load_dotenv()

client_id = os.getenv("ZOHO_CLIENT_ID")
client_secret = os.getenv("ZOHO_CLIENT_SECRET")
refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")

# Zoho CRM user
user = UserSignature("coretrst@alchemisttechme.tech")

# US Data Center
environment = USDataCenter.PRODUCTION()

# OAuth refresh token
token = OAuthToken(
    client_id=client_id,
    client_secret=client_secret,
    token=refresh_token,
    token_type=TokenType.REFRESH,
    redirect_url="http://localhost:8000/oauth/callback"
)

# Store OAuth token locally
store = FileStore(os.path.join(os.getcwd(), "zoho_tokens.txt"))

# SDK configuration
sdk_config = SDKConfig(
    auto_refresh_fields=True,
    pick_list_validation=False
)

# Resource directory
resource_path = os.path.join(os.getcwd(), "resources")
os.makedirs(resource_path, exist_ok=True)

# Initialize Zoho CRM SDK
Initializer.initialize(
    user=user,
    environment=environment,
    token=token,
    store=store,
    sdk_config=sdk_config,
    resource_path=resource_path
)

print("Zoho CRM SDK initialized successfully!")

# Fetch Leads
record_operations = RecordOperations()

# response = record_operations.get_records("Leads")

print("Status Code:", response.get_status_code())

if response.get_object() is not None:
    print(response.get_object())
else:
    print("No data received.")