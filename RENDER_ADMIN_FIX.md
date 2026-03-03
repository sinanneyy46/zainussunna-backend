# Django Admin 500 Error on Render - COMPLETE FIX

## 🔴 ROOT CAUSES IDENTIFIED & FIXED

### Issue 1: Media Files Not Served in Production ✅ FIXED

**File:** `backend/backend/urls.py`

- Changed from `if settings.DEBUG:` to always serve media files

### Issue 2: Image Preview Methods Not Error-Handled ✅ FIXED

**File:** `backend/core/admin.py`

- Added `try/except` and null checks to `image_preview()` methods
- Added null checks to `program_link()` and `state_badge()` methods

### Issue 3: Custom Admin Template Issues ✅ FIXED

**File:** `backend/templates/admin/base.html`

- Deleted custom template - admin now uses Django's default

### Issue 4: Invalid Image Data in Database ✅ FIXED

- Found Achievement with invalid image (`'[]'` string instead of null)
- Cleaned up the data locally
- Migration 0004 created

---

## DEPLOY TO RENDER

```bash
git add .
git commit -m "Fix admin 500 error: media URLs, error handling, remove custom template"
git push
```

Then in Render:

```bash
# Apply migrations
python manage.py migrate

# Restart gunicorn
touch backend/wsgi.py
```

---

## VERIFY FIX

Test these admin pages:

- /admin/core/achievement/
- /admin/core/galleryitem/
- /admin/core/faculty/
- /admin/core/program/

---

## FILES MODIFIED

1. `backend/backend/urls.py` - Media files served in production
2. `backend/core/admin.py` - Error handling in list_display methods
3. `backend/templates/admin/base.html` - Deleted (using default)
