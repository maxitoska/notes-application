# Notes Application

The Notes Application is a web-based service that allows users to create, manage, and organize their notes efficiently. This README file provides an overview of the functionality and features offered by the Notes Application.

[Visit the Notes Application Website](https://notes-application-qlmn.onrender.com/)
## Features

1. **User Authentication**
   - Users can register for an account and log in securely.
   - Passwords are securely hashed and stored.

2. **Note Management**
   - Users can create new notes, edit existing notes, and delete notes.
   - Each note includes a title, content, category, and creation date.
   - Notes support basic formatting such as bold, italic, and lists.

3. **Category Management**
   - Users can create new categories to organize their notes.
   - Notes can be categorized under specific categories for easy management.

4. **Filtering and Sorting**
   - Users can filter notes based on categories, creation date, word count, and unique words.
   - Sorting options are available for sorting notes by date, word count, and category.

5. **Responsive Design**
   - The application is responsive and works seamlessly on desktop and mobile devices.
   - The user interface adapts to different screen sizes for optimal user experience.

6. **User-Friendly Interface**
   - The interface is intuitive and easy to navigate, making it convenient for users to manage their notes effectively.

## Installation and Setup

To run the Notes Application locally, follow these steps:

1. Clone the repository to your local machine:
`git clone https://github.com/yourusername/notes-application.git`

2. Navigate to the project directory:
`cd notes-application`
3. Install the required dependencies using pip:
`pip install -r requirements.txt`
4. Create migrations
`python manage.py makemigrations`
5. Apply migrations to create the database schema:
`python manage.py migrate`
6. Create a superuser account for administrative access:
`python manage.py createsuperuser`
7. Start the development server:
`python manage.py runserver`

7. Access the application in your web browser at `http://localhost:8000`.

## Usage

1. **Login/Register**
- Open the application in your browser and log in with your credentials or register for a new account if you don't have one.

2. **View Notes**
- Once logged in, you can view all your notes on the dashboard.
- Use the sidebar to filter and sort notes based on your preferences.

3. **Create/Edit/Delete Notes**
- Click on the "Create a new note" button to create a new note.
- Click on a note to view/edit its content.
- Use the delete button to delete a note permanently.

4. **Manage Categories**
- You can manage categories by creating new categories or assigning notes to existing categories.

5. **Logout**
- Click on the logout button to securely log out of your account.

## Technologies Used

- Python (Django framework)
- HTML/CSS/JavaScript (Bootstrap for styling)
- SQLite database(for development), PostgreSQL(for deploying)
