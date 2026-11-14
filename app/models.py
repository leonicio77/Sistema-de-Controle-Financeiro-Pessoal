
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    limite_mensal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )

    def __str__(self):
        return self.nome


class Lancamento(models.Model):
    TIPOS = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    FORMAS_PAGAMENTO = [
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
        ('credito', 'Cartão de Crédito'),
        ('debito', 'Cartão de Débito'),
        ('transferencia', 'Transferência Bancária'),
        ('outro', 'Outro'),
    ]

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMAS_PAGAMENTO,
        default='pix'
    )

    descricao = models.CharField(max_length=200)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'))
        ]
    )

    data = models.DateField()

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.descricao

    
class Conta(models.Model):
    TIPOS = [
        ('pagar', 'A pagar'),
        ('receber', 'A receber'),
    ]

    STATUS = [
        ('pendente', 'Pendente'),
        ('concluida', 'Concluída'),
    ]

    descricao = models.CharField(max_length=200)

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'))
        ]
    )

    vencimento = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pendente'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.descricao

