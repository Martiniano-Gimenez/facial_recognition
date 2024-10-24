import base64
import io
import json

import face_recognition
import requests
from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils import compare_encodings


@api_view(["POST"])
def recognize_image(request):
    # Get the image encoding from the JSON
    encoding_data = request.data.get("encoding")

    if encoding_data is None:
        return Response(
            {"error": "No encoding provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        image_bytes = base64.b64decode(encoding_data)
        uploaded_image = face_recognition.load_image_file(io.BytesIO(image_bytes))
        # Guardar la imagen para verificar visualmente
        with open("received_image.jpg", "wb") as f:
            f.write(image_bytes)
        # Mostrar la imagen para verificar
        img = Image.open(io.BytesIO(image_bytes))
        img.show()

        encodings = face_recognition.face_encodings(uploaded_image)

        if len(encodings) == 0:
            return Response(
                {"error": "No se encontraron rostros en la imagen"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uploaded_encoding = encodings[0]
        result = compare_encodings(uploaded_encoding)
        return Response({"result": result}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {
                "error": str(e),
                "type": type(e).__name__,
                "args": e.args,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def log_message(request):
    log_message = request.data.get("log", None)
    if log_message is None:
        return Response(
            {"error": "No log message provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if log_message:
        print(log_message)
        if log_message.startswith("Access"):
            print()
    return Response({"message": "Log received"}, status=status.HTTP_200_OK)


def test_api(img_name):
    image_path = f"/home/fabri/Escritorio/img/{img_name}"

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Crear el payload con la imagen codificada
    payload = {"encoding": json.dumps(encoded_image)}

    url = "http://localhost:8000/api/recognize/"

    response = requests.post(url, json=payload)

    print(response.json())
