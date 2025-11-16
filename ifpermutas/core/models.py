from django.db import models
from accounts.models import Professor

class Aula(models.Model):
    TIPO_CHOICES = [
        ('oferecida', 'Aula Oferecida'),
        ('desejada', 'Aula Desejada'),
    ]
    
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('negociacao', 'Em Negociação'),
        ('realizada', 'Permuta Realizada'),
    ]
    
    DIAS_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
    ]
    TURNO_CHOICES = [
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'), 
        ('noturno', 'Noturno'),
    ]
    
    CARGA_HORARIA_CHOICES = [
        ('2h', '2 horas'),
        ('4h', '4 horas'),
        ('6h', '6 horas'),
    ]

    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, default='noturno')
    carga_horaria = models.CharField(max_length=10, choices=CARGA_HORARIA_CHOICES, default='4h')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='oferecida')
    disciplina = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    horario = models.CharField(max_length=50, help_text="Ex: 19:00-20:40")
    dia_semana = models.CharField(max_length=20, choices=DIAS_SEMANA)
    turma = models.CharField(max_length=50, blank=True)
    observacoes = models.TextField(blank=True, help_text="Informações adicionais sobre a aula")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.disciplina} - {self.get_dia_semana_display()} {self.horario}"