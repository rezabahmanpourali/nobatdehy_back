# API حذف اکانت کاربر

سلام! اینجا میخوایم بگیم چطور میتونی از API حذف اکانت استفاده کنی.

## API حذف اکانت
```
DELETE /customers/{customer_id}
```

**کی استفاده کنم؟**
- وقتی کاربر میخواد اکانت خودش رو حذف کنه
- مثلا در بخش تنظیمات اکانت
- یا وقتی کاربر میخواد از برنامه خارج بشه

**نکته مهم:** این API تمام اطلاعات کاربر رو حذف میکنه، پس حتماً قبل از فرستادن درخواست، از کاربر تأیید بگیرید!

**مثال درخواست موفق:**
```json
{
    "message": "اکانت با موفقیت حذف شد"
}
```

**خطاهای احتمالی:**
- 404: کاربر یافت نشد
- 500: خطای سرور

## مثال کد فرانت‌اند (React)
```typescript
const deleteAccount = async (customerId: number) => {
  try {
    const response = await fetch(`/customers/${customerId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        // حتماً توکن احراز هویت رو هم بفرستید
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error('خطا در حذف اکانت');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('خطا:', error);
    throw error;
  }
};
```

## نکات مهم
1. این API تمام اطلاعات کاربر رو حذف میکنه، پس حتماً از کاربر تأیید بگیرید
2. حتماً قبل از فرستادن درخواست، توکن احراز هویت رو در هدر درخواست قرار بدید
3. بعد از حذف اکانت، کاربر رو از برنامه خارج کنید
4. اگر خطایی رخ داد، به کاربر اطلاع بدید

## امنیت
- فقط خود کاربر میتونه اکانت خودش رو حذف کنه
- حتماً از توکن احراز هویت استفاده کنید
- برای امنیت بیشتر، میتونید یک کد تأیید (مثل OTP) هم درخواست کنید

امیدوارم این راهنما کمکتون کرده باشه! اگر سوال دیگه‌ای دارید، خوشحال میشیم کمکتون کنیم 😊 