from django.db import models


class TitulosNorma(models.Model):
    nome_titulo = models.TextField(max_length=50)

    def __str__(self):
        return self.nome_titulo


class NormaPdf(models.Model):
    tituloFK = models.ForeignKey(TitulosNorma, on_delete=models.CASCADE)
    documento = models.IntegerField(default=0)
    norma1 = models.CharField(max_length=5)
    norma2 = models.CharField(max_length=5)
    norma3 = models.CharField(max_length=5)
    conteudo = models.TextField(max_length=500)

    def __str__(self):
        return str(self.documento)+" - "+str(self.tituloFK)+" - "+self.norma1+"."+self.norma2+"."+self.norma3+" - "+\
               str(self.conteudo)


class empresa(models.Model):
    nome = models.CharField(max_length=50)
    codigo = models.IntegerField(default=0)


