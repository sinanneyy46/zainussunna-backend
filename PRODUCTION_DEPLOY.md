# Production Deployment Checklist - Fixing 500 Error

## Current Issue

500 Internal Server Error on `/admin/login/` in production

## Quick Fix - Steps to Resolve

### Step 1: Add Environment Variables on Render

Go to **Render Dashboard → Your Backend Service → Environment** and add these variables:

| Variable               | Value                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| `DJANGO_SECRET_KEY`    | Generate: `python -c "import secrets; print(secrets.token_hex(50))"`                                   |
| `DEBUG`                | `False`                                                                                                |
| `ALLOWED_HOSTS`        | `zainussunnaacademy.com,www.zainussunnaacademy.com,api.zainussunnaacademy.com`                         |
| `CSRF_TRUSTED_ORIGINS` | `https://zainussunnaacademy.com,https://www.zainussunnaacademy.com,https://api.zainussunnaacademy.com` |

### Step 2: Run Migrations in Render Shell

In **Render → Shell**, run:

```bash
python3 manage.py migrate
python3 manage.py init_system
```

### Step 3: Redeploy

Click **Deploy** in Render to apply the changes.

---

## For Local Development

The settings now work out of the box with a fallback SECRET_KEY:

```bash
cd backend
python3 manage.py migrate
python3 manage.py init_system
python3 manage.py runserver
```

---

## Common Error Messages & Solutions

| Error                                                | Solution                          |
| ---------------------------------------------------- | --------------------------------- |
| `DJANGO_SECRET_KEY environment variable is not set!` | Set the variable in Render        |
| `relation "core_program" does not exist`             | Run `python3 manage.py migrate`   |
| `disallowed host`                                    | Add domain to `ALLOWED_HOSTS`     |
| `CSRF verification failed`                           | Add URL to `CSRF_TRUSTED_ORIGINS` |

---

## Code Changes Made

1. **settings.py**: Made configuration dynamic with environment variable support
2. **init_system.py**: Fixed Achievement model field name (`images` → `image`)
3. **Created .env.example**: Documents required environment variables
4. **Created PRODUCTION_DEPLOY.md**: This checklist
