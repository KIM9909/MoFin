from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class SignupView(RegisterView):
    serializer_class = CustomRegisterSerializer


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response(
                {"detail": "Account successfully deleted."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        

from rest_framework.decorators import api_view, permission_classes
from .serializers import UserUpdateSerializer

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = UserUpdateSerializer(
        user, 
        data=request.data, 
        context={'request': request},
        partial=True
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)