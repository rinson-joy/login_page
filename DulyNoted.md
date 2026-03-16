# DulyNoted

DulyNoted is a web-based note-taking application designed for secure and organized personal documentation. It supports user authentication, note management (CRUD), sharing, and data portability through import/export features.

## Project Overview

- **Purpose:** A lightweight, secure note-taking platform.
- **Backend:** [Flask](https://flask.palletsprojects.com/) (Python) using Blueprints for modular routing.
- **Database:** [MongoDB](https://www.mongodb.com/) via `pymongo`, with collections for `userdata`, `notes`, and `shared`.
- **Frontend:** HTML templates using [Jinja2](https://jinja.palletsprojects.com/) and custom CSS located in the `beaut/` directory.
- **Architecture:** 
    - `server/`: Core logic, including routes (`server/routes/`), database models/utilities (`server/monkey.py`), and the entry point (`server/main.py`).
    - `templates/`: Jinja2 templates for the web interface.
    - `beaut/`: Static assets (CSS, images).

## Building and Running

### Prerequisites
- Python 3.x
- MongoDB instance (local or Atlas)
- Required Python packages: `flask`, `pymongo`

### Environment Variables
The application requires two key environment variables to function correctly:
- `apple`: Controls the execution mode. 
    - Set to `'apple keeps doc away'` to run in **Debug Mode** (local development).
    - Any other value will trigger **Production Mode** (runs on `0.0.0.0:5000` with SSL context).
- `banana`: The MongoDB connection string (e.g., `mongodb+srv://...`).

### Running the Application
```powershell
# Development mode
$env:apple = 'apple keeps doc away'
$env:banana = 'your_mongodb_connection_string'
python server/main.py
```

### Deployment
A `deploy.sh` script is provided for server-side updates, which pulls the latest code from `main` and restarts the `dulynoted` systemd service.

## Development Conventions

- **Modular Routing:** All routes are organized into Blueprints under `server/routes/`.
- **Authentication:** Use the `@login_required` decorator from `server/monkey.py` to protect routes.
- **Admin Access:** Use the `@admin_required` decorator for administrative functions (requires existing `role: "master"` in the database). No new master accounts can be created through the application.
- **Styling:** CSS is centralized in `beaut/ooo.css`.
- **API Responses:** Prefer `fl.jsonify` for consistent API responses.

## Roadmap & Known Issues
- [ ] **React Migration:** Plans to move the frontend to React (as noted in `todo.md`).
- [ ] **Diary Feature:** Implementation of a "keystroke-replaying" diary.
- [ ] **Email Sharing:** Enhancing the sharing feature with email notifications.
- [ ] **UI Bug:** When line numbers are toggled off in the notes area, text overflow may disable scrolling in the hit area.

## Key Files
- `server/main.py`: Entry point and application configuration.
- `server/monkey.py`: Database connection and authentication decorators.
- `server/routes/notes.py`: Core note management logic.
- `todo.md`: Tracks ongoing tasks and feature requests.
