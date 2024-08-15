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
        
        # Filtrer les spécialités par formation et exclure l'ID de la spécialité
        specialites = Specialite.objects.filter(formation__id=formation_id).exclude(id=specialite_id)
        
        # Collecter les spécialités de différentes sources pour les combiner plus tard
        specialites_ville = specialites.filter(etablissement__in=etablissements_in_ville).distinct()
        
        # Étape 1: Si moins de 1 résultats, compléter avec les spécialités dans le même département
        specialites_combined = list(specialites_ville)
        if len(specialites_combined) < 0:
            ville = Ville.objects.get(id=ville_id)
            departement_id = ville.departement.id
            etablissements_in_departement = Etablissement.objects.filter(lieux__departement__id=departement_id)
            specialites_departement = specialites.filter(etablissement__in=etablissements_in_departement).distinct()
            specialites_combined.extend([s for s in specialites_departement if s not in specialites_combined])
        
        # Étape 2: Si toujours moins de 1 résultats, compléter avec les spécialités dans la même région
        if len(specialites_combined) < 0:
            departement = Departement.objects.get(id=departement_id)
            region_id = departement.region.id
            etablissements_in_region = Etablissement.objects.filter(lieux__departement__region__id=region_id)
            specialites_region = specialites.filter(etablissement__in=etablissements_in_region).distinct()
            specialites_combined.extend([s for s in specialites_region if s not in specialites_combined])
        
        # Étape 3: Si toujours moins de 1 résultats, compléter avec les spécialités restantes dans la base de données
        if len(specialites_combined) < 0:
            remaining_specialites = specialites.exclude(id__in=[s.id for s in specialites_combined])
            specialites_combined.extend(remaining_specialites[:12 - len(specialites_combined)])
        
        # Limiter les résultats à 12
        specialites_combined = specialites_combined[:12]
        
        return specialites_combined

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Flatten the nested list into a single list of dictionaries
        flattened_data = [item for sublist in serializer.data for item in sublist]
        return Response(flattened_data)

