from django.contrib import admin
from  .models import  Formation, Specialite, Cycle, Region, Departement, Ville, Cycle, Etablissement, Payement
from django_select2.forms import Select2MultipleWidget
from django_select2.forms import Select2Widget
from django import forms

class SpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialite
        fields = '__all__'
        widgets = {
            'etablissement': Select2MultipleWidget(),
        }

class SpecialiteAdmin(admin.ModelAdmin):
    form = SpecialiteForm
    list_display = ('nom', 'formation', 'cycle')
    search_fields = ('nom', 'formation__nom', 'cycle__nom')
    list_filter = ('formation', 'cycle')

class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = '__all__'
        widgets = {
            'departement': Select2Widget(),  # Utilisation de Select2 pour le champ département
        }

class VilleAdmin(admin.ModelAdmin):
    form = VilleForm
    list_display = ('nom', 'departement')
    search_fields = ('nom', 'departement__nom')
    list_filter = ('departement',)

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = '__all__'
        widgets = {
            'departement': Select2Widget(),  # Utilisation de Select2 pour le champ département
        }

class EtablissementAdmin(admin.ModelAdmin):
    form = VilleForm
    list_display = ('nom', 'lieux')
    search_fields = ('nom', 'lieux__nom')
    list_filter = ('lieux',)

# Register your models here.
admin.site.register(Formation)
admin.site.register(Specialite, SpecialiteAdmin)
admin.site.register(Etablissement, EtablissementAdmin)
admin.site.register(Region)
admin.site.register(Departement)
admin.site.register(Ville, VilleAdmin)
admin.site.register(Cycle)
admin.site.register(Payement)
