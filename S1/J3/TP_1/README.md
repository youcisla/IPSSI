# Task Manager Application

## Overview

This is a web-based Task Manager application built with Flask. It supports user registration, login, and various task operations. Administrators have additional features like bulk user upload, task export/import, reward updates, ranking, and more.

## Project Structure

- **app.py**: The Flask application file containing all routes, models, and logic.
- **templates/**: Contains HTML templates split into:
  - **auth/**: Authentication pages (login, register, forgot password).
  - **admin/**: Admin routes and panels (admin panel, ranking, bulk upload, etc.)
  - **tasks/**: Task-related pages (home, finished tasks, delayed tasks).
  - **base.html**: The layout template with navigation and shared structure.
- **static/**:
  - **css/**: Custom CSS files (style.css).
  - **js/**: Custom JavaScript files (index.js for inline editing and AJAX updates).
- **instance/**: Contains the SQLite database file (db.sqlite3).
- **requirements.txt**: Lists the Python package dependencies.

## Setup and Installation

1. **Clone/Download the repository** to your local machine.
2. **Create a virtual environment** (optional but recommended):
   - Windows: `python -m venv venv` and then `venv\Scripts\activate`
3. **Install the dependencies** using:
   - `pip install -r requirements.txt`
4. **Run the application**:
   - Execute `python app.py`
   - The app will start in debug mode on `http://127.0.0.1:5000/`

## Database and Initialization

- The app uses SQLite (db.sqlite3) located in the instance folder.
- On first run, the database is created and seeded with default users (user0, user1, and an admin). Also, test tasks are added (to-do, finished, and delayed tasks).
- The admin account credentials are:
  - Username: **admin**
  - Password: **admin**

## Navigating the Application

### For Regular Users

- **Login/Register**: Use the login or register pages (under the auth folder) to create and log into your account.
- **Home (To-Do List)**:
  - Add new tasks with defined priorities (Low, Normal, High).
  - Edit tasks inline by clicking the "Edit" button.
  - Mark tasks as completed using the checkbox (which awards reward points).
  - Filter tasks by priority, status, and update time.
- **Finished Tasks & Delayed Tasks**:
  - View tasks that have been marked as finished on the Finished Tasks page.
  - View tasks that are delayed (past due) on the Delayed Tasks page.
- **Password Reset**:
  - Use the "Forgot Password?" link on the login page.
  - You must retype the secret phrase shown on the form exactly to reset your password.
  - The system does not allow reusing your previous password.

### For Administrators

After logging in as an admin (e.g., using the admin account above), you have access to additional features:

- **Admin Panel**:
  - Accessible via the navigation bar.
  - Link to view all tasks, export/import tasks (CSV), update rewards, view ranking, and bulk upload users.
- **Admin Tasks**: 
  - See a detailed table of all tasks created by any user.
- **Export/Import Tasks**:
  - Export tasks as CSV.
  - Import tasks after selecting a CSV file with the required columns.
- **Update Rewards**:
  - Update users' reward points manually via an admin form.
- **User Ranking**:
  - View a ranking list of users ordered by their reward points.
- **Bulk Upload**:
  - Add many users at once using a CSV file.
  - CSV format: username, email, password, (optional)isAdmin, (optional)reward_points.
- **Admin Users**:
  - View all users and their information (username, email, hashed password, admin status, assigned tasks).

## Running the App (Technical Details)

- **Flask & SQLAlchemy**: The application uses Flask for routing and SQLAlchemy for ORM mapping.
- **Security**: Passwords are stored using bcrypt hashed format.
- **Forms**: The application leverages Flask-WTForms for form validation.
- **AJAX**: Inline task editing uses JavaScript (AJAX call to endpoints like `/update_task` and `/update_priority`).
- **Session Management**: User session info (like user_id and username) is stored in Flask's session.
- **Decorators**: Custom decorators (`login_required` and `admin_required`) restrict access to specific routes.

## How to Navigate (User Perspective)

1. **Start at the Home Page**: After login, you are redirected to the To-Do list.
2. **Add Tasks**: Use the text input and select the task priority then click "Add Task."
3. **Edit Tasks and Priority**: Click "Edit" to change task text or "Edit Priority" to update a task’s priority.
4. **Mark Tasks as Done/Undone**: Simply check/uncheck the checkbox beside each task.
5. **Filter Tasks**: Use the filter form at the top to filter tasks by priority, status, or update date.
6. **Use Navigation Bar**: Access other pages like Finished Tasks, Delayed Tasks, or Help Modal for instructions.
7. **Help Modal**: Click the Help icon (question mark) in the navigation bar to see an explanation of all features.

## How to Navigate (Admin Perspective)

1. **Access the Admin Panel**: Log in as an admin and click the "Admin Panel" link in the navigation.
2. **View All Tasks/Users**: Navigate to view tasks and various admin functionalities.
3. **Perform Bulk Operations**: Use links to export/import tasks and bulk upload users.
4. **Update Rewards & View Ranking**: Manage user rewards on the update rewards page and check the ranking page for user standings.

## Additional Notes

- **Modifications**: The application is designed to be modular. Template inheritance is used with `base.html` providing a shared layout.
- **Styling**: Bootstrap 5 is used for UI components and custom styling is in `static/css/style.css`.
- **JavaScript**: Client-side editing and AJAX updates are in `static/js/index.js`.
- **Debug Mode**: Running `app.py` in debug mode allows changes to be reloaded automatically.

Happy task managing!
