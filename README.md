# Job Board Backend API

A comprehensive Django REST Framework backend for a Job Board platform with user authentication, job listings, applications, reviews, and payment integration.

## 🚀 Features

### 1. User Authentication (10 Marks) ✅
- **Two User Roles**: Job Seeker and Employer
- User registration with email verification
- Login/Logout functionality with JWT tokens
- Email verification link (24-hour expiry)
- Only verified users can log in

### 2. Job Listings (5 Marks) ✅
- Employers can create job listings
- Job details: title, description, requirements, location
- Display key information: title, company, date posted

### 3. Job Details (5 Marks) ✅
- Detailed job view
- Job description, requirements, application instructions
- Job Seekers can apply with resume upload

### 4. User Dashboard (20 Marks) ✅
**Employer Dashboard:**
- Manage posted job listings
- View received applications
- Update job details
- Track application statistics

**Job Seeker Dashboard:**
- Track job applications
- Update resume and profile
- View application status

### 5. Job Categories (5 Marks) ✅
- Industry-based categorization (IT, Healthcare, Finance, etc.)
- Filter jobs by category
- Category management

### 6. Email Notifications (5 Marks) ✅
- Application confirmation to Job Seekers
- New application alerts to Employers
- Application status updates
- Email verification notifications

### 7. Resume Management (10 Marks) ✅
- Upload multiple resumes
- Set default resume
- Secure storage
- Update/Delete resumes

### 8. Application Status Tracking (10 Marks) ✅
- Status: Pending, Reviewing, Shortlisted, Interviewed, Offered, Accepted, Rejected, Withdrawn
- Job Seekers track application status
- Employers update application status
- Status history tracking

### 9. Employer Reviews (5 Marks) ✅
- Job Seekers leave reviews for employers
- Rating system (1-5 stars)
- Comments and detailed ratings
- Verified reviews

### 10. Deployment Ready (5 Marks) ✅
- Production-ready configuration
- Environment variables
- Comprehensive documentation

### 11. Payment Gateway Integration ✅
- Stripe integration for premium features
- Featured job listings
- Payment history and invoices
- Webhook handling

### 12. Swagger Documentation ✅
- Complete API documentation
- Interactive API testing
- Schema definitions

---

## 📋 Table of Contents

- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [User Credentials](#user-credentials)
- [Testing](#testing)
- [Deployment](#deployment)

---

## 🛠 Technology Stack

- **Framework**: Django 4.2.7, Django REST Framework 3.14.0
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Email**: SMTP (Gmail/SendGrid)
- **Payment**: Stripe
- **Task Queue**: Celery + Redis
- **File Storage**: Local/AWS S3

---

## 🏗 Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (React/Vue/Mobile App)                                     │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS (REST API)
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   API Gateway Layer                          │
│  - CORS Middleware                                          │
│  - JWT Authentication                                       │
│  - Rate Limiting                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Application Layer                           │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Users    │  │    Jobs    │  │Applications│           │
│  │   Module   │  │   Module   │  │   Module   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│                                                              │
│  ┌────────────┐  ┌────────────┐                            │
│  │  Reviews   │  │  Payments  │                            │
│  │   Module   │  │   Module   │                            │
│  └────────────┘  └────────────┘                            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Data Layer                                 │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │    Redis     │  │  File Storage│     │
│  │   Database   │  │   (Cache)    │  │   (Media)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  External Services                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     SMTP     │  │    Stripe    │  │    Celery    │     │
│  │ Email Service│  │   Payments   │  │  Task Queue  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Application Workflow

#### 1. User Registration & Authentication Flow
```
User Registration
    ↓
Create User Account (inactive)
    ↓
Generate Verification Token
    ↓
Send Verification Email
    ↓
User Clicks Verification Link
    ↓
Activate Account
    ↓
User Can Login
    ↓
Receive JWT Tokens (Access & Refresh)
```

#### 2. Job Application Flow
```
Job Seeker Views Job Listing
    ↓
Clicks "Apply"
    ↓
Upload Resume + Cover Letter
    ↓
Submit Application
    ↓
Send Email to Job Seeker (Confirmation)
    ↓
Send Email to Employer (New Application)
    ↓
Application Status: Pending
    ↓
Employer Reviews Application
    ↓
Update Status (Shortlisted/Rejected/etc.)
    ↓
Send Status Update Email to Job Seeker
```

#### 3. Payment Flow
```
Employer Selects Premium Feature
    ↓
Choose Payment Plan
    ↓
Create Payment Intent (Stripe)
    ↓
Process Payment
    ↓
Webhook Receives Payment Status
    ↓
Update Payment Record
    ↓
Generate Invoice
    ↓
Apply Premium Features
```

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Redis (for Celery)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd job_board_project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 5: Database Setup
```bash
# Create PostgreSQL database
createdb job_board_db

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Create Initial Data
```bash
python manage.py shell
```

```python
from apps.jobs.models import JobCategory

categories = [
    {'name': 'Information Technology', 'slug': 'it', 'icon': '💻'},
    {'name': 'Healthcare', 'slug': 'healthcare', 'icon': '🏥'},
    {'name': 'Finance', 'slug': 'finance', 'icon': '💰'},
    {'name': 'Education', 'slug': 'education', 'icon': '📚'},
    {'name': 'Marketing', 'slug': 'marketing', 'icon': '📢'},
    {'name': 'Sales', 'slug': 'sales', 'icon': '🤝'},
    {'name': 'Engineering', 'slug': 'engineering', 'icon': '⚙️'},
    {'name': 'Design', 'slug': 'design', 'icon': '🎨'},
]

for cat in categories:
    JobCategory.objects.get_or_create(**cat)
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

### Step 9: Start Celery (Optional, for async tasks)
```bash
# In a new terminal
celery -A config worker -l info

# For scheduled tasks
celery -A config beat -l info
```

---

## ⚙️ Configuration

### Database Configuration
Edit `.env` file:
```env
DB_NAME=job_board_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Email Configuration (Gmail Example)
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note**: For Gmail, you need to generate an App Password:
1. Go to Google Account Settings
2. Security → 2-Step Verification
3. App passwords → Generate

### Stripe Configuration
```env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 📚 API Endpoints

### Base URL
```
http://localhost:8000/api
```

### Swagger Documentation
```
http://localhost:8000/api/docs/
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register/` | User registration | No |
| POST | `/auth/login/` | User login | No |
| GET | `/auth/verify-email/?token=` | Verify email | No |
| POST | `/auth/token/refresh/` | Refresh JWT token | No |
| GET | `/auth/profile/` | Get user profile | Yes |
| PUT | `/auth/profile/` | Update user profile | Yes |
| GET | `/auth/profile/job-seeker/` | Get job seeker profile | Yes |
| PUT | `/auth/profile/job-seeker/` | Update job seeker profile | Yes |
| GET | `/auth/profile/employer/` | Get employer profile | Yes |
| PUT | `/auth/profile/employer/` | Update employer profile | Yes |

### Resume Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/auth/resumes/` | List resumes | Yes |
| POST | `/auth/resumes/` | Upload resume | Yes |
| GET | `/auth/resumes/{id}/` | Get resume details | Yes |
| PUT | `/auth/resumes/{id}/` | Update resume | Yes |
| DELETE | `/auth/resumes/{id}/` | Delete resume | Yes |

### Job Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/jobs/categories/` | List job categories | No |
| GET | `/jobs/` | List all jobs | No |
| POST | `/jobs/` | Create job (Employer) | Yes |
| GET | `/jobs/{id}/` | Get job details | No |
| PUT | `/jobs/{id}/` | Update job (Employer) | Yes |
| DELETE | `/jobs/{id}/` | Delete job (Employer) | Yes |
| GET | `/jobs/my-jobs/` | List employer's jobs | Yes |
| GET | `/jobs/saved/` | List saved jobs | Yes |
| POST | `/jobs/{id}/save/` | Save/unsave job | Yes |

### Application Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/applications/` | List applications | Yes |
| POST | `/applications/` | Submit application | Yes |
| GET | `/applications/{id}/` | Get application details | Yes |
| PUT | `/applications/{id}/` | Update application | Yes |
| DELETE | `/applications/{id}/` | Withdraw application | Yes |
| GET | `/applications/my-applications/` | List job seeker applications | Yes |
| GET | `/applications/job/{job_id}/` | List job applications (Employer) | Yes |
| PATCH | `/applications/{id}/status/` | Update status (Employer) | Yes |

### Review Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/reviews/` | List user's reviews | Yes |
| POST | `/reviews/` | Create review | Yes |
| GET | `/reviews/{id}/` | Get review details | Yes |
| PUT | `/reviews/{id}/` | Update review | Yes |
| DELETE | `/reviews/{id}/` | Delete review | Yes |
| GET | `/reviews/employer/{employer_id}/` | List employer reviews | No |

### Payment Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/payments/plans/` | List payment plans | No |
| POST | `/payments/create/` | Create payment | Yes |
| GET | `/payments/` | List user payments | Yes |
| GET | `/payments/{id}/` | Get payment details | Yes |
| POST | `/payments/webhook/stripe/` | Stripe webhook | No |

---

## 🗄️ Database Models

### User Model
- Custom user model with email as username
- Roles: Job Seeker, Employer, Admin
- Email verification system

### JobSeekerProfile
- Bio, skills, experience
- Education, portfolio links
- Resume management

### EmployerProfile
- Company information
- Industry, location
- Company logo

### Job
- Job details and requirements
- Salary range, location
- Job type, experience level
- Featured listings

### Application
- Resume and cover letter
- Application status tracking
- Status history

### EmployerReview
- Rating system (1-5 stars)
- Comments and feedback
- Verification status

### Payment & Invoice
- Payment processing
- Transaction history
- Invoice generation

---

## 👥 User Credentials

### Admin Credentials
```
Email: admin@jobboard.com
Password: Admin@123456
Role: Admin
```

### Job Seeker Credentials
```
Email: jobseeker@example.com
Password: JobSeeker@123
Role: Job Seeker
```

### Employer Credentials
```
Email: employer@company.com
Password: Employer@123
Role: Employer
```

### Creating Test Users

#### Via Django Admin
1. Go to `http://localhost:8000/admin`
2. Login with admin credentials
3. Navigate to Users → Add User
4. Fill in details and select role

#### Via API
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass@123",
    "password_confirm": "TestPass@123",
    "first_name": "Test",
    "last_name": "User",
    "role": "job_seeker"
  }'
```

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### With Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### API Testing with Swagger
1. Go to `http://localhost:8000/api/docs/`
2. Click "Authorize" button
3. Enter JWT token: `Bearer <your_access_token>`
4. Test endpoints interactively

---

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku App**
```bash
heroku create job-board-api
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set Environment Variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
```

5. **Deploy**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### AWS/DigitalOcean Deployment

1. **Setup Server (Ubuntu)**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

2. **Clone Repository**
```bash
git clone <repository-url>
cd job_board_project
```

3. **Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

4. **Configure Gunicorn**
Create `/etc/systemd/system/gunicorn.service`

5. **Configure Nginx**
Create `/etc/nginx/sites-available/jobboard`

6. **Setup SSL (Let's Encrypt)**
```bash
sudo certbot --nginx -d yourdomain.com
```

---

## 📝 API Usage Examples

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "SecurePass@123",
    "password_confirm": "SecurePass@123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "job_seeker",
    "phone": "+1234567890"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "SecurePass@123"
  }'
```

### Create Job (Employer)
```bash
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "Looking for experienced Python developer",
    "requirements": "5+ years Python, Django experience",
    "category": "<category_id>",
    "job_type": "full_time",
    "location": "New York, NY",
    "salary_min": 80000,
    "salary_max": 120000,
    "status": "published"
  }'
```

### Apply for Job (Job Seeker)
```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Bearer <access_token>" \
  -F "job=<job_id>" \
  -F "resume=@/path/to/resume.pdf" \
  -F "cover_letter=I am interested in this position..."
```

---

## 🔧 Troubleshooting

### Common Issues

#### Email Not Sending
- Check email configuration in `.env`
- Verify SMTP credentials
- Check firewall settings

#### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials
- Ensure database exists

#### JWT Token Expired
- Tokens expire after 1 hour
- Use refresh token endpoint to get new access token

---

## 📄 License

MIT License

## 👨‍💻 Author

Job Board Backend Team

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📞 Support

For issues and questions:
- Email: support@jobboard.com
- GitHub Issues: [Create Issue]

---

**Happy Coding! 🚀**