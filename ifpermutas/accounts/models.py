from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, default='MAT-TEMP')
    departamento = models.CharField(max_length=100, default='A definir')
    campus = models.CharField(max_length=100, default='Principal')
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)  # ← ADICIONE ESTA LINHA
    
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.matricula}"

@receiver(post_save, sender=User)
def create_professor(sender, instance, created, **kwargs):
    if created:
        Professor.objects.create(
            user=instance,
            matricula=f"MAT-{instance.id}",
            departamento="A definir",
            campus="Principal"
        )

@receiver(post_save, sender=User)
def save_professor(sender, instance, **kwargs):
    if hasattr(instance, 'professor'):
        instance.professor.save()