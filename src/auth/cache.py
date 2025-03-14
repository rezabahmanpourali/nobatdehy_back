from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException
from .config import RATE_LIMIT_REQUESTS, RATE_LIMIT_PERIOD, ERROR_MESSAGES

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = {}

    def is_rate_limited(self, key: str) -> bool:
        """بررسی محدودیت تعداد درخواست"""
        now = datetime.utcnow()
        if key not in self.requests:
            self.requests[key] = []
        
        # حذف درخواست‌های قدیمی
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < timedelta(seconds=RATE_LIMIT_PERIOD)
        ]
        
        if len(self.requests[key]) >= RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail=ERROR_MESSAGES["rate_limit_exceeded"]
            )
        
        self.requests[key].append(now)
        return False

class Cache:
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl: Dict[str, datetime] = {}

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """ذخیره مقدار در کش با زمان انقضا"""
        self.cache[key] = value
        self.ttl[key] = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        """دریافت مقدار از کش"""
        if key not in self.cache:
            return None
        
        if datetime.utcnow() > self.ttl[key]:
            del self.cache[key]
            del self.ttl[key]
            return None
        
        return self.cache[key]

    def delete(self, key: str) -> None:
        """حذف مقدار از کش"""
        if key in self.cache:
            del self.cache[key]
        if key in self.ttl:
            del self.ttl[key]

# نمونه‌های سراسری
rate_limiter = RateLimiter()
cache = Cache() 