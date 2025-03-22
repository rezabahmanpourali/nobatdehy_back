# مستندات تغییرات دیتابیس

## تغییرات انجام شده

### 1. اضافه شدن جدول Working Hours
**تاریخ**: 22 مارچ 2024
**فایل مایگریشن**: `bb89d4b67f59_add_working_hours_table.py`

این جدول برای ذخیره ساعات کاری آرایشگاه‌ها اضافه شده است.

#### ساختار جدول:
```sql
CREATE TABLE working_hours (
    id SERIAL PRIMARY KEY,
    barber_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL, -- شماره روز هفته (0 تا 6)
    start_time TIME NOT NULL,    -- ساعت شروع
    end_time TIME NOT NULL,      -- ساعت پایان
    is_active BOOLEAN DEFAULT true,
    FOREIGN KEY (barber_id) REFERENCES barbers(id)
);
```

#### توضیحات فیلدها:
- `barber_id`: شناسه آرایشگر
- `day_of_week`: شماره روز هفته (0=شنبه تا 6=جمعه)
- `start_time`: ساعت شروع کار
- `end_time`: ساعت پایان کار
- `is_active`: وضعیت فعال بودن این زمان‌بندی

### 2. اضافه شدن جدول OTP Store
**تاریخ**: 22 مارچ 2024
**فایل مایگریشن**: `add_otp_store.py`

این جدول برای ذخیره و مدیریت کدهای تایید (OTP) اضافه شده است.

#### ساختار جدول:
```sql
CREATE TABLE otp_store (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(11) NOT NULL UNIQUE,
    otp VARCHAR(6) NOT NULL,
    expires_at TIMESTAMP NOT NULL
);
```

#### توضیحات فیلدها:
- `phone`: شماره موبایل کاربر (یکتا)
- `otp`: کد تایید 6 رقمی
- `expires_at`: زمان انقضای کد تایید

## نحوه اجرای مایگریشن‌ها

برای اجرای مایگریشن‌ها، دستورات زیر را به ترتیب اجرا کنید:

1. اجرای مایگریشن Working Hours:
```bash
alembic upgrade bb89d4b67f59
```

2. اجرای مایگریشن OTP Store:
```bash
alembic upgrade add_otp_store
```

## نکات مهم
1. قبل از اجرای هر مایگریشن، از دیتابیس backup بگیرید
2. مایگریشن‌ها باید به ترتیب اجرا شوند
3. در صورت خطا در اجرای مایگریشن، از دستور `alembic downgrade` برای برگشت به عقب استفاده کنید 