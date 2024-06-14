import requests
import json
# get access token


url_token = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
payload_token = json.dumps({
	"app_id": "cli_a6c93653ecf8d02f",
	"app_secret": "iqgCanHjBViHOw2e6nURbgKInpBgAHuD"
})


headers_token = {
  'Content-Type': 'application/json'
}
response_token = requests.request("POST", url_token, headers=headers_token, data=payload_token)
print(response_token.text)
token_data = response_token.json()
access_token = token_data.get('tenant_access_token')

# Kiểm tra xem có access token hay không
if access_token:
    # Lưu access token vào tệp
    with open('access_token.txt', 'w') as file:
        file.write(access_token)
else:
    print("Failed to retrieve access token")