from django.db import models
from django.contrib.auth.models import User
from accounts.models import Professor

class Aula(models.Model):
    DISCIPLINA_CHOICES = [
        ('matematica', 'Matemática'),
        ('portugues', 'Língua Portuguesa'),
        ('historia', 'História'),
        ('geografia', 'Geografia'),
        ('ciencias', 'Ciências'),
        ('fisica', 'Física'),
        ('quimica', 'Química'),
        ('biologia', 'Biologia'),
        ('ingles', 'Inglês'),
        ('educacao_fisica', 'Educação Física'),
        ('artes', 'Artes'),
        ('filosofia', 'Filosofia'),
        ('sociologia', 'Sociologia'),
    ]
    
    DIA_SEMANA_CHOICES = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
    ]
    
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
        ('integral', 'Integral'),
    ]
    
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
        ('permutada', 'Permutada'),
    ]
    
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    disciplina = models.CharField(max_length=50, choices=DISCIPLINA_CHOICES)
    campus = models.CharField(max_length=100)
    dia_semana = models.CharField(max_length=20, choices=DIA_SEMANA_CHOICES)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)
    carga_horaria = models.IntegerField(help_text="Carga horária semanal em horas")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
    
    def __str__(self):
        return f"{self.disciplina} - {self.campus} - {self.get_dia_semana_display()} - {self.get_turno_display()}"

class PropostaPermuta(models.Model):
    STATUS_CHOICES = [
        ('pendente', '📋 Pendente'),
        ('aceita', '✅ Aceita'),
        ('recusada', '❌ Recusada'),
        ('cancelada', '🚫 Cancelada'),
    ]
    
    aula_origem = models.ForeignKey('Aula', on_delete=models.CASCADE, related_name='propostas_enviadas')
    aula_destino = models.ForeignKey('Aula', on_delete=models.CASCADE, related_name='propostas_recebidas')
    professor_origem = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='propostas_feitas')
    professor_destino = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='propostas_recebidas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_proposta = models.DateTimeField(auto_now_add=True)
    mensagem = models.TextField(blank=True, verbose_name="Mensagem para o professor")
    
    class Meta:
        ordering = ['-data_proposta']
        verbose_name = 'Proposta de Permuta'
        verbose_name_plural = 'Propostas de Permuta'
    
    def __str__(self):
        return f"Permuta: {self.aula_origem} ↔ {self.aula_destino}"

class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('proposta', '📨 Nova Proposta'),
        ('aceita', '✅ Proposta Aceita'),
        ('recusada', '❌ Proposta Recusada'),
        ('cancelada', '🚫 Proposta Cancelada'),
        ('sistema', '🔔 Notificação do Sistema'),
    ]
    
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='sistema')
    link = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
    
    def __str__(self):
        return f"Notificação para {self.professor.user.username}: {self.mensagem[:50]}..."