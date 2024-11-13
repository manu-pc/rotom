import random
import math
import wikipediaapi
import re
import openai
import os
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup

from translate import  Translator

idiomas = ['it', 'ru', 'nl', 'kg', 'fi', 'ko', 'lv', 'zh', 'gl']

def acerto(letra, str, i,completo):

        if completo:
            print('completo')
            return str[0:4*i+1] + '|'+letra+'|' + str[4*i+4:len(str)]
        else:
            print('parcial')
            return str[0:4*i+1] + '_'+letra+'_' + str[4*i+4:len(str)]

def replace_str(str,letra,i):
    return str[0:i]+letra+str[i+1:len(str)]

wiki = wikipediaapi.Wikipedia('CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0')

wiki.language = 'es'


vocabulario = [
    'traballar', 'demasiado', 'encantame', 'traballo', 'gracioso', 'pregunta', 'entonces', 'cristina', 'porcerto', 'alberto', 'despois', 'chamada', 'siempre', 'facendo', 'gracias', 'deberes', 'coñoque', 'chamada', 'mensaje', 'gustame', 'youtube', 'alberto', 'gracias', 'enserio', 'podedes', 'falando', 'facendo', 'porque', 'hostia', 'mellor', 'despos', 'bensio', 'alguen', 'espera', 'chicos', 'porque', 'hostia', 'bensio', 'parece', 'mellor', 'despos', 'chicos', 'estado', 'pensei', 'camara', 'ingles', 'acabar', 'carmen', 'despos', 'ostias', 'mellor', 'chicos', 'manuel', 'alguen', 'quitar', 'suerte', 'ahora', 'facer', 'cando', 'igual', 'ruben', 'video', 'tamen', 'verda', 'merda', 'decir', 'menos', 'certo', 'todos', 'estou', 'cousa', 'pouco', 'outra', 'mismo', 'podes', 'xente', 'favor', 'https', 'hasta', 'mañan', 'bueno', 'quero', 'muito', 'outro', 'tempo', 'tarde', 'antes', 'final', 'acabo', 'temos', 'tonto', 'grupo', 'clase', 'tiven', 'libro', 'ainda', 'sabes', 'dixen', 'ahora', 'ruben', 'facer', 'podes', 'verda', 'bueno', 'https', 'cando', 'fixen', 'tamen', 'antes', 'muito', 'video', 'tempo', 'pouco', 'certo', 'toume', 'tonto', 'nunca', 'donde', 'regla', 'tamos', 'vamos', 'todos', 'outro', 'estou', 'acabo', 'going', 'mañan', 'tiven', 'seria', 'tarde', 'decir', 'dixen', 'faime', 'joder', 'maria', 'sabes', 'temos', 'verda', 'ahora', 'facer', 'ostia', 'ainda', 'tamen', 'cando', 'todos', 'voume', 'bueno', 'mañan', 'video', 'hasta', 'pouco', 'quero', 'adios', 'fixen', 'joder', 'regla', 'temos', 'desde', 'poder', 'tamos', 'antes', 'dixen', 'final', 'muito', 'habia', 'libro', 'comer', 'cousa', 'menos', 'merda', 'tiven', 'outra', 'pasar', 'teria', 'porfa', 'cenar', 'pero', 'unha', 'como', 'para', 'teño', 'esta', 'podo', 'algo', 'solo', 'creo', 'mais', 'todo', 'dios', 'nada', 'este', 'vale', 'tete', 'cham', 'hoxe', 'esto', 'polo', 'dixo', 'quen', 'miña', 'mira', 'coño', 'cada', 'home', 'inda', 'eres', 'puta', 'casa', 'pola', 'loco', 'fora', 'toda', 'digo', 'pera', 'puto', 'hora', 'está', 'dias', 'jaja', 'xogo', 'tipo', 'aqui', 'pais', 'pasa', 'pode', 'dame', 'pero', 'unha', 'como', 'dios', 'solo', 'creo', 'teño', 'esta', 'algo', 'cham', 'para', 'podo', 'hoxe', 'mira', 'nada', 'manu', 'esto', 'plan', 'osea', 'chao', 'hola', 'dixo', 'quen', 'rafa', 'todo', 'puta', 'vale', 'casa', 'dame', 'digo', 'este', 'bien', 'pode', 'puto', 'hora', 'imos', 'eres', 'tipo', 'peor', 'pera', 'casi', 'dime', 'mais', 'miña', 'seas', 'pero', 'unha', 'como', 'pork', 'vale', 'teño', 'manu', 'solo', 'podo', 'cham', 'creo', 'nada', 'osea', 'algo', 'hoxe', 'miña', 'todo', 'dios', 'jaja', 'esta', 'home', 'esto', 'hola', 'este', 'veña', 'para', 'puta', 'tete', 'taba', 'tiña', 'eres', 'pode', 'polo', 'bros', 'pais', 'casa', 'dame', 'casi', 'hora', 'dime', 'vida', 'foto', 'tipo', 'pasa', 'cada', 'traballar', 'demasiado', 'encantame', 'traballo', 'gracioso', 'pregunta', 'entonces', 'cristina', 'porcerto', 'alberto', 'despois', 'chamada', 'siempre', 'facendo', 'gracias', 'deberes', 'coñoque', 'chamada', 'mensaje', 'gustame', 'youtube', 'alberto', 'gracias', 'enserio', 'podedes', 'falando', 'facendo', 'porque', 'hostia', 'mellor', 'despos', 'bensio', 'alguen', 'espera', 'chicos', 'porque', 'hostia', 'bensio', 'parece', 'mellor', 'despos', 'chicos', 'estado', 'pensei', 'camara', 'ingles', 'acabar', 'carmen', 'despos', 'ostias', 'mellor', 'chicos', 'manuel', 'alguen', 'quitar', 'suerte', 'ahora', 'facer', 'cando', 'igual', 'ruben', 'video', 'tamen', 'verda', 'merda', 'decir', 'menos', 'certo', 'todos', 'estou', 'cousa', 'pouco', 'outra', 'mismo', 'podes', 'xente', 'favor', 'https', 'hasta', 'mañan', 'bueno', 'quero', 'muito', 'outro', 'tempo', 'tarde', 'antes', 'final', 'acabo', 'temos', 'tonto', 'grupo', 'clase', 'tiven', 'libro', 'ainda', 'sabes', 'dixen', 'ahora', 'ruben', 'facer', 'podes', 'verda', 'bueno', 'https', 'cando', 'fixen', 'tamen', 'antes', 'muito', 'video', 'tempo', 'pouco', 'certo', 'toume', 'tonto', 'nunca', 'donde', 'regla', 'tamos', 'vamos', 'todos', 'outro', 'estou', 'acabo', 'going', 'mañan', 'tiven', 'seria', 'tarde', 'decir', 'dixen', 'faime', 'joder', 'maria', 'sabes', 'temos', 'verda', 'ahora', 'facer', 'ostia', 'ainda', 'tamen', 'cando', 'todos', 'voume', 'bueno', 'mañan', 'video', 'hasta', 'pouco', 'quero', 'adios', 'fixen', 'joder', 'regla', 'temos', 'desde', 'poder', 'tamos', 'antes', 'dixen', 'final', 'muito', 'habia', 'libro', 'comer', 'cousa', 'menos', 'merda', 'tiven', 'outra', 'pasar', 'teria', 'porfa', 'cenar', 'pero', 'unha', 'como', 'para', 'teño', 'esta', 'podo', 'algo', 'solo', 'creo', 'mais', 'todo', 'dios', 'nada', 'este', 'vale', 'tete', 'cham', 'hoxe', 'esto', 'polo', 'dixo', 'quen', 'miña', 'mira', 'coño', 'cada', 'home', 'inda', 'eres', 'puta', 'casa', 'pola', 'loco', 'fora', 'toda', 'digo', 'pera', 'puto', 'hora', 'está', 'dias', 'jaja', 'xogo', 'tipo', 'aqui', 'pais', 'pasa', 'pode', 'dame', 'pero', 'unha', 'como', 'dios', 'solo', 'creo', 'teño', 'esta', 'algo', 'cham', 'para', 'podo', 'hoxe', 'mira', 'nada', 'manu', 'esto', 'plan', 'osea', 'chao', 'hola', 'dixo', 'quen', 'rafa', 'todo', 'puta', 'vale', 'casa', 'dame', 'digo', 'este', 'bien', 'pode', 'puto', 'hora', 'imos', 'eres', 'tipo', 'peor', 'pera', 'casi', 'dime', 'mais', 'miña', 'seas', 'pero', 'unha', 'como', 'pork', 'vale', 'teño', 'manu', 'solo', 'podo', 'cham', 'creo', 'nada', 'osea', 'algo', 'hoxe', 'miña', 'todo', 'dios', 'jaja', 'esta', 'home', 'esto', 'hola', 'este', 'veña', 'para', 'puta', 'tete', 'taba', 'tiña', 'eres', 'pode', 'polo', 'bros', 'pais', 'casa', 'dame', 'casi', 'hora', 'dime', 'vida', 'foto', 'tipo', 'pasa', 'cada', 'traballar', 'demasiado', 'encantame', 'traballo', 'gracioso', 'pregunta', 'entonces', 'cristina', 'porcerto', 'alberto', 'despois', 'chamada', 'siempre', 'facendo', 'gracias', 'deberes', 'coñoque', 'chamada', 'mensaje', 'gustame', 'youtube', 'alberto', 'gracias', 'enserio', 'podedes', 'falando', 'facendo', 'porque', 'hostia', 'mellor', 'despos', 'bensio', 'alguen', 'espera', 'chicos', 'porque', 'hostia', 'bensio', 'parece', 'mellor', 'despos', 'chicos', 'estado', 'pensei', 'camara', 'ingles', 'acabar', 'carmen', 'despos', 'ostias', 'mellor', 'chicos', 'manuel', 'alguen', 'quitar', 'suerte', 'ahora', 'facer', 'cando', 'igual', 'ruben', 'video', 'tamen', 'verda', 'merda', 'decir', 'menos', 'certo', 'todos', 'estou', 'cousa', 'pouco', 'outra', 'mismo', 'podes', 'xente', 'favor', 'https', 'hasta', 'mañan', 'bueno', 'quero', 'muito', 'outro', 'tempo', 'tarde', 'antes', 'final', 'acabo', 'temos', 'tonto', 'grupo', 'clase', 'tiven', 'libro', 'ainda', 'sabes', 'dixen', 'ahora', 'ruben', 'facer', 'podes', 'verda', 'bueno', 'https', 'cando', 'fixen', 'tamen', 'antes', 'muito', 'video', 'tempo', 'pouco', 'certo', 'toume', 'tonto', 'nunca', 'donde', 'regla', 'tamos', 'vamos', 'todos', 'outro', 'estou', 'acabo', 'going', 'mañan', 'tiven', 'seria', 'tarde', 'decir', 'dixen', 'faime', 'joder', 'maria', 'sabes', 'temos', 'verda', 'ahora', 'facer', 'ostia', 'ainda', 'tamen', 'cando', 'todos', 'voume', 'bueno', 'mañan', 'video', 'hasta', 'pouco', 'quero', 'adios', 'fixen', 'joder', 'regla', 'temos', 'desde', 'poder', 'tamos', 'antes', 'dixen', 'final', 'muito', 'habia', 'libro', 'comer', 'cousa', 'menos', 'merda', 'tiven', 'outra', 'pasar', 'teria', 'porfa', 'cenar', 'pero', 'unha', 'como', 'para', 'teño', 'esta', 'podo', 'algo', 'solo', 'creo', 'mais', 'todo', 'dios', 'nada', 'este', 'vale', 'tete', 'cham', 'hoxe', 'esto', 'polo', 'dixo', 'quen', 'miña', 'mira', 'coño', 'cada', 'home', 'inda', 'eres', 'puta', 'casa', 'pola', 'loco', 'fora', 'toda', 'digo', 'pera', 'puto', 'hora', 'está', 'dias', 'jaja', 'xogo', 'tipo', 'aqui', 'pais', 'pasa', 'pode', 'dame', 'pero', 'unha', 'como', 'dios', 'solo', 'creo', 'teño', 'esta', 'algo', 'cham', 'para', 'podo', 'hoxe', 'mira', 'nada', 'manu', 'esto', 'plan', 'osea', 'chao', 'hola', 'dixo', 'quen', 'rafa', 'todo', 'puta', 'vale', 'casa', 'dame', 'digo', 'este', 'bien', 'pode', 'puto', 'hora', 'imos', 'eres', 'tipo', 'peor', 'pera', 'casi', 'dime', 'mais', 'miña', 'seas', 'pero', 'unha', 'como', 'pork', 'vale', 'teño', 'manu', 'solo', 'podo', 'cham', 'creo', 'nada', 'osea', 'algo', 'hoxe', 'miña', 'todo', 'dios', 'jaja', 'esta', 'home', 'esto', 'hola', 'este', 'veña', 'para', 'puta', 'tete', 'taba', 'tiña', 'eres', 'pode', 'polo', 'bros', 'pais', 'casa', 'dame', 'casi', 'hora', 'dime', 'vida', 'foto', 'tipo', 'pasa', 'cada']
