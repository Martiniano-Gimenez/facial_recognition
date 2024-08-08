import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import face_recognition

from api.utils import compare_encodings

@api_view(['POST'])
def recognize_image(request):
    # Get the image encoding from the JSON
    encoding_data = request.data.get('encoding', None)
    
    if encoding_data is None:
        return Response({"error": "No encoding provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Convert the received JSON back to a NumPy array
        uploaded_encoding = face_recognition.face_encodings(
            face_recognition.load_image_file(io.BytesIO(json.loads(encoding_data)))
        )[0]
        
        result = compare_encodings(uploaded_encoding)
        return Response({"result": result}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
