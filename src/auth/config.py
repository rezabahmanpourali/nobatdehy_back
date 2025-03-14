from datetime import timedelta
from typing import Dict, Any

SECRET_KEY = "k7Nv5K9R6xFO3IuQvL6b0YqYHjFQWKh65ltPhSm9YXk"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

OTP_EXPIRE_MINUTES = 2
MAX_OTP_ATTEMPTS = 3
OTP_RESEND_TIMEOUT_MINUTES = 1

RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_PERIOD = 60

PHONE_REGEX = r"^09[0-9]{9}$"
LATITUDE_RANGE = (-90, 90)
LONGITUDE_RANGE = (-180, 180)

ERROR_MESSAGES: Dict[str, Any] = {
    "invalid_phone": "شماره موبایل نامعتبر است",
    "invalid_otp": "کد تایید نامعتبر یا منقضی شده است",
    "max_otp_attempts": "تعداد تلاش‌های مجاز برای ارسال کد تایید به پایان رسیده است",
    "otp_resend_timeout": "لطفاً کمی صبر کنید و دوباره تلاش کنید",
    "invalid_token": "توکن نامعتبر یا منقضی شده است",
    "invalid_credentials": "اطلاعات ورودی نامعتبر است",
    "user_not_found": "کاربر یافت نشد",
    "invalid_address": "آدرس نامعتبر است",
    "server_error": "خطای سرور، لطفاً دوباره تلاش کنید",
    "rate_limit_exceeded": "تعداد درخواست‌های شما از حد مجاز بیشتر شده است",
} 