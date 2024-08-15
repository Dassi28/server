from django.shortcuts import render
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Formation, Specialite, Cycle
from .models import  Region, Departement, Ville, Payement, Etablissement
from .serializers import RegisterSerializer, LoginSerializer,  PayementSerializer, SpecialiteSerializer, VilleSerializers
from rest_framework.generics import GenericAPIView
from .serializers import  SpecialiteSerializers, VilleSerializer, FormationSerializer, CycleSerializer
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404


class LoginRegisterView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create_or_login_user()
            return Response({
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VilleListView(APIView):
    def get(self, request, format=None):
        villes = Ville.objects.all()
        serializer = VilleSerializers(villes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FormationListView(APIView):
    def get(self, request, format=None):
        formations = Formation.objects.all()
        serializer = FormationSerializer(formations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SpecialiteListView(APIView):
    def get(self, request, format=None):
        specialites = Specialite.objects.all()
        serializer = SpecialiteSerializers(specialites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CycleListView(APIView):
    def get(self, request, format=None):
        cycles = Cycle.objects.all()
        serializer = CycleSerializer(cycles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def payement_data(request):
    if request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Données reçues et enregistrées'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecialitesByFormationView(generics.ListAPIView):
    serializer_class = SpecialiteSerializer

    def get_queryset(self):
        formation_id = self.kwargs['formation_id']
        specialite_id = self.kwargs['specialite_id']
        ville_id = self.kwargs['ville_id']
        
        # Filtrer les établissements par ville
        etablissements_in_ville = Etablissement.objects.filter(lieux__id=ville_id)
        
        # Filtrer les spécialités par formation dans la ville choisie, exclure l'ID de la spécialité
        specialites_ville = Specialite.objects.filter(
            formation__id=formation_id,
            etablissement__in=etablissements_in_ville
        ).exclude(id=specialite_id).distinct()
        
        # Limiter les résultats
        return specialites_ville[:120]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

