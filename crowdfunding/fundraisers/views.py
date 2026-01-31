from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.generics import get_object_or_404
from .models import Fundraiser, Pledge
from .permissions import IsOwnerOrReadOnly
# from .serializers import FundraiserSerializer, PledgeSerializer
from .serializers import FundraiserSerializer, PledgeSerializer, FundraiserDetailSerializer

class FundraiserList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
        ]

    def get(self, request):
        fundraisers = Fundraiser.objects.all()
        serializer = FundraiserSerializer(fundraisers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FundraiserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            ) 
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class FundraiserDetail(APIView):
permission_classes = [
    permissions.IsAuthenticatedOrReadOnly,
    IsOwnerOrReadOnly
]

    def get(self, request, pk):
        fundraiser = get_object_or_404(Fundraiser, pk=pk)
        # serializer = FundraiserSerializer(fundraiser)
        serializer = FundraiserDetailSerializer(fundraiser)
        return Response(serializer.data)
    
    def put(self, request, pk):
        fundraiser = self.get_object_or_404(fundraiser, pk=pk)
        self.check_object_permissions(request, fundraiser)
        serializer = FundraiserDetailSerializer(
            instance=fundraiser,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

 
class PledgeList(APIView):

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

