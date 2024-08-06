from rest_framework import serializers
from .models import Formation, Specialite, Cycle, Region, Departement, Ville, Etablissement
from .models import Payement
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

class SpecialiteSerializers(serializers.ModelSerializer):


    class Meta:
        model = Specialite
        fields = ['id', 'nom']

class VilleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ville
        fields = ['id', 'nom']


class CycleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cycle
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['email']  # Utiliser l'email comme nom d'utilisateur
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create_or_login_user(self):
        email = self.validated_data['email']
        password = self.validated_data['password']
        
        # Tenter de récupérer l'utilisateur existant
        user = User.objects.filter(email=email).first()
        
        if user:
            # Authentifier l'utilisateur existant
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
        else:
            # Créer un nouvel utilisateur
            user = User.objects.create_user(email=email, password=password, username=email)
        
        return user

class PayementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payement
        fields = '__all__'

#test 

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = ['id', 'nom', 'lieux']

class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = ['id', 'nom']

class SpecialiteSerializer(serializers.ModelSerializer):
    etablissement = EtablissementSerializer(many=True)
    
    class Meta:
        model = Specialite
        fields = ['id', 'nom', 'formation', 'cycle', 'etablissement']


    def to_representation(self, instance):
        specialite_data = super().to_representation(instance)
        etablissement_data = specialite_data.pop('etablissement')
        
        result = []
        for etab in etablissement_data:
            ville = Ville.objects.get(id=etab['lieux'])
            etab_data = {
                'nom': specialite_data['nom'],
                'etablissement': etab['nom'],
                'ville': ville.nom
            }
            result.append(etab_data)
        return result