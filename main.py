import os
from urllib.error import URLError
from flask import Flask, render_template, request, redirect
import requests
import csv

global URL
URL = "https://raw.githubusercontent.com/xavigm/ctveteranos/main/veteranos.csv"
global URLplantilla
URLplantilla = "https://raw.githubusercontent.com/xavigm/ctveteranos/main/veteranos_plantilla.csv"
global URLnoticias
URLnoticias = "https://raw.githubusercontent.com/xavigm/ctveteranos/main/veteranos_noticias.csv"

global footer
footer='<div id="footer-wrapper"><footer id="footer" class="container"><div class="row"><div class="col-9 col-9-medium col-12-small"><section class="widget links"><h3>Patrocinadores</h3><ul class="style2"><li><img src="../images/fs.png" style="width:150px;padding:20px"><img src="../images/zarca.jpeg" style="width:150px;padding:20px"><img src="../images/secreto.jpeg" style="width:150px;padding:20px"><img src="../images/yoki.jpeg" style="width:150px;padding:20px"><img src="../images/sofagrup.jpeg" style="width:150px;padding:20px"><img src="../images/cerro.png" style="width:150px;padding:20px"></li></ul></section></div><section class="widget contact last"><h3>Contacto</h3><ul><li><a href="https://www.instagram.com/udcantrias_veteranos/?hl=es" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li></ul><p>C/ Isaac Albéniz, s/n <br />08232 Viladecavalls<br />Barcelona, España</p></section></div></div><div class="row"><div class="col-12"><div id="copyright"><ul class="menu"><li>&copy; Doki Studio 2022. All rights reserved</li><li>Design: <a href="http://dokistudio.es">Doki Studio</a></li></ul></div></div></div></footer></div></div>'

def siguientePartido():

    global sig_nombre
    global sig_fecha
    global sig_mapa
    global sig_hora
    global sig_escudo

    response = requests.get(URL)
    open("veteranos.csv", "wb").write(response.content)
    
    with open('veteranos.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[7]=="0":
                sig_nombre=row[3]
                sig_fecha=row[1]
                sig_mapa=row[6]
                sig_hora=row[2]
                sig_escudo=row[9]
                break

    os.remove("veteranos.csv")

def setCalendario():

    response = requests.get(URL)
    open("veteranos.csv", "wb").write(response.content)
    
    calendar=""

    with open('veteranos.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            calendar=calendar+'<div class="col-4 col-12-medium"><section class="box feature"><a href="" class="image featured"><img src="../images/'+row[9]+'" width="50%" height="200px" alt="" /></a><div class="inner"><header><h2>'+row[0]+': '+row[3]+'</h2><p>Fecha: <b>'+row[1]+'</b></p><p>Resultado:<b>'+row[8]+'</b></p><p><b>'+row[4]+'</b></p><p>'+row[5]+'</p><p><a href="'+row[6]+'">Como llegar</a></p></header></div></section></div>'      
    
    os.remove("veteranos.csv")
    
    return calendar


def setPlantilla():

    response = requests.get(URLplantilla)
    open("veteranos_plantilla.csv", "wb").write(response.content)
    
    plantilla=""

    with open('veteranos_plantilla.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if int(row[0]) < 10:
                plantilla=plantilla+'<div class="col-4 col-12-medium"><section class="box feature"><a href=""><img class="image featured camiseta" src="shirt.jpg" alt="" /></a><div class="dorsal1">'+row[0]+'</div><div class="inner"><header>Nombre: <h3>'+row[2]+'</h3>Posición: <b>'+row[1]+'</b><br>Goles: <b>'+row[3]+'</b></header></div></section></div>'
            else:
                plantilla=plantilla+'<div class="col-4 col-12-medium"><section class="box feature"><a href=""><img class="image featured camiseta" src="shirt.jpg" alt="" /></a><div class="dorsal">'+row[0]+'</div><div class="inner"><header>Nombre: <h3>'+row[2]+'</h3>Posición: <b>'+row[1]+'</b><br>Goles: <b>'+row[3]+'</b></header></div></section></div>'
            
    os.remove("veteranos_plantilla.csv")
    
    return plantilla

def setNoticias():

    response = requests.get(URLnoticias)
    open("veteranos_noticias.csv", "wb").write(response.content)
    
    noticias=""

    with open('veteranos_noticias.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            noticias=noticias+'<div class="col-4 col-12-medium"><section class="box feature"><a href="" class="noticias image featured"><img src="'+row[3]+'" alt="" /></a><div class="inner"><header><h2>'+row[1]+'</h2><p>Fecha: <b>'+row[0]+'</b></p><p>'+row[2]+'</b></p></header></div></section></div>'      
    
    os.remove("veteranos_noticias.csv")
    
    return noticias    

app = Flask(__name__, static_folder='')
@app.route('/')
def index():

        siguientePartido()

        templateData = {
        'nombre': sig_nombre,
        'fecha' : sig_fecha,
        'mapa' : sig_mapa,
        'hora' : sig_hora,
        'escudo' : sig_escudo,
        'footer' : footer
    }

        return render_template('index.html', **templateData)

@app.route('/calendario')
def calendario():

        calendar=setCalendario()

        templateData = {
        'calendar': calendar,
        'footer' : footer
    }

        return render_template('calendario.html', **templateData)

@app.route('/campo')
def campo():


        templateData = {
        'footer' : footer
    }

        return render_template('campo.html', **templateData)     

@app.route('/plantilla')
def plantilla():

        plantilla=setPlantilla()
        
        templateData = {
        'plantilla' : plantilla
    }

        return render_template('plantilla.html', **templateData)        

@app.route('/noticias')
def noticias():

        noticias=setNoticias()

        templateData = {
        'noticias' : noticias
    }

        return render_template('noticias.html', **templateData)             


app.run() ##Replaced with below code to run it using waitress
#serve(app, host='127.0.0.1', port=80)  
    