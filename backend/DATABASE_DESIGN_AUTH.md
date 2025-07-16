# Desain Database Fitur Auth

## 1. Tabel Utama

### users
| Kolom           | Tipe Data           | Keterangan                        |
|-----------------|---------------------|-----------------------------------|
| id              | SERIAL / BIGINT (PK)| Primary key (auto increment)      |
| username        | VARCHAR(150)        | Unique, required                  |
| email           | VARCHAR(255)        | Unique, required                  |
| hashed_password | VARCHAR(255)        | Password hash                     |
| full_name       | VARCHAR(255)        | Opsional                          |
| avatar          | VARCHAR(255)        | URL gambar/avatar                 |
| is_active       | BOOLEAN             | Default: TRUE                     |
| is_superuser    | BOOLEAN             | Default: FALSE                    |
| created_at      | TIMESTAMP           | Default: now()                    |
| updated_at      | TIMESTAMP           | Default: now()                    |

### user_roles (opsional, jika ingin multi-role)
| Kolom     | Tipe Data      | Keterangan                |
|-----------|---------------|---------------------------|
| id        | SERIAL (PK)   | Primary key               |
| user_id   | BIGINT (FK)   | Relasi ke users.id        |
| role      | VARCHAR(50)   | Contoh: admin, user, dsb  |

### oauth_accounts (opsional, untuk login sosial)
| Kolom         | Tipe Data      | Keterangan                |
|---------------|---------------|---------------------------|
| id            | SERIAL (PK)    | Primary key               |
| user_id       | BIGINT (FK)    | Relasi ke users.id        |
| provider      | VARCHAR(50)    | Contoh: google, github    |
| provider_id   | VARCHAR(255)   | ID dari provider          |
| access_token  | VARCHAR(255)   | Token dari provider       |
| refresh_token | VARCHAR(255)   | Opsional                  |
| expires_at    | TIMESTAMP      | Opsional                  |

---

## 2. ERD Sederhana

```
users
  |
  |--< user_roles
  |
  |--< oauth_accounts
```

---

## 3. Contoh Model SQL

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE oauth_accounts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    access_token VARCHAR(255),
    refresh_token VARCHAR(255),
    expires_at TIMESTAMP
);
```

---

**Catatan:**
- Untuk password, simpan hash-nya saja, bukan plain text.
- Tabel `oauth_accounts` hanya diperlukan jika mendukung login sosial (Google, GitHub, dsb).
- Tabel `user_roles` bisa di-skip jika hanya ada satu role per user (gunakan kolom `is_superuser` saja).

Jika ingin contoh model Pydantic/SQLAlchemy, silakan minta lebih