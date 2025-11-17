from django import forms
from .models import Aula

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['disciplina', 'campus', 'dia_semana', 'turno', 'carga_horaria', 'status']
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'campus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Campus São Paulo'}),
            'dia_semana': forms.Select(attrs={'class': 'form-select'}),
            'turno': forms.Select(attrs={'class': 'form-select'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '40'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'disciplina': 'Disciplina',
            'campus': 'Campus',
            'dia_semana': 'Dia da Semana',
            'turno': 'Turno',
            'carga_horaria': 'Carga Horária Semanal (horas)',
            'status': 'Status',
        }

class BuscaAulaForm(forms.Form):
    disciplina = forms.ChoiceField(
        choices=[('', 'Todas as disciplinas')] + Aula.DISCIPLINA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    campus = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por campus...'
        })
    )
    dia_semana = forms.ChoiceField(
        choices=[('', 'Todos os dias')] + Aula.DIA_SEMANA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    turno = forms.ChoiceField(
        choices=[('', 'Todos os turnos')] + Aula.TURNO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )