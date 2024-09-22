import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Student, New_Commers_Validate

@receiver(post_delete, sender=Student)
def delete_face_file(sender, instance, **kwargs):
    """
    Deletes the corresponding face image file in the known_faces directory
    when a Student record is deleted.
    Also deletes the corresponding New_Commers_Validate record.
    """
    # Split the Student's name into first and last names
    try:
        f_name, l_name = instance.name.split(' ', 1)
    except ValueError:
        # If the name doesn't have a space, treat it as f_name with no l_name
        f_name, l_name = instance.name, ''

    # Delete the New_Commers_Validate record
    try:
        new_comer_record = New_Commers_Validate.objects.get(f_name=f_name, l_name=l_name)
        new_comer_record.delete()
    except New_Commers_Validate.DoesNotExist:
        pass  # Record does not exist, do nothing

    # Delete the face image file
    known_faces_dir = 'C:\\Users\\rudra\\PycharmProjects\\face_recog_attendance\\known_faces'  # Replace with your actual directory path
    possible_extensions = ['png', 'jpg']
    for ext in possible_extensions:
        face_image_path = os.path.join(known_faces_dir, f"{instance.name}.{ext}")
        if os.path.exists(face_image_path):
            os.remove(face_image_path)
            break  # Stop after deleting the first match

