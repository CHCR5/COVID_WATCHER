from django.contrib import admin
from .models import Administrador, DatosAlgoritmo, Empleado, Empresa, Area, DiaLaboral, FormularioDiario, ReporteDeContagio, ReporteDeFalta
# Register your models here.
admin.site.register(Administrador)
admin.site.register(Empleado)
admin.site.register(Empresa)
admin.site.register(Area)
admin.site.register(DiaLaboral)
admin.site.register(FormularioDiario)
admin.site.register(ReporteDeContagio)
admin.site.register(ReporteDeFalta)
admin.site.register(DatosAlgoritmo)