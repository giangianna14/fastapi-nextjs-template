# Dokumentasi Project FastAPI-NextJS

## Teknologi yang Digunakan

### 1. Next.js
- Framework React untuk SSR, SSG, dan API routes.
- Konfigurasi: `next.config.mjs`
- Folder terkait: `.next`, `src/app`

### 2. React
- Library utama untuk membangun UI.
- Komponen berada di: `src/components`

### 3. Tailwind CSS
- Utility-first CSS framework.
- Konfigurasi: `tailwind.config.js`
- File CSS: `src/assets/styles`

### 4. PostCSS
- Digunakan untuk memproses CSS.
- Konfigurasi: `postcss.config.mjs`

### 5. ESLint & Prettier
- Untuk menjaga konsistensi dan kualitas kode.
- Konfigurasi: `eslint.config.mjs`, `.prettierrc`, `.prettierignore`

### 6. NextAuth.js
- Autentikasi berbasis Next.js.
- Implementasi: `src/middleware.js`, `src/configs/auth.config`

### 7. FastAPI (Backend)
- Backend Python (asumsi dari nama folder `backend`).
- Berjalan terpisah dari frontend Next.js.

### 8. Internationalization (i18n)
- Dukungan multi-bahasa.
- Folder: `src/i18n`

### 9. Lodash
- Utility library, contoh: `debounce` pada `src/components/template/Search.jsx`

### 10. React Icons
- Library ikon untuk React.
- Contoh: `react-icons/hi`, `react-icons/pi`

### 11. Testing & Build Tools
- Dependency management: npm/yarn (`package.json`)
- Build output: `.next`

---

## Struktur Folder

```
.
├── backend/                # Backend FastAPI (Python)
├── public/                 # Static assets (gambar, favicon, dsb)
├── src/
│   ├── app/                # Next.js app directory
│   ├── assets/
│   │   └── styles/         # File CSS (Tailwind, komponen, dsb)
│   ├── components/         # Komponen React
│   ├── configs/            # Konfigurasi aplikasi (auth, routes, dsb)
│   ├── constants/          # Konstanta global
│   ├── i18n/               # Internationalization
│   ├── mock/               # Mock data
│   ├── server/             # Server-side logic
│   ├── services/           # Service layer (API call, dsb)
│   ├── utils/              # Utility functions
│   ├── auth.js             # Auth logic
│   └── middleware.js       # Middleware NextAuth
├── .env                    # Environment variables
├── package.json            # Dependency & script management
├── next.config.mjs         # Next.js config
├── tailwind.config.js      # Tailwind CSS config
├── postcss.config.mjs      # PostCSS config
├── eslint.config.mjs       # ESLint config
├── .prettierrc             # Prettier config
└── README.md               # Dokumentasi project
```

---

## Cara Menjalankan Project

1. **Install dependencies**
   ```sh
   npm install
   ```

2. **Jalankan development server**
   ```sh
   npm run dev
   ```
   Akses aplikasi di `http://localhost:3000`

3. **Konfigurasi Environment**
   - Edit file `.env` untuk mengatur variabel lingkungan (API URL, secret, dsb).

4. **Build untuk Production**
   ```sh
   npm run build
   npm start
   ```

---

## Autentikasi

- Menggunakan NextAuth.js, middleware di `src/middleware.js` untuk proteksi route.
- Konfigurasi route publik dan autentikasi di `src/configs/routes.config`.

---

## Styling

- Menggunakan Tailwind CSS dan custom CSS di `src/assets/styles`.
- Komponen CSS diimpor melalui `src/assets/styles/components/index.css`.

---

## Backend

- Backend terpisah di folder `backend` (asumsi FastAPI).
- Frontend berkomunikasi dengan backend melalui API.

---

## Internationalization

- Dukungan multi-bahasa di folder `src/i18n`.

---

**Referensi kode dan file:**
- `src/middleware.js`
- `src/components/template/Search.jsx`
- `src/assets/styles/components/index.css`
- `package.json`
- `next.config.mjs`
- `tailwind.config.js`

Jika butuh dokumentasi lebih detail pada bagian tertentu, silakan sebutkan bagian yang diinginkan!