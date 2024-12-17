from rest_framework.viewsets import ReadOnlyModelViewSet
from authors.serializers import AuthSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class AuthView(ReadOnlyModelViewSet):
    serializer_class = AuthSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        User = get_user_model()

        query_set = User.objects.filter(username=self.request.user.username)
        return query_set
    
    @action(
            methods=['get',],
            detail=False,
    )
    def me(self,request):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj
        )
        return Response(serializer.data)

    
    