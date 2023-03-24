# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:44:01 2023

@author: Aaron Hernandez
"""
import PySimpleGUI as sg
from datetime import datetime
import time
import os

icon_path = './contabilidad.ico'

sg.theme('DarkTanBlue') #Tema de la interfaz del programa (PySimpleGUI)
sg.set_options(font=('Arial', 15)) # Aumentamos el tamaño de la fuente

# Definir el diseño de la interfaz de usuario

layout = [
    [sg.Column([
        [sg.Text("Ingreso de datos para calcular finiquito", font=("Helvetica", 20), justification="center", expand_x=True)] #En esta columna tenemos el titulo
    ])],
    [sg.Column([
        [sg.Text("Fecha de inicio del contrato (formato: dd/mm/yyyy): ", size=(40, 1)), sg.Input(key="-FECHA_INICIO-", size=(20, 1))], #los campos a validar
        [sg.Text("Fecha final del contrato (formato: dd/mm/yyyy): ", size=(40, 1)), sg.Input(key="-FECHA_FINAL-", size=(20, 1))], #los campos a validar
        [sg.Text("Salario diario: ", size=(40, 1)), sg.Input(key="-SALARIO_DIARIO-", size=(20, 1))], #los campos a validar
        [sg.Text("Días de vacaciones pendientes por tomar: ", size=(40, 1)), sg.Input(key="-DIAS_PEND_VACACIONES-", size=(20, 1))], #los campos a validar
        [sg.Button("Calcular")]  #boton que genera la consulta 
    ], element_justification='right')]

]

# Crear la ventana de la interfaz de usuario
window = sg.Window("Calculadora de liquidación laboral", layout, icon=icon_path)

# Event Loop para procesar eventos y obtener valores de entrada de la interfaz de usuario
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Calcular":
        
        #validamos datos por posibles errores como que ingresen mal un valor o un dato
        try:
            fecha_inicio = datetime.strptime(values["-FECHA_INICIO-"], '%d/%m/%Y')
            fecha_final = datetime.strptime(values["-FECHA_FINAL-"], '%d/%m/%Y')
            salario_diario = float(values["-SALARIO_DIARIO-"])
            dias_pend_vacaciones = float(values["-DIAS_PEND_VACACIONES-"]) if values["-DIAS_PEND_VACACIONES-"] else 0
        except ValueError:
            #En caso de que el usuario escriba mal los valores , vamos a enviar un mensaje indicando que algo esta mal y repita
            sg.popup("Por favor ingrese valores válidos.",icon=icon_path)
            continue
        
        
        # Obtener valores de entrada
        
        
        fecha_inicio = datetime.strptime(values["-FECHA_INICIO-"], '%d/%m/%Y')
        fecha_final = datetime.strptime(values["-FECHA_FINAL-"], '%d/%m/%Y')
        salario_diario = float(values["-SALARIO_DIARIO-"])
        dias_pend_vacaciones = float(values["-DIAS_PEND_VACACIONES-"])
        
        # Calcular liquidación

        ano_inicio = fecha_inicio.year
        ano_fin = fecha_final.year
        # Días trabajados en el último año
        dias_ultimo_ano = (fecha_final - datetime(ano_fin, 1, 1)).days
        # Días trabajados en el año anterior
        dias_ano_anterior = (datetime(ano_fin, 1, 1) - datetime(ano_inicio, 1, 1)).days
        #calcular dias trabajados
        dias_trabajados = (fecha_final - fecha_inicio).days + 1
        # Calcular años trabajados
        anios_trabajados = round((fecha_final - fecha_inicio).days / 365, 2)
        #Calcular salario diario
        Salario = round(salario_diario,2) 
        #Calcular sueldo
        Sueldo = round(Salario * 7,2)
        # Calcular salario integrado
        salario_integrado = round(Salario * 1.0452, 2)
        # Calcular días de vacaciones proporcional
        dias_vacaciones = (dias_pend_vacaciones)
        #Calcular importe de vacaciones
        importe_vacaciones = round(salario_diario * dias_vacaciones / 12 * 12, 2)
        # Calcular prima vacacional
        prima_vacacional = round(Salario * dias_vacaciones * 0.25, 2)
        # Calcular dias de aguinaldo
        aguinaldo_dias = round(dias_ultimo_ano  * 15 / 365, 2)
        # Calcular aguinaldo proporcional
        aguinaldo_proporcional = round(Salario * aguinaldo_dias, 2)
        # Calcular dias de indemnización
        dias_indemnizacion = round(20 * anios_trabajados)
        # Calcular indemnización
        indemnizacion = round(salario_integrado * dias_indemnizacion, 2)
        #calcular separacion unica
        separacion_unica1 = round(90, 0 )
        separacion_unica = round(salario_integrado * separacion_unica1, 0)
        #calcular los dias de prima de antiguedad
        dias_antiguo = round(anios_trabajados * 12)
        #calcular el importe de la antiguedad 
        importe_antiguo = round(dias_antiguo * 160.08,0) 
        #totales a pagar , primera opcion
        Total_primer_opcion = round(Sueldo + importe_vacaciones +  prima_vacacional + aguinaldo_proporcional +  indemnizacion + separacion_unica + importe_antiguo ,2)
        #total a pagar segunda opcion
        Total_segunda_opcion = round(Sueldo + importe_vacaciones +  prima_vacacional + aguinaldo_proporcional + separacion_unica + importe_antiguo ,2)
        
        #total a pagar segunda opcion
        Total_tercera_opcion = round(Sueldo + importe_vacaciones +  prima_vacacional + aguinaldo_proporcional,2)

          #muestra en una ventana emergente los resultados obtenidos por parte del usuario
    sg.popup(f"Dias trabajados: {dias_trabajados}",
             f"Dias ultimo año para Aginaldo:{dias_ultimo_ano}",
             f"Años trabajados: {anios_trabajados}",
             f"Salario diario: ${Salario}",
             f"Sueldo semanal:${Sueldo}",
             f"Salario integrado:${salario_integrado}",
             f"Dias de vacaciones:{dias_vacaciones}",
             f"Importe vacaciones:${importe_vacaciones}",
             f"Prima de vacaciones:${prima_vacacional}",
             f"Dias de aguinaldo:{aguinaldo_dias}",
             f"Proporcional a aginaldo:${aguinaldo_proporcional}",
             f"Dias indemnizacion:{dias_indemnizacion}",            
             f"Indemnizacion:${indemnizacion}",
             f"Separacion unica:{separacion_unica1}",
             f"Separacion unica:${separacion_unica}",
             f"Importe de antiguedad:${importe_antiguo}",
             f"Primer opcion:${Total_primer_opcion}",
             f"Segunda opcion:${Total_segunda_opcion}",
             f"Tercer opcion:${Total_tercera_opcion}",icon=icon_path)
    


               # Genera el archivo txt con los resultados obtenidos una vez cerremos el mensaje emergente
    ruta = os.path.abspath(os.path.join(os.getcwd(), "../../Resultados"))
    filename = "Finiquito_{}.txt".format(int(time.time()))
    archivo = os.path.join(ruta, filename)
                 # Escribir resultad"os en archivo de texto 
    with open(archivo, "w") as f:
                   f.write("Valores para finiquito: \n")
                   f.write("Días trabajados: {}\n".format(dias_trabajados))
                   f.write("Ultimos dias del año para aginaldo: {}\n".format(dias_ultimo_ano))
                   f.write("Años trabajados: {}\n".format(anios_trabajados))
                   f.write("Salario diario: {}\n".format(Salario))
                   f.write("Sueldo semanal: {}\n".format(Sueldo))
                   f.write("Salario Integrado: {}\n".format(salario_integrado))
                   f.write("Dias de vacaciones: {}\n".format(dias_vacaciones))
                   f.write("Importe de vacaciones: {}\n".format(importe_vacaciones))
                   f.write("Prima vacacional: {}\n".format(prima_vacacional))
                   f.write("Dias de aguinaldo: {}\n".format(aguinaldo_dias))
                   f.write("Importe Aginaldo: {}\n".format(aguinaldo_proporcional))
                   f.write("Dias de indemnizacion: {}\n".format(dias_indemnizacion))
                   f.write("Importe de Indemnizacion: {}\n".format(indemnizacion))
                   f.write("Importe de separacion unica: {}\n".format(separacion_unica1))
                   f.write("Importe de separacion unica: {}\n".format(separacion_unica))
                   f.write("Dias de antiguedad: {}\n".format(dias_antiguo))
                   f.write("Importe de antiguedad: {}\n".format(importe_antiguo))
                   f.write("\n")
                   f.write("\n")
                   f.write("Importe a pagar de primera opcion: {}\n".format(Total_primer_opcion))
                   f.write("Importe a pagar de segunda opcion: {}\n".format(Total_segunda_opcion))
                   f.write("Importe a pagar de tercera opcion: {}\n".format(Total_tercera_opcion))    


window.close()#Cierre de las ventanas emergentes



