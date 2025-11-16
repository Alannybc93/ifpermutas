from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    campus = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.matricula or 'Sem matrícula'}"