# CloudRunFunctionPostgreSQL

Local quickstart for exercising `hello_http` against the same Cloud SQL instance your Cloud Run service uses.

## Prerequisites
- Python 3.11+ installed locally
- `gcloud` CLI (for Application Default Credentials) and permission to connect to the Cloud SQL instance
- Service account with **Cloud SQL Client** + **Cloud SQL Instance User** (for IAM DB auth) — reuse `303227967106-compute@developer.gserviceaccount.com` or another user you control

## One-time setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Authenticate locally (writes ADC at ~/.config/gcloud/application_default_credentials.json)
gcloud auth application-default login
```

## Environment
Create a file like `.env.local` (or export in your shell):
```bash
export INSTANCE_CONNECTION_NAME="poc-openai-api-call:us-central1:api-project"
export DB_NAME="poc_open_ai"
export DB_USER="303227967106-compute@developer"  # IAM DB user

# For local runs prefer public IP; set to "false" unless you have VPC access to the private address
export PRIVATE_IP="false"

# Only if you use a downloaded key instead of ADC
# export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/sa-key.json"
```

> The Cloud Run YAML sets `PRIVATE_IP=true`, but that requires being on the VPC. When running from your laptop, use `PRIVATE_IP=false` unless you are connected via VPN/VPC peering.

Load the env vars in your shell: `source .env.local`.

## Run the function locally
```bash
functions-framework --target hello_http --port 8080 --debug
```

The Cloud SQL Python Connector will open an IAM-authenticated connection using the values above. On first connect you should see a line similar to:
```
PRIVATE_IP=false ip_type=PUBLIC DB_USER=303227967106-compute@developer
```

## Smoke test
In another terminal:
```bash
curl -i http://localhost:8080
```

Expected response on success (HTTP 200):
```
Success! Authenticated as: <cloud-sql-user>
```
If you get an error, the body will include the exception string coming from the connector (common causes: missing IAM permissions, wrong `INSTANCE_CONNECTION_NAME`, or private IP set to true without VPC access).

## Notes
- This local flow uses the same IAM DB authentication path as Cloud Run; no Cloud SQL Auth Proxy required.
- If you prefer private IP locally, ensure your machine has network reachability to the VPC (VPN/Interconnect) and leave `PRIVATE_IP=true`.
