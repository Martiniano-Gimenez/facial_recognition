import face_recognition
from api.models import ReferenceImage

def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    """
    Compare a list of face encodings against a candidate encoding to see if they match.

    :param known_face_encodings: A list of known face encodings
    :param face_encoding_to_check: A single face encoding to compare against the list
    :param tolerance: How much distance between faces to consider it a match. Lower is more strict. 0.6 is default.
    :return: A list of True/False values indicating which known_face_encodings match the face encoding to check
    """
    distances = face_recognition.face_distance(known_face_encodings, face_encoding_to_check)
    # For debugging
    # print(f"Distances: {distances}")
    return list(distances <= tolerance)

def compare_encodings(uploaded_encoding):
    ref_encodings = []
    ref_names = []
    ref_legajos = []

    # Get all encodings from reference images
    for ref_image in ReferenceImage.objects.all():
        try:
            ref_image_path = ref_image.image.path
            reference_image = face_recognition.load_image_file(ref_image_path)
            reference_encoding = face_recognition.face_encodings(reference_image)

            if reference_encoding:  # If valid encodings are found
                ref_encodings.append(reference_encoding[0])  # Add the reference encoding
                ref_names.append(ref_image.name)
                ref_legajos.append(ref_image.legajo)
        except Exception as e:
            print(f"Error procesando la imagen de referencia {ref_image.name}: {e}")

    if not ref_encodings:
        return "No se encontraron imágenes de referencia"

    # Compare the uploaded encoding with all reference encodings
    matches = compare_faces(ref_encodings, uploaded_encoding, tolerance=0.6)
    # For debugging
    # print(f"Matches: {matches}")
    distances = face_recognition.face_distance(ref_encodings, uploaded_encoding)

    # Find the best match (the one with the smallest distance) and check if it is below the tolerance
    best_match_index = None
    if matches:
        best_match_index = distances.argmin() if len(distances) > 0 else None

    if best_match_index is not None and distances[best_match_index] <= 0.6:
        return f"Es el alumno: {ref_names[best_match_index]} con legajo: {ref_legajos[best_match_index]}"
    else:
        return "No se encontro alumno similar"
