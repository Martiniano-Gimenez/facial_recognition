import face_recognition
from django.core.cache import cache

from api.models import ReferenceImage

CACHE_TIMEOUT = 60 * 60  # Cachea las codificaciones por 1 hora


def load_reference_encodings():
    """Carga las codificaciones de referencia y las almacena en el caché de Django."""
    ref_encodings = []
    ref_names = []
    ref_legajos = []

    for ref_image in ReferenceImage.objects.all():
        try:
            ref_image_path = ref_image.image.path
            reference_image = face_recognition.load_image_file(ref_image_path)
            reference_encoding = face_recognition.face_encodings(reference_image)

            if reference_encoding:  # Si se encuentran codificaciones válidas
                ref_encodings.append(reference_encoding[0])
                ref_names.append(ref_image.name)
                ref_legajos.append(ref_image.legajo)
        except Exception as e:
            print(f"Error procesando la imagen de referencia {ref_image.name}: {e}")

    # Guarda en el caché de Django
    cache.set(
        "reference_encodings",
        {"encodings": ref_encodings, "names": ref_names, "legajos": ref_legajos},
        CACHE_TIMEOUT,
    )


def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    """Compara las codificaciones faciales para determinar coincidencias dentro de la tolerancia."""
    distances = face_recognition.face_distance(
        known_face_encodings, face_encoding_to_check
    )
    return list(distances <= tolerance), distances


def compare_encodings(uploaded_encoding):
    # Cargar las codificaciones de referencia desde el caché
    reference_data = cache.get("reference_encodings")

    if not reference_data:
        print("Cargando las codificaciones de referencia en la caché...")
        load_reference_encodings()
        reference_data = cache.get("reference_encodings")

    if not reference_data or not reference_data["encodings"]:
        return "No se encontraron imágenes de referencia"

    ref_encodings = reference_data["encodings"]
    ref_names = reference_data["names"]
    ref_legajos = reference_data["legajos"]

    # Comparar la codificación cargada con las codificaciones de referencia
    matches, distances = compare_faces(ref_encodings, uploaded_encoding, tolerance=0.5)

    best_match_index = None
    if matches:
        best_match_index = distances.argmin() if len(distances) > 0 else None

    if best_match_index is not None and distances[best_match_index] <= 0.5:
        return f"Es el alumno: {ref_names[best_match_index]} con legajo: {ref_legajos[best_match_index]}"
    else:
        return "No se encontro alumno similar"
