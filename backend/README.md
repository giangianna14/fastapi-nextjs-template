# Standarisasi Backend FastAPI (Reusable & Industri)

## Tujuan
Dokumen ini menjelaskan standar pengembangan backend FastAPI agar:
- **Reusable**: Mudah digunakan ulang di project lain.
- **Industri**: Mengikuti best practice industri (struktur, keamanan, testing, dokumentasi, dsb).

---

## Struktur Folder Standar

```
backend/
├── app/
│   ├── api/            # Router/endpoint terpisah per fitur
│   ├── core/           # Konfigurasi inti (settings, security, logging, dsb)
│   ├── db/             # Koneksi & utilitas database
│   ├── models/         # Model ORM (SQLAlchemy, dsb)
│   ├── schemas/        # Skema data (Pydantic)
│   ├── services/       # Logika bisnis/service layer
│   ├── utils/          # Helper/utilitas umum
│   └── main.py         # Entry point aplikasi FastAPI
├── tests/              # Unit & integration test
├── requirements.txt    # Dependencies
├── .env                # Environment variables
└── README.md           # Dokumentasi backend
```

---

## Standar Pengembangan

### 1. **Konfigurasi & Environment**
- Semua konfigurasi (DB, secret, dsb) diatur lewat file `.env` dan `app/core/config.py`.
- Gunakan [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) untuk manajemen konfigurasi.

### 2. **Struktur Modular**
- Setiap fitur (user, auth, dsb) punya folder sendiri di `app/api/`, `app/services/`, `app/schemas/`, dst.
- Router di-include di `app/api/__init__.py` dan didaftarkan di `main.py`.

### 3. **Database & ORM**
- Gunakan SQLAlchemy atau Tortoise ORM.
- Semua model di `app/models/`, skema response/request di `app/schemas/`.
- Koneksi database diatur di `app/db/session.py`.

### 4. **Service Layer**
- Logika bisnis dipisah di `app/services/`, tidak langsung di router.

### 5. **Autentikasi & Otorisasi**
- Implementasi JWT atau OAuth2 di `app/core/security.py`.
- Middleware untuk validasi token dan role-based access.


## Checklist Standarisasi

- [x] Struktur folder modular & scalable
- [x] Konfigurasi environment terpusat
- [x] Service layer terpisah dari router
- [x] Autentikasi JWT/OAuth2
- [x] Error handling konsisten
- [x] Logging terpusat
- [x] Unit test & coverage
- [x] Dokumentasi endpoint otomatis
- [x] Linting & formatting

---

**Catatan:**
Template ini dapat dikembangkan sesuai kebutuhan project dan tim.
Untuk implementasi lebih lanjut, silakan tambahkan contoh kode, template, atau guideline di masing-masing folder.

**Contoh Implementasi Sederhana:**

**security.py**
```python
# app/core/security.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

**Endpoint login:**
```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login")
def login():
    # Validasi user (dummy)
    user_id = 1
    access_token = create_access_token({"sub": str(user_id)})
    return {"access_token": access_token, "token_type": "bearer"}
```

**Dependency validasi token:**
```python
# app/core/security.py (tambahan)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return payload
```

**Penggunaan di endpoint:**
```python
# app/api/v1/endpoints/user.py
from fastapi import Depends
from app.core.security import get_current_user

@router.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {"user": current_user}
```

**Manfaat:**
- Aman, stateless, dan mudah diintegrasikan dengan frontend modern.
- Bisa dikembangkan untuk role-based access control.

- [x] Autentikasi JWT/OAuth2
---

**Catatan:**  
Template ini dapat dikembangkan sesuai kebutuhan project dan tim.  
Untuk implementasi lebih lanjut, silakan tambahkan contoh kode, template, atau guideline di masing-masing folder.