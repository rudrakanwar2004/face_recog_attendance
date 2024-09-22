import cv2
import os
import sys
import face_recognition


def capture_image(f_name, l_name):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("Starting camera...")

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return 1

    print("Camera opened, waiting for key press...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame_for_saving = frame.copy()

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles on the frame for display
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Face Detection', frame)

        # Press 's' to save the image or 'q' to quit
        key = cv2.waitKey(1)
        if key == ord('s'):
            print("Saving image...")

            # Extract face encodings
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                face_encoding = face_recognition.face_encodings(frame, known_face_locations=face_locations)[0]

                # Check if face already exists
                known_faces_dir = 'C:\\Users\\rudra\\PycharmProjects\\face_recog_attendance\\known_faces'
                for image_file in os.listdir(known_faces_dir):
                    known_image = face_recognition.load_image_file(os.path.join(known_faces_dir, image_file))
                    known_encoding = face_recognition.face_encodings(known_image)[0]
                    results = face_recognition.compare_faces([known_encoding], face_encoding)
                    if results[0]:
                        print("Face record already exists!")
                        cap.release()
                        cv2.destroyAllWindows()
                        return 2

                # Save the image without rectangles
                image_path = os.path.join(known_faces_dir, f'{f_name} {l_name}.jpg')
                cv2.imwrite(image_path, frame_for_saving)
                print(f"Image saved to {image_path}")
                cap.release()
                cv2.destroyAllWindows()
                return 0
            else:
                print("No face detected.")
        elif key == ord('q'):
            print("Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python capture_image.py <first_name> <last_name>")
    else:
        f_name = sys.argv[1]
        l_name = sys.argv[2]
        exit(capture_image(f_name, l_name))

# C:\\Users\\rudra\\PycharmProjects\\face_recog_attendance\\known_faces\\