# Django Admin 500 Error on Render - Complete Debugging Guide

## 1. MOST LIKELY CAUSE

**The `core_faculty` table doesn't exist in your PostgreSQL on Render.**

Why:

- `/admin/` loads because it doesn't query specific model tables
- `/admin/core/faculty/` queries the `core_faculty` table → **FAILS**
- Faculty model created in migration `0003_faculty_alter_achievement_image.py` likely didn't run in production

---

## 2. CONFIRM USING RENDER LOGS

```bash
render logs --service <your-service-name> --tail 100
```

**Look for these exact errors:**

| Error                                    | Meaning               |
| ---------------------------------------- | --------------------- |
| `relation "core_faculty" does not exist` | Table missing         |
| `column "image" does not exist`          | Schema mismatch       |
| `ProgrammingError`                       | Migration not applied |

---

## 3. FIX IN PRODUCTION

```bash
# Step 1: Check migration status
python manage.py showmigrations core

# Step 2: Apply all migrations
python manage.py migrate

# Step 3: If faculty fails, fake it
python manage.py migrate core 0003_faculty_alter_achievement_image --fake

# Step 4: Restart
touch backend/wsgi.py
```

---

## 4. CODE VERIFICATION - ALL CHECKED ✅

### ✅ All `__str__` Methods OK

| Model             | **str**                                                                       | Status |
| ----------------- | ----------------------------------------------------------------------------- | ------ |
| Program           | `self.name`                                                                   | ✅     |
| ProgramField      | `f"{self.program.name} - {self.label}"`                                       | ✅     |
| Admission         | `f"{self.application_number} - {self.name} ({self.state})"`                   | ✅     |
| AdmissionStateLog | `f"{self.admission.application_number}: {self.old_state} → {self.new_state}"` | ✅     |
| AdmissionEvent    | `f"{self.admission.application_number} - {self.event_type}"`                  | ✅     |
| InternalNote      | `f"Note on {self.admission.application_number} by {self.author}"`             | ✅     |
| ContentPage       | `self.title`                                                                  | ✅     |
| Achievement       | `self.title`                                                                  | ✅     |
| GalleryItem       | `self.title or f"Gallery item {self.id}"`                                     | ✅     |
| Enquiry           | `f"Enquiry from {self.name} ({self.status})"`                                 | ✅     |
| Faculty           | `f"{self.name} - {self.role}"`                                                | ✅     |
| AnalyticEvent     | `f"{self.category} - {self.created_at}"`                                      | ✅     |

### ✅ All Admin list_display Fields Exist

| Admin            | list_display fields                                                           | Status       |
| ---------------- | ----------------------------------------------------------------------------- | ------------ |
| ProgramAdmin     | name, slug, min_age, max_age, is_active, display_order                        | ✅ All exist |
| AdmissionAdmin   | application_number, name, program_link, state_badge, current_step, created_at | ✅ All exist |
| EnquiryAdmin     | name, email, status, program_interest, created_at                             | ✅ All exist |
| ContentPageAdmin | title, slug, is_published, version, created_at                                | ✅ All exist |
| AchievementAdmin | title, image_preview, date, is_visible, display_order, created_at             | ✅ All exist |
| GalleryItemAdmin | title, image_preview, date_taken, is_visible, display_order                   | ✅ All exist |
| FacultyAdmin     | name, role, qualification, is_active, display_order                           | ✅ All exist |

### ✅ All search_fields Valid

| Admin            | search_fields                          | Status |
| ---------------- | -------------------------------------- | ------ |
| ProgramAdmin     | name, slug                             | ✅     |
| AdmissionAdmin   | name, application_number, phone, email | ✅     |
| EnquiryAdmin     | name, email, message                   | ✅     |
| ContentPageAdmin | title, slug                            | ✅     |
| AchievementAdmin | title, description                     | ✅     |
| GalleryItemAdmin | title, caption                         | ✅     |
| FacultyAdmin     | name, role, qualification              | ✅     |

### ✅ All ordering Valid

| Admin              | ordering              | Status |
| ------------------ | --------------------- | ------ |
| ProgramAdmin       | display_order, name   | ✅     |
| AdmissionAdmin     | -created_at           | ✅     |
| ProgramFieldInline | step, display_order   | ✅     |
| EnquiryAdmin       | -created_at           | ✅     |
| ContentPageAdmin   | title                 | ✅     |
| AchievementAdmin   | -date, -display_order | ✅     |
| GalleryItemAdmin   | -display_order        | ✅     |
| FacultyAdmin       | display_order, name   | ✅     |

### ✅ All ForeignKey Relationships Valid

| Model                         | ForeignKey | On Delete | Status |
| ----------------------------- | ---------- | --------- | ------ |
| ProgramField → Program        | CASCADE    | ✅        |
| Admission → Program           | PROTECT    | ✅        |
| AdmissionStateLog → Admission | CASCADE    | ✅        |
| AdmissionEvent → Admission    | CASCADE    | ✅        |
| InternalNote → Admission      | CASCADE    | ✅        |
| Enquiry → Program             | SET_NULL   | ✅        |
| AnalyticEvent → Admission     | CASCADE    | ✅        |

---

## 5. COMPLETE CHECKLIST

- [ ] Check Render logs for exact error
- [ ] Run `showmigrations core`
- [ ] Run `migrate` command
- [ ] If fails: fake the migration
- [ ] Test with: `from core.models import Faculty; list(Faculty.objects.all())`

---

## SUMMARY

| Issue                     | Likelihood    | Solution             |
| ------------------------- | ------------- | -------------------- |
| **Faculty table missing** | **HIGH**      | Run migrations       |
| Migration not applied     | HIGH          | Check showmigrations |
| Schema mismatch           | MEDIUM        | Fake + re-migrate    |
| Broken **str**            | ❌ None found | Code is correct      |
| Admin config error        | ❌ None found | Code is correct      |
| ForeignKey issue          | ❌ None found | All valid            |

**FIX: Run migrations on Render**
