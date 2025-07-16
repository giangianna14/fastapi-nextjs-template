
# Standarisasi Backend FastAPI (Reusable & Industri)

## Tujuan
Dokumen ini menjelaskan standar pengembangan backend FastAPI agar:
- **Reusable**: Mudah digunakan ulang di project lain.
- **Industri**: Mengikuti best practice industri (struktur, keamanan, testing, dokumentasi, dsb).

---


---

## 1. Struktur Folder Modular & Scalable

Struktur folder yang modular memudahkan pengembangan, testing, dan scaling aplikasi. Setiap komponen utama dipisahkan ke dalam folder sesuai tanggung jawabnya.

**Struktur folder standar:**
```text
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

**Contoh penambahan fitur baru (misal: fitur user):**
```
app/
├── api/
│   └── v1/
│       └── endpoints/
│           └── user.py
├── models/
│   └── user.py
├── schemas/
│   └── user.py
├── services/
│   └── user_service.py
```

**Prinsip:**
- Setiap fitur/entitas utama punya folder/file sendiri di models, schemas, services, dan endpoints.
- Mudah di-scale dan di-maintain.

---


## 2. Konfigurasi Environment Terpusat

Semua konfigurasi penting (database, secret, dsb) dikelola secara terpusat menggunakan file `.env` dan modul `app/core/config.py`.

**Langkah-langkah:**
1. Simpan variabel rahasia dan konfigurasi di file `.env` (jangan commit ke git).
2. Gunakan Pydantic Settings untuk membaca konfigurasi secara otomatis.

**Contoh .env:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=supersecretkey
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Contoh config.py:**
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```


**Manfaat:**
- Konfigurasi mudah diubah tanpa mengubah kode.
- Aman, tidak hardcode credential di source code.

---

## 3. Service Layer Terpisah dari Router

Pisahkan logika bisnis dari router/endpoint agar kode lebih terstruktur, mudah di-maintain, dan dapat di-reuse.

**Contoh:**
```python
# app/services/user_service.py
from app.models.user import User

def get_user_by_id(user_id: int):
    # Query ke database (dummy)
    return User(id=user_id, name="User Example")
```

```python
# app/api/v1/endpoints/user.py
from fastapi import APIRouter
from app.services.user_service import get_user_by_id

router = APIRouter()

@router.get("/user/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)
    return user
```


**Manfaat:**
- Router hanya fokus pada HTTP request/response.
- Logika bisnis mudah di-test dan diubah tanpa mengganggu endpoint.

---

## 4. Autentikasi JWT/OAuth2

Gunakan JWT (JSON Web Token) atau OAuth2 untuk autentikasi yang aman dan stateless. Implementasi dilakukan di `app/core/security.py` dan digunakan di endpoint.

**Contoh implementasi JWT:**
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

**Contoh endpoint login:**
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

---

## 5. Error Handling Konsisten

Terapkan penanganan error yang konsisten dan terpusat agar response error mudah dipahami dan seragam di seluruh aplikasi.

**Contoh custom exception handler:**
```python
# app/core/exception_handler.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )
```

**Registrasi handler di main.py:**
```python
# app/main.py
from fastapi import FastAPI, HTTPException, Request
from app.core.exception_handler import http_exception_handler, validation_exception_handler
from fastapi.exception_handlers import RequestValidationError

app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
```


**Manfaat:**
- Error response seragam dan mudah di-debug.
- Validasi otomatis dari FastAPI tetap ter-handle dengan baik.

---

## 6. Logging Terpusat

Implementasi logging terpusat agar seluruh aktivitas aplikasi (info, error, dsb) tercatat rapi dan mudah di-audit/debug.

**Contoh logging.py:**
```python
# app/core/logging.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("app")
```

**Penggunaan di service/router:**
```python
# app/services/user_service.py
from app.core.logging import logger

def get_user_by_id(user_id: int):
    logger.info(f"Get user by id: {user_id}")
    # ...kode lain...
```


**Manfaat:**
- Memudahkan troubleshooting dan monitoring aplikasi.
- Bisa diintegrasikan dengan tools monitoring/log aggregator (ELK, Sentry, dsb).

---

## 7. Unit Test & Coverage

Selalu buat unit test untuk setiap service, model, dan endpoint utama. Gunakan pytest untuk testing dan coverage.py untuk mengukur cakupan kode.

**Struktur test:**
```
backend/
└── tests/
    ├── api/
    │   └── test_user.py
    └── services/
        └── test_user_service.py
```

**Contoh test service:**
```python
# tests/services/test_user_service.py
from app.services.user_service import get_user_by_id

def test_get_user_by_id():
    user = get_user_by_id(1)
    assert user.id == 1
    assert user.name == "User Example"
```

**Contoh test endpoint:**
```python
# tests/api/test_user.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user():
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

**Coverage:**
- Jalankan `pytest --cov=app` untuk melihat cakupan kode.


**Manfaat:**
- Menjamin kualitas dan stabilitas kode.
- Memudahkan refactor tanpa takut merusak fitur lain.

---

## 8. Dokumentasi Endpoint Otomatis

FastAPI secara otomatis menghasilkan dokumentasi OpenAPI/Swagger untuk seluruh endpoint. Dokumentasi ini dapat diakses di `/docs` (Swagger UI) dan `/redoc` (ReDoc).

**Contoh penambahan deskripsi dan response model:**
```python
# app/api/v1/endpoints/user.py
from fastapi import APIRouter
from app.schemas.user import UserSchema

router = APIRouter()

@router.get("/user/{user_id}", response_model=UserSchema, summary="Get user by ID", description="Ambil data user berdasarkan ID.")
def get_user(user_id: int):
    # ...kode ambil user...
    pass
```

**Akses dokumentasi:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


**Manfaat:**
- Memudahkan frontend/dev lain memahami dan mencoba API.
- Dokumentasi selalu up-to-date dengan kode.

---

## 9. Linting & Formatting

Gunakan tools linting dan formatting untuk menjaga konsistensi dan kualitas kode secara otomatis.

**Tools yang direkomendasikan:**
- `black` (formatter Python)
- `isort` (import sorter)
- `flake8` (linter)
- `pre-commit` (hook otomatis sebelum commit)

**Contoh konfigurasi pre-commit:**
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/psf/black
  rev: 23.7.0
  hooks:
    - id: black
- repo: https://github.com/PyCQA/isort
  rev: 5.12.0
  hooks:
    - id: isort
- repo: https://github.com/pycqa/flake8
  rev: 6.0.0
  hooks:
    - id: flake8
```

**Langkah setup:**
1. Install pre-commit: `pip install pre-commit`
2. Install hook: `pre-commit install`
3. Jalankan manual: `pre-commit run --all-files`

**Manfaat:**
- Kode selalu rapi, konsisten, dan bebas error style sebelum masuk repository.


