"""Decode Gmail token and credentials from env vars before bot starts."""
import os
import base64

# Gmail token
token_b64 = os.environ.get("GMAIL_TOKEN_B64", "")
if token_b64:
    token_path = os.environ.get("GMAIL_TOKEN_PATH", "/app/gmail_token.pickle")
    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    with open(token_path, "wb") as f:
        f.write(base64.b64decode(token_b64))
    print(f"Gmail token written to {token_path}")
else:
    print("GMAIL_TOKEN_B64 not set")

# Gmail credentials (for token refresh)
creds_b64 = os.environ.get("GMAIL_CREDS_B64", "")
if creds_b64:
    creds_path = os.environ.get("GMAIL_CREDS_PATH", "/app/gmail_credentials.json")
    os.makedirs(os.path.dirname(creds_path), exist_ok=True)
    with open(creds_path, "wb") as f:
        f.write(base64.b64decode(creds_b64))
    print(f"Gmail credentials written to {creds_path}")

# Ensure DB directory exists
db_path = os.environ.get("DB_PATH", "/app/news.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
print("Startup complete")
