<div dir="rtl">
# سیستم رزرو اتاق جلسات


پروژه دوم بوت کمپ کوئرا زمستان ۱۴۰۲ گروه ۵


## مشارکت کنندگان
- [مشاهده مشارکت کنندگان](https://github.com/Yashar1989/Meeting-Room-Booking-System/network/dependencies)
- منتور - [ Mohamad Erfan Sajjadi ](https://github.com/mohamadsajjadi)



## Installation

برای نصب و استفاده مراحل زیر را به ترتیب پیش بروید:

۱-ابتدا این ریپازیتوری را روی سیستم خود کلون کنید
```bash
        git clone https://github.com/Yashar1989/Meeting-Room-Booking-System.git
```
۲-محیط مجازی خود را بسازید و فعال کنید
```bash
        python -m venv venv

        linux user:
        source venv/bin/activate
        windows user:
        venv\Scripts\activate
```
۳-نیازمندیها را نصب کنید
```bash
        pip install -r requirements.txt
```
۴-سرور را اجرا کنید
```bash
        python manage.py runserver
```

## نکات مهم

- دیتابیس postgres روی سرورهای لیارا تنظیم شده است.
- نیازی به اجرای makemigrations و migrate اولیه نیست.
- کاربر سوپریوزر با نام کاربری و رمز عبور admin قابل دسترس است.
- برای کد نویسی برنچ خود را بسازید و از برنچ خود پوش کنید.از ایجاد برنچ های متعدد خودداری کنید و با یک برنچ کار کنید تا ریپازیتوری دارای نظم باشد.

- نمونه دستورات جهت ایجاد برنچ و پوش کردن
```bash
    git branch <your-name>
    git switch <your-name>
    ... write code and make changes
    git add .
    git commit -m 'your message'
    git push origin <your-name>

```
- از pull گرفتن در برنچ main نترسید. بعد از اعلام دوستان در گروه حتماٌ pull بگیرید تا کمتر به کانفلیکت بخورید.
</div>
