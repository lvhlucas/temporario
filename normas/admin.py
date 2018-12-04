from django.contrib import admin

from .models import NormaPDF, CategoriaNorma, Documento

admin.site.register(Documento)
admin.site.register(CategoriaNorma)
admin.site.register(NormaPDF)