simbolos_de_puntuacion = ['.', ',', '?']
respuestas_sino = ['si', 'no', 'depende', 'definitivamente', 'pode que si', 'nin de coña', 'como quiras', 'igual si', 'eu diria que non','casi mellor non']
respuestas_mencion = ['dime', 'que pasa', 'hola', 'contame']
respuestas_quetal = ['ben', 'imos indo', 'todo ben', 'ben, e ti?','ben, ti que tal?']



#palabras tomadas do excel do whatsapp


hangman = 0
h_palabra = vocabulario[random.randint(1, 947)]
h_guess = ''
errores = 6
intentos = [ ]
h_long = 0
quetal = False
#variables globales que se usan no ahorcado. igual se podia facer como locales pero nn sei como


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

        model=model,

        messages=messages,

        temperature=0,

    )

    return response.choices[0].message["content"]


def handle_response(username, message) -> str:
    #funcion principal. message é o que lee polo chat, a variable respuesta é o que responde.
    print(message)
    global hangman
    global h_palabra
    global h_guess
    global errores
    global intentos
    global quetal
    global h_long
    #queda feo

    p_message = message.lower()
    #ignora mayúsculas

## CONVERSA
    print(p_message)
    if random.randint(0,100) == 69:
        respuesta = 'minte menos se podes'


    if 'ola' in p_message or 'bos' in p_message or 'buenos' in p_message or 'boas' in p_message or 'buenas' in p_message or 'chao' or 'feliz' in p_message:
        if (len(p_message) < 20 and 'rotom' in p_message):
            p_message = p_message.replace('rotom', username)
            p_message += '!'
            respuesta = p_message

    if 'gracias' in p_message:
        respuesta = 'de nada!'

    if 'cala' in p_message:
        respuesta = 'ok'

    if 'chao' in p_message or 'adios' in p_message:
        respuesta = 'chao'
    if 'rotom' in p_message:
        if 'tal' in p_message or 'estas' in p_message or 'estás' in p_message:
            respuesta = respuestas_quetal[random.randint(0, 4)]
            quetal = True



    if 'rotom fala' in p_message or 'fala rotom' in p_message:

        respuesta = ''
        numerodepalabras = random.randint(2,10)
        print(numerodepalabras)
        for index in range(numerodepalabras):
            if random.randint(0,5) == 5 and index>3:
                    respuesta = respuesta + simbolos_de_puntuacion[random.randint(0,2)]
            else:
                    respuesta = respuesta + ' '+ vocabulario[random.randint(1,94)]

        if 'clyde' in p_message:
                respuesta = '@Clyde ' + respuesta


    if p_message == 'rotom':
            respuesta = respuestas_mencion[random.randint(0, len(respuestas_mencion)-1)]

    if 'debería' in p_message or 'deberia' in p_message or 'crees' in p_message or 'cres' in p_message or 'si ou no' in p_message or 'si ou non' in p_message:
            respuesta = respuestas_sino[random.randint(0, len(respuestas_sino)-1)]


    if quetal == True:
        quetal = False
        if 'tamen' in p_message or 'ben' in p_message or 'estupendo' in p_message or 'genial' in p_message:
            respuesta = 'alegrome!'

        elif 'mal' in p_message:
            respuesta = 'sintoo'


    if 'bomba' in p_message or 'aeropuerto' in p_message:
        respuesta = 'bomba cargada'
        #bomba cargada. non debería sobreescribir comandos como /guess bomba
    if 'non' in p_message and random.randint(1,4) == 2:
        respuesta = 'non pouco'


