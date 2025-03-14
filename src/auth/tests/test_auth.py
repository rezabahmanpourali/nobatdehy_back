import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .. import model, crud
from ..config import SECRET_KEY
from main import app
from database import Base, get_db

# تنظیمات تست
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_send_otp(client):
    response = client.post("/auth/customers/otp/", params={"phone": "09123456789"})
    assert response.status_code == 200
    assert "message" in response.json()

def test_verify_otp(client, test_db):
    # ارسال OTP
    phone = "09123456789"
    client.post("/auth/customers/otp/", params={"phone": phone})
    
    # دریافت OTP از دیتابیس
    otp_record = test_db.query(model.OtpStore).filter(model.OtpStore.phone == phone).first()
    assert otp_record is not None
    
    # تایید OTP
    response = client.post(
        "/auth/customers/verify/",
        params={"phone": phone, "otp": otp_record.otp}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_get_current_user(client, test_db):
    # ثبت‌نام کاربر
    phone = "09123456789"
    client.post("/auth/customers/otp/", params={"phone": phone})
    otp_record = test_db.query(model.OtpStore).filter(model.OtpStore.phone == phone).first()
    response = client.post(
        "/auth/customers/verify/",
        params={"phone": phone, "otp": otp_record.otp}
    )
    access_token = response.json()["access_token"]
    
    # دریافت اطلاعات کاربر
    response = client.get(
        "/auth/customers/me/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "customer" in response.json()
    assert "addresses" in response.json()

def test_update_customer(client, test_db):
    # ثبت‌نام کاربر
    phone = "09123456789"
    client.post("/auth/customers/otp/", params={"phone": phone})
    otp_record = test_db.query(model.OtpStore).filter(model.OtpStore.phone == phone).first()
    response = client.post(
        "/auth/customers/verify/",
        params={"phone": phone, "otp": otp_record.otp}
    )
    access_token = response.json()["access_token"]
    
    # به‌روزرسانی اطلاعات
    update_data = {
        "name": "تست",
        "lastn": "کاربر"
    }
    response = client.put(
        "/auth/customers/edit/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]
    assert response.json()["lastn"] == update_data["lastn"]

def test_add_address(client, test_db):
    # ثبت‌نام کاربر
    phone = "09123456789"
    client.post("/auth/customers/otp/", params={"phone": phone})
    otp_record = test_db.query(model.OtpStore).filter(model.OtpStore.phone == phone).first()
    response = client.post(
        "/auth/customers/verify/",
        params={"phone": phone, "otp": otp_record.otp}
    )
    access_token = response.json()["access_token"]
    
    # افزودن آدرس
    address_data = {
        "latitude": 35.7219,
        "longitude": 51.3347
    }
    response = client.post(
        "/auth/customers/addresses/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=address_data
    )
    assert response.status_code == 200
    assert response.json()["latitude"] == address_data["latitude"]
    assert response.json()["longitude"] == address_data["longitude"]

def test_get_addresses(client, test_db):
    # ثبت‌نام کاربر و افزودن آدرس
    phone = "09123456789"
    client.post("/auth/customers/otp/", params={"phone": phone})
    otp_record = test_db.query(model.OtpStore).filter(model.OtpStore.phone == phone).first()
    response = client.post(
        "/auth/customers/verify/",
        params={"phone": phone, "otp": otp_record.otp}
    )
    access_token = response.json()["access_token"]
    
    # افزودن آدرس
    address_data = {
        "latitude": 35.7219,
        "longitude": 51.3347
    }
    client.post(
        "/auth/customers/addresses/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=address_data
    )
    
    # دریافت لیست آدرس‌ها
    response = client.get(
        "/auth/customers/addresses/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["latitude"] == address_data["latitude"]
    assert response.json()[0]["longitude"] == address_data["longitude"]

def test_delete_customer(client, test_db):
    # ثبت‌نام کاربر
    phone = "09123456789"
    client.post("/auth/customers/otp/", params={"phone": phone})
    otp_record = test_db.query(model.OtpStore).filter(model.OtpStore.phone == phone).first()
    response = client.post(
        "/auth/customers/verify/",
        params={"phone": phone, "otp": otp_record.otp}
    )
    access_token = response.json()["access_token"]
    
    # حذف حساب کاربری
    response = client.delete(
        "/auth/customers/delete/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    
    # بررسی حذف شدن کاربر
    response = client.get(
        "/auth/customers/me/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 404 