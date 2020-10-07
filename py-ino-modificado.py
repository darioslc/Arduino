# Captura de datos desde puerto serial desde Arduino
# modificado de acuerdo a los datos tomados desde Arduino

import serial, time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## PROGRAMA
print('Para valores grandes/pequeños escribir #eexponente/#e-exponente respectivamente')
C = float(input("Ingresar el valor de C en faradios: "))
Rc = float(input("Ingresar el valor de Rcarga en ohmios: "))
Rd = float(input("Ingresar el valor de Rdescarga en ohmios: "))

tau_c = Rc*C
tau_d = Rd*C

print('RCcarga= '+ str(np.around(Rc*C, 5)) + ' s')
print('RCdescarga= '+ str(np.around(Rd*C, 5)) + ' s')


muestras = 300 # número de mediciones de Arduino

puerto = '/dev/ttyACM0' # puerto de la computadora que conecta a Arduino
baudios = 9600

# Procedimiento

# Inicializa comunicación con arduino
arduino = serial.Serial(puerto, baudios)
arduino.setDTR(False)
time.sleep(0.3)
# limpia buffer de datos anteriores
arduino.flushInput()
arduino.setDTR(True)
time.sleep(0.3)
print('\nEstado del puerto: ',arduino.isOpen())
print('Nombre del dispositivo conectado: ', arduino.name)
print('Dump de la configuración:\n ',arduino)
print('\n###############################################\n')

# Captura datos
datos = [] # lista donde guarda cada dato
i = 0
df_datos = pd.DataFrame() # conjunto de datos para luego graficar lo medido
muestra = [] # almacena el número de muestra
valores = [] # valor crudo en cuentas de Arduino (depués se pasa a voltaje)
tiempos = [] # tiempo de medición para luego graficar en función del tiempo y no de muestra
t0 = time.time() # define el instante en que comienza la medición, para luego calcular tiempos de carga/descarga en segundos

while (i<muestras):
    while (arduino.inWaiting()==0):
        pass #esperar hasta recibir un dato
    linea = arduino.readline() # lee puerto serial
    lectura_ino = linea.decode().strip()# borra rn por el salto de línea desde arduino
    #valor = lectura_ino
    muestra.append(i) # guarda el # de muestra
    tiempos.append(time.time()) # para después ver los tiempos de carga/descarga
    valores.append(lectura_ino) # guarda valor en otra lista que se usa en el df
    print(lectura_ino) # imprime en pantalla cada medición
    i=i+1
arduino.close()

tf = time.time() # tiempo en que finaliza

## prueba guardando en pandas
df_datos_orig = pd.DataFrame(list(zip(muestra, tiempos, valores)), columns = ('muestra', 'tiempo', 'voltaje'), index = muestra)

## pasaje de tiempo a segundos en lugar de condiciones
df_datos = df_datos_orig # para no borrar el original
df_datos.tiempo[0]

acum_t = [] # inicia con este valor inicial

# calcula los tiempos en segundos a partir de que comienza la medición
for i in range(0,len(df_datos)):
    acum_t.append(df_datos.tiempo[i]-tiempos[0]) # guarda el delta t en segundos

df_datos.tiempo = acum_t # cambia por segundos de medición

## pasaje a unidades de voltaje
# convierte a número real la cadena y luego a voltaje
for i in range(0,len(df_datos.voltaje)):
    df_datos.voltaje[i] = int(df_datos.voltaje[i])*5/1023

# guarda datos
df_datos.to_csv('/home/darioslc/Documentos/educación/unlu/Física II 2020/Electrostática - 5 RC/datos_RC_' + str(muestras) + '_' + str(C) + '_F-' + str(Rc) + '_ohmios.csv')

## comparación con lo teórico
tM = df_datos.tiempo.max()

busca_M = df_datos.loc[:, 'voltaje'] == df_datos.voltaje.max()
df_datos.loc[busca_M]
busca_m =  df_datos.loc[:, 'voltaje'] == ((df_datos.voltaje.min())
df_datos.loc[busca_m]
for rel in range(0,len(df_datos)):
    if

## Corriente (en proceso de prueba)
# acum_i = []
# for i in range(0,len(df_datos)-1):
#     acum_i.append(C*(df_datos.voltaje[i+1]-df_datos.voltaje[i])/(df_datos.tiempo[i+1]-df_datos.tiempo[i]))
#     len(acum_i)
# df_datos['corriente'] = acum_i

## Gráficos
# gráfico medido
plt.plot(df_datos.tiempo,df_datos.voltaje)
plt.title('Carga y descarga de capacitor')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.show()

# gráfico teórico
# plt.plot(df_datos.tiempo,df_datos.voltaje)
# plt.title('Carga y descarga de capacitor')
# plt.xlabel('Tiempo [s]')
# plt.ylabel('Voltaje [V]')
# plt.show()


# plt.plot(df_datos.tiempo,df_datos.voltaje*22e-6)
# plt.title('Carga y descarga de capacitor')
# plt.xlabel('Tiempo [s]')
# plt.ylabel('Carga [C]')
# plt.show()

# plt.plot(df_datos.tiempo,C*df_datos.voltaje/df_datos.tiempo)
# plt.title('Carga y descarga de capacitor')
# plt.xlabel('Tiempo [s]')
# plt.ylabel('Corriente [C]')
# plt.show()

plt.savefig('RC_'+str(C)+'_F-'+str(Rc) + '_ohmios.png')