## AHORCADO
    if p_message == '/ha':
        if hangman != 0:
            return 'Ya hay una partida en curso.'
            #solo pode haber unha partida de cada vez obv

        else:

            hangman = 1
            h_palabra = vocabulario[random.randint(1, 947)]
            h_guess = ''
            intentos = []
            errores = 6
            #resetea as globales

            print(h_palabra)
            #debug. tamén permite facer trampas

            h_long = len(h_palabra)
            for index in range(h_long):
                h_guess = h_guess + ' \_ '
            print(h_guess)
            respuesta = h_guess
            #esto genera a lista de guiones _ _ _ _ que simbolizan os espacios no ahorcado. un por cada letra en h_palabra

    if '/forfeit' in p_message and hangman==1:
            respuesta = 'La partida ha acabado por rendición! La respuesta era: ' + h_palabra
            hangman = 0

    if '/guess' in p_message and hangman == 1:
        #se o mensaje é un comando /guess e hai unha partida de hangman en curso:

        p_message = p_message.replace('/guess ', '')
        #elimina o /guess do mensaje para poder leer o contenido

        print(p_message)
        if p_message == '':
            respuesta = 'Uso del comando: /guess letra'
        else:
            if not p_message in intentos:
                #comproba que a letra ou palabra non fose adivinada antes. adivinar unha palabra que xa fui dita non quita puntos
                intentos += [p_message]

                if p_message in h_palabra:
                    #en caso de acerto:
                    if p_message == h_palabra:
                        #se o guess é a palabra tal cual, ganas a partida
                        respuesta = 'Correcto! La palabra era ' + h_palabra
                        hangman = 0

                    else:
                        #se acertas unha letra.
                        i = 0
                        for letter in h_palabra:
                            i=i+1
                            if letter ==  p_message:
                                h_guess = h_guess[:((i*4)-3)] + ' ' + letter + h_guess[((i*4)-1):]
                                #por cada letra na palabra correcta, colle as que sean a letra adivinada e
                                #toma a súa posición (i). despois, colle o string cos guions baixos e
                                #cortao en dous cachos, para reemplazar un \_ por un espacio e a letra
                                #adivinada na posición correcta.
                                print(h_guess)

                        respuesta = p_message + ' es correcto! ' + h_guess



                else:
                    #en caso de error, resta 1 error e se chega a 0 perdes. ez
                    errores = errores - 1
                    respuesta = 'No, "' + p_message + '" no es correcto. Intentos restantes: ' + str(errores) + '.     ' + h_guess
                    if errores == 0:
                        respuesta = 'La partida ha acabado! La respuesta era: ' +  h_palabra
                        hangman = 0

            else:
                respuesta = p_message + ' ya ha sido intentado.'

