# Facial Recognition Attendance System

This is an automated attendance management system using facial recognition technology. The system captures faces in real-time, compares them to a known database, and marks attendance accordingly. The project is built using Python, Django, OpenCV, and machine learning libraries.

## Features

- **Automated Attendance**: Uses facial recognition to mark attendance.
- **Real-time Processing**: Detects and processes faces live using a webcam.
- **Admin Management**: Includes an admin interface for viewing attendance records and managing users.
- **User-Friendly Frontend**: Smooth animations, progress bars, and alerts for better user experience.

---

## Installation

Follow these steps to set up and run the project locally.

### Prerequisites

Before you begin, make sure you have the following installed:

- Python (version 3.12 or later)
- Django (version 4.2 or later)
- Virtual environment (Recommended: `virtualenv`)
- Git

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YourUsername/facial_recognition_attendance_system.git
    cd facial_recognition_attendance_system
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv facial_recognition_env
    ```

3. **Activate the virtual environment**:

    - **Windows**:
        ```bash
        facial_recognition_env\Scripts\activate
        ```
    - **Linux/Mac**:
        ```bash
        source facial_recognition_env/bin/activate
        ```

4. **Install the required Python modules**:
    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file contains the following necessary libraries:
    ```text
    Django==4.2
    dlib
    face_recognition
    opencv-python
    numpy
    pillow
    ```

5. **Set up the Django environment**:
    - Navigate to your project folder and run migrations:
      ```bash
      python manage.py makemigrations
      python manage.py migrate
      ```

6. **Create a superuser for Django admin**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Django development server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the application**:
   - Open your browser and visit `http://127.0.0.1:8000/` to view the application.
   - Go to `http://127.0.0.1:8000/admin/` to access the Django admin interface.

---

## Usage

1. **Mark Attendance**: On the homepage, click "Mark Your Attendance" and allow the system to access your webcam. The system will process the face, mark the attendance, and store it in the database.

2. **Admin Dashboard**: Use the admin login to access and manage attendance records.

3. **Add New Users**: Add new students and their facial data via the "Add User" option. The system validates and stores the face in the database.

---

## Screenshots

Include relevant screenshots of your system to give a visual understanding of how the system works. Example:

1. **Homepage**:
   ![Homepage](![image](https://github.com/user-attachments/assets/f7aa8ec2-24cf-4756-8cfb-c5e70dacfbaf)
)

2. **Admin Dashboard**:
   ![Admin Dashboard](![image](https://github.com/user-attachments/assets/479c9860-a1be-4b76-a164-52fcb9fa23f1)
)

---

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Facial Recognition**: OpenCV, dlib, face_recognition library
- **Database**: SQLite
- **Version Control**: Git, GitHub

---

## Contributing

Feel free to open issues or pull requests to improve this project.

---

## License

This project is licensed under the MIT License.

---


