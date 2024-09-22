

from django.shortcuts import render,redirect
from attendance.models import Student, AttendanceRecord,New_Commers_Validate,Contact
from django.contrib import messages
import cv2
import face_recognition
import numpy as np
from datetime import datetime, date
from django.http import StreamingHttpResponse, JsonResponse,HttpResponse
from django.shortcuts import render
import os
from django.conf import settings
from django.db import IntegrityError
import time,re
import subprocess

def index(request):
    return render(request, 'index.html')

def video_feed(request):
    return StreamingHttpResponse(generate(Camera()), content_type='multipart/x-mixed-replace; boundary=frame')

def mark(request):
    return render(request, "mark.html")

def attendance_list(request):

    try:
        today = date.today()
        students = Student.objects.all()
        attendance_records = AttendanceRecord.objects.filter(date=today)
        detected_students = []

        for student in students:
            if attendance_records.filter(student=student).exists():
                detected_students.append({
                    'name': student.name,
                    'is_present': True
                })

        return JsonResponse(detected_students, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class Camera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.known_face_encodings = []
        self.known_face_names = []

    def __del__(self):
        self.video_capture.release()

    def get_frame(self):
        success, frame = self.video_capture.read()
        if success:
            return frame
        else:
            return None

KNOWN_FACES_DIR = "C:\\Users\\rudra\\PycharmProjects\\face_recog_attendance\\known_faces"
def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    current_file_names = set()

    for file_name in os.listdir(KNOWN_FACES_DIR):
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            current_file_names.add(file_name)

            image_path = os.path.join(KNOWN_FACES_DIR, file_name)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]

            name = os.path.splitext(file_name)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)

            # Sync with Student model
            student, created = Student.objects.get_or_create(name=name)
            if not created:
                # If the student exists, check if the encoding needs to be updated
                if not np.array_equal(np.frombuffer(student.face_encoding, dtype=np.float64), encoding):
                    student.face_encoding = encoding.tobytes()
                    student.save()

    # Remove any students from the database that no longer have a corresponding file
    for student in Student.objects.all():
        if f"{student.name}.jpg" not in current_file_names and f"{student.name}.png" not in current_file_names:
            student.delete()

    return known_face_encodings, known_face_names

def generate(camera):
    AttendanceRecord.objects.all().delete()
    known_face_encodings, known_face_names = load_known_faces()

    while True:
        frame = camera.get_frame()
        if frame is None:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            name = "Unknown"

            if any(matches):
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    student = Student.objects.get(name=name)
                    now = datetime.now()

                    attendance_record, created = AttendanceRecord.objects.get_or_create(
                        student=student,
                        date=now.date(),
                        defaults={'time': now.time()}
                    )

                    if not created:
                        attendance_record.time = now.time()
                        attendance_record.save()


            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')



def add(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        roll_no = request.POST.get('roll_no')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            new_stu = New_Commers_Validate(f_name=f_name, l_name=l_name, roll_no=roll_no, email=email, phone=phone)
            new_stu.save()
            return render(request, 'add.html', {'success': True})
        except IntegrityError as e :
            var1 = str(e)
            match = re.search(r'\.([^.]*)$',var1)
            if match:
                result = match.group(1)
            caps_result = result.capitalize()
            error_message = f"ERROR: {caps_result} already exists!"
            return render(request, 'add.html', {'error_message': error_message})

    return render(request, 'add.html')


def validate_user(request):
    f_name = request.GET.get('f_name', '')
    l_name = request.GET.get('l_name', '')
    roll_no = request.GET.get('roll_no', '')
    email = request.GET.get('email', '')
    phone = request.GET.get('phone', '')

    try:
        # Check if the user with the same first name and last name already exists
        if New_Commers_Validate.objects.filter(f_name=f_name, l_name=l_name).exists():
            return JsonResponse({"status": "error", "message": "User with this name already exists."})

        # Check if roll number already exists
        if New_Commers_Validate.objects.filter(roll_no=roll_no).exists():
            return JsonResponse({"status": "error", "message": "Roll number already exists."})

        # Check if email already exists
        if New_Commers_Validate.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already exists."})

        # Check if phone number already exists
        if New_Commers_Validate.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone number already exists."})

        # If all validations pass
        return JsonResponse({"status": "valid"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

def capture_image_view(request):
    f_name = request.GET.get('f_name', '')
    l_name = request.GET.get('l_name', '')

    try:
        # Construct the command with the correct interpreter path
        command = ['C:\\Users\\rudra\\PycharmProjects\\facial_recognition\\.venv\\Scripts\\python.exe', 'capture_image.py', f_name, l_name]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()

        if "Face record already exists!" in output:
            return JsonResponse({"status": "exists"})
        elif "Image saved to" in output:
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": output})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def about(request):
    return render(request,"about.html")
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc,
                          date=datetime.today())
        contact.save()
        messages.success(request, "Form Successfully Submitted")
    return render(request, "contact.html")
def sub_index(request):
    return render(request,"sub_index.html")