from django.db import models


class Pedido(models.Model):
    SENDO_FEITO = "SNF"
    A_CAMINHO = "ACO"
    ENTREGUE = "ETE"
    STATUS_PEDIDO_ESCOLHA = [(SENDO_FEITO, "SENDO FEITO"),
                             (A_CAMINHO, "A CAMINHO"),
                             (ENTREGUE, "ENTREGUE")]
    status_pedido = models.CharField(
        choices=STATUS_PEDIDO_ESCOLHA, max_length=3, default=SENDO_FEITO)
    hora_pedido = models.DateTimeField(null=True, blank=True)
    num_pedido = models.IntegerField(blank=True, null=True)


class Clients(models.Model):
    PIX = "PX"
    DINHEIRO = "DIN"
    CARTAO = "CC"
    FORMA_DE_PAGAMENTO_ESCOLHA = [(PIX, "Pix"),
                                  (DINHEIRO, "Dinheiro"),
                                  (CARTAO, "Credito ou Débito")]
    numero_whatsapp = models.IntegerField(null=True, blank=True)
    nome = models.CharField(null=True, blank=True, max_length=160)
    endereco = models.CharField(null=True, blank=False, max_length=260)
    forma_de_pagamento = models.CharField(
        max_length=3, choices=FORMA_DE_PAGAMENTO_ESCOLHA, default=DINHEIRO)
    pedido = models.CharField(max_length=260, null=True, blank=True)
    num_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
