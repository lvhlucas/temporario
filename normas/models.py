from django.db import models
from django.contrib.auth.models import User


class CategoriaNorma(models.Model):
    nome_categoria = models.TextField(max_length=50)

    def __str__(self):
        return self.nome_categoria


class Documento(models.Model):
    nome_documento = models.TextField(max_length=50)

    def __str__(self):
        return self.nome_documento


class NormaPDF(models.Model):
    documentoFK = models.ForeignKey(Documento, on_delete=models.CASCADE)
    categoriaFK = models.ForeignKey(CategoriaNorma, on_delete=models.CASCADE)
    norma_paiFK = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    identificador = models.CharField(max_length=10)
    possui_subnorma = models.BooleanField()
    conteudo = models.TextField(max_length=500)

    def __str__(self):
        return str(self.documentoFK) + " - " + str(self.categoriaFK) + " - " + str(self.identificador) + "-"\
               + str(self.norma_paiFK) + "." + str(self.possui_subnorma) + " - " + str(self.conteudo)


class Empresa(models.Model):
    nome = models.CharField(max_length=50)
    codigo = models.IntegerField(default=0, unique=True)
    gerentePK = models.IntegerField(default=0)


class Funcionario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
