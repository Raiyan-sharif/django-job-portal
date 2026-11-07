# Job Portal (Raiyan_Sharif_JobPortal)

A job portal built with Django for *Web Application Development with Python, Level 4, Job 01*.

Many recruiters and many job seekers from different domains share one platform. A recruiter can post several job openings from one account. A job seeker can apply to several openings based on their skills. Both types of user manage their own profile, and both get a dashboard that ranks matches by shared skills.

**Author:** Raiyan Sharif
**ID:** *(add your ID)*

---

## Features

| # | Requirement | How it is built | URL |
|---|---|---|---|
| 1 | Create a Django project named `Name_ID_Project` | Project `Raiyan_Sharif_JobPortal` with two apps, `accounts` and `jobs` | n/a |
| 2 | Registration page: Username, Display name, Email, Password, Confirm password, User type | `RegistrationForm` (extends Django's `UserCreationForm`) and a custom `User` model | `/register/` |
| 3 | Login page: Username, Password | `PortalLoginView` (extends Django's `LoginView`) | `/login/` |
| 4a | Profile page for recruiters: company information | `RecruiterProfile` model and form | `/profile/` |
| 4b | Profile page for job seekers: skill set and resume upload | `JobSeekerProfile` model and form, accepting PDF, DOC or DOCX up to 5 MB | `/profile/` |
| 5 | Job posting page for recruiters: Title, Number of openings, Category, Job description, Skill set | `Job` model and `JobForm` | `/jobs/new/` |
| 6 | Job applying page for job seekers, with search | Keyword and category search, a job detail page with an Apply form | `/jobs/` |
| 7 | Skill-matching dashboard for recruiters and job seekers | Job seekers see jobs ranked by match. Recruiters see candidates ranked for each job. | `/dashboard/` |
| | Create and store the database | SQLite, saved as `db.sqlite3` in the project root | n/a |

Other details:

- The same profile page creates the profile the first time and edits it afterwards, so it also works as the profile manager.
- Each page is limited to the right user type. A job seeker cannot post jobs, for example.
- A job seeker can apply to each job only once. The database enforces this.
- Recruiters can open an applicant's uploaded resume from their dashboard.

---

## Tech stack

- Python 3.13
- Django 6.1
- SQLite (Django's built-in database)
- Django templates with plain CSS. No JavaScript framework is used.

---

## Project structure

```
django-job-portal/
├── manage.py
├── db.sqlite3                     # the database
├── requirements.txt
├── Raiyan_Sharif_JobPortal/       # project settings
│   ├── settings.py
│   └── urls.py                    # root URLs, also serves uploaded media
├── accounts/                      # users and profiles
│   ├── models.py                  # User, Skill, RecruiterProfile, JobSeekerProfile
│   ├── forms.py                   # registration, login and profile forms
│   ├── views.py                   # register, login, logout, profile
│   ├── urls.py
│   ├── utils.py                   # turns "Python, Django" into Skill records
│   └── admin.py
├── jobs/                          # jobs, applications and matching
│   ├── models.py                  # Job, Application
│   ├── forms.py                   # JobForm, ApplicationForm
│   ├── views.py                   # posting, search, apply, dashboards
│   ├── urls.py
│   ├── matching.py                # skill-matching logic
│   ├── decorators.py              # recruiter_required, jobseeker_required
│   └── admin.py
├── templates/
│   ├── base.html                  # shared layout and navigation
│   ├── includes/                  # field.html, match.html, chips.html
│   ├── accounts/                  # register, login, profile
│   └── jobs/                      # job_form, my_jobs, search, job_detail,
│                                  # my_applications, dashboard_jobseeker,
│                                  # dashboard_recruiter
└── media/
    └── resumes/                   # uploaded resumes
```

---

## Setup and running

### 1. Get the code

```bash
git clone <your-repository-url>
cd django-job-portal
```

### 2. Create and activate a virtual environment

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

`(venv)` appears at the start of the terminal line when it is active.

### 3. Install the requirements

```bash
pip install -r requirements.txt
```

### 4. Set up the database

```bash
python manage.py migrate
```

If `db.sqlite3` is already included, this only applies changes that are missing. If it is not included, this creates it.

### 5. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in a browser. Press `Ctrl + C` in the terminal to stop the server.

### Starting again later

```bash
cd django-job-portal
source venv/bin/activate        # Windows: venv\Scripts\activate
python manage.py runserver
```

---

## How to use it

### As a recruiter

1. Go to **Create account** and choose **Recruiter** as the user type.
2. Fill in the company information on the profile page.
3. Open **Post a job** and enter the title, number of openings, category, description and required skills (for example `Python, Django, Git`).
4. **My postings** lists your jobs and how many people applied to each.
5. **Skill matches** shows the job seekers who fit each job, best match first. It includes an *Applied* badge and a link to their resume.

### As a job seeker

1. Go to **Create account** and choose **Job seeker** as the user type.
2. On the profile page, enter your skills separated by commas, and upload your resume.
3. **Skill matches** lists open jobs that share at least one of your skills, best match first.
4. **Find jobs** searches every open job by title, company, skill or keyword, and filters by category.
5. Open a job and click **Apply**. You can add an optional cover letter.
6. **My applications** lists every job you have applied to.

---

## How skill matching works

Skills are stored in one shared table, used by both job postings and job seeker profiles. They are saved in lowercase, so `Python` and `python` count as the same skill.

For each job and job seeker, the portal compares the two skill lists:

```
match % = (required skills the job seeker has ÷ total required skills) × 100
```

**Example:** a job needs `python, django, git, postgresql`. A job seeker has `python, django, git, html`. They have 3 of the 4 required skills, so the match is **75%**. Skills the job doesn't ask for, such as `html` here, don't affect the score.

The dashboard colours each result by strength:

| Match | Level | Colour |
|---|---|---|
| 75% and above | Strong | Green |
| 40% to 74% | Partial | Amber |
| Below 40% | Weak | Red |

Skills the job seeker has appear filled in. Skills they are missing appear with a dashed outline.

The logic is in `jobs/matching.py`.

---

## Database

The project uses SQLite, stored as `db.sqlite3` in the project root.

| Table (model) | Purpose |
|---|---|
| `User` | Login account: username, display name, email, password and user type |
| `Skill` | One row per skill name, shared by jobs and job seekers |
| `RecruiterProfile` | Company information, linked one-to-one with a recruiter |
| `JobSeekerProfile` | Headline, domain, experience, skill set and resume, linked one-to-one with a job seeker |
| `Job` | A job posting. One recruiter can have many jobs. |
| `Application` | A job seeker's application to a job, unique per job and applicant |

To browse the data, create an admin account (step 5 above) and open **http://127.0.0.1:8000/admin/**.

To start over with an empty database:

```bash
rm db.sqlite3                   # Windows: del db.sqlite3
python manage.py migrate
```

---

## URL reference

| URL | Page | Who can use it |
|---|---|---|
| `/register/` | Registration | Anyone |
| `/login/` | Login | Anyone |
| `/profile/` | Create or edit profile | Signed-in users |
| `/dashboard/` | Skill-matching dashboard | Signed-in users with a profile |
| `/jobs/` | Search jobs | Signed-in users |
| `/jobs/<id>/` | Job details and Apply form | Signed-in users |
| `/jobs/new/` | Post a job | Recruiters |
| `/jobs/mine/` | My postings | Recruiters |
| `/applications/` | My applications | Job seekers |
| `/admin/` | Django admin panel | Superusers |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `InconsistentMigrationHistory` | The database was created before the custom user model existed. Delete `db.sqlite3` and run `python manage.py migrate` again. |
| `TemplateDoesNotExist` | Check that the file exists under `templates/` with exactly the name shown in the error (for example `register.html`). |
| `NoReverseMatch` | A template or setting uses a URL name that doesn't exist. Check `LOGIN_REDIRECT_URL` in `settings.py` and the names in each `urls.py`. |
| `No module named django` | The virtual environment isn't active. Run `source venv/bin/activate`. |
| Resume link doesn't open | Check that `MEDIA_URL` and `MEDIA_ROOT` are set in `settings.py`, and that the root `urls.py` adds `static(settings.MEDIA_URL, ...)`. |