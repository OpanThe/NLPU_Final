# ❓ FAQ & Troubleshooting Guide

## Frequently Asked Questions

### Q1: Bagaimana cara mulai menggunakan aplikasi ini?

**A:** Ikuti langkah-langkah berikut:

1. Buka folder `d:\nlp-final\chatbot-app`
2. Di Windows: Double-click `start.bat`
3. Di Mac/Linux: Run `bash start.sh` di terminal
4. Buka browser ke `http://localhost:3000`

---

### Q2: Apa perbedaan antara backend dan frontend?

**A:**

- **Backend (server.js)** - Express server yang handle API requests, manage chat history, connect ke AI models
- **Frontend (React)** - User interface yang user lihat, kirim message, switch models, display chat

---

### Q3: Bagaimana cara menambah AI model baru?

**A:** Edit `backend/server.js` di `AVAILABLE_MODELS`:

```javascript
{
  id: 'model-id',
  name: 'Model Name',
  provider: 'provider',
  description: 'Description',
  icon: '🎉'
}
```

---

### Q4: Apakah bisa integrate dengan API OpenAI, Claude, dll?

**A:** Ya! Lihat `AI_INTEGRATION_EXAMPLES.js` untuk code examples. Setiap AI provider punya SDK yang bisa digunakan.

---

### Q5: Bagaimana cara deploy aplikasi ini?

**A:**

- **Frontend:** Build (`npm run build`) dan upload ke Vercel/Netlify
- **Backend:** Push ke GitHub dan deploy ke Railway/Heroku
- Lihat `SETUP_GUIDE.md` untuk detail deployment

---

### Q6: Data chat saya kemana? Apakah tersimpan?

**A:** Saat ini data disimpan di memory backend. Data hilang saat server restart. Untuk persistent storage, Anda perlu tambah database (MongoDB, PostgreSQL, etc).

---

### Q7: Bisa ganti warna/tema website?

**A:** Ya! Edit `frontend/tailwind.config.js`:

```javascript
colors: {
  'dark-bg': '#your-color',
  'dark-card': '#your-color',
  'accent': '#your-color'
}
```

---

### Q8: Bagaimana kalau lupa API keys di .env?

**A:** Edit file `backend/.env` dan tambah API keys Anda. Restart server dengan `npm run dev`.

---

### Q9: Bisa host di localhost saja atau harus online?

**A:** Bisa localhost saja untuk development. Untuk production, Anda perlu deploy ke server online.

---

### Q10: Apa ini gratis? Ada lisensi apa?

**A:** Ya, open source MIT License. Gratis untuk personal dan commercial use.

---

## Troubleshooting Guide

### ❌ Error: "Cannot find module 'express'"

**Problem:** Module tidak terinstall  
**Solution:**

```bash
cd backend
npm install
```

---

### ❌ Error: "EADDRINUSE: address already in use :::5000"

**Problem:** Port 5000 sudah dipakai aplikasi lain  
**Solution:**

**Windows:**

```bash
# Cari proses yang pakai port 5000
netstat -ano | findstr :5000

# Kill proses (ganti PID dengan nomor yang muncul)
taskkill /PID 12345 /F

# Atau ganti port di backend/.env
PORT=5001
```

**macOS/Linux:**

```bash
# Cari dan kill proses
lsof -ti:5000 | xargs kill -9

# Atau ganti port
PORT=5001 npm run dev
```

---

### ❌ Error: "CORS policy: Cross-Origin Request Blocked"

**Problem:** Frontend tidak bisa akses backend API  
**Solution:**

1. Pastikan backend running di `http://localhost:5000`
2. Check `server.js` sudah punya `app.use(cors())`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Hard refresh (Ctrl+F5)

---

### ❌ Error: "GET http://localhost:5000/api/models 404"

**Problem:** Backend endpoint tidak ditemukan  
**Solution:**

1. Check backend running (`npm run dev`)
2. Check URL di `utils/api.js` benar
3. Check `server.js` punya endpoint `/api/models`
4. Restart backend server

---

### ❌ Frontend tidak load, blank page

**Problem:** React tidak render  
**Solution:**

1. Check console (F12) untuk errors
2. Check `src/main.jsx` ada `#root` element
3. Check `index.html` ada `<div id="root"></div>`
4. Restart dev server (`npm run dev`)

---

### ❌ "Cannot find .env file"

**Problem:** File .env tidak ada di backend  
**Solution:**

```bash
cd backend
cp .env.example .env
# Edit .env dengan text editor
```

---

### ❌ npm install sangat lama / gagal

**Problem:** Network issue atau package conflict  
**Solution:**

