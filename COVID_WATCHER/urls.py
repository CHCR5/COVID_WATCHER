"""COVID_WATCHER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from unicodedata import name
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from Aplicaciones.Inicio.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicioMain, name="inicio"),
    path('guiaUsuario/', guiaUsuario, name="guiaUsuario"),
    path('AcercaDe/', inicioAcerca, name="acercaDe"),
    path('registro/', registroMain, name="registro"),
    path('registroEmpleado/', registroEmpleado, name="registroEmpleado"),
    path('registroEmpleado2/', registroEmpleado2, name="registroEmpleado2"),
    path('registroEmpleado3/', registroEmpleado3, name="registroEmpleado3"),
    path('registroEmpleado4/', registroEmpleado4, name="registroEmpleado4"),
    path('inicioSesion/', inicioSesion, name="inicioSesion"),
    path('cierreSesion/', cierreSesion, name="cierreSesion"),
    path('registroEmpleado5/', registroEmpleado5, name="registroEmpleado5"),
    path('registroAdministrador/', registroAdministrador, name="registroAdministrador"),
    path('registroAdministradorDatos/', registroAdministradorDatos, name="registroAdministradorDatos"),
    path('menuEmpleado/', menuEmpleado, name="menuEmpleado"),
    path('formularioDiario/', formularioDiario, name="formularioDiario"),
    path('reporteContagio/', reporteContagio, name="reporteContagio"),
    path('reporteFalta/', reporteFalta, name="reporteFalta"),
    path('cambiarDatos/', cambiarDatos, name="cambiarDatos"),
    path('menuAdmin/', menuAdmin, name="menuAdmin"),
    path('crearArea/', crearArea, name="crearArea"),
    path('altaEmpleados/', altaEmpleados, name="altaEmpleados"),
    path('altaEmpleadosManual/', altaEmpleadosManual, name="altaEmpleadosManual"),
    path('altaEmpleadosCSV/', altaEmpleadosCSV, name="altaEmpleadosCSV"),
    path('alertaFaltasReporte/', alertaFaltasReporte, name="alertaFaltasReporte"),
    path('alertaFaltasReportePDF/', alertaFaltasReportePDF, name="alertaFaltasReportePDF"),
    path('alertaFaltasReporteDia/', alertaFaltasReporteDia, name="alertaFaltasReporteDia"),
    path('alertaFaltasReporteDiaPDF/', alertaFaltasReporteDiaPDF, name="alertaFaltasReporteDiaPDF"),
    path('alertaFaltasReporteMes/', alertaFaltasReporteMes, name="alertaFaltasReporteMes"),
    path('alertaFaltasReporteMesPDF/', alertaFaltasReporteMesPDF, name="alertaFaltasReporteMesPDF"),
    path('alertaFaltasReporteTipo/', alertaFaltasReporteTipo, name="alertaFaltasReporteTipo"),
    path('alertaFaltasReporteTipoPDF/', alertaFaltasReporteTipoPDF, name="alertaFaltasReporteTipoPDF"),
    path('alertaCOVIDReporte/', alertaCOVIDReporte, name="alertaCOVIDReporte"),
    path('alertaCOVIDReportePDF/', alertaCOVIDReportePDF, name="alertaCOVIDReportePDF"),
    path('alertaCOVIDReporteDia/', alertaCOVIDReporteDia, name="alertaCOVIDReporteDia"),
    path('alertaCOVIDReporteDiaPDF/', alertaCOVIDReporteDiaPDF, name="alertaCOVIDReporteDiaPDF"),
    path('alertaCOVIDReporteMes/', alertaCOVIDReporteMes, name="alertaCOVIDReporteMes"),
    path('alertaCOVIDReporteMesPDF/', alertaCOVIDReporteMesPDF, name="alertaCOVIDReporteMesPDF"),
    path('procDatos/', procDatos, name="procDatos"),
    path('historialRes/', historialRes, name="historialRes"),
    path('historialResDia/', historialResDia, name="historialResDia"),
    path('historialResDiaPDF/', historialResDiaPDF, name="historialResDiaPDF"),
    path('historialResMes/', historialResMes, name="historialResMes"),
    path('historialResMesPDF/', historialResMesPDF, name="historialResMesPDF"),
    path('cambiarDatosAdmin/', cambiarDatosAdmin, name="cambiarDatosAdmin"),
    path('modifArea/', modifArea, name="modifArea"),
    path('consEmpleados/', consEmpleados, name="consEmpleados"),
    path('bajaEmpleados/', bajaEmpleados, name="bajaEmpleados"),
    path('elimArea/', elimArea, name="elimArea"),
    path('modifAreaEmp/', modifAreaEmp, name="modifAreaEmp"),
]
