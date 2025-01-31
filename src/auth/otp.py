import requests

Token = "8DE4C0056B1E6E848B4F9F2E2FA6E7D3C8B6F349"
Mobile = "9306501396"
CodeLength = 4
OptionalCode = "12352"

url = "https://portal.amootsms.com/rest/SendQuickOTP"
headers = {"Authorization": Token}
data = {
    "Mobile": Mobile,
    "CodeLength": str(CodeLength),
    "OptionalCode": OptionalCode
}

response = requests.post(url, headers=headers, data=data)
json_response = response.text  # خروجی

print(json_response)