```bash
# Clear npm cache
npm cache clean --force

# Install ulang
rm -rf node_modules package-lock.json
npm install

# Atau gunakan yarn
npm install -g yarn
yarn install
```

---

### ❌ "Module 'react' has no default export"

**Problem:** Import statement salah  
**Solution:** Check import statement:

```javascript
// ✅ Benar
import React from "react";

// ❌ Salah
import { React } from "react";
```

---

### ❌ Message tidak terkirim, loading terus

**Problem:** Backend error atau timeout  
**Solution:**

1. Check backend console untuk error messages
2. Check Network tab (F12) untuk API response
3. Pastikan backend model valid
4. Restart backend

---

### ❌ "TypeError: Cannot read property 'map' of undefined"

**Problem:** State belum loaded saat render  
**Solution:**

```javascript
// Tambah default value
const [models, setModels] = useState([]);

// Atau check sebelum map
{models && models.map(...)}
```

---

### ❌ Git merge conflict

**Problem:** Multiple people edit file yang sama  
**Solution:**

```bash
# View conflicts
git status

# Edit files, keep yang benar

# Resolve
git add .
git commit -m "Resolve merge conflicts"
```

---

### ❌ "Cannot find command npm"

**Problem:** Node.js tidak terinstall atau PATH salah  
**Solution:**

1. Download Node.js dari https://nodejs.org/
2. Install dengan default settings
3. Restart terminal
4. Check: `node --version` dan `npm --version`

---

### ❌ Port 3000 sudah dipakai (frontend)

**Problem:** Frontend port conflict  
**Solution:**

Edit `frontend/vite.config.js`:

```javascript
server: {
  port: 3001,  // Ganti ke port lain
}
```

---

### ❌ "openai is not defined"

**Problem:** SDK tidak terinstall  
**Solution:**

```bash
cd backend
npm install openai
```

---

### ❌ Message hilang setelah refresh page

**Problem:** Data hanya tersimpan di memory  
**Solution:** Ini normal untuk demo. Untuk production, add database:

- MongoDB
- PostgreSQL
- Firebase
- Supabase

---

### ❌ Styling tidak berfungsi (Tailwind)

**Problem:** Tailwind CSS tidak di-process  
**Solution:**

1. Check `tailwind.config.js` ada template paths
2. Pastikan `index.css` ada `@tailwind` directives
3. Clear browser cache
4. Restart dev server

---

### ❌ "env file not found"

**Problem:** dotenv tidak bisa find .env  
**Solution:**

1. Create `.env` file di `backend/` folder
2. Pastikan file bukan `.env.txt`
3. Check file extension: `.env` (no extension)
4. Restart server

---

## Performance Issues

### Aplikasi lambat?

**Solution:**

1. Check Network tab (F12) - API response time
2. Check Console untuk memory leaks
3. Reduce number of messages di display
4. Add pagination untuk chat history

---

### Banyak API errors?

**Solution:**

1. Check backend logs
2. Verify API keys di `.env`
3. Check internet connection
4. Check backend restart dengan error terlihat

---

## Browser Compatibility

| Browser | Support | Note           |
| ------- | ------- | -------------- |
| Chrome  | ✅      | Recommended    |
| Firefox | ✅      | Full support   |
| Safari  | ✅      | Works fine     |
| Edge    | ✅      | Chromium-based |
| IE 11   | ❌      | Not supported  |

---

## Common Tips

### 1. Check Server Status

```bash
curl http://localhost:5000/api/health
```

### 2. View Logs

```bash
# Backend - lihat console output saat npm run dev
# Frontend - lihat F12 → Console
```

### 3. Test API Endpoint

Gunakan tools seperti:

- Postman
- Insomnia
- cURL
- Thunder Client (VS Code extension)

### 4. Clear Data

```bash
# Clear browser data
F12 → Application → Clear All

# Clear npm cache
npm cache clean --force
```

### 5. Update Node.js

```bash
# Check version
node --version

# Download latest dari https://nodejs.org/
```

---

## Still Having Issues?

1. **Check documentation:** SETUP_GUIDE.md, DEVELOPMENT_GUIDE.md
2. **Search Google** dengan error message
3. **Check GitHub issues** untuk similar problems
4. **Look at console errors** (F12)
5. **Check .env file** untuk missing API keys
6. **Restart everything:**
   - Kill terminal processes
   - Close browser
   - Reopen and start fresh

---

## Getting Help

- 📖 Read: SETUP_GUIDE.md, DEVELOPMENT_GUIDE.md
- 💻 Check: Project structure di PROJECT_STRUCTURE.md
- 🔗 API Examples: AI_INTEGRATION_EXAMPLES.js
- ⚡ Quick commands: QUICK_REFERENCE.md

---

**If problem persist, check all files dalam documentation first!** 📚
