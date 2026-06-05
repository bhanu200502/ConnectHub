# ConnectHub

A Django-based social networking application that allows users to connect, share posts, and interact with each other.

## Features

- User authentication (Login/Register)
- User profiles with profile editing
- Create, read, update, and delete posts
- Social interactions (likes, comments)
- Search functionality
- User discovery and following system
- Dashboard for personalized content

## Tech Stack

- **Backend**: Django 3.2+
- **Database**: SQLite (default, can be changed to PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Language**: Python 3.8+

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhanu200502/ConnectHub.git
   cd ConnectHub
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   cd connecthub
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Application: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Project Structure

```
ConnectHub/
├── connecthub/              # Django project settings
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL configuration
│   └── wsgi.py              # WSGI configuration
├── social/                  # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin configuration
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
├── static/                  # CSS and JavaScript files
├── media/                   # User-uploaded media
├── manage.py                # Django management script
└── requirements.txt         # Project dependencies
```

## Usage

### User Registration
1. Navigate to the registration page
2. Fill in your details and create an account
3. Log in with your credentials

### Creating Posts
1. Log in to your account
2. Navigate to the dashboard
3. Click "Create Post" and add your content
4. Posts will be visible to other users

### Profile Management
1. Click on your profile
2. Edit your profile information
3. Update your profile picture or bio

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or suggestions, please contact [your-email@example.com]

---

**Happy Coding! 🚀**
