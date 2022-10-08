from urllib.error import HTTPError
import wget
import sys
import json

def downloadFile(date):

    # Descargo archivo de reporte
    try:
        site_url = f"""http://file-server:8080/proyect/proyect/{date}_200000/proyect_{date}.json"""
        print(site_url)
        file_name = wget.download(site_url)
        print("\nDescargado: ", file_name)
    except HTTPError as err:
        if err.code == 404:
            print("Error 404, no debes estar conectado a la red")
        else:
            print("Error Code ", err)
        sys.exit(1)
    
    return file_name

def parseoReporte(archivo):
    # Abro el archivo .json y lo cargo
    file = open(archivo, 'rb')

    data = json.load(file)  

    totales = str(data['stats']['tests'])

    pasados = str(data['stats']['passes'])

    fallidos = str(data['stats']['failures'])

    pendientes = str(data['stats']['pending'])

    results = data['results']

    bodyMailF = ""
    #print("########################### FALLIDOS ###########################")
    for r in results:
        for suit in r['suites']:
            if len(suit['failures']) != 0:
                for test in suit['tests']:
                    if test['fail']:
                        bodyMailF = bodyMailF + "<br><strong> - " + test['title'] + "</strong>\n"

    bodyMailP = ""
    #print("########################### PASADOS ###########################")
    for r in results:
        for suit in r['suites']:
            if len(suit['passes']) != 0:
                for test in suit['tests']:
                    if test['pass']:
                        bodyMailP = bodyMailP + "<br> - " + test['title'] + "\n"

    file.close()
    return [totales,pasados, fallidos, pendientes, bodyMailF]