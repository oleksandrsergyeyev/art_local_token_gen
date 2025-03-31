# Artifactory Access Automation

This project provides a developer-friendly solution for interacting with Volvo Cars' Artifactory using a refreshable identity token, managed and stored securely via environment variables.

## ✅ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/oleksandrsergyeyev/art_local_token_gen.git
cd art_local_token_gen
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Create Initial Token (Non-Refreshable, One-Time Step)
1. Log into Artifactory
2. Go to **USER → Edit Profile**
3. Press **"Generate an Identity Token"**
4. Copy the token (this is TEMP_TOKEN_1)

### 5. Generate Refreshable Token
```bash
py .\token_refresher\generate_init_token_json.py
```
Then:
- Paste the **Identity Token** when prompted
- A new refreshable token will be saved to `token_refresher/init_tokens.json`

### 6. Enable Background Refresh Automatically
Run this once in **PowerShell as Administrator**:
```powershell
.\register_token_refresher_task.ps1
```
This adds a scheduled task to refresh your token in the background at login.

---

✅ **DONE!**
Your `.env` will be auto-created and kept up to date.

---

## 🔁 NOTE: Token Expiry
All tokens have a TTL (time to live). If your machine was off for an extended period and the token expired, you must repeat steps:
- **4:** Generate a new identity token
- **5:** Generate a new refreshable token using the updated identity token

---

## 💡 EXAMPLE: Using the Artifactory Client
To run a custom query and download a file:
```bash
python get_artifact_cli.py \
  --repo ARTBC-SUM-LTS \
  --version BSW_VCC_20.0.0 \
  --type PROD \
  --path SWLM/xcp_disabled/vbf \
  --out downloads/
```

This will search for the first file that matches the properties and path, and download it to the `downloads/` folder.

---

## 🔒 Security Note
`.env` stores both the access token and refresh token. Keep this file secure and **never commit it to version control**.

---

## 📄 License
Volvo Cars AB
