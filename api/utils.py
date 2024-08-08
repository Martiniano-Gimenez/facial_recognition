import face_recognition
from .models import ReferenceImage

def compare_encodings(uploaded_encoding):
    reference_encodings = []
    reference_names = []

    for ref_image in ReferenceImage.objects.all():
        try:
            ref_image_path = ref_image.image.path
            reference_image = face_recognition.load_image_file(ref_image_path)
            reference_encoding = face_recognition.face_encodings(reference_image)
            if reference_encoding:
                reference_encodings.append(reference_encoding[0])
                reference_names.append(ref_image.name)
        except Exception as e:
            continue

    for ref_encoding, name in zip(reference_encodings, reference_names):
        if face_recognition.compare_faces([ref_encoding], uploaded_encoding)[0]:
            return f"Match found: {name}"

    return "No match found"
