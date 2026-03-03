# Zainussunna Academy - Backend API

A comprehensive Django-based backend for the Zainussunna Academy admission system.

## 🏗️ Architecture

This backend follows a **process-driven, state-controlled architecture** where:

- Backend enforces all rules, validation, and state transitions
- Frontend acts only as a structured interface
- Each step owns its fields - cannot modify previous steps
- Program locking prevents changes after step 1

## 🚀 Features

### Admission System

- **State Machine**: Draft → Submitted → Under Review → Approved/Rejected
- **Step-by-Step Progress**: Each step tracked and locked
- **Auto Age Calculation**: Backend recalculates age independently
- **Draft Auto-Save**: Auto-save on blur, step change, and idle timer
- **File Upload**: Photos and documents with duplicate detection (hash-based)

### Program-Aware Logic

- Programs stored in DB (not hardcoded)
- Dynamic form fields per program
- Conditional questions and validation rules
- Age limits enforced by backend

### Admin Panel

- Filter by program, status, date range
- View complete admission snapshots
- Internal notes (staff only)
- State transition logging

### Analytics

- Time spent per step tracking
- Drop-off analysis
- Program demand trends
- Validation failure tracking

## 📁 Project Structure

```
backend/
├── backend/          # Django project config
│   ├── settings.py   # Settings with JWT, CORS, logging
│   └── urls.py       # Root URL configuration
├── core/             # Main application
│   ├── models.py     # All data models
│   ├── serializers.py # API serializers
│   ├── views.py      # API viewsets
│   ├── urls.py       # API URLs
│   ├── admin.py      # Admin panel config
│   ├── signals.py    # Event handling
│   └── management/
│       └── commands/ # Custom management commands
└── requirements.txt  # Python dependencies
```

## 🛠️ Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Initialize System (Optional)

```bash
python manage.py init_system
```

This creates sample programs, content pages, and achievements.

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## 📡 API Endpoints

### Programs

- `GET /api/programs/` - List all active programs
- `GET /api/programs/{id}/schema/` - Get program form schema

### Admissions

- `POST /api/admissions/` - Create new admission
- `GET /api/admissions/` - List admissions (with filters)
- `GET /api/admissions/{id}/` - Get admission details
- `POST /api/admissions/{id}/complete_step/` - Complete current step
- `POST /api/admissions/{id}/submit/` - Submit admission
- `POST /api/admissions/{id}/transition/` - Admin state transition

### Content

- `GET /api/content/` - List published pages
- `GET /api/content/{slug}/` - Get specific page

### Analytics

- `GET /api/analytics/admissions/` - Admission analytics
- `GET /api/analytics/dashboard/` - Dashboard summary

## 🔐 Authentication

Uses JWT tokens:

```
POST /api/auth/token/        # Get tokens
POST /api/auth/token/refresh/ # Refresh token
```

Include token in headers:

```
Authorization: Bearer <access_token>
```

## 🎨 Frontend Integration

The backend returns form schemas that the frontend renders:

```javascript
// GET /api/programs/{id}/schema/
{
  "program": { "name": "Thahfīẓ-ul-Qur'an", "min_age": 9, "max_age": 18 },
  "schema": [
    { "step": 1, "field_key": "name", "label": "Full Name", "required": "required" },
    { "step": 1, "field_key": "dob", "label": "Date of Birth", "field_type": "date" },
    ...
  ]
}
```

## 📊 State Machine

```
Draft → Submitted → Under Review → Approved/Rejected
  ↑                              ↓
  └────────── Back to Draft ─────┘
```

## 🛡️ Security Features

- Rate limiting (configure in production)
- Duplicate detection (phone + program)
- File hash verification
- Admin action audit logs
- Soft delete only (never hard delete)

## 📈 Future Extensions

The architecture supports adding:

- Fee collection module
- Batch allocation
- Attendance tracking
- Certificate generation
- Alumni tracking
- WhatsApp/Telegram bot integration

## 📝 License

Proprietary - Zainussunna Academy
