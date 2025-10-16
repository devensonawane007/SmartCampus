from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account JSON
SERVICE_ACCOUNT_FILE = 'gemini.json'

# Scopes required for Gemini (usually cloud-platform scope works)
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Initialize Gemini API client
# Replace 'gemini' and 'v1' with the correct API name/version
gemini_service = build('gemini', 'v1', credentials=credentials)

print("Gemini API client ready!")
