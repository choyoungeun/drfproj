from rest_framework import viewsets, serializers
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FileSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

class MyPagination(PageNumberPagination):
    page_size = 2

class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer
    pagination_class = MyPagination

    filter_backends = [SearchFilter]
    search_fields = ('title','body')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            qs = qs.filter(author = self.request.user)
        else:
            qs = qs.none()
        
        return qs

class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FileSerializer

    parser_classes = (MultiPartParser, FormParser)  #다양한 타입들의 파일을 수락하도록 설정

    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)