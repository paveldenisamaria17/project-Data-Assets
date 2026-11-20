import requests

CID = "Rb9BQfzRYeQNzXcLiEYQm1UVh4om"
SECRET = "ed42756a-3624-4257-8e5c-f228b951f573"

for base in ("https://test-api.service.hmrc.gov.uk", "https://api.service.hmrc.gov.uk"):
    r = requests.post(base + "/oauth/token", data={
        "client_id": CID, "client_secret": SECRET, "grant_type": "client_credentials"})
    print(base, r.status_code, r.text[:150])