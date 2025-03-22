import requests
from .logger import logger
from fastapi import HTTPException
from typing import Optional

def send_otp(phone: str, otp_code: str = None) -> Optional[str]:
    """
    ارسال OTP از طریق سرویس پیامک
    """
    Token = "8DE4C0056B1E6E848B4F9F2E2FA6E7D3C8B6F349"
    Mobile = phone
    CodeLength = 5
    OptionalCode = otp_code if otp_code else ""
    
    url = "https://portal.amootsms.com/rest/SendQuickOTP"
    headers = {"Authorization": Token}
    data = {
        "Mobile": Mobile,
        "CodeLength": str(CodeLength),
        "OptionalCode": OptionalCode
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        print(f"Raw API Response: {response.text}")
        
        try:
            json_response = response.json()
        except ValueError as e:
            logger.error(f"Failed to parse API response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="خطا در پردازش پاسخ سرویس پیامک"
            )
            
        if not json_response:
            logger.error("Empty API response")
            raise HTTPException(
                status_code=500,
                detail="پاسخ خالی از سرویس پیامک"
            )
            
        # بررسی وضعیت پاسخ
        status = json_response.get("Status")
        if status == "User_Expired":
            logger.error("SMS API token is expired or invalid")
            raise HTTPException(
                status_code=500,
                detail="خطا در احراز هویت سرویس پیامک"
            )
        elif status == "Invalid_Mobile":
            logger.error(f"Invalid mobile number: {Mobile}")
            raise HTTPException(
                status_code=400,
                detail="شماره موبایل نامعتبر است"
            )
        elif status != "Success":
            logger.error(f"Unexpected API status: {status}")
            raise HTTPException(
                status_code=500,
                detail=f"خطای سرویس پیامک: {status}"
            )
            
        data_section = json_response.get("Data", {})
        if not data_section:
            logger.error(f"No Data section in response: {json_response}")
            raise HTTPException(
                status_code=500,
                detail="خطا در دریافت کد تایید"
            )
            
        generated_otp = data_section.get("Code")
        if not generated_otp:
            logger.error(f"No Code in Data section: {data_section}")
            raise HTTPException(
                status_code=500,
                detail="خطا در دریافت کد تایید"
            )
        
        logger.info(f"OTP sent successfully to {Mobile}: {generated_otp}")
        print(f"Generated OTP for {Mobile}: {generated_otp}")
        return generated_otp
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending SMS to {Mobile}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در ارتباط با سرویس پیامک"
        )