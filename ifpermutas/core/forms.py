from django import forms
from .models import Aula

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = [
            'tipo', 'disciplina', 'campus', 'horario', 
            'dia_semana', 'turma', 'observacoes', 'turno', 'carga_horaria'
        ]
        widgets = {
            'disciplina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Matemática, Programação...'}),
            'campus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Campus Principal'}),
            'horario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 19:00-20:40'}),
            'turma': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: TSI-2024.1'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Informações adicionais...'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'carga_horaria': forms.Select(attrs={'class': 'form-control'}),
        }

class BuscaAulaForm(forms.Form):
    disciplina = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ex: Matemática, Programação...'
    }))
    campus = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Ex: Campus Principal'
    }))
    dia_semana = forms.ChoiceField(
        choices=[('', 'Todos os dias')] + Aula.DIAS_SEMANA,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    turno = forms.ChoiceField(
        choices=[('', 'Todos os turnos')] + Aula.TURNO_CHOICES,
        required=False, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )