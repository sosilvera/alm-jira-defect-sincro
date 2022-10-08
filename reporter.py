from datetime import date
from datetime import timedelta
import manageFile
import sendMail
import env

# Obtengo la fecha de ayer
ayer = date.today() - timedelta(1)
ayer = ayer.strftime("%d-%m-%Y")

# Descargo archivo de reporte
manageFile.downloadFile(ayer)

# Obtengo el archivo
archivo = f'proyect_{ayer}.json'

# Paseo el archivo y obtengo los resultados
resultParseo = manageFile.parseoReporte(archivo)

totales = resultParseo[0]
pasados = resultParseo[1]
fallidos = resultParseo[2]
bodyMailF = resultParseo[4]

# body
html = sendMail.buildMail(ayer, pasados, fallidos, bodyMailF)

#Envio el mail
sendMail.send(sendMail.buildMsjHeader(env.TITLE_REPORTER_CYPRESS), html, env.MAILSRV, env.USR, env.PASS, env.SRC, env.DST)

# TO DO:
# - Agregar parametro para cambiar titulo
# - Agregar parametro para tomar lista de destino a partir de archivo
# - Agregar parametro para tomar Proyecto para descargar reporte