## WORDLE

    if p_message == '/wo':
        if hangman != 0:
            return 'Ya hay una partida en curso.'

        else:

            hangman = 2
            h_palabra = vocabulario[random.randint(1, 947)]
            h_guess = ''
            intentos = []
            errores = 6
            #resetea as globales

            print(h_palabra)
            #debug. tamén permite facer trampas

            h_long = len(h_palabra)
            for index in range(h_long):
                h_guess = h_guess + ' *█*'
            print(h_guess)
            respuesta = h_guess
            # en wordle uso cuadrados en vez de os guions porque queda mas bonito e tocame menos os collons co formato

    if '/forfeit' in p_message and hangman==2:
            respuesta = 'La partida ha acabado por rendición! La respuesta era: ' + h_palabra
            hangman = 0

    if '/guess' in p_message and hangman == 2:
        #se o mensaje é un comando /guess e hai unha partida de wordle en curso:

        p_message = p_message.replace('/guess ', '')
        #elimina o /guess do mensaje para poder leer o contenido



        print(p_message)
        if len(p_message)!=h_long:
            respuesta = 'Utiliza /guess palabra, con una palabra de ' + str(h_long) + ' letras.'
        elif p_message == h_palabra:
            respuesta = 'Correcto! La palabra era ' + h_palabra
            hangman = 0
        else:
            #basicamente aqui solo hai unha cousa complicada. se por ejemplo a palabra é 'pota' e ti dis
            #'lata', se o fas directamente o programa poria a primeira 'a' en amarillo, o cal e incorrecto
            #porque leva a pensar que pota ten duas 'a's. asi que ten que iterar duas veces pola palabra,
            #primeiro marcando as de verde e sustituindoas para que non se marquen duas veces.

            #creo a h_palabra_copia para ter unha version modificable de h palabra na que podo facer
            #perversiones sin alterar a solucion do problema

            h_palabra_copia = h_palabra
            intentos += [p_message]

            for i in range(h_long):#verdes
                if p_message[i] == h_palabra_copia[i]:
                    print("acierto completo coa letra " + p_message[i])
                    h_guess = acerto(p_message[i], h_guess, i, True)
                    print(h_palabra_copia)
                    p_message = p_message.replace(p_message[i], '€', 1)
                    h_palabra_copia = h_palabra_copia.replace(p_message[i], '#', 1)

                    print(h_palabra_copia)


            for i in range(h_long):#amarelos
                if p_message[i] in h_palabra_copia:
                    print("acierto parcial coa letra " + p_message[i])
                    h_guess = acerto(p_message[i], h_guess, i, False)
                    h_palabra_copia = h_palabra_copia.replace(p_message[i], '#', 1)

            if len(intentos)==errores:
                respuesta = 'La partida ha acabado! La palabra era ' + h_palabra
                hangman = 0

            else: #fin de ronda e xa
                respuesta = h_guess.upper()
                h_guess = ''
                for index in range(h_long):
                    h_guess = h_guess + ' *█*'  # olvidase de os acertos en cada ronda





