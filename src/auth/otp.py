import requests
def send_otp(phone):
 Token = "8DE4C0056B1E6E848B4F9F2E2FA6E7D3C8B6F349"
 Mobile = phone
 CodeLength = 5
 OptionalCode = ""
 
 url = "https://portal.amootsms.com/rest/SendQuickOTP"
 headers = {"Authorization": Token}
 data = {
     "Mobile": Mobile,
     "CodeLength": str(CodeLength),
     "OptionalCode": OptionalCode
 }
 
 response = requests.post(url, headers=headers, data=data)

 json_response = response.json()
 data_section = json_response.get("Data", {})
 generated_otp = data_section.get("Code")

 return generated_otp