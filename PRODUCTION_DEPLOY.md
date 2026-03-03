# Production Deployment Checklist - Zainussunna Academy Backend

## Quick Fix - Steps to Resolve

### Step 1: Add Environment Variables on Render

Go to **Render Dashboard → Your Backend Service → Environment** and add these variables:

| Variable                 | Value                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| `DJANGO_SETTINGS_MODULE` | `backend.production`                                                                                   |
| `DJANGO_SECRET_KEY`      | Generate: `python -c "import secrets; print(secrets.token_hex(50))"`                                   |
| `DEBUG`                  | `False`                                                                                                |
| `ALLOWED_HOSTS`          | `zainussunnaacademy.com,www.zainussunnaacademy.com,api.zainussunnaacademy.com`                         |
| `CSRF_TRUSTED_ORIGINS`   | `https://zainussunnaacademy.com,https://www.zainussunnaacademy.com,https://api.zainussunnaacademy.com` |
| `CORS_ALLOWED_ORIGINS`   | `https://zainussunnaacademy.com,https://www.zainussunnaacademy.com`                                    |
| `DATABASE_URL`           | (Should be auto-provided by Render PostgreSQL)                                                         |

### Step 2: Update Build Command

In Render, set the build command to:

```bash
pip install -r requirements.txt && python manage.py migrate
```

### Step 3: Update Start Command

Set the start command to:

```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 4: Run Initialization in Render Shell

In **Render → Shell**, run:

```bash
python3 manage.py migrate
python3 manage.py init_system
```

### Step 5: Redeploy

Click **Deploy** in Render to apply the changes.

---

## Issues Fixed

### 1. Achievement Image 500 Error (FIXED)

- **Problem**: Invalid image data in database (`image='[]'`, `image=None`) caused 500 errors
- **Fix**:
  - Cleaned up invalid image data in database
  - Made `image` field optional (`null=True, blank=True`)
  - Created migration `0004_achievement_image_nullable.py`

### 2. Admin Enhancement (FIXED)

- Added image preview in Achievement admin list view with null handling

### 3. Production Settings (NEW)

- Created `backend/production.py` with optimized settings for production
- Enables HTTPS, HSTS, secure cookies
- Proper CORS configuration

---

## Common Error Messages & Solutions

| Error                                                   | Solution                                         |
| ------------------------------------------------------- | ------------------------------------------------ |
| `DJANGO_SECRET_KEY environment variable is not set!`    | Set the variable in Render                       |
| `relation "core_program" does not exist`                | Run `python3 manage.py migrate`                  |
| `disallowed host`                                       | Add domain to `ALLOWED_HOSTS`                    |
| `CSRF verification failed`                              | Add URL to `CSRF_TRUSTED_ORIGINS`                |
| `500 Internal Server Error on /admin/core/achievement/` | Database has invalid image data - run migrations |

---

## For Local Development

```bash
cd backend
python3 manage.py migrate
python3 manage.py init_system
python3 manage.py runserver
```

---

## API Endpoints

| Endpoint             | Description            |
| -------------------- | ---------------------- |
| `/api/programs/`     | List all programs      |
| `/api/admissions/`   | List/create admissions |
| `/api/achievements/` | List achievements      |
| `/api/gallery/`      | List gallery items     |
| `/api/faculty/`      | List faculty members   |
| `/api/enquiries/`    | List/create enquiries  |
| `/api/analytics/`    | Analytics data         |
| `/api/health/`       | Health check           |
| `/api/auth/token/`   | JWT token              |

---

## Frontend API Configuration

Update `frontend/src/services/api.js` to point to your production API:

```javascript
const API_BASE_URL = "https://api.zainussunnaacademy.com";
```