## WIKI
    if '/wiki' in p_message:
        message = message.replace('/wiki ', '')
        if not ', ' in message:
            if message == 'random':
                url = requests.get('https://es.wikipedia.org/wiki/Especial:Aleatoria')
                soup = BeautifulSoup(url.content, "html.parser")
                title = soup.find(class_="firstHeading").text
                page = wiki.page(title)
                print(page.text)
                print(page.title)
            else:
                page = wiki.page(message)
            if page.text == '':
                return 'No se ha encontrado la página. Por favor, comprueba el uso de mayúsculas.'
            if len(page.text) > 1950:
                print(f"{len(page.text)} error 1")
                if len(page.summary) > 1950:
                    print(f"{len(page.summary)} error 2")
                    respuesta = page.summary.split('\n')
                    print(page.summary)
                    return re.sub("[\(\[].*?[\)\]]", "", respuesta[0])
                else:
                    respuesta = page.summary
                    return re.sub("[\(\[].*?[\)\]]", "", respuesta)

            else:
                respuesta = page.text
                return re.sub("[\(\[].*?[\)\]]", "", respuesta)

        elif 'categorías' in p_message:
            message = message.split(', ')
            page = wiki.page(message[0])
            if page.text == '':
                return 'No se ha encontrado la página. Por favor, comprueba el uso de mayúsculas.'
            categorias = []
            j = 0
            for index in range(len(page.sections)):
                terraria = page.sections[index].title
                print(terraria)
                print(categorias)
                categorias = categorias + [terraria]

            categorias_str = 'Categorías: '
            for index in categorias:
                categorias_str += categorias[j]
                if j != len(categorias) - 1:
                    categorias_str += ', '
                else:
                    categorias_str += '.'

                j+=1

            return categorias_str


        else:
            message = message.split(', ')
            message[0] = message[0].title()
            page = wiki.page(message[0])
            if page.text == '':
                return 'No se ha encontrado la página. Por favor, comprueba el uso de mayúsculas.'
            message[1] = message[1].capitalize()
            respuesta = page.sections_by_title(message[1])
            respuesta_str = respuesta[0].text
            return re.sub("[\(\[].*?[\)\]]", "", respuesta_str)


## COMANDOS RANDOM
    inputs = []
    if '/pick' in p_message:
        p_message = p_message.replace('/pick ', '')
        if p_message == '':
            respuesta = 'Uso del comando: /pick opcion1, opcion2, opcion3...'
        else:
            inputs = p_message.split(',')
            respuesta = inputs[random.randint(0, len(inputs) -1)]
    if '/random' in p_message:
        p_message = p_message.replace('/random ', '')
        print(p_message)
        if p_message == '':
            respuesta = 'Uso del comando: /random numero1, numero2. Elige un número entero aleatorio entre ambos.'
        else:
            inputs = p_message.split(', ')
            print(inputs)
            try:
                respuesta = random.randint(int(inputs[0]), int(inputs[1]))
            except Exception as e:
                respuesta = 'Uso del comando: /random numero1, numero2. Elige un número entero aleatorio entre ambos.'
                print(e)






## AXUDA
    if p_message == '/rotom' or p_message == '/help':
        respuesta = '/ha: crea unha partida de ahorcado, /guess para participar \n' \
                    '/pick: permite escoller entre varias opcions ao azar \n' \
                    '/random: permite escoller un numero aleatorio entre dous numeros \n' \
                    '/wiki: busca un término en wikipedia' \




    return respuesta


