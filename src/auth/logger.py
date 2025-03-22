import logging
from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from .config import ERROR_MESSAGES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auth.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AuthException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.timestamp = datetime.utcnow()
        self._log_error()

    def _log_error(self):
        logger.error(
            f"Auth Error: {self.detail} | Code: {self.error_code} | "
            f"Status: {self.status_code} | Time: {self.timestamp}"
        )

def handle_auth_error(error: Exception) -> dict:
    """مدیریت خطاهای احراز هویت و تبدیل آنها به پاسخ مناسب"""
    if isinstance(error, AuthException):
        raise HTTPException(
            status_code=error.status_code,
            detail={
                "status": "error",
                "code": error.error_code,
                "message": error.detail,
                "timestamp": error.timestamp.isoformat()
            }
        )
    
    logger.error(f"Unexpected error: {str(error)}")
    raise HTTPException(
        status_code=500,
        detail={
            "status": "error",
            "code": "internal_server_error",
            "message": ERROR_MESSAGES["server_error"],
            "timestamp": datetime.utcnow().isoformat()
        }
    ) 