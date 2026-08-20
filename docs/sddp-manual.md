SDDP
Manual de Archivos
VERSIÓN 17.2

Tabla de Contenido
1 Archivos de Entrada ............................................................................................................... 1
2 Datos del Sistema .................................................................................................................. 3
2.1 Nombre de los directorios .............................................................................................. 3
2.2 Identificador de los sistemas .......................................................................................... 3
2.3 Datos generales y opciones de ejecución ....................................................................... 3
2.4 Unidad monetaria ......................................................................................................... 21
2.5 Duración de los bloques ................................................................................................ 22
3 Centrales Hidroeléctricas .................................................................................................... 24
3.1 Configuración hidroeléctrica ......................................................................................... 24
3.2 Modificación de la configuración hidroeléctrica .......................................................... 30
3.3 Factor de pérdidas de hidroeléctricas .......................................................................... 32
3.4 Mantenimiento de las hidroeléctricas .......................................................................... 33
3.5 Datos de riego ............................................................................................................... 34
3.6 Defluencia total máxima ............................................................................................... 35
3.7 Defluencia total mínima ................................................................................................ 36
3.8 Vertimiento máximo ..................................................................................................... 37
3.9 Vertimiento mínimo ...................................................................................................... 38
3.10 Volúmenes de alerta .............................................................................................. 40
3.11 Volúmenes máximos operativos ............................................................................ 41
3.12 Volúmenes de seguridad ........................................................................................ 42
3.13 Volúmenes de espera ............................................................................................. 43
3.14 Datos adicionales ................................................................................................... 44
3.15 Volumen muerto .................................................................................................... 44
3.16 Curva de aversión al riesgo .................................................................................... 45
3.17 Cálculo energía almacenada .................................................................................. 46
3.18 Configuración de conjuntos de embalses .............................................................. 48
3.19 Energía de alerta .................................................................................................... 49
3.20 Energía de seguridad .............................................................................................. 50
3.21 Energía de espera ................................................................................................... 51
3.22 Tabla caudal turbinable x rendimiento del grupo turbina/generador .................. 52

3.23 Restricciones operativas ........................................................................................ 53
4 Centrales Termoeléctricas ................................................................................................... 54
4.1 Configuración termoeléctrica ....................................................................................... 54
4.2 Modificación de la configuración térmica .................................................................... 57
4.3 Consumo específico por bloco ...................................................................................... 58
4.4 Mantenimiento de las termoeléctricas ......................................................................... 59
4.5 Configuración de combustible ...................................................................................... 59
4.6 Precios de combustible ................................................................................................. 60
4.7 Tasa de consumo de combustible ................................................................................. 61
4.8 Disponibilidad de combustible ...................................................................................... 61
4.9 Generación mínima operativa ...................................................................................... 62
4.10 Costo de arranque variables para centrales commitment ..................................... 63
4.11 Estado operativo de térmicas ciclo combinado ..................................................... 64
4.12 Costos de adquisición de créditos de emisión ....................................................... 65
4.13 Datos de configuración de contrato de combustible ............................................. 66
4.14 Datos de configuración de reservorio de combustible .......................................... 67
4.15 Dados de modificación de reservorio de combustible .......................................... 68
4.16 Relación contrato de combustible x térmica ......................................................... 69
4.17 Relación contrato x reservorio de combustible ..................................................... 69
4.18 Relación reservorio de combustible x térmica ...................................................... 70
4.19 Costos de contrato de combustible ....................................................................... 70
4.20 Disponibilidad de contrato de combustible ........................................................... 71
4.21 Límites de inyección de reservorio de combustible .............................................. 72
4.22 Límites de retirada de reservorio de combustible ................................................. 73
4.23 Restricciones operativas ........................................................................................ 74
4.24 Datos de emisión.................................................................................................... 74
4.25 Coeficientes de emisión térmica ............................................................................ 75
4.26 Costos cronológicos de emisión ............................................................................. 75
4.27 Restricción de presupuesto de emisión ................................................................. 76
5 Restricciones Mixtas ............................................................................................................ 77
5.1 Restricciones de generación ......................................................................................... 77

5.2 Reserva primaria ........................................................................................................... 78
5.3 Configuración restricciones de reserva secundaria ...................................................... 80
5.4 Modificación restricciones de reserva secundaria........................................................ 81
6 Datos de Transmisión – Modelo de Intercambios ............................................................... 84
6.1 Configuración de intercambios ..................................................................................... 84
6.2 Modificación de los intercambios ................................................................................. 84
6.3 Configuración de suma de intercambios ...................................................................... 85
6.4 Modificación de restricciones de suma de intercambios ............................................. 86
6.5 Costos de intercambio .................................................................................................. 86
7 Datos de Transmisión – Modelo de Flujo de Potencia ........................................................ 88
7.1 Configuración de barras ................................................................................................ 88
7.2 Modificación de los datos de barra............................................................................... 89
7.3 Demanda por barra ....................................................................................................... 90
7.4 Configuración de circuitos ............................................................................................ 91
7.5 Modificación de los datos de circuitos .......................................................................... 92
7.6 Datos de enlace CC........................................................................................................ 93
7.7 Modificación de los enlaces CC ..................................................................................... 94
7.8 Dados de áreas eléctricas ............................................................................................. 95
7.9 Modificación de los límites de exportación e importación por área ............................ 95
7.10 Configuración de suma de flujo en circuitos .......................................................... 96
7.11 Modificación de restricciones de suma de flujo en circuitos ................................. 97
7.12 Costos en circuitos internacionales ....................................................................... 97
8 Demanda ............................................................................................................................. 99
8.1 Configuración de demanda ........................................................................................... 99
8.2 Demanda de energía ..................................................................................................... 99
8.3 Precios de energía ....................................................................................................... 100
9 Déficit ................................................................................................................................ 102
9.1 Modificación curva costo de déficit ............................................................................ 102
10Disponibilidad y Transporte de Gas Natural
104
10.1 Nodos de la red de gas ......................................................................................... 104

10.2 Costos cronológicos de producción de gas .......................................................... 105
10.3 Demanda no-termoeléctrica de gas ..................................................................... 106
10.4 Gasoductos ........................................................................................................... 107
11 ................................................................................................................................. Hidrología
110
11.1 Configuración de las estaciones hidrológicas ...................................................... 110
11.2 Histórico de caudales ........................................................................................... 110
11.3 Archivos de parámetros ....................................................................................... 111
11.4 Archivo externo de secuencias de caudales (FORW.DAT) ................................... 111
11.5 Archivo externo de caudales condicionados (BACK.DAT) .................................... 112
11.6 Incertidumbre reducida ....................................................................................... 112
11.7 Histórico de variable climática ............................................................................. 113
11.8 Escenario de previsión de la variable climática ................................................... 114
11.9 Parámetros de uso de la variable climática ......................................................... 114
12Fuentes Renovables
116
12.1 Configuración fuentes renovables ....................................................................... 116
12.2 Escenarios de generación de fuentes renovables ................................................ 117
13 ...................................................................................................................................... batería
119
13.1 Configuración de batería ...................................................................................... 119
13.2 Modificación de batería ....................................................................................... 120
13.3 Tablas de carga y descarga de la batería ............................................................. 121
14Análisis de Sensibilidad
122
14.1 Registro tipo 1 ...................................................................................................... 122
14.2 Registro tipo 2 ...................................................................................................... 122
14.3 Registro tipo 3 ...................................................................................................... 123
14.4 Registro tipo 4 ...................................................................................................... 123
15Función de Costo Futuro
125
15.1 Registro 1 ............................................................................................................. 125
15.2 Registro 2 ............................................................................................................. 126

15.3 Registro 3 en adelante... ...................................................................................... 126
16Volumen Inicial
128
16.1 Registro 1 ............................................................................................................. 128
16.2 Registro 2 ............................................................................................................. 128
16.3 Registro 3 ............................................................................................................. 128
16.4 Registro 4 ............................................................................................................. 129
16.5 Registro 5 ............................................................................................................. 129

SDDP MANUAL DE ARCHIVOS
1 ARCHIVOS DE ENTRADA
El SDDP utiliza los siguientes archivos de entrada:
1. datos del sistema
• nombre de los directorios
• identificador de los sistemas
• datos generales y opciones de ejecución
2. centrales hidroeléctricas
• configuración hidroeléctrica
• modificación
• mantenimiento
• riego
• volúmenes de seguridad
• volúmenes de alerta
• defluencia máxima
• volumen de espera
3. centrales térmicas
• configuración termoeléctrica
• modificación
• mantenimiento
• costos de combustible
• tasa de consumo del combustible
• disponibilidad del combustible
• generación mínima para soporte reactivo
4. restricciones mixtas
• restricciones de generación
• reserva primaria
• reserva secundaria
5. transmisión - modelo de interconexiones
• datos de interconexión
• modificación
6. transmisión - modelo de flujo de potencia
• configuración de barras
• modificación datos de barras
• configuración de circuitos y enlaces CC
• modificación datos circuitos y enlaces CC
• límite de exportación e importación por área eléctrica
• modificación límite de exportación e importación por área eléctrica
1

SDDP MANUAL DE ARCHIVOS
7. demanda de mediano y largo plazo
8. hidrología
• configuración hidrológica
• histórico de caudales
• parámetros del modelo estocástico
• secuencia de caudales
• caudales condicionados
• incertidumbre reducida
9. contratos
10. corto plazo
• demanda
• pronóstico de caudales
• reserva primaria
• AGC
11. análisis de sensibilidad
12. salidas seleccionadas
2

SDDP MANUAL DE ARCHIVOS
2  DATOS DEL SISTEMA
Los datos del sistema incluyen:
•  nombre de los directorios
•  identificador de los sistemas
•  datos generales y opciones de ejecución
2.1  Nombre de los directorios
Archivo ASCII llamado PATH.DAT, con el siguiente formato.

| Registro  | Columna  | Tipo  Descripción                       |
| --------- | -------- | --------------------------------------- |
| 1         |          |   Comentario                            |
| 2         | 27-66    | A40  Directorio de datos del estudio    |
| 3         | 27-66    | A40  Directorio de datos de hidrología  |
Este archivo está en el mismo directorio del módulo ejecutable del SDDP.
2.2  Identificador de los sistemas
Archivo ASCII llamado SISTEM.DAT, ubicado en el mismo directorio del módulo ejecutable del
SDDP.
El primer registro es comentario. Los demás tienen el siguiente formato:

| Campo  | Columna  | Tipo  Descripción                    |
| ------ | -------- | ------------------------------------ |
| 1      | 1-4      | I4  Número del sistema               |
| 2      | 6-17     | A12  Nombre del sistema              |
| 3      | 27-28    | A2  Identificador del sistema        |
| 4      | 30-32    | A3  Identificador de la unidad mone- |
taria asociada al sistema
2.3  Datos generales y opciones de ejecución
Archivo ASCII llamado SDDP.DAT, ubicado en el directorio de datos del estudio (registro 2 del
archivo PATH.DAT). Los datos se dividen en cinco grupos:
1.  opciones de ejecución y datos generales;
2.  datos de los sistemas en estudio;
3.  datos de las series a simular;
4.  datos de las funciones de costo de déficit;
3

SDDP MANUAL DE ARCHIVOS
5.  opciones para escribir y leer funciones de costo futuro.
2.3.1  Opciones de ejecución y datos generales

| Registro  | Columna  | Tipo  Descripción     |     |     |     |
| --------- | -------- | --------------------- | --- | --- | --- |
| 1         |          |   Título del estudio  |     |     |     |
| 2         | 27-30    | I4  Idioma:           |     |     |     |
0 = Inglés;
1 = Español;
2 = Portugués.
| 3   | 27-30  | I4  Objetivo:  |     |     |     |
| --- | ------ | -------------- | --- | --- | --- |
1 = Política Operativa;
2 = Simulación;
7 = Corto Plazo;
13 = SDDP Escenarios.
| 4   | 27-30  | I4  Opción:  |     |     |     |
| --- | ------ | ------------ | --- | --- | --- |
1 = Aislado;
2 = Coordinado
3 = Integrado.
| 5   | 27-30  | I4  Etapa:  |     |     |     |
| --- | ------ | ----------- | --- | --- | --- |
1 = Semanal;
2 = Mensual.
| 6   | 27-30  | I4  Caudales:  |     |     |     |
| --- | ------ | -------------- | --- | --- | --- |
1 = Series sintéticas internas.
2 = Series históricas para la simulación for-
|     |     | ward,  series  | sintéticas  | en  la  recursión  | ba- |
| --- | --- | -------------- | ----------- | ------------------ | --- |
ckward.
3 = Caudales externos para la simulación for-
ward (archivos FORW.DAT) y para la recursión
backward (archivo BACK.DAT)
4 = Caudales externos para la simulación for-
ward (archivo FORW.DAT) y series sintéticas
internas para la recursión backward
| 7   | 27-30  | I4  Usa cronograma de mantenimiento:  |     |     |     |
| --- | ------ | ------------------------------------- | --- | --- | --- |
0 = Usa Factor de Indisponibilidad Progra-
mada;
1 = Usa Programa de Mantenimiento.
| 8   | 27-30  | I4  Tipo de configuración:  |     |     |     |
| --- | ------ | --------------------------- | --- | --- | --- |
0 = Estática (no hay expansión)
1 = Dinámica (hay expansión)
4

SDDP MANUAL DE ARCHIVOS
| Registro  | Columna  | Tipo  Descripción                |
| --------- | -------- | -------------------------------- |
| 9         | 27-30    | I4  Tipo de red de transmisión:  |
0 = Solo hay interconexiones;
1 = Flujo de potencia DC (estrategia de relaja-
ción)
| 10  | 27-30  | I4  Pérdidas en la transmisión  |
| --- | ------ | ------------------------------- |
0 = No representa pérdidas
1 = Representa pérdidas
| 11  | 27-30  | I4  Horizonte:  |
| --- | ------ | --------------- |
0 = Transforma los costos de operación de los
años adicionales en una serie infinita;
1 = No transforma
| 12  | 27-30  | I4  Series a simular:  |
| --- | ------ | ---------------------- |
0 = Todas;
1 = Seleccionadas por el usuario.
| 13  | 27-30  | I4  Mes o semana de inicio del estudio.           |
| --- | ------ | ------------------------------------------------- |
| 14  | 27-30  | I4  Año de inicio del estudio.                    |
| 15  | 27-30  | I4  Número de etapas del estudio.                 |
| 16  | 27-30  | I4  Mes o semana de la condición inicial para la  |
hidrología.
17  27-30  I4  Año de la condición inicial para la hidrología.
| 18  | 27-30  | I4  Número de sistemas.                       |
| --- | ------ | --------------------------------------------- |
| 19  | 27-30  | I4  Número de series para la simulación "for- |
ward"
| 20  | 27-30  | I4  Número de aperturas para la recursión "ba- |
| --- | ------ | ---------------------------------------------- |
ckward"
| 21  | 27-30  | I4  Número de bloques.                 |
| --- | ------ | -------------------------------------- |
| 21  | 32-32  | I1  Bloques en la política operativa:  |
0: no considera (default)
1: considera
| 22  | 27-30  | I4  Número de años adicionales.  |
| --- | ------ | -------------------------------- |
| 22  | 32-32  | I1  Simulación final:            |
0: no se extiende por los años adicionales (de-
fault)
1: se extiende por los años adicionales (sólo
válido para política operativa)
| 22  | 34-34  | I1  Datos cronológicos:  |
| --- | ------ | ------------------------ |
0: años adicionales repiten datos cronológicos
del último año del estudio (default)
1: el usuario debe especificar los datos crono-
lógicos para los años adicionales
| 23  | 27-30  | I4  Número máximo de iteraciones.  |
| --- | ------ | ---------------------------------- |
5

SDDP MANUAL DE ARCHIVOS
Registro Columna Tipo Descripción
24 27-30 F4.0 Tolerancia de convergencia para estudios de-
terminísticos (%)
En estudios estocásticos este campo es igno-
rado.
25 27-30 I4 Impresión de informes:
0 = Normal; 1 = Detallado.
26 27-30 F8.0 Tasa de descuento.
27 23-30 F8.0 Penalidad por violación de las restricciones de
caudal mínimo ($/hm3)
53-60 F8.0 Penalidad por vertimiento (k$/hm3)
Obs.: Hay tres campos de datos en el registro 27.
2.3.2 Datos de los sistemas en estudio
El registro 28 es comentario. El registro 29 contiene:
Campo Columna Tipo Descripción
1 1-4 I4 Código del primer sistema
2 6-9 I4 Código del segundo sistema
3-5 etc. etc. etc.
6 26-29 I4 Código del sexto sistema
2.3.3 Datos de las series a simular
Los registros 30 y 31 son comentarios. El registro 32 contiene:
Campo Columna Tipo Descripción
1 1-4 I4 Número de series a simular.
2 6-9 I4 Número de la primera serie a simular.
3 11-14 I4. Número de la segunda serie a simular.
4 etc. etc. etc.
2.3.4 Costo de la energía no suministrada
Los registros 33 y 34 son comentarios. El registro 35 contiene:
Campo Columna Tipo Descripción
1 1-6 F6.0 Primer segmento de la energía no suministrada (%).
2 8-15 F8.0 Primer segmento del costo de la ENS ($/MWh).
3 17-22 F6.0 Segundo segmento de la ENS (%).
6

SDDP MANUAL DE ARCHIVOS
4 24-31 F8.0 Segundo segmento del costo de la ENS ($/MWh).
5 33-38 F6.0 Tercer segmento de la ENS (%).
6 40-47 F8.0 Tercer segmento del costo de la ENS ($/MWh).
7 49-54 F6.0 Cuarto segmento de la ENS (%).
8 56-63 F8.0 Cuarto segmento del costo de la ENS ($/MWh).
Observación:
La suma de los valores en los campos 1, 3 y 5 debe ser igual a 100.
2.3.5 Creación y lectura de la función de costo futuro terminal
Registro Columna Tipo Descripción
36 Comentario.
37 27-30 I4 Opción de crear un archivo de costo futuro terminal:
=0, no crea;
=1, crea proyectando en los caudales promedio del
histórico;
=2, crea proyectando en los caudales anteriores del
histórico.
38 27-30 I4 número de la etapa de la función de costo futuro que
se va crear
39 27-30 I4 año de la función de costo futuro.
40 26-30 A5 El nombre del archivo es aaaaaxx.fcf, donde aaaaa es
el contenido del campo y xx es el identificador del
sistema.
El nombre "default" es teeaaxx.fcf donde:
t=S o M (semana o mes);
ee=número de la etapa informado en el registro 37;
aa=año informado en el registro 38.
41 27-30 I4 Opción de leer un archivo de costo futuro terminal
para la última etapa:
= 0, no lee;
= 1, lee;
42 26-30 A5 El nombre del archivo es bbbbbxx.fcf, donde bbbbb
es el contenido del campo y xx es el identificador del
sistema.
El nombre "default" es tffgg.fcf donde:
t=S o M (semana o mes);
ff=número de la última etapa del estudio;
gg=año de la última etapa del estudio.
7

SDDP MANUAL DE ARCHIVOS
2.3.6 Partidas en caliente
Registro Columna Tipo Descripción
43 Comentario.
44 27-30 I4 Opción de leer un archivo de costos futuros obtenido
en ejecución anterior
=0, no lee;
=1, lee;
45 27-30 I4 Opción para usar los volúmenes iníciales de una eje-
cución anterior desactivada.
Toda partida en caliente pasó a leer el archivo de vo-
lúmenes.
2.3.7 Etapas inicial y final para refinamiento de la FCF en la partida en caliente
Registro Columna Tipo Descripción
49 Comentario.
50 27-30 I4 Etapa inicial para refinamiento de la FCF en el hot
start
51 27-30 I4 Etapa final para refinamiento de la FCF en el hot start
Observación:
Para mantener la compatibilidad con datos antiguos que no disponen de esta información, si
estos registros no existen el programa asume que las etapas inicial y final para refinamiento
de la FCF corresponden a las etapas inicial y final del estudio.
2.3.8 Parámetros de ejecución
El modelo permite seleccionar un conjunto de parámetros de ejecución, con los cuales es po-
sible definir parámetros adicionales de ejecución, así como desactivar datos existentes sin la
necesidad de remover los conjuntos de datos del directorio de estudio. Entre ellos podemos
mencionar:
• opción para selección de la unidad monetaria;
• opción para modificación de las tolerancias de convergencia primal y dual;
• opción para desactivar datos de mantenimiento;
• opción de cálculo de las energías almacenada, almacenable máxima y afluente por sis-
tema;
• opción para desactivar datos cronológicos: reserva primaria, volumen de alerta, volumen
de espera, entre otros;
• selección de subconjunto de barras para corte de carga;
• selección de subconjunto de circuitos para monitorear sus límites operativos.
8

SDDP MANUAL DE ARCHIVOS
Los registros son consecutivos e independientes de su orden de aparición. Cada registro es
representado por una palabra clave y un escalar o palabra clave, como indicado a seguir.

| Registro  | Columna  | Tipo  Descripción  |     |
| --------- | -------- | ------------------ | --- |
| 52        |          |   Comentario.      |     |
2.3.8.1  Unidad monetaria

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
UMON
2  7-9  A3  Unidad monetaria en la cual son especificados los
datos de penalidad por vertimiento, penalidad de
defluencia mínima y costo de energía no suminis-
trada.
2.3.8.2  Selección de barras para corte de carga

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
CCAR
| 2   | 6-9  | I4  Opción que permite seleccionar un subconjunto  |     |
| --- | ---- | -------------------------------------------------- | --- |
de barras de carga para corte de carga.
= 0: opción default del SDDP, todas las barras de
carga del sistema son candidatas a corte de carga;
= 1: solamente un subconjunto de barras seleccio-
nada en los datos de configuración de barras se-
rán candidatas a corte de carga.
2.3.8.3  Selección de circuitos monitoreados

| Campo  | Columna  | Tipo  Descripción                                  |        |
| ------ | -------- | -------------------------------------------------- | ------ |
| 1      | 1-4      | A4  Palabra clave:                                 | CMON   |
| 2      | 6-9      | I4  Opción que permite seleccionar un subconjunto  |        |
de circuitos del sistema para monitorear sus lími-
tes de flujo.
= 0: opción default del SDDP, todos los circuitos
del sistema tendrán sus límites monitoreados;
= 1: solamente un subconjunto de circuitos selec-
cionado en los datos de configuración de circuitos
tendrán sus límites monitoreados.
9

SDDP MANUAL DE ARCHIVOS
2.3.8.4  Datos adicionales
2.3.8.4.1  Mantenimiento plantas hidro

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
PMHI
3  11-11  I1  Indica si serán o no considerados los datos del
programa de mantenimiento de las plantas hidro-
eléctricas.
= 1: opción default del programa, serán conside-
rados los datos de mantenimiento;
= 0: los datos existentes de mantenimiento serán
desconsiderados.
2.3.8.4.2  Mantenimiento plantas térmicas

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  | PMTR   |
| --- | ---- | ------------------- | ------ |
3  11-11  I1  Indica si serán o no considerados los datos del
programa de mantenimiento de las plantas térmi-
cas.
= 1: opción default del programa, serán conside-
rados los datos de mantenimiento;
= 0: los datos existentes de mantenimiento serán
desconsiderados.
2.3.8.4.3  Datos de costo de arranque

| Campo  | Columna  | Tipo  Descripción   |        |
| ------ | -------- | ------------------- | ------ |
| 1      | 1-4      | A4  Palabra clave:  | DCRO   |
| 2      | 6-9      | A4  Palabra clave:  |        |
CARR
3  11-11  I1  Indica si serán o no considerados los datos de
costo de arranque.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.4  Datos de volumen de alerta

| Campo  | Columna  | Tipo  Descripción  |     |
| ------ | -------- | ------------------ | --- |
10

SDDP MANUAL DE ARCHIVOS
| 1   | 1-4  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
DCRO
| 2   | 6-9  | A4  Palabra clave:  | . Indica que no serán conside- |
| --- | ---- | ------------------- | ------------------------------ |
VALE
rados los datos de
3  11-11  I1  Indica si serán o no considerados los datos de vo-
lumen de alerta.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.5  Datos de volumen mínimo

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
VMIN
3  11-11  I1  Indica si serán o no considerados los datos de vo-
lumen mínimo.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.6  Datos de volumen operativo máximo

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
Palabra clave:
| 2   | 6-9  | A4  | VMXO |
| --- | ---- | --- | ---- |
3  11-11  I1  Indica si serán o no considerados los datos de vo-
lumen máximo.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.7  Datos de volumen de espera

| Campo  | Columna  | Tipo  Descripción  |     |
| ------ | -------- | ------------------ | --- |
Palabra clave:
| 1   | 1-4  | A4                  | DCRO |
| --- | ---- | ------------------- | ---- |
| 2   | 6-9  | A4  Palabra clave:  |      |
VESP
3  11-11  I1  Indica si serán o no considerados los datos de vo-
lumen de espera.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
11

SDDP MANUAL DE ARCHIVOS
2.3.8.4.8  Datos de restricción de generación

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
RGER
3  11-11  I1  Indica si serán o no considerados los datos de res-
tricción de generación.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.9  Datos de consumo de combustible

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
Palabra clave:
| 2   | 6-9  | A4  | FCON |
| --- | ---- | --- | ---- |
3  11-11  I1  Indica si serán o no considerados los datos de fac-
tor de consumo de combustible.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.10  Datos de tasa de consumo de combustible

| Campo  | Columna  | Tipo  Descripción  |     |
| ------ | -------- | ------------------ | --- |
Palabra clave:
| 1   | 1-4  | A4                  | DCRO |
| --- | ---- | ------------------- | ---- |
| 2   | 6-9  | A4  Palabra clave:  |      |
FRAT
3  11-11  I1  Indica si serán o no considerados los datos de tasa
de consumo de combustible.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.11  Datos de defluencia máxima

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
MXTO
12

SDDP MANUAL DE ARCHIVOS
3  11-11  I1  Indica si serán o no considerados los datos de de-
fluencia máxima.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.12  Reserva primaria

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
MROD
3  11-11  I1  Indica si serán o no considerados los datos de re-
serva primaria.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.13  Datos de defluencia mínima

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
MNTO
3  11-11  I1  Indica si serán o no considerados los datos de de-
fluencia mínima.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.14  Datos de generación mínima

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
GMIN
3  11-11  I1  Indica si serán o no considerados los datos de ge-
neración mínima.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.15  Datos de reserva secundaria

| Campo  | Columna  | Tipo  Descripción  |     |
| ------ | -------- | ------------------ | --- |
13

SDDP MANUAL DE ARCHIVOS
| 1   | 1-4  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
RESG
3  11-11  I1  Indica si serán o no considerados los datos de re-
serva secundaria.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.16  Datos de duración variable bloques

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
DUVA
3  11-11  I1  Indica si serán o no considerados los datos de du-
ración variable de los bloques.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.17  Datos de riego

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
Palabra clave:
| 2   | 6-9  | A4  | RIEG  |
| --- | ---- | --- | ----- |
3  11-11  I1  Indica si serán o no considerados los datos de
riego.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.18  Datos de costos de emisión CO2

| Campo  | Columna  | Tipo  Descripción  |     |
| ------ | -------- | ------------------ | --- |
Palabra clave:
| 1   | 1-4  | A4                  | DCRO |
| --- | ---- | ------------------- | ---- |
| 2   | 6-9  | A4  Palabra clave:  |      |
CEMI
3  11-11  I1  Indica si serán o no considerados los datos de cos-
tos de emisión de CO2.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
14

SDDP MANUAL DE ARCHIVOS
2.3.8.4.19  Dados de costos de combustible

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
CCMB
3  11-11  I1  Indica se serán o no considerados los datos de cos-
tos de combustible.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.20  Dados de costos de contrato de combustible

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
Palabra clave:
| 2   | 6-9  | A4  | CCST |
| --- | ---- | --- | ---- |
3  11-11  I1  Indica se serán o no considerados los datos de cos-
tos de contrato de combustible.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.21  Dados de disponibilidad de contrato de combustible

| Campo  | Columna  | Tipo  Descripción  |     |
| ------ | -------- | ------------------ | --- |
Palabra clave:
| 1   | 1-4  | A4                  | DCRO |
| --- | ---- | ------------------- | ---- |
| 2   | 6-9  | A4  Palabra clave:  |      |
FCCR
3  11-11  I1  Indica se serán o no considerados los datos de dis-
ponibilidad de contrato de combustible.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.22  Dados de límite de inyección de reservorio de combustible

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |
| --- | ---- | ------------------- | --- |
FRCI
15

SDDP MANUAL DE ARCHIVOS
3  11-11  I1  Indica se serán o no considerados los datos de lí-
mites de inyección de embalse de combustible.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.4.23  Dados de límite de retirada de reservorio de combustible

| Campo  | Columna  | Tipo  Descripción   |     |     |     |
| ------ | -------- | ------------------- | --- | --- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |     |     |
DCRO
| 2   | 6-9  | A4  Palabra clave:  |     |     |     |
| --- | ---- | ------------------- | --- | --- | --- |
FRCR
3  11-11  I1  Indica se serán o no considerados los datos de lí-
mites de retirada de reservorio de combustible.
= 1: opción default del programa, los datos serán
considerados;
= 0: los datos existentes serán desconsiderados.
2.3.8.5  Balance por sistema y por serie

| Campo  | Columna  | Tipo  Descripción   |     |     |     |
| ------ | -------- | ------------------- | --- | --- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |     |     |
BALC
| 2   | 6-9  | I4  Opción que permite imprimir el balance por sis- |     |     |     |
| --- | ---- | --------------------------------------------------- | --- | --- | --- |
tema, por etapa y por serie.
= 0: opción default del SDDP, no imprime archivos
de balance
= 1, imprime 1 archivo de balance por sistema y
|     |     | por  serie.  | Su  nombre  | es  definido  | por  balan- |
| --- | --- | ------------ | ----------- | ------------- | ----------- |
cnnnnxx.csv, donde “nnnn” corresponde al nú-
mero de la serie y “xx” al identificador del sistema.
2.3.8.6  Curva de aversión al riesgo
2.3.8.6.1  Curva de aversión al riesgo
Permite seleccionar las opciones de ejecución para la Curva de Aversión al Riesgo (CAR).

| Campo  | Columna  | Tipo  Descripción   |     |     |     |
| ------ | -------- | ------------------- | --- | --- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |     |     |
AVRS
16

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                |     |
| ------ | -------- | -------------------------------- | --- |
| 2      | 6-9      | I4  Existen tres posibilidades:  |     |
0 = no considera curva de aversión al riesgo;
1 = considera curva de aversión al riesgo desde la po-
lítica operativa;
2 = considera curva de aversión al riesgo solamente
en la simulación final. Opción padrón SDDP.
2.3.8.6.2  Penalización de la curva de aversión al riesgo
Permite seleccionar el tipo de penalización para violación de la Curva de Aversión al Riesgo.

| Campo  | Columna  | Tipo  Descripción                |      |
| ------ | -------- | -------------------------------- | ---- |
|        |          | Palabra clave:                   |      |
| 1      | 1-4      | A4                               | CARP |
| 2      | 6-9      | I4  Existen tres posibilidades:  |      |
0 = considera la penalización de la CAR como siendo
la penalización de referencia. Opción padrón del
SDDP;
1 = determina la penalización reducida de la CAR so-
lamente en la primera abertura de la fase backward;
2 = determina la penalización reducida de la CAR in-
dividualizada en cada abertura de la fase backward.
2.3.8.6.3  Factor de producción para curva de aversión al riesgo
Permite seleccionar las opciones de representación del factor de producción para la Curva de
Aversión al Riesgo (CAR).

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
ARCV
17

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                 |     |     |     |
| ------ | -------- | --------------------------------- | --- | --- | --- |
| 2      | 6-9      | I4  Existen tres posibilidades:   |     |     |     |
0 = considera el factor de producción resultado de la
tabla factor de producción x volumen en todas las
etapas del programa. Opción default del SDDP;
1 = para el cálculo de la EA en el proceso forward y
en la simulación final, se considera el factor de pro-
|     |     | ducción  equivalente  | en  el  volumen  | inicial  | de  la  |
| --- | --- | --------------------- | ---------------- | -------- | ------- |
etapa, resultado de la integral del PCV entre los vo-
|     |     | lúmenes  mínimo  | e  inicial.  Para  | la  recursión  | ba- |
| --- | --- | ---------------- | ------------------ | -------------- | --- |
ckward, se aplica el factor de producción promedio
o factor de producción equivalente en el volumen
máximo;
2 = se aplica el factor de producción equivalente en
el volumen inicial de la etapa para todas las etapas
del programa.
2.3.8.7  Vertimiento no controlable
La opción, cuando seleccionada, será aplicada a todas las plantas con vertimiento no contro-
lable.

| Campo  | Columna  | Tipo  Descripción   |     |     |     |
| ------ | -------- | ------------------- | --- | --- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |     |     |
VNOC
| 2   | 6-9  | I4  Existen de los posibilidades:  |     |     |     |
| --- | ---- | ---------------------------------- | --- | --- | --- |
0 = vertimiento no controlable penalizado en la fun-
ción objetivo. Opción default del modelo;
= 1 vertimiento no controlable modelado como pro-
gramación entera 0-1
2.3.8.8  Red de gas
Permite seleccionar la representación de la red de gas y el tipo de costo de producción.

| Campo  | Columna  | Tipo  Descripción   |     |     |     |
| ------ | -------- | ------------------- | --- | --- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |     |     |
RGAS
18

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                |     |
| ------ | -------- | -------------------------------- | --- |
| 2      | 6-9      | I4  Existen tres posibilidades:  |     |
0 = no representa la red de gas;
1 = representa la red de gas con costo de combusti-
ble por térmica (ignora costo de producción de gas
por nodo);
= 2 representa la red de gas con costo por nodo (ig-
nora costo de combustible y de transporte y se con-
sideran los costos de O&M)
2.3.8.9  Número mínimo de iteraciones
Permite definir un número mínimo de iteraciones. El programa va a iterar e continuar adicio-
nando hiperplanos en la Función de Costo Futuro hasta atender este número mínimo de ite-
raciones, inclusive si el criterio de convergencia ya fue atendido.

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
MNIT
| 2   | 6-9  | I4  Número mínimo de iteraciones  |     |
| --- | ---- | --------------------------------- | --- |
2.3.8.10  Escenarios de generación de fuentes renovables
Determina el número de escenarios de fuentes renovables para la simulación final.

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
CGND
| 2   | 6-9  | I4  Existen de los posibilidades:  |     |
| --- | ---- | ---------------------------------- | --- |
0: opción default del programa, el número de esce-
narios de fuentes renovables en la simulación final
corresponde al número de aberturas;
1: o número de escenarios de fuentes renovables en
la simulación final corresponde al número de series
forward.
2.3.8.11  Volumen inicial para la primera etapa
Determina la opción de lectura de los volúmenes iníciales para la primera etapa.

| Campo  | Columna  | Tipo  Descripción   |        |
| ------ | -------- | ------------------- | ------ |
| 1      | 1-4      | A4  Palabra clave:  | VIEX   |
19

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                  |     |
| ------ | -------- | ---------------------------------- | --- |
| 2      | 6-9      | I4  Existen de los posibilidades:  |     |
0: opción default del programa, volúmenes iníciales
leídos de los datos de configuración de las plantas
hidroeléctricas;
1: volúmenes iníciales leídos de un archivo externo
importado en formato CSV.
2.3.8.12  Volumen inicial para primera recursión backward
Determina la opción de lectura de los volúmenes iniciales para las demás etapas en la primera
recursión backward.

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
VBCK
| 2   | 6-9  | I4  Existen de los posibilidades:  |     |
| --- | ---- | ---------------------------------- | --- |
0: opción default del programa, volúmenes discreti-
zados;
1: volúmenes iníciales leídos de un archivo externo
importado en formato CSV.
2.3.8.13  Representación de pérdidas
Los siguientes parámetros están asociados a la representación de pérdidas en el modelo.
2.3.8.13.1  Micro-iteraciones de pérdidas

| Campo  | Columna  | Tipo  Descripción   |        |
| ------ | -------- | ------------------- | ------ |
| 1      | 1-4      | A4  Palabra clave:  | MXLS   |
2  6-9  I4  Indica el número de micro-iteraciones en el método
de relajación de pérdidas. Por default este número
es seleccionado igual a 6.
2.3.8.13.2  Penalidad inicial delas pérdidas

| Campo  | Columna  | Tipo  Descripción                                 |        |
| ------ | -------- | ------------------------------------------------- | ------ |
| 1      | 1-4      | A4  Palabra clave:                                | PLSS   |
| 2      | 6-9      | I4  Indica la penalidad inicial de las pérdidas.  |        |
Por default este número es seleccionado igual a 0.
2.3.8.13.3  Aproximación de pérdidas en la política operativa

20

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
ITAL
| 2   | 6-9  | I4  Este campo tiene dos representaciones:  |     |
| --- | ---- | ------------------------------------------- | --- |
= 0: la aproximación de pérdidas no es representada
en la política operativa
>0: Indica la iteración en la cual la aproximación de
pérdidas es representada en la política operativa.
Por default este valor es igual a 3.
2.3.8.14  Series con filtro outliers

| Campo  | Columna  | Tipo  Descripción  |     |
| ------ | -------- | ------------------ | --- |
Palabra clave:
| 1   | 1-4  | A4  | GSFI |
| --- | ---- | --- | ---- |
2  6-9  I4  0: no filtra outliers de los escenarios generados
1: filtra outliers de los escenarios generados
2.3.8.15  Demanda variable

| Campo  | Columna  | Tipo  Descripción   |     |
| ------ | -------- | ------------------- | --- |
| 1      | 1-4      | A4  Palabra clave:  |     |
DEMV
| 2   | 6-9  | I4  0: demanda fija  |     |
| --- | ---- | -------------------- | --- |
3: demanda variable con distribución normal en la
simulación final
4: demanda variable con distribución normal en la
política operativa y simulación final
2.4  Unidad monetaria
Archivo ASCII denominado UNIMON.DAT, ubicado en el directorio de datos del estudio. Este
archivo es opcional y define la unidad monetaria de referencia y las tasas de conversión entre
unidades monetarias y la unidad monetaria de referencia. Sus registros tienen el siguiente
formato.
2.4.1  Registro tipo 1
Indica la unidad monetaria de referencia.

| Campo  | Columna  | Tipo  Descripción         |     |
| ------ | -------- | ------------------------- | --- |
| 1      | 1-5      | A5  Palabra clave: $UREF  |     |
2  7-9  A3  Unidad monetaria de referencia en la cual son produ-
cidos los resultados
21

SDDP MANUAL DE ARCHIVOS
2.4.2  Registro tipo 2
Registro comentario.
2.4.3  Registro tipo 3
Indica la tasa de conversión de una determinada unidad monetaria para la unidad monetaria
de referencia.

| Campo  | Columna  | Tipo  Descripción     |
| ------ | -------- | --------------------- |
| 1      | 1-3      | A3  Unidad monetaria  |
2  5-12  F8.0  Tasa de conversión de la unidad monetaria para la uni-
dad monetaria de referencia
2.5  Duración de los bloques
2.5.1  Duración fija
Archivo opcional DURFIXYYY.DAT, en formato ASCII, ubicado en el directorio de datos del estu-
dio, considerando YYY bloques. Él contiene las duraciones fijas de los bloques, válidas para
todos los períodos del horizonte de estudio.
El registro contiene las duraciones de los bloques en el siguiente formato:

| Campo  | Columna  | Tipo  Descripción                  |
| ------ | -------- | ---------------------------------- |
| 1      | 1        | real  Duración del bloque 1 (%).   |
| 2      | 1        | real  Duración del bloque 2 (%).   |
| …      | …        | …  …                               |
| YYY    | 1        | real  Duración del bloque YYY (%)  |
2.5.2  Duración variable
Archivo opcional DUVAZZYY.DAT, en formato ASCII, ubicado en el directorio de datos del estu-
dio, considerando YY bloques y donde ZZ indica lo siguiente:
  ZZ = ME, si las demandas son mensuales,
|   ZZ = SE,   |     | si las demandas son semanales.  |
| ------------ | --- | ------------------------------- |
Él contiene las duraciones variables de los bloques por año, bloque y período. Por ejemplo, el
archivo DUVAME03.DAT contiene los datos de la duración variable de los bloques, a periodos
mensuales y considerando 3 bloques.
El primer registro es comentario. El segundo registro contiene las duraciones, en horas, de los
bloques, en el siguiente formato:
22

SDDP MANUAL DE ARCHIVOS
Campo Columna Tipo Descripción
1 1-4 I4 Año del dato de demanda.
2 6-8 I3 Número del bloque de demanda.
3 9-14 F6.0 Duración del primer mes o semana (horas.)
4 15-20 F6.0 Duración del segundo mes o semana (horas.)
5-53 etc. etc. etc.
54 315-320 F6.0 Duración de la semana 52 (horas.)
23

SDDP MANUAL DE ARCHIVOS
3  CENTRALES HIDROELÉCTRICAS
Los datos de centrales hidroeléctricas incluyen:
•  configuración hidroeléctrica
•  modificaciones de la configuración
•  mantenimiento
•  riego
•  volúmenes de seguridad
•  volúmenes de alerta
•  reserva primaria
3.1  Configuración hidroeléctrica
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
CHIDROXX.DAT contiene los datos de la configuración hidroeléctrica del sistema XX.
El primer registro es comentario. Los demás tienen el siguiente formato:
3.1.1  Datos generales

| Campo  | Columna  | Tipo  Descripción                       |
| ------ | -------- | --------------------------------------- |
| 1      | 1-4      | I4  Número de la central.               |
| 2      | 6-17     | A12  Nombre de la central.              |
| 3      | 19-22    | I4  Número de la estación hidrológica.  |
4  24-27  I4  Índice de la central aguas abajo para vertimiento.
5  29-32  I4  Índice de la central aguas abajo para turbinamiento.
| 6   | 34-37  | I4  Número de unidades.  |
| --- | ------ | ------------------------ |
| 7   | 39-42  | I4  Tipo de central:     |
0 = Existente;
1 = Futura.
3.1.2  Datos de la central

| Campo  | Columna  | Tipo  Descripción               |
| ------ | -------- | ------------------------------- |
| 8      | 44-50    | F7.0  Potencia instalada (MW).  |
Factor de producción promedio (MW/m3/s).
| 9   | 52-58  | F7.0                                        |
| --- | ------ | ------------------------------------------- |
| 10  | 60-66  | F7.0  Defluencia turbinable mínima (m3/s).  |
Defluencia turbinable máxima (m3/s).
| 11  | 68-74  | F7.0                         |
| --- | ------ | ---------------------------- |
| 12  | 76-82  | F7.0  Volumen mínimo (hm3).  |
| 13  | 84-90  | F7.0  Volumen máximo (hm3).  |
24

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción  |     |     |
| ------ | -------- | ------------------ | --- | --- |
14  92-98  F7.0  Condición inicial del embalse (ver campo 71). Si la
condición inicial está dada en volumen (p.u.), el vo-
lumen inicial se calcula como v.inicial = vmínimo +
c.inic.* (v.máximo – v.mínimo). Si la condición ini-
cial está dada en cota (m), si calcula el volumen ini-
cial interpolando la tabla volumen x cota.
15  100-106  F7.0  Defluencia  total  mínima  (turbinamiento  +  verti-
miento) (m3/s)
| 16  | 111-114  | I4  Indicador de vertimiento no controlable  |     |     |
| --- | -------- | -------------------------------------------- | --- | --- |
0 =  vertimiento controlable
|     |     | 1 =  vertimiento  | no  controlable  | (solamente  |
| --- | --- | ----------------- | ---------------- | ----------- |
vierte cuando está en el volumen máximo)
2 =  vertimiento parcialmente controlable
17  116-122  F7.0  Factor de indisp. de corto plazo - ICP (%).
| 18  | 124-130  | F7.0  Factor de indisp. histórico - IH (%).  |     |     |
| --- | -------- | -------------------------------------------- | --- | --- |
3.1.3  Tabla factor de producción x volumen

| Campo  | Columna  | Tipo  Descripción  |     |     |
| ------ | -------- | ------------------ | --- | --- |
19  132-138  F7.0  Tabla factor de producción x volumen; factor de
producción 1 (MW/m3/s).
Volumen 1 (hm3) (tiene que ser igual al volumen mí-
| 20  | 140-146  | F7.0  |     |     |
| --- | -------- | ----- | --- | --- |
nimo)
Factor de producción 2 (MW/m3/s).
| 21  | 148-154  | F7.0                                     |     |     |
| --- | -------- | ---------------------------------------- | --- | --- |
| 22  | 156-162  | F7.0  Volumen 2 (hm3).                   |     |     |
| 23  | 164-170  | F7.0  Factor de producción 3 (MW/m3/s).  |     |     |
| 24  | 172-178  | F7.0  Volumen 3 (hm3).                   |     |     |
| 25  | 180-186  | F7.0  Factor de producción 4 (MW/m3/s).  |     |     |
| 26  | 188-194  | F7.0  Volumen 4 (hm3).                   |     |     |
Factor de producción 5 (MW/m3/s).
| 27  | 196-202  | F7.0  |     |     |
| --- | -------- | ----- | --- | --- |
28  204-210  F7.0  Volumen 5 (hm3) (tiene que ser igual al volumen
máximo).
3.1.4  Tabla área x volumen

| Campo  | Columna  | Tipo  Descripción                          |     |     |
| ------ | -------- | ------------------------------------------ | --- | --- |
| 29     | 212-218  | F7.0  Tabla área x volumen; área 1 (Km2).  |     |     |
30  220-226  F7.0  Tabla área x volumen; volumen 1 (hm3) (tiene que
ser igual al volumen mínimo).
| 31  | 228-234  | F7.0  Área 2 (Km2).  |     |     |
| --- | -------- | -------------------- | --- | --- |
25

SDDP MANUAL DE ARCHIVOS
| 32  | 236-242  | F7.0  Volumen 2 (hm3).  |
| --- | -------- | ----------------------- |
| 33  | 244-250  | F7.0  Área 3 (Km2).     |
| 34  | 252-258  | F7.0  Volumen 3 (hm3).  |
| 35  | 260-266  | F7.0  Área 4 (Km2).     |
Volumen 4 (hm3).
| 36  | 268-274  | F7.0                 |
| --- | -------- | -------------------- |
| 37  | 276-282  | F7.0  Área 5 (Km2).  |
38  284-290  F7.0  Volumen 5 (hm3) (tiene que ser igual al volumen
máximo).
3.1.5  Tabla infiltración x volumen

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
39  292-298  F7.0  Tabla infiltración x volumen; infiltración 1 (m3/s).
40  300-306  F7.0  Volumen 1 (hm3) (igual al volumen mínimo).
Infiltración 2 (m3/s).
| 41  | 308-314  | F7.0  |
| --- | -------- | ----- |
Volumen 2 (hm3).
| 42  | 316-322  | F7.0                          |
| --- | -------- | ----------------------------- |
| 43  | 324-330  | F7.0  Infiltración 3 (m3/s).  |
| 44  | 332-338  | F7.0  Volumen 3 (hm3).        |
| 45  | 340-346  | F7.0  Infiltración 4 (m3/s).  |
| 46  | 348-354  | F7.0  Volumen 4 (hm3).        |
| 47  | 356-362  | F7.0  Infiltración 5 (m3/s).  |
Volumen 5 (hm3) (igual al volumen máximo).
| 48  | 364-370  | F7.0  |
| --- | -------- | ----- |
3.1.6  Tabla cota x volumen

| Campo  | Columna  | Tipo  Descripción                        |
| ------ | -------- | ---------------------------------------- |
| 49     | 372-378  | F7.0  Tabla Cota × Volumen: Cota 1 (m).  |
50  380-386  F7.0  Volumen 1 (hm3) (tiene que ser igual al volumen mí-
nimo).
| 51  | 388-394  | F7.0  Cota 2 (m).       |
| --- | -------- | ----------------------- |
| 52  | 396-402  | F7.0  Volumen 2 (hm3).  |
| 53  | 404-410  | F7.0  Cota 3 (m).       |
Volumen 3 (hm3).
| 54  | 412-418  | F7.0                    |
| --- | -------- | ----------------------- |
| 55  | 420-426  | F7.0  Cota 4 (m).       |
| 56  | 428-434  | F7.0  Volumen 4 (hm3).  |
| 57  | 436-442  | F7.0  Cota 5 (m).       |
58  444-450  F7.0  Volumen 5 (hm3) (tiene que ser igual al volumen
máximo).
26

SDDP MANUAL DE ARCHIVOS
3.1.7 Coeficientes de evaporación
Campo Columna Tipo Descripción
59 452-455 F4.0 Coeficiente de evaporación/enero (mm./mes).
60 457-460 F4.0 Coeficiente de evaporación/febrero (mm./mes).
61 462-465 F4.0 Coeficiente de evaporación/marzo (mm./mes).
62 467-470 F4.0 Coeficiente de evaporación/abril (mm./mes).
63 472-475 F4.0 Coeficiente de evaporación/mayo (mm./mes).
64 477-480 F4.0 Coeficiente de evaporación/junio (mm./mes).
65 482-485 F4.0 Coeficiente de evaporación/julio (mm./mes).
66 487-490 F4.0 Coeficiente de evaporación/agosto (mm./mes).
67 492-495 F4.0 Coeficiente de evaporación/septiembre (mm./mes).
68 497-500 F4.0 Coeficiente de evaporación/octubre (mm./mes).
69 502-505 F4.0 Coeficiente de evaporación/noviembre (mm./mes).
70 507-510 F4.0 Coeficiente de evaporación/diciembre (mm./mes).
3.1.8 Otros datos
Campo Columna Tipo Descripción
71 512-515 I4 Tipo de condición inicial en el campo 14
= 0 volumen (p.u.)
= 1 cota (m)
72 517-520 I4 Tipo de infiltración
= 0 infiltra para la central aguas abajo para
turbinamiento (campo 5)
=1 infiltra para la central aguas abajo para
infiltración (campo 73)
73 522-525 I4 Código de la central aguas abajo para infiltración
74 527-530 I4 Tipo de valor constante para el área en la recursión
backward o en plantas filo de agua
= 0 valor máximo de la tabla área × volumen
= 1 valor indicado en el campo 75
75 532-538 F7.0 Valor constante de área para la recursión backward
o en plantas filo de agua (Km2)
76 540-543 I4 Tipo de valor constante para la infiltración en la re-
cursión backward
= 0 valor máximo de la tabla infiltración × vol
= 1 valor indicado en el campo 77
77 545-551 F7.0 Valor constante de infiltración para la recursión. ba-
ckward (m3/s)
27

SDDP MANUAL DE ARCHIVOS
Campo Columna Tipo Descripción
78 553-559 F7.0 Factor de regularización de central filo de agua
( 0 ≤ α ≤ 1 ).
79 561-564 I4 Factor de producción en el cálculo de la política
= 0 constante;
= 1 en función del volumen inicial (utiliza tabla de
factor de producción vs. volumen)
80 566-569 I4 Indicador de costo explícito para vertimiento
81 571-577 F7.0 Costo de vertimiento (k$/hm3)
82 579-582 I4 Indicador para sorteo de fallas
83 584-590 F7.0 Costo de O&M para generación hidro ($/MWh)
84 592-595 I4 Factor de producción en la simulación final
= -1 constante;
= 0 en función del volumen inicial (utiliza tabla de
factor de producción vs. volumen);
= 1 en función de la diferencia entre la altura del ni-
vel inicial del embalse y el nivel promedio del canal
de desfogue (utiliza tabla cota vs. volumen y campo
87);
= 2 en función de la diferencia entre la altura del ni-
vel inicial del embalse y la altura variable del canal
de desfogue (utiliza tabla cota vs. volumen y tabla
de altura de canal de desfogue vs. caudal de-
fluente).
85 597-603 F7.0 Rendimiento del grupo turbina generador (p.u.)
86 605-608 I4 Número del embalse asociado (en el caso del indi-
cador de cálculo del factor de producción en fun-
ción de la altura – campo 84 – sea igual a 1 y que la
central sea de pasada)
87 610-616 F7.0 Nivel promedio del canal de desfogue (m.s.n.m.)
3.1.9 Central aguas abajo para energía almacenada
88 618-618 I1 Tipo de central aguas abajo para cálculo de energía
almacenada
= 0 igual a la central aguas abajo para turbinamiento
= 1 central para cálculo de energía almacenada es-
pecificada por el usuario
89 620-623 I4 Número de la central aguas abajo para cálculo de la
energía almacenada especificada por el usuario,
caso se haya escogido la opción 1 en el campo an-
terior.
28

SDDP MANUAL DE ARCHIVOS
3.1.10 Tabla de caudal turbinable en función del caudal total

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 90     | 625      | I1  Indicador      |
=1 los siguientes datos serán utilizados
=0 los siguientes datos serán ignorados
Caudal Turbinable Punto 1 (m3/s).
| 91  | 627-633  | F7.0  |
| --- | -------- | ----- |
Caudal Total Punto 1 (m3/s).
| 92  | 635-641  | F7.0                                     |
| --- | -------- | ---------------------------------------- |
| 93  | 643-649  | F7.0  Caudal Turbinable Punto 2 (m3/s).  |
| 94  | 651-657  | F7.0  Caudal Total Punto 2 (m3/s).       |
| 95  | 659-665  | F7.0  Caudal Turbinable Punto 3 (m3/s).  |
| 96  | 667-673  | F7.0  Caudal Total Punto 3 (m3/s).       |
| 97  | 675-681  | F7.0  Caudal Turbinable Punto 4 (m3/s).  |
Caudal Total Punto 4 (m3/s).
| 98   | 683-689  | F7.0                                     |
| ---- | -------- | ---------------------------------------- |
| 99   | 691-697  | F7.0  Caudal Turbinable Punto 5 (m3/s).  |
| 100  | 699-705  | F7.0  Caudal Total Punto 5 (m3/s).       |
3.1.11 Tabla defluencia en función de la altura del canal de desfogue

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 101    | 709:709  | I1  Indicador      |
=1 si el vertimiento influencia la altura del canal de
desfogue
| 102  | 711:717  | F7.0  Canal de desfogue (m) – punto 1  |
| ---- | -------- | -------------------------------------- |
| 103  | 719:725  | F7.0  Defluencia (m3/s) – punto 1      |
| 104  | 727:733  | F7.0  Canal de desfogue (m) – punto 2  |
| 105  | 735:741  | F7.0  Defluencia (m3/s) – punto 2      |
| 106  | 743:749  | F7.0  Canal de desfogue (m) – punto 3  |
| 107  | 751:757  | F7.0  Defluencia (m3/s) – punto 3      |
| 108  | 759:765  | F7.0  Canal de desfogue (m) – punto 4  |
| 109  | 767:773  | F7.0  Defluencia (m3/s) – punto 4      |
| 110  | 775:781  | F7.0  Canal de desfogue (m) – punto 5  |
| 111  | 783:789  | F7.0  Defluencia (m3/s) – punto 5      |
3.1.12 Indicador participación en el cálculo de energías

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
29

SDDP MANUAL DE ARCHIVOS
| 112  | 791  | I1  Existen de los posibilidades:  |
| ---- | ---- | ---------------------------------- |
= 0 (padrón) planta que participa en el cálculo de las
energías afluentes y almacenadas.
= 1 planta que no participa del cálculo de las energías
afluentes y almacenadas.
3.1.13 Factor de pérdidas hidráulicas en las defluencias

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
114  793  F7.0  Factor de pérdidas hidráulicas en las defluencias de
turbinamiento (p.u.)

115  801  F7.0  Factor de pérdidas hidráulicas en las defluencias de
vertimiento (p.u.)

3.2  Modificación de la configuración hidroeléctrica
Conjuntos de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo lla-
mado MHIDROXX.DAT contiene las modificaciones a la configuración hidroeléctrica inicial del
sistema XX. El programa solamente utiliza estas informaciones si la configuración es dinámica
(registro 8 del archivo SDDP.DAT). Este archivo contiene 4 tipos de registro:
3.2.1  Registro tipo 1
| Campo  | Columna   | Tipo  Descripción              |
| ------ | --------- | ------------------------------ |
|        | 1  1-9    | A9  Palabra clave: $version=   |
|        | 2  10-13  | I4  Número de la versión       |
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
3.2.2  Registro tipo 2
Identifica la etapa (día/mes/año) de la modificación.

| Campo  | Columna  | Tipo  Descripción                    |
| ------ | -------- | ------------------------------------ |
| 1      | 1-4      | A  Debe contener la palabra "MOD:".  |
| 2      | 6-7      | I2  Día de la modificación.          |
| 3      | 9-10     | I2  Número del mes                   |
| 4      | 12-15    | I4  Año                              |
30

SDDP MANUAL DE ARCHIVOS
3.2.3  Registro tipo 3
Es un header igual al de los archivos CHIDROXX.DAT. Contiene la palabra " NUM" en las 4 prime-
ras columnas.
3.2.4  Registro tipo 4
Contiene los nuevos datos de la central, en el mismo formato de los archivos CHIDROXX.DAT.
Se pueden actualizar los siguientes campos:

| Campo  | Columna  | Tipo  Descripción                               |
| ------ | -------- | ----------------------------------------------- |
| 6      | 34-37    | I4  Número de unidades.                         |
| 8      | 44-50    | F7.0  Potencia instalada (MW)                   |
| 9      | 52-58    | F7.0  Factor de producción promedio (MW/m3/s).  |
| 10     | 60-66    | F7.0  Defluencia mínima (m3/s).                 |
| 11     | 68-74    | F7.0  Defluencia máxima (m3/s).                 |
| 13     | 84-90    | F7.0  Volumen máximo (hm3).                     |
15  100-106  F7.0  Defluencia total mínima (turbinamiento + verti-
miento) (m3/s)
17  116-122  F7.0  Factor de indisp. de corto plazo - ICP (%).
| 18  | 124-130  | F7.0  Factor de indisp. histórico - IH (%).  |
| --- | -------- | -------------------------------------------- |
| …   | …        | …  …                                         |
| 90  | 625      | I1  Indicador                                |
=1 los siguientes datos serán utilizados
=0 los siguientes datos serán ignorados
| 91  | 627-633  | F7.0  Caudal Turbinable Punto 1 (m3/s).  |
| --- | -------- | ---------------------------------------- |
| 92  | 635-641  | F7.0  Caudal Total Punto 1 (m3/s).       |
| 93  | 643-649  | F7.0  Caudal Turbinable Punto 2 (m3/s).  |
| 94  | 651-657  | F7.0  Caudal Total Punto 2 (m3/s).       |
| 95  | 659-665  | F7.0  Caudal Turbinable Punto 3 (m3/s).  |
Caudal Total Punto 3 (m3/s).
| 96  | 667-673  | F7.0  |
| --- | -------- | ----- |
Caudal Turbinable Punto 4 (m3/s).
| 97   | 675-681  | F7.0                                     |
| ---- | -------- | ---------------------------------------- |
| 98   | 683-689  | F7.0  Caudal Total Punto 4 (m3/s).       |
| 99   | 691-697  | F7.0  Caudal Turbinable Punto 5 (m3/s).  |
| 100  | 699-705  | F7.0  Caudal Total Punto 5 (m3/s).       |
| …    | …        | …  …                                     |
| 102  | 711:717  | F7.0  Canal de desfogue (m) – punto 1    |
| 103  | 719:725  | F7.0  Defluencia (m3/s) – punto 1        |
| 104  | 727:733  | F7.0  Canal de desfogue (m) – punto 2    |
| 105  | 735:741  | F7.0  Defluencia (m3/s) – punto 2        |
| 106  | 743:749  | F7.0  Canal de desfogue (m) – punto 3    |
| 107  | 751:757  | F7.0  Defluencia (m3/s) – punto 3        |
31

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                      |
| ------ | -------- | -------------------------------------- |
| 108    | 759:765  | F7.0  Canal de desfogue (m) – punto 4  |
| 109    | 767:773  | F7.0  Defluencia (m3/s) – punto 4      |
| 110    | 775:781  | F7.0  Canal de desfogue (m) – punto 5  |
| 111    | 783:789  | F7.0  Defluencia (m3/s) – punto 5      |
112  791  I1  Indicador participación en el cálculo de las ener-
gías. Existen de los posibilidades:
= 0 (padrón) planta que participa en el cálculo
de las energías afluentes y almacenadas.
= 1 planta que no participa del cálculo de las
energías afluentes y almacenadas.
Se coloca un registro tipo 3 por cada central modificada en esa etapa.
3.3 Factor de pérdidas de hidroeléctricas
Archivo ASCII denominado MLOSFXX.DAT localizado en el directorio de datos del sistema. Este
archivo contiene las modificaciones de los factores de pérdidas de hidroeléctricas del sistema
XX. Este archivo está organizado de la siguiente manera:
3.3.1  Registro tipo 1
| Campo  | Columna  | Tipo  Descripción              |
| ------ | -------- | ------------------------------ |
| 1      | 1-9      | A9  Palabra clave: $version=   |
| 2      | 10-13    | I4  Número de la versión       |
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
3.3.2  Registro tipo 2
| Campo  | Columna  | Tipo  Descripción               |
| ------ | -------- | ------------------------------- |
| 1      | 1-10     | Fecha  Fecha dd/mm/yyyy         |
| 2      | 12-16    | I5  Código del agente           |
| 3      | 18-29    | A12  Nombre del agente          |
| 4      | 31-40    | A10  Atributo a ser modificado  |
5  42-46  I5  Identificador del bloque (* = todos los bloques)
| 6   | 48-57  | F10.0  Valor  |
| --- | ------ | ------------- |
En este caso el atributo que puede ser modificado es:
 – Factor de pérdidas de hidroeléctricas (p.u.)
HYDLSF
32

SDDP MANUAL DE ARCHIVOS
3.4  Mantenimiento de las hidroeléctricas
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
PMHIZZXX.DAT contiene los programas de mantenimiento (semanal si ZZ = "SE" o mensual si ZZ
= "ME") del sistema XX (definido en el campo 3 del registro del archivo SISTEM.DAT).
El archivo contiene 5 tipos de registros.
3.4.1  Registro tipo 1
Identifica el tipo de mantenimiento.

| Campo  | Columna  | Tipo  Descripción                         |
| ------ | -------- | ----------------------------------------- |
| 1      | 1-12     | A4  Contiene las palabras "Tipo Info. :"  |
| 2      | 17-17    | I1  Tipo de Mantenimiento:                |
=1 se informa el valor que se debe retirar (Reduc-
ción)
=2 se informa el valor resultante después del
mantenimiento (Absoluto)
3.4.2  Registro tipo 2
Identifica las unidades del mantenimiento.

| Campo  | Columna  | Tipo  Descripción                       |
| ------ | -------- | --------------------------------------- |
| 1      | 1-12     | A4  Contiene las palabras "Unidades :"  |
| 2      | 17-17    | I1  Tipo de medida para mantenimiento:  |
=1 número de unidades
=2 %
=3 MW
=4 m3/s
3.4.3  Registro tipo 3
Identifica la central en mantenimiento.

| Campo  | Columna  | Tipo  Descripción                         |
| ------ | -------- | ----------------------------------------- |
| 1      | 1-12     | A4  Contiene las palabras "**** Planta:"  |
| 2      | 15-17    | I3  Número de la central                  |
| 3      | 19-30    | A12  Nombre de la central                 |
3.4.4  Registro tipo 4
Header del programa de mantenimiento.
33

SDDP MANUAL DE ARCHIVOS

| Campo  | Columna  | Tipo  Descripción                |
| ------ | -------- | -------------------------------- |
| 1      | 1-4      | A4  Contiene la palabra "A~NO".  |
3.4.5  Registro tipo 5
Valores del mantenimiento. Hay un registro tipo 5 para cada año del programa de manteni-
miento.

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 1      | 1-4      | I4  Año            |
2  5-12  F8.0  Valor del mantenimiento en la etapa 1 (semana o
mes).
| 3     | 13-20    | F8.0  Valor del mantenimiento en la etapa 2   |
| ----- | -------- | --------------------------------------------- |
| 4     | 21-28    | F8.0  Valor del mantenimiento en la etapa 3   |
| 5-51  | etc.     | etc.  etc.                                    |
| 52    | 413-420  | F8.0  Valor del mantenimiento en la etapa 52  |
3.5  Datos de riego
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
RIEGYYXX.DAT contiene los datos de riego por etapa (YY = ME para etapas mensuales; YY = SE
para etapas semanales) del sistema XX, donde XX es el identificador del sistema definido en el
campo 3 del registro del archivo SISTEM.DAT.
Este archivo contiene 3 tipos de registro:
3.5.1  Registro tipo 1
Identifica la central que está aguas abajo del riego.

| Campo  | Columna  | Tipo  Descripción                    |
| ------ | -------- | ------------------------------------ |
| 1      | 1-4      | A4  Contiene la palabra NUM:         |
| 2      | 5-8      | I4  Número de la central             |
| 3      | 10-21    | A12  Nombre de la central            |
| 4      | 39-39    | I1  =0: riego prioritario (default)  |
=1: energía prioritaria
=2: valor proporcionado por el usuario
| 5   | 41-50  | F10.0  Valor proporcionado por el usuario  |
| --- | ------ | ------------------------------------------ |
La selección de los campos 4, 5 y 6 es mutuamente excluyente.
34

SDDP MANUAL DE ARCHIVOS
3.5.2  Registro tipo 2
Este registro es un header y debe ser colocado siempre a continuación de un registro tipo 1.
Debe contener la palabra "A~NO" en las 4 primeras columnas.
3.5.3  Registro tipo 3
Contiene los datos de riego variables por etapa. Cada registro está asociado a un año y cada
columna a una etapa.

| Campo  | Columna  | Tipo  Descripción                  |
| ------ | -------- | ---------------------------------- |
| 1      | 1-4      | I4  Año                            |
| 2      | 5-10     | F6.0  Riego en la etapa 1 (m3/s).  |
| 3      | 11-16    | F6.0  Riego en la etapa 2 (m3/s).  |
| etc.   | etc.     | etc.  etc.                         |
Observaciones:
•  Se coloca un registro tipo 3 por cada año del estudio.
•  Se debe repetir un conjunto de registros 1, 2 y 3 para cada punto de riego.
3.6  Defluencia total máxima
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
MXTOYYXX.DAT contiene los límites en la defluencia total (caudales turbinados + vertidos) (YY =
ME para etapas mensuales; YY = SE para etapas semanales) del sistema XX. El programa sola-
mente lee estas informaciones si se indicó que la configuración es dinámica (registro 8 del
archivo SDDP.DAT). Este archivo contiene 3 tipos de registro:
3.6.1  Registro tipo 1
Identifica la central con límites en la defluencia máxima:

| Campo  | Columna  | Tipo  Descripción                    |
| ------ | -------- | ------------------------------------ |
| 1      | 1-12     | A4  Debe contener "**** Planta:"     |
| 1      | 14-17    | I4  Código de la central             |
| 2      | 19-30    | A12  Nombre de la central            |
| 3      | 41-50    | F10.0  factor de penalidad (k$/hm3)  |
3.6.2  Registro tipo 2
Header para las etapas.

35

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                                |
| ------ | -------- | ------------------------------------------------ |
| 1      | 1-4      | A4  Este campo debe contener la palabra "A~NO".  |
3.6.3  Registro tipo 3
Contiene los límites en la defluencia máxima por etapa. Cada registro está asociado a un año
y cada columna a una etapa. Sólo es necesario llenar los campos donde existe una alteración
de los límites.

| Campo  | Columna  | Tipo  Descripción                                |
| ------ | -------- | ------------------------------------------------ |
| 1      | 1-4      | I4  Año                                          |
| 2      | 5-12     | A8  Límite en la defluencia máxima (m3/s) de la  |
etapa 1
Límite en la defluencia máxima (m3/s) de la
| 3   | 13-20  | A8  |
| --- | ------ | --- |
etapa 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  un campo vacío indica que no hay variación de la defluencia máxima con respecto a la
etapa anterior.
•  Se coloca un registro tipo 3 por cada año del estudio.
•  El conjunto de registros 1, 2 y 3 se repiten para cada central con límites en la defluencia
máxima.
3.7  Defluencia total mínima
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
MNTOYYXX.DAT contiene los límites en la defluencia mínima (caudales turbinados + vertidos) (YY
= ME para etapas mensuales; YY = SE para etapas semanales) del sistema XX. El programa sola-
mente lee estas informaciones si se indicó que la configuración es dinámica (registro 8 del
archivo SDDP.DAT). Este archivo contiene 3 tipos de registro:
3.7.1  Registro tipo 1
Identifica la central con límites en la defluencia mínima:

|     | Campo  Columna  | Tipo  Descripción                    |
| --- | --------------- | ------------------------------------ |
|     | 1  1-12         | A4  Debe contener "**** Planta:"     |
|     | 2  14-17        | I4  Código de la central             |
|     | 3  19-30        | A12  Nombre de la central            |
|     | 4  41-50        | F10.0  Factor de penalidad (k$/hm3)  |
36

SDDP MANUAL DE ARCHIVOS
3.7.2  Registro tipo 2
Header para las etapas.

| Campo  | Columna  | Tipo  Descripción                                |
| ------ | -------- | ------------------------------------------------ |
| 1      | 1-4      | A4  Este campo debe contener la palabra "A~NO".  |
3.7.3  Registro tipo 3
Contiene los límites en la defluencia mínima por etapa. Cada registro está asociado a un año
y cada columna a una etapa. Sólo es necesario llenar los campos donde existe una alteración
de los límites.

| Campo  | Columna  | Tipo  Descripción                                |
| ------ | -------- | ------------------------------------------------ |
| 1      | 1-4      | I4  Año                                          |
| 2      | 5-12     | A8  Límite en la defluencia mínima (m3/s) de la  |
etapa 1
| 3   | 13-20  | A8  Límite en la defluencia mínima (m3/s) de la  |
| --- | ------ | ------------------------------------------------ |
etapa 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•
Un campo vacío indica que no hay variación de la defluencia mínima con respecto a la
etapa anterior.
•
Se coloca un registro tipo 3 por cada año del estudio.
•
El conjunto de registros 1, 2 y 3 se repiten para cada central con límites en la defluencia
mínima.
3.8  Vertimiento máximo
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
MXSPYYXX.DAT contiene los límites máximos en el vertimiento (YY = ME para etapas mensuales;
YY = SE para etapas semanales) del sistema XX. El programa solamente lee estas informaciones
si se indicó que la configuración es dinámica (registro 8 del archivo SDDP.DAT). Este archivo
contiene 3 tipos de registro:
3.8.1  Registro tipo 1
Identifica la central con límites en el vertimiento máximo:

|     | Campo  Columna  | Tipo  Descripción                 |
| --- | --------------- | --------------------------------- |
|     | 1  1-12         | A4  Debe contener "**** Planta:"  |
|     | 1  14-17        | I4  Código de la central          |
37

SDDP MANUAL DE ARCHIVOS
|     | 2  19-30  | A12  Nombre de la central  |                 |      |
| --- | --------- | -------------------------- | --------------- | ---- |
|     | 3  41-50  | F10.0  Penalización        | por  violación  | del  |
vertimiento máximo
= -1, el cálculo es automático
> 0, valor en k$/hm3 de la penali-
dad
3.8.2  Registro tipo 2
Header para las etapas.

| Campo  | Columna  | Tipo  Descripción                                |     |     |
| ------ | -------- | ------------------------------------------------ | --- | --- |
| 1      | 1-4      | A4  Este campo debe contener la palabra "A~NO".  |     |     |
3.8.3  Registro tipo 3
Contiene los límites en el vertimiento máximo por etapa. Cada registro está asociado a un año
y cada columna a una etapa. Sólo es necesario llenar los campos donde existe una alteración
de los límites.

| Campo  | Columna  | Tipo  Descripción                                 |     |     |
| ------ | -------- | ------------------------------------------------- | --- | --- |
| 1      | 1-4      | I4  Año                                           |     |     |
| 2      | 5-12     | A8  Límite en el vertimiento máximo (m3/s) de la  |     |     |
etapa 1
| 3   | 13-20  | A8  Límite en el vertimiento máximo (m3/s) de la  |     |     |
| --- | ------ | ------------------------------------------------- | --- | --- |
etapa 2
| etc.  | etc.  | etc.  etc.  |     |     |
| ----- | ----- | ----------- | --- | --- |
Observaciones:
•  un campo vacío indica que no hay variación del vertimiento máximo con respecto a la
etapa anterior.
•  Se coloca un registro tipo 3 por cada año del estudio.
•  El conjunto de registros 1, 2 y 3 se repiten para cada central con límites en el vertimiento
máximo.
3.9  Vertimiento mínimo
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
MNSPYYXX.DAT contiene los límites en el vertimiento mínimo (YY = ME para etapas mensuales; YY
= SE para etapas semanales) del sistema XX. El programa solamente lee estas informaciones si
se indicó que la configuración es dinámica (registro 8 del archivo SDDP.DAT). Este archivo con-
tiene 3 tipos de registro:
38

SDDP MANUAL DE ARCHIVOS
3.9.1  Registro tipo 1
Identifica la central con límites en el vertimiento mínimo:

|     | Campo  Columna  | Tipo  Descripción                 |                 |      |
| --- | --------------- | --------------------------------- | --------------- | ---- |
|     | 1  1-12         | A4  Debe contener "**** Planta:"  |                 |      |
|     | 2  14-17        | I4  Código de la central          |                 |      |
|     | 3  19-30        | A12  Nombre de la central         |                 |      |
|     | 4  41-50        | F10.0  Penalización               | por  violación  | del  |
vertimiento mínimo
= -1, el cálculo es automático
> 0, valor en k$/hm3 de la penali-
dad
3.9.2  Registro tipo 2
Header para las etapas.

| Campo  | Columna  | Tipo  Descripción                                |     |     |
| ------ | -------- | ------------------------------------------------ | --- | --- |
| 1      | 1-4      | A4  Este campo debe contener la palabra "A~NO".  |     |     |
3.9.3  Registro tipo 3
Contiene los límites en el vertimiento mínimo por etapa. Cada registro está asociado a un año
y cada columna a una etapa. Sólo es necesario llenar los campos donde existe una alteración
de los límites.

| Campo  | Columna  | Tipo  Descripción                                 |     |     |
| ------ | -------- | ------------------------------------------------- | --- | --- |
| 1      | 1-4      | I4  Año                                           |     |     |
| 2      | 5-12     | A8  Límite en el vertimiento mínimo (m3/s) de la  |     |     |
etapa 1
Límite en el vertimiento mínimo (m3/s) de la
| 3   | 13-20  | A8  |     |     |
| --- | ------ | --- | --- | --- |
etapa 2
| etc.  | etc.  | etc.  etc.  |     |     |
| ----- | ----- | ----------- | --- | --- |
Observaciones:
•  Un campo vacío indica que no hay variación del vertimiento mínimo con respecto a la
etapa anterior.
•  Se coloca un registro tipo 3 por cada año del estudio.
•  El conjunto de registros 1, 2 y 3 se repiten para cada central con límites en el vertimiento
mínimo.
39

SDDP MANUAL DE ARCHIVOS
3.10  Volúmenes de alerta
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
VALEYYXX.DAT contiene los volúmenes de alerta por etapa (YY = ME para etapas mensuales; YY
= SE para etapas semanales). El programa solamente lee estas informaciones si se indicó que
la configuración es dinámica (registro 8 del archivo SDDP.DAT). Este archivo contiene 3 tipos
de registro:
3.10.1 Registro tipo 1
Este registro identifica una central que tiene volúmenes de alerta:

| Campo  | Columna  | Tipo  Descripción                           |
| ------ | -------- | ------------------------------------------- |
| 1      | 14-17    | I4  Código de la central                    |
| 2      | 19-30    | A12  Nombre de la central                   |
| 3      | 41-50    | F10.0  Penalización por violación del volu- |
men de alerta
= -1, el cálculo es automático
> 0, valor en k$/hm3 de la penalidad
3.10.2 Registro tipo 2
Es un header que se coloca a continuación del registro tipo 1.
3.10.3 Registro tipo 3
Contiene los volúmenes de alerta por etapa. Cada registro está asociado a un año y cada co-
lumna a una etapa. Sólo es necesario llenar los campos donde existe una alteración del volu-
men de alerta.

| Campo  | Columna  | Tipo  Descripción                          |
| ------ | -------- | ------------------------------------------ |
| 1      | 1-4      | I4  Año                                    |
| 2      | 5-12     | A8  Volumen de alerta (hm3) de la etapa 1  |
| 3      | 13-20    | A8  Volumen de alerta (hm3) de la etapa 2  |
| etc.   | etc.     | etc.  etc.                                 |
Observaciones:
•  Un campo vacío indica que no hay variación del volumen de alerta con respecto a la etapa
anterior.
•  Se coloca un registro tipo 3 por cada año del estudio.
•  El conjunto de registros 1, 2 y 3 se repiten para cada central con volumen de alerta.
40

SDDP MANUAL DE ARCHIVOS
3.11  Volúmenes máximos operativos
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
VMXOYYXX.DAT contiene los volúmenes máximos operativos por etapa (YY = ME para etapas
mensuales; YY = SE para etapas semanales). El programa solamente lee estas informaciones si
se indicó que la configuración es dinámica (registro 8 del archivo SDDP.DAT). Este archivo con-
tiene 3 tipos de registro:
3.11.1 Registro tipo 1
Este registro identifica una central que tiene volúmenes de seguridad:

| Campo  | Columna  | Tipo  Descripción          |
| ------ | -------- | -------------------------- |
| 1      | 14-17    | I4  Código de la central   |
| 2      | 19-30    | A12  Nombre de la central  |
3  41-50  F10.0  Penalización por violación del volumen de vo-
lumen máximo operativo
= -1, el cálculo es automático
> 0, valor en k$/hm3 de la penalización
3.11.2 Registro tipo 2
Es un header que se coloca a continuación del registro tipo 1.
3.11.3 Registro tipo 3
Contiene los volúmenes máximos operativos por etapa. Cada registro está asociado a un año
y cada columna a una etapa. Sólo necesario llenar los campos donde existe una alteración del
volumen máximo operativo.

| Campo  | Columna  | Tipo  Descripción                               |
| ------ | -------- | ----------------------------------------------- |
| 1      | 1-4      | I4  Año                                         |
| 2      | 5-12     | A8  Volumen máximo operativo (hm3) de la etapa  |
1
| 3   | 13-20  | A8  Volumen máximo operativo (hm3) de la etapa  |
| --- | ------ | ----------------------------------------------- |
2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que no hay variación del volumen de volumen máximo operativo
con respecto a la etapa anterior.
•  Se coloca un registro tipo 3 por cada año del estudio.
41

SDDP MANUAL DE ARCHIVOS
•  Los registros 1, 2 y 3 se repiten para cada central con volumen máximo operativo.
3.12  Volúmenes de seguridad
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
VMINYYXX.DAT contiene los volúmenes de seguridad por etapa (YY = ME para etapas mensuales;
YY = SE para etapas semanales). El programa solamente lee estas informaciones si se indicó
que la configuración es dinámica (registro 8 del archivo SDDP.DAT). Este archivo contiene 3
tipos de registro:
3.12.1 Registro tipo 1
Este registro identifica una central que tiene volúmenes de seguridad:

| Campo  | Columna  | Tipo  Descripción          |
| ------ | -------- | -------------------------- |
| 1      | 14-17    | I4  Código de la central   |
| 2      | 19-30    | A12  Nombre de la central  |
3  41-50  F10.0  Penalización por violación del volumen de se-
guridad
= -1, el cálculo es automático
> 0, valor en k$/hm3 de la penalización
3.12.2 Registro tipo 2
Es un header que se coloca a continuación del registro tipo 1.
3.12.3 Registro tipo 3
Contiene los volúmenes de seguridad por etapa. Cada registro está asociado a un año y cada
columna a una etapa. Sólo necesario llenar los campos donde existe una alteración del volu-
men de seguridad.

| Campo  | Columna  | Tipo  Descripción                             |
| ------ | -------- | --------------------------------------------- |
| 1      | 1-4      | I4  Año                                       |
| 2      | 5-12     | A8  Volumen de seguridad (hm3) de la etapa 1  |
Volumen de seguridad (hm3) de la etapa 2
| 3     | 13-20  | A8          |
| ----- | ------ | ----------- |
| etc.  | etc.   | etc.  etc.  |
Observaciones:
•  Un campo vacío indica que no hay variación del volumen de seguridad con respecto a la
etapa anterior.
•  Se coloca un registro tipo 3 por cada año del estudio.
42

SDDP MANUAL DE ARCHIVOS
•  Los registros 1, 2 y 3 se repiten para cada central con volumen de seguridad.
3.13  Volúmenes de espera
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
VESPYYXX.DAT contiene los volúmenes de espera por etapa (YY = ME para etapas mensuales; YY =
SE para etapas semanales). El programa solamente lee estas informaciones si se indicó que la
configuración es dinámica (registro 8 del archivo SDDP.DAT). Este archivo contiene 3 tipos de
registro:
3.13.1 Registro tipo 1
Este registro identifica una central que tiene volúmenes de espera:

|     | Campo  | Columna  Tipo  Descripción        |
| --- | ------ | --------------------------------- |
|     | 1      | 14-17  I4  Código de la central   |
|     | 2      | 19-30  A12  Nombre de la central  |
3.13.2 Registro tipo 2
Es un header que se coloca a continuación del registro tipo 1.
3.13.3 Registro tipo 3
Contiene los volúmenes de espera por etapa. Cada registro está asociado a un año y cada
columna a una etapa. Sólo es necesario llenar los campos donde existe una alteración del
volumen de espera.

| Campo  | Columna  | Tipo  Descripción                          |
| ------ | -------- | ------------------------------------------ |
| 1      | 1-4      | I4  Año                                    |
| 2      | 5-12     | A8  Volumen de espera (hm3) de la etapa 1  |
| 3      | 13-20    | A8  Volumen de espera (hm3) de la etapa 2  |
| etc.   | etc.     | etc.  etc.                                 |
Observaciones:
•  Un campo vacío indica que no hay variación del volumen de espera con respecto a la etapa
anterior.
•  Se coloca un registro tipo 3 por cada año del estudio.
•  El conjunto de registros 1, 2 y 3 se repiten para cada central con volumen de espera.
43

SDDP MANUAL DE ARCHIVOS
3.14  Datos adicionales
Cada archivo denominado POLHIDXX.DAT en formato ASCII, localizado en el directorio de datos
del estudio, contiene la información de los coeficientes del polinomio cota-volumen para las
plantas del sistema XX con esta representación. Este archivo contiene 2 tipos de registros:
3.14.1 Registro tipo 1
Es un header que contiene la palabra " NUM" en las primeras 4 columnas.
3.14.2 Registro tipo 2
Este registro contiene los datos de entrada para el cálculo del factor de producción en función
del polinomio cota-volumen para cada planta hidráulica del sistema XX. Los siguientes campos
son definidos:

| Campo  | Columna  | Tipo  Descripción                                  |
| ------ | -------- | -------------------------------------------------- |
| 1      | 1-4      | I4  Número de la central.                          |
| 2      | 6-17     | A12  Nombre de la central.                         |
| 3      | 19-21    | A3  Es definido igual a PCV e indica que es un Po- |
linomio Cota-Volumen. Este campo es igno-
rado en la versión corriente del programa.
| 4   | 23-34  | F12.0  Productibilidad específica                |
| --- | ------ | ------------------------------------------------ |
| 5   | 36-47  | F12.0  Pérdidas hidráulicas                      |
| 6   | 49     | I1  Unidad asociada a las pérdidas hidráulicas:  |
=1 en %;
=2 en metros.
| 7   | 51-62  | E12.0  Coeficiente del término independiente del  |
| --- | ------ | ------------------------------------------------- |
PCV
| 8   | 64-75  | E12.0  Coeficiente del término lineal del PCV      |
| --- | ------ | -------------------------------------------------- |
| 9   | 77-88  | E12.0  Coeficiente del término cuadrático del PCV  |
10  90-101  E12.0  Coeficiente del término de la tercera poten-
cia del PCV
11  103-114  E12.0  Coeficiente del término de la cuarta potencia
del PCV
Se coloca un registro tipo 2 para cada planta del sistema.
3.15  Volumen muerto
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado VOLMORXX.DAT contiene el cronograma para llenar el volumen muerto de los embalses
para el sistema identificado por XX.
44

SDDP MANUAL DE ARCHIVOS
3.15.1 Registro tipo 1
Es un comentario (header).
3.15.2 Registro tipo 2
Contiene la etapa de inicio, la duración prevista y el estado operativo inicial para completar el
volumen muerto.

| Campo  | Columna  | Tipo  Descripción                                 |
| ------ | -------- | ------------------------------------------------- |
| 1      | 1-4      | I4  Número de la central.                         |
| 2      | 6-17     | A12  Nombre de la central.                        |
| 3      | 19-20    | I2  Día de inicio                                 |
| 4      | 22-23    | I2  Etapa (semana/mês) de inicio                  |
| 5      | 25-28    | I4  Año de inicio                                 |
| 6      | 30-33    | I4  Duración, en etapas, del período para comple- |
tar el volumen muerto
7  35-41  F7.0  Condición del embalse en la etapa inicial. Dada
en volumen (p.u. del volumen muerto).
3.16  Curva de aversión al riesgo
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo, deno-
minado CARIYYXX.DAT contiene los datos de la curva de aversión al riesgo por etapa (XX = iden-
tificador del sistema, YY = ME para etapas mensuales e YY = SE para etapas semanales). Sola-
mente será necesario especificar las curvas de aversión al riesgo para los sistemas de interés.
El programa solamente le estas informaciones si fue indicado que la configuración es dinámica
(registro 8 del archivo SDDP.DAT). Este archivo contiene los siguientes 3 tipos de registros:
3.16.1 Registro tipo 1
Este registro identifica el sistema con curva de aversión al riesgo:

| Campo  | Columna  | Tipo  Descripción         |
| ------ | -------- | ------------------------- |
| 1      | 14-17    | I4  Código del sistema    |
| 2      | 19-30    | A12  Nombre del sistema   |
3  41-50  F10.0  Penalización por violación de la curva de aversión al
riesgo
= -1, el cálculo es automático
> 0, valor en k$/MWh de la penalidad
45

SDDP MANUAL DE ARCHIVOS
3.16.2 Registro tipo 2
Es un header que es colocado en seguida del registro tipo 1.
3.16.3 Registro tipo 3
Contiene la curva de aversión al riesgo por etapa. Cada registro está asociado a un año y cada
columna a una etapa. Sólo es necesario completar los campos donde existe una alteración de
la curva de aversión al riesgo.
Campo Columna Tipo Descripción
1 1-4 I4 Año
2 5-12 F8.0 Curva de aversión al riesgo (%) de la etapa 1
3 13-20 F8.0 Curva de aversión al riesgo (%) de la etapa 2
Etc. etc. etc. etc.
Observaciones:
• El porcentaje es aplicado a la energía almacenada máxima del sistema.
• Un campo vacío indica que no hay variación de la curva de aversión al riesgo en relación
a la etapa anterior.
• Se coloca un registro tipo 3 para cada año del estudio.
3.17 Cálculo energía almacenada
El usuario tiene la e posibilidad de determinar el factor de utilización del volumen útil de una
planta para el cálculo de la energía almacenada, energía almacenable máxima y energía
afluente. El archivo de datos en formato ASCII, ENAPRN.DAT, debe encontrarse en el directorio
de estudio. Los siguientes tipos de registros deben ser especificados:
3.17.1 Registro tipo 1
El primer registro contiene la opción para cálculo de las energías, en el siguiente formato.
Campo Columna Tipo Descripción
1 1-4 A4 Palabra clave:
CENA
46

SDDP MANUAL DE ARCHIVOS
2 6-9 I4 Opción que indica la manera de calcular la energía
almacenada, la energía almacenable máxima y la
energía afluente por sistema.
= 0: Opción padrón del SDDP. En el caso de la ener-
gía almacenada, esta opción indica que cada em-
balse contribuye para el sistema al cual pertenece
con la energía resultante del producto de su volu-
men útil y la suma de los factores de producción
de todas las centrales aguas abajo, independien-
temente del sistema al cual ellas pertenecen. Ra-
zonamiento similar se aplica a la energía almace-
nable máxima y a la energía afluente.
= 1: En el caso de la energía almacenada, esta op-
ción indica que cada central contribuye para el sis-
tema al cual pertenece con la energía resultante
del producto de su factor de producción y la suma
de los volúmenes útiles de todos los embalses
aguas arriba, independientemente del sistema al
cual ellos pertenecen. Razonamiento similar se
aplica a la energía almacenable máxima y a la
energía afluente.
Obs. La principal diferencia entre estas opciones
corresponde al hecho de que, en la primera, es
contabilizada la contribución de los embalses y, en
la segunda, la contribución de las turbinas/gene-
radores. En el caso de todas las centrales de la cas-
cada pertenezcan a un mismo sistema, estas de
los maneras son equivalentes.
3.17.2 Registro tipo 2
El segundo registro indica que será especificado a seguir un subconjunto de plantas
Hidroeléctricas, que pueden tener un factor de utilización del volumen útil diferente de uno,
para cálculo de la energía almacenada, energía almacenable máxima y energía afluente.
Campo Columna Tipo Descripción
1 1-4 A4 Palabra clave:
NUSI
3.17.3 Registro tipo 3
El tercer registro contiene el factor de utilización del volumen útil para el cálculo de la energía
almacenada, energía almacenable máxima y energía afluente, en el siguiente formato.
47

SDDP MANUAL DE ARCHIVOS
Campo Columna Tipo Descripción
1 1-4 I4 Número de la planta hidroeléctrica
2 6-7 I2 Número del sistema al cual la planta
pertenece
3 11-15 F5.0 Factor de participación (p.u) del volu-
men útil de la planta en el sistema s1
4 17-18 I2 Número del sistema s1
5 20-24 F5.0 Factor de participación (p.u) del volu-
men útil de la planta en el sistema s2
6 26-27 I2 Número del sistema s2
7 29-33 F5.0 Factor de participación (p.u) del volu-
men útil de la planta en el sistema s3
8 35-36 I2 Número del sistema s3
9 38-42 F5.0 Factor de participación (p.u) del volu-
men útil de la planta en el sistema s4
10 44-45 I2 Número del sistema s4
11 47-51 F5.0 Factor de participación (p.u) del volu-
men útil de la planta en el sistema s5
12 53-54 I2 Número del sistema s5
3.18 Configuración de conjuntos de embalses
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. El archivo, denomi-
nado CSETRESV.DAT, contiene el registro de todos los conjuntos de embalses. Este archivo con-
tiene los siguientes 2 tipos de registros:
3.18.1 Registro tipo 1
Es un header que describe los elementos del registro tipo 2.
3.18.2 Registro tipo 2
Este registro define un nuevo conjunto de embalses o incluye una central a un conjunto ya
existente. A él corresponden los siguientes datos:
Campo Columna Tipo Descripción
1 1-4 I4 Número identificador del conjunto de embalses
2 6-17 A12 Nombre del conjunto de embalses
Identificador del sistema al cual está asociado la
3 19-20 I2
central
4 22-25 I4 Número identificador de la central
5 27-38 A12 Nombre de la central
48

SDDP MANUAL DE ARCHIVOS
3.19  Energía de alerta
Archivo ASCII ubicado en el directorio de datos del estudio, denominado ENEALEYY.DAT conte-
niendo las energías de alerta por etapa (YY = ME para etapas mensuales; YY = SE para etapas
semanales). El programa solamente lee estas informaciones se fue indicado que la configura-
ción es dinámica (registro 8 del archivo SDDP.DAT). Este archivo contiene 3 tipos de registros:
3.19.1 Registro tipo 1
Este registro identifica un conjunto de embalses que tienen energía de alerta:

| Campo  | Columna  | Tipo  Descripción                         |
| ------ | -------- | ----------------------------------------- |
| 1      | 14-17    | I4  Número identificador del conjunto de  |
embalses
| 2   | 19-30  | A12  Nombre del conjunto de embalses          |
| --- | ------ | --------------------------------------------- |
| 3   | 41-50  | F10.0  Penalización por violación da energía  |
de alerta
= -1, o cálculo é automático
> 0, valor en k$/MWh de la penalidad
3.19.2 Registro tipo 2
Es un header que es colocado enseguida del registro tipo 1.
3.19.3 Registro tipo 3
Contiene las energías de alerta por etapa. Cada registro está asociado a un año y cada columna
a una etapa. Es necesario rellenar todos los campos da tabla.

| Campo  | Columna  | Tipo  Descripción                          |
| ------ | -------- | ------------------------------------------ |
| 1      | 1-4      | I4  Ano                                    |
| 2      | 5-12     | A8  Energía de alerta (GWh) de la etapa 1  |
| 3      | 13-20    | A8  Energía de alerta (GWh) de la etapa 2  |
| etc.   | etc.     | etc.  etc.                                 |
Observaciones:
•  Se coloca un registro tipo 3 para cada año del estudio.
•  El conjunto de registros 1, 2 e 3 se repite para cada conjunto de embalses con energía de
alerta.
49

SDDP MANUAL DE ARCHIVOS
3.20  Energía de seguridad
Archivo ASCII localizado en el directorio de datos del estudio denominado ENEMINYY00.DAT con-
teniendo las energías mínimas de seguridad por etapa (YY = ME para etapas mensuales; YY = SE
para etapas semanales). El programa solamente lee estas informaciones si fue indicado que la
configuración es dinámica (registro 8 del archivo SDDP.DAT). Este archivo contiene 3 tipos de
registros:
3.20.1 Registro tipo 1
Este registro identifica un conjunto de embalses que tiene energía de seguridad:

| Campo  | Columna  | Tipo  Descripción                                  |     |     |     |     |
| ------ | -------- | -------------------------------------------------- | --- | --- | --- | --- |
| 1      | 14-17    | I4  Número identificador del conjunto de embalses  |     |     |     |     |
| 2      | 19-30    | A12  Nombre del conjunto de embalses               |     |     |     |     |
3  41-50  F10.0  Penalización por violación da energía mínima de
seguridad
= -1, el cálculo es automático
> 0, valor en k$/MWh de la penalización
3.20.2 Registro tipo 2
Es un header que es colocado enseguida del registro tipo 1.
3.20.3 Registro tipo 3
Contiene las energías de seguridad por etapa. Cada registro está asociado a un año y cada
columna a una etapa. Es necesario rellenar todos los campos de la tabla.

| Campo  | Columna  | Tipo  Descripción  |         |                |        |         |
| ------ | -------- | ------------------ | ------- | -------------- | ------ | ------- |
| 1      | 1-4      | I4  Ano            |         |                |        |         |
| 2      | 5-12     | A8  Energía        | mínima  | de  seguridad  | (GWh)  | de  la  |
etapa 1
| 3   | 13-20  | A8  Energía  | mínima  | de  seguridad  | (GWh)  | de  la  |
| --- | ------ | ------------ | ------- | -------------- | ------ | ------- |
etapa 2
| etc.  | etc.  | etc.  etc.  |     |     |     |     |
| ----- | ----- | ----------- | --- | --- | --- | --- |
Observaciones:
•  Se coloca un registro tipo 3 para cada año del estudio.
•  Los registros 1, 2 e 3 se repiten para cada conjunto de embalses con energía mínima de
seguridad.
50

SDDP MANUAL DE ARCHIVOS
3.21  Energía de espera
Archivo ASCII ubicado en el directorio de datos del estudio, denominado ENEESPYY.DAT conte-
niendo las energías de espera por etapa (YY = ME para etapas mensuales; YY = SE para etapas
semanales). El programa solamente lee estas informaciones si fue indicado que la configura-
ción es dinámica (registro 8 del archivo SDDP.DAT). Este archivo contiene 3 tipos de registros:
3.21.1 Registro tipo 1
Este registro identifica un conjunto de embalses que tiene energía de espera:

|     | Campo  | Columna  Tipo  Descripción           |
| --- | ------ | ------------------------------------ |
|     | 1      | 14-17  I4  Número identificador del  |
conjunto de embalses
|     | 2   | 19-30  A12  Nombre del conjunto de  |
| --- | --- | ----------------------------------- |
embalses
3.21.2 Registro tipo 2
Es un header que es colocado enseguida del registro tipo 1.
3.21.3 Registro tipo 3
Contiene las energías de espera por etapa. Cada registro está asociado a un año y cada co-
lumna a una etapa. Es necesario rellenar todos los campos da tabla.

| Campo  | Columna  | Tipo  Descripción                          |
| ------ | -------- | ------------------------------------------ |
| 1      | 1-4      | I4  Ano                                    |
| 2      | 5-12     | A8  Energía de espera (GWh) de la etapa 1  |
| 3      | 13-20    | A8  Energía de espera (GWh) de la etapa 2  |
| etc.   | etc.     | etc.  etc.                                 |
Observaciones:
•  Se coloca un registro tipo 3 para cada año del estudio.
•  El conjunto de registros 1, 2 e 3 se repite para cada conjunto de embalses con energía de
espera.

51

SDDP MANUAL DE ARCHIVOS
3.22 Tabla caudal turbinable x rendimiento del grupo turbina/generador
Archivo ASCII ubicado en el directorio de datos del estudio, denominado HEFFXX.DAT conteniendo
las tablas caudal turbinable x rendimiento del grupo turbina/generador para las plantas hidro-
eléctricas del sistema XX con esa representación. Este archivo posee formato CSV y contiene
5 tipos de registros:
3.22.1 Registro tipo 1
Indica la versión del archivo. En la versión actual se debe rellenar "$ version = 1".
3.22.2 Registro tipo 2
Es un header que es colocado enseguida del registro tipo 3.
3.22.3 Registro tipo 3
Contiene los identificadores de la central hidroeléctrica y número de puntos de la tabla
Columna Tipo Descripción
1 Entero Número de la central hidroeléctrica
2 String Nombre de la central hidroeléctrica
3 Entero Número de puntos de la tabla.
3.22.4 Registro tipo 4
Es un header que es colocado enseguida del registro tipo 5.
3.22.5 Registro tipo 5
Contiene los valores de la tabla
Columna Tipo Descripción
1 Real Valores del caudal turbinable en m³/s.
2 Real Valores del rendimiento del grupo turbina/gene-
rador en pu.
Observaciones:
• Los registros 2, 3, 4 y 5 se repiten para cada planta con tabla caudal turbinable x rendi-
miento del grupo turbina/generador.
52

SDDP MANUAL DE ARCHIVOS
3.23 Restricciones operativas
Conjunto de archivos ASCII denominados OPECHDXX.DAT (donde XX es el identificador del sis-
tema definido en el campo 3 del registro del archivo SISTEM.DAT). Contienen las restricciones
operativas cronológicas de las centrales hidroeléctricas, utilizadas en ejecuciones horarias. Las
restricciones representadas son: tiempo de viaje del agua turbinada/vertida, rampa de
subida/bajada de defluencia y rampa de subida/bajada.
El primer registro indica la versión del archivo. En este punto, debe venir con el texto "$versión
1". El segundo registro es un header. Los restantes tienen formato CSV (delimitado por co-
mas):
Columna Tipo Descripción
1 Entero Código de la central hidroeléctrica
2 String Nombre de la central hidroeléctrica
3 Real Tiempo de viaje del agua turbinada (h)
4 Real Tiempo de viaje del agua vertida (h)
5 Real Rampa de subida de defluencia (m3/s/min)
6 Real Rampa de bajada de defluencia (m3/s/min)
7 Real Rampa de subida (MW/min)
8 Real Rampa de bajada (MW/min)
53

SDDP MANUAL DE ARCHIVOS
4  CENTRALES TERMOELÉCTRICAS
Los datos de centrales termoeléctricas incluyen:
•  configuración termoeléctrica
•  modificación de la configuración
•  mantenimiento
•  precios de los combustibles
•  tasa de consumo de combustible
•  disponibilidad de combustible por etapa
4.1  Configuración termoeléctrica
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
CTERMIXX.DAT contiene los datos de la configuración termoeléctrica del sistema XX.
El archivo tiene dos tipos de registro:
4.1.1  Registro tipo 1
| Campo  | Columna   | Tipo  Descripción             |
| ------ | --------- | ----------------------------- |
|        | 1  1-8    | A8  Palabra clave: $version   |
|        | 2  10-13  | I4  Número de la versión      |
Registros que comienzan con el carácter “!” se consideran comentarios y son ignorados
4.1.2  Registro tipo 2
4.1.2.1  Datos generales y costos operativos

| Campo  | Columna  | Tipo  Descripción                   |
| ------ | -------- | ----------------------------------- |
| 1      | 1-4      | I4  Número de la central térmica.   |
| 2      | 6-17     | A12  Nombre de la central térmica.  |
| 3      | 19-22    | I4  Número de unidades.             |
| 4      | 24-27    | I4  Tipo de central:                |
0 = Existente;
1 = Futura.
| 5   | 29-35  | F7.0  Potencia instalada (MW).  |
| --- | ------ | ------------------------------- |
| 6   | 37-43  | F7.0  Generación mínima (MW).   |
| 7   | 45-51  | F7.0  Generación máxima (MW).   |
8  53-59  F7.0  Factor de indisponibilidad de corto plazo ICP (%).
9  61-67  F7.0  Factor de indisponibilidad histórica IH (%).
| 10  | 69-75  | F7.0  Costo variable de O&M ($/MWh)  |
| --- | ------ | ------------------------------------ |
54

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                  |     |     |     |
| ------ | -------- | ---------------------------------- | --- | --- | --- |
| 11     | 77-80    | I4  Indicador de tipo de central:  |     |     |     |
0 = central estándar
1 = central "must run": se considera una generación
obligatoria igual a la generación máxima aplicados los
|     |     | factores  | de  disponibilidad  | (forzada  | y  programada).  |
| --- | --- | --------- | ------------------- | --------- | ---------------- |
Obs: en el caso de una central "must run" el campo 6
(generación mínima) tiene que ser 0.
2 = central "beneficio": se considera que la generación
es negativa, esto es, la generación de este tipo de cen-
tral equivale a un aumento en la demanda; el costo
operativo también es negativo y representa, por lo
tanto, un ingreso para el sistema. Este tipo de central
se utiliza para representar exportaciones de energía y
beneficios.
4.1.2.2  Combustibles

| Campo  | Columna  | Tipo  Descripción           |     |     |     |
| ------ | -------- | --------------------------- | --- | --- | --- |
| 12     | 82-85    | I4  Número de combustible.  |     |     |     |
13  87-93  F7.0  Segmento 1 de la curva de consumo específico(%)
| 14  | 95-101  | F7.0  Consumo específico 1 (unidades/MWh)  |     |     |     |
| --- | ------- | ------------------------------------------ | --- | --- | --- |
15  103-109  F7.0  Segmento 2 de la curva de consumo específico(%)
| 16  | 111-117  | F7.0  Consumo específico 2 (unidades/MWh)  |     |     |     |
| --- | -------- | ------------------------------------------ | --- | --- | --- |
17  119-125  F7.0  Segmento 3 de la curva de consumo específico(%)
| 18  | 127-133  | F7.0  Consumo específico 3 (unidades/MWh)  |     |     |     |
| --- | -------- | ------------------------------------------ | --- | --- | --- |
4.1.2.3  Combustibles alternativos

| Campo  | Columna  | Tipo  Descripción                        |     |     |     |
| ------ | -------- | ---------------------------------------- | --- | --- | --- |
| 19     | 135-138  | I4  Número de combustibles alternativos  |     |     |     |
20  140-143  I4  Número externo de la térmica ficticia que representa
el combustible alternativo 1
21  145-148  I4  Número externo de la térmica ficticia que representa
el combustible alternativo 2
22  150-153  I4  Número externo de la térmica ficticia que representa
el combustible alternativo 3
4.1.2.4  Otros datos

55

SDDP MANUAL DE ARCHIVOS
Campo Columna Tipo Descripción
23 155-158 I4 Indicador de térmica tipo commitment.
= 1 indica que existe una variable de decisión 0-1 aso-
ciada a esta central térmica para cada etapa
= 2 indica que existe una variable de decisión 0-1 aso-
ciada a esta central térmica para cada bloque
24 160-166 F7.0 Costo de transporte del combustible ($/unidades)
25 168-174 F7.0 Costo de Arranque para térmica tipo commitment (k$)
26 176-179 I4 Indicador de sorteo de fallas
4.1.2.5 Representación de restricciones de disponibilidad y transporte de gas
Campo Columna Tipo Descripción
27 181-184 I4 Puntero para el sistema de gas donde pertenece esta
central térmica. Para las unidades térmicas que están
asociadas a un nodo de la red de gas, el consumo es-
pecífico debe ser informado en kUV/MWh (miles de
unidades volumétricas por MWh). Ver ítem 10.
4.1.2.6 Térmicas ciclo combinado
Campo Columna Tipo Descripción
28 186-189 I4 Número de la central térmica ciclo combinado
29 191-202 A12 Nombre de la central térmica ciclo combinado
4.1.2.7 Coeficiente de emisión
Campo Columna Tipo Descripción
30 204-209 F6.0 Coeficiente de emisión de CO2 (p.u.). Si es igual a 1,
significa que la central térmica emite todo el CO pro-
2
veniente de la quema del combustible. Valores entre 0
y 1, indican que existe un filtro que reduce la emisión
de CO2. Por ejemplo 0.8 indica que la central térmica
emite solamente 80% del C02 proveniente de la quema
de combustible.
Observaciones:
• La suma de los segmentos 1, 2 y 3 (campos 13, 15 y 17) debe ser 100.
• El costo de la generación térmica para cada segmento es definido como:
Costo= Precio del combustible (US$/unidad) × Consumo específico (unidad/MWh)
56

SDDP MANUAL DE ARCHIVOS
+ Costo del transporte ($/unid) × Consumo específico (unidad/MWh)
+ Costo variable no combustible (US$/MWh)
• Las térmicas multi-combustible se representan de la siguiente manera:
• Debe indicarse un registro para la central térmica indicando el combustible prin-
cipal en el campo 12, el número de combustibles alternativos en el campo 19 y
para cada combustible alternativo, el número externo de la térmica ficticia que
representa la generación con el combustible alternativo. Estos números externos
deben ser indicados en los campos 20 a 22.
• Para los registros correspondientes a las térmicas ficticias todos los campos son
ignorados excepto los campos correspondientes al número de combustible y a la
curva de consumo específico.
• El programa decide etapa a etapa si es económico arrancar térmicas tipo commitment. En
el caso de decidir arrancar la térmica el costo es:
c (k$/MWh) × g (MWh) + Costo de Arranque (k$)
• Las térmicas ciclo combinado se representan de la siguiente manera
• Cada estado operativo o configuración se representa como una térmica.
• Estas térmicas están todas asociadas a una central térmica Ciclo Combinado a través
de los campos 28 y 29.
• Existe un solo estado operativo o configuración activa en cada etapa. Se asume que el
primer estado operativo informado es el estado en operación. La definición de cual el
estado en operación a cada etapa del estudio se define en el archivo de Datos crono-
lógicos de estados operativos de centrales térmicas ciclo combinado (ccstZZXX.dat).
Ver 4.9.
4.2 Modificación de la configuración térmica
Conjuntos de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo lla-
mado MTERMIXX.DAT contiene modificaciones a la configuración térmica inicial del sistema XX.
El programa sólo lee estas informaciones si se indicó que la configuración es dinámica (registro
8 del archivo SDDP.DAT).
Este archivo contiene 4 tipos de registro:
4.2.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-8 A8 Palabra clave: $version
2 10-13 I4 Número de la versión
Registros que comienzan con el carácter “!” se consideran comentarios y son ignorados
57

SDDP MANUAL DE ARCHIVOS
4.2.2 Registro tipo 2
Este registro identifica la etapa (día/mes/año) de la modificación.
Campo Columna Tipo Descripción
1 1-4 A Debe contener la palabra "MOD:".
2 6-7 I2 día de la modificación.
3 9-10 I2 Número del mes
4 12-15 I4 Año
4.2.3 Registro tipo 3
Es un header igual al de los archivos CTERMIXX.DAT. Contiene la palabra " NUM" en las 4 prime-
ras columnas.
4.2.4 Registro tipo 4
Contiene los datos de la central a ser modificada en la etapa indicada en el registro tipo 1. El
formato de este registro es idéntico al formato del registro de los archivos CTERMIXX.DAT. Sin
embargo, los únicos campos reconocidos por el programa son:
Campo Columna Tipo Descripción
1 1-4 I4 Número de la central térmica.
2 6-17 A12 Nombre de la central térmica.
3 19-22 I4 Número de unidades.
4 37-43 F7.0 Generación mínima (MW).
5 45-51 F7.0 Generación máxima (MW).
6 53-59 F7.0 Factor de disponibilidad teif (%).
7 61-67 F7.0 Factor de indisponibilidad programada ip (%).
8 69-75 F7.0 Costo variable de O&M ($/MWh)
9 160-166 F7.0 Costo de transporte del combustible ($/unida-
des)
10 204-209 F6.0 Coeficiente de emisión de CO2 (p.u.)
Observaciones:
• Se coloca un registro tipo 3 por cada central modificada en esa etapa.
4.3 Consumo específico por bloco
Archivo ASCII denominado MCESPYYYXX.DAT localizado en el directorio de datos del sistema.
Este archivo contiene las modificaciones de los factores de consumo por bloque de las térmi-
cas del sistema XX para un estudio de YYY bloques. Este archivo está organizado de la siguiente
manera:
58

SDDP MANUAL DE ARCHIVOS
4.3.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-8 A8 Palabra clave: $version
2 10-13 I4 Número de la versión
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
4.3.2 Registro tipo 2
Campo Columna Tipo Descripción
1 1-10 Fecha Fecha dd/mm/yyyy
2 12-16 I5 Código del agente
3 18-29 A12 Nombre del agente
4 31-40 A10 Atributo a ser modificado
5 42-46 I5 Identificador del bloque (* = todos los bloques)
6 48-57 F10.0 Valor
En este caso los atributos que pueden ser modificados son:
• – Consumo específico para o segmento 1 (UC/MWh)
CESPS1
• – Consumo específico para o segmento 2 (UC/MWh)
CESPS2
• – Consumo específico para o segmento 3 (UC/MWh)
CESPS3
4.4 Mantenimiento de las termoeléctricas
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
PMTRZZXX.DAT contiene el programa de mantenimiento (semanal si ZZ = "SE" o mensual si ZZ =
"ME") del sistema XX (definido en el campo 3 del registro del archivo SISTEM.DAT).
El formato de este archivo es idéntico al de los archivos de mantenimiento de las hidroeléctri-
cas.
4.5 Configuración de combustible
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado CCOMBUXX.DAT contiene los datos de combustible para el sistema XX.
El primer registro es un comentario. Los demás tienen el siguiente formato:
4.5.1 Registro tipo 1
Este registro identifica los datos generales de combustible.
Campo Columna Tipo Descripción
1 1-4 I4 Número del combustible
59

SDDP MANUAL DE ARCHIVOS
| 2   | 6-17   | A12  Nombre del combustible                       |     |     |     |
| --- | ------ | ------------------------------------------------- | --- | --- | --- |
| 3   | 19-25  | A7  Nombre de la Unidad de Combustible (por ejem- |     |     |     |
plo, galón, m3, kg, etc.)
| 4   | 27-34  | F8.0  Costo del combustible ($/unidad)  |              |          |              |
| --- | ------ | --------------------------------------- | ------------ | -------- | ------------ |
| 5   | 36-41  | F6.0  Factor                            | de  emisión  | de  CO2  | por  unidad  |
(tCO2/unid.)
4.6  Precios de combustible
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado COMBYYXX.DAT contiene los precios de combustible por etapa (YY = ME para etapas
mensuales; YY = SE para etapas semanales) del sistema XX.
Este archivo contiene 3 tipos de registros:
4.6.1  Registro tipo 1
Este registro identifica el combustible con variación de precio:

|     | Campo  | Columna  Tipo  | Descripción             |     |     |
| --- | ------ | -------------- | ----------------------- | --- | --- |
|     | 1      | 14-17  I4      | Número del combustible  |     |     |
|     | 2      | 19-30  A12     | Nombre del combustible  |     |     |
4.6.2  Registro tipo 2
Es un header que es colocado en seguida del registro tipo 1.
4.6.3  Registro tipo 3
Contiene los datos de precio de combustible por etapa. Cada registro está asociado a un año
y cada columna a una etapa. Sólo es necesario rellenar los campos donde existe una alteración
del precio del combustible.

| Campo  | Columna  | Tipo  Descripción                                  |     |     |     |
| ------ | -------- | -------------------------------------------------- | --- | --- | --- |
| 1      | 1-4      | I4  Año                                            |     |     |     |
| 2      | 5-12     | A8  Precio del combustible ($/unidad) de la etapa  |     |     |     |
1
| 3   | 13-20  | A8  Precio del combustible ($/unidad) de la etapa  |     |     |     |
| --- | ------ | -------------------------------------------------- | --- | --- | --- |
2
| etc.  | etc.  | etc.  etc.  |     |     |     |
| ----- | ----- | ----------- | --- | --- | --- |
Observaciones:
60

SDDP MANUAL DE ARCHIVOS
•  Un campo vacío indica que no hay variación de precio del combustible en relación a la
etapa anterior.
•  Se coloca un registro tipo 3 para cada año del estudio.
•  El conjunto de registros 1, 2 e 3 se repite para cada combustible con variación de precio a
lo largo del período de estudio.
4.7  Tasa de consumo de combustible
Conjunto de archivos ASCII en el directorio de datos del sistema (ver registro 2 del archivo
PATH.DAT). El nombre de cada archivo es FURAYYXX.DAT, donde:
| YY  | duración de la etapa (= ME, mensual; = SE, semanal)   |     |
| --- | ----------------------------------------------------- | --- |
| XX  | número del sistema (campo 3 del archivo SISTEM.DAT).  |     |
El archivo contiene tres tipos de registro:
4.7.1  Registro tipo 1
Identifica el combustible con disponibilidad limitada.

| Campo  | Columna  | Tipo  Descripción           |
| ------ | -------- | --------------------------- |
| 1      | 14-17    | I4  número del combustible  |
4.7.2  Registro tipo 2
Este registro es un header que viene después del registro 1.
4.7.3  Registro tipo 3
Hay un registro tipo 3 para cada año del periodo de estudio. Cada registro contiene las tasas
máximas de utilización del combustible (unidades/hora) para cada etapa del año. Solamente
se informan los valores que cambian de una etapa para la siguiente.

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 1      | 1-4      | I4  Año            |
2  5-12  A8  Tasa máxima de utilización (unid./hora) en la etapa 1
3  13-20  A8  Tasa máxima de utilización (unid./hora) en la etapa 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
4.8  Disponibilidad de combustible
Conjunto de archivos ASCII en el directorio de datos del sistema (ver registro 2 del archivo
PATH.DAT). El nombre de cada archivo es FUELYYXX.DAT, donde:
61

SDDP MANUAL DE ARCHIVOS
YY duración de la etapa (= ME, mensual; = SE, semanal)
XX número del sistema (campo 3 del archivo SISTEM.DAT).
El archivo contiene tres tipos de registro:
4.8.1 Registro tipo 1
Identifica el combustible con disponibilidad limitada.
Campo Columna Tipo Descripción
1 14-17 I4 número del combustible
4.8.2 Registro tipo 2
Este registro es un header que viene después del registro 1.
4.8.3 Registro tipo 3
Hay un registro tipo 3 para cada año del periodo de estudio. Cada registro contiene el total de
combustible disponible para cada etapa (miles de unidades) del año. Solamente se informan
los valores que cambian de una etapa para la siguiente.
Campo Columna Tipo Descripción
1 1-4 I4 Año
2 5-12 A8 Combustible disponible en la etapa 1 (miles de unid.)
3 13-20 A8 Combustible disponible en la etapa 2 (miles de unid.)
etc. etc. etc. etc.
4.9 Generación mínima operativa
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo lla-
mado GMZZYYXX.DAT contiene restricciones de generación mínima operativa por etapa y por
bloque (donde ZZ=ME para etapas mensuales y ZZ=SE para etapas semanales; YY es el número
de bloques; XX es el identificador del sistema definido en el campo 3 del registro del archivo
SISTEM.DAT) por central. El programa solamente lee estas informaciones si se indicó que la
configuración es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 3 tipos de registro:
4.9.1 Registro tipo 1
Este registro identifica a central.
62

SDDP MANUAL DE ARCHIVOS
Campo Columna Tipo Descripción
1 1-12 A12 Header: contiene "**** Planta:"
2 14-17 I4 Número de la central
4.9.2 Registro tipo 2
Es un header a continuación del registro tipo 1.
4.9.3 Registro tipo 3
Contiene los datos de las generaciones mínimas por etapa para cada año y bloque de de-
manda. Cada registro está asociado a un año y a un bloque y cada columna a una etapa. Solo
es necesario llenar los campos donde la generación mínima se alteró con respecto a la etapa
anterior.
Campo Columna Tipo Descripción
1 1-4 I4 Año
2 5-8 I4 Bloque
3 9-16 F8.0 Generación mínima en el mes o semana 1
(MW).
4 17-24 F8.0 Generación mínima en el mes o semana 2
(MW).
etc. etc. etc. etc.
Observaciones:
• si la central especificada es del tipo "must run" (ver campo 11 del archivo CTERMIXX.DAT),
la generación mínima se interpreta como una generación obligatoria
• un campo vacío indica que no hay cambios con respecto al campo antecedente
• Se coloca un registro tipo 3 para cada año y bloque del estudio
• Los registros 1, 2 y 3 se informan para cada central con generación mínima
4.10 Costo de arranque variables para centrales commitment
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo lla-
mado CAZZYYXX.DAT contiene los costos de arranque variables par las centrales commitment (ZZ
= ME para etapas mensuales; ZZ = SE para etapas semanales y YY indica el número de bloques)
del sistema XX. El programa solamente lee estas informaciones si se indicó que la configuración
es dinámica (registro 8 del archivo SDDP.DAT). Si este archivo no existe entonces, entonces se
asume el costo de arranque indicado en el archivo de configuración térmica CTERMIXX.DAT para
todas las etapas y bloques del estudio.
Este archivo contiene 3 tipos de registro:
63

SDDP MANUAL DE ARCHIVOS
4.10.1 Registro tipo 1
Este registro identifica la central térmica commitment.

| Campo  | Columna  | Tipo  Descripción                            |
| ------ | -------- | -------------------------------------------- |
| 1      | 1-12     | A12  Palabra clave: Contiene "**** Planta:"  |
| 2      | 14-17    | I4  Número de la central                     |
| 3      | 19-30    | A12  Nombre de la central                    |
4.10.2 Registro tipo 2
Es un header a continuación del registro tipo 1. Es ignorado por el programa.
4.10.3 Registro tipo 3
Contiene los datos de los costos de arranque variables por etapa y por. Cada registro está
asociado a un año y a un bloque y cada columna a una etapa (mes o semana). Solo es necesario
llenar los campos donde el costo de arranque alteró con respecto a la etapa anterior.

| Campo  | Columna  | Tipo  Descripción                                 |
| ------ | -------- | ------------------------------------------------- |
| 1      | 1-4      | I4  Año                                           |
| 2      | 5-8      | i4  Bloque de demanda                             |
| 3      | 9-16     | A8  Costo de arranque para la primera etapa (mes  |
o semana) en k$
| 4   | 17-24  | A8  Costo de arranque para la primera etapa (mes  |
| --- | ------ | ------------------------------------------------- |
o semana) en k$
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  un campo vacío indica que no hay cambios con respecto al campo antecedente
•  Se coloca un registro tipo 3 para cada año y bloque del estudio
4.11  Estado operativo de térmicas ciclo combinado
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo lla-
mado CCSTZZXX.DAT contiene la información del estado operativo de centrales térmicas ciclo
combinado por etapa (donde ZZ=ME para etapas mensuales y ZZ=SE para etapas semanales;
XX es el identificador del sistema definido en el campo 3 del registro del archivo SISTEM.DAT)
de un conjunto de centrales. El programa solamente lee estas informaciones si se indicó que
la configuración es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 3 tipos de registro:
64

SDDP MANUAL DE ARCHIVOS
4.11.1 Registro tipo 1
Este registro identifica la central ciclo combinado.
Campo Columna Tipo Descripción
1 1-12 A12 Header: contiene "**** Planta:"
2 14-17 I4 Número de la central térmica ciclo combinado
como definido en el campo 40 del archivo CTER-
MIXX.DAT.
3 19-30 A12 Nombre de la central térmica ciclo combinado
como definido en el campo 41 del archivo CTER-
MIXX.DAT.
4.11.2 Registro tipo 2
Es un header a continuación del registro tipo 1.
4.11.3 Registro tipo 3
Estos datos cronológicos contienen para cada etapa (mes o semana) de cada año, el número
externo de la central térmica (como definido en el campo 1 del archivo CTERMIXX.DAT) que
corresponde al estado operativo de la central térmica ciclo combinado.
Campo Columna Tipo Descripción
1 1-4 I4 Año
2 9-16 F8.0 Número del estado operativo de la central tér-
mica ciclo combinado para la primera etapa
(mes o semana) del año
4 17-24 F8.0 Número del estado operativo de la central tér-
mica ciclo combinado para la segunda etapa
(mes o semana) del año.
etc. etc. etc. etc.
Observaciones:
• un campo vacío indica que no hay cambios con respecto al campo antecedente
• Se coloca un registro tipo 3 para cada año del estudio
• Los registros 1, 2 y 3 se informan para cada central térmica ciclo combinado
4.12 Costos de adquisición de créditos de emisión
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado CEMIYYXX.DAT contiene los valores de costos de adquisición de crédito de emisión por
65

SDDP MANUAL DE ARCHIVOS
etapa (YY = ME para etapas mensuales; YY = SE para etapas semanales) para el sistema XX. El
programa solamente lee estas informaciones si fue indicado que la configuración es dinámica
(registro 8 del archivo SDDP.DAT). Este archivo contiene 3 tipos de registros:
4.12.1 Registro tipo 1
Este registro identifica el tipo de emisión.

| Campo  | Columna  | Tipo  Descripción          |
| ------ | -------- | -------------------------- |
| 1      | 14-17    | I4  Número de la emisión   |
= 1
| 2   | 19-30  | A12  Código de la emisión  |
| --- | ------ | -------------------------- |
= CO2
4.12.2 Registro tipo 2
Es un header que es colocado enseguida del registro tipo 1.
4.12.3 Registro tipo 3
Contiene los costos de adquisición de créditos por tipo de emisión. Cada registro está asociado
a un año y cada columna a una etapa.

| Campo  | Columna  | Tipo  Descripción                                |
| ------ | -------- | ------------------------------------------------ |
| 1      | 1-4      | I4  Ano                                          |
| 2      | 5-12     | A8  Costo de adquisición de créditos de emisión  |
($/ton CO2) de la etapa 1
| 3   | 13-20  | A8  Costo de adquisición de créditos de emisión  |
| --- | ------ | ------------------------------------------------ |
($/ton CO2) de la etapa 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que no hay variación de costo de adquisición de crédito de emisión
en relación a la etapa anterior.
•  Se coloca un registro tipo 3 para cada año del estudio.
4.13  Datos de configuración de contrato de combustible
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado FUECNTXX.DAT contiene los datos de contrato de combustibles para el sistema XX.
El primer registro es un comentario. Los demás tienen el siguiente formato:
66

SDDP MANUAL DE ARCHIVOS
4.13.1 Registro tipo 1
Este registro identifica los datos de configuración de los contratos de combustible.
Campo Columna Tipo Descripción
1 1-4 I4 Número del contrato de combustible
2 6-17 A12 Nombre del contrato de combustible
3 19-22 I4 Número del combustible asociado
4 24-31 F8.0 Costo adicional del contrato en $/unidad de com-
bustible
5 33-36 I4 Tipo:
0: Spot
1: Take or pay
6 38-47 A10 Etapa inicial especificada como dd-mm-yyyy
7 49-58 A10 Etapa final especificada como dd-mm-yyyy
8 60-63 I4 Número de repeticiones del contrato
9 65-71 F8.0 Límite mínimo del contrato, en 1000 unidades de
combustible
10 74-81 F8.0 Límite máximo del contrato, en 1000 unidades de
combustible
11 83-90 F8.0 Condición inicial del contrato p.u. Este valor co-
rresponde al montante consumido
12 92-99 F8.0 Límite de disponibilidad de combustible, en unida-
des de combustible/hora
13 101-108 F8.0 Cantidad mínima contratada y no utilizada que
puede ser transferida para la próxima renovación
del contrato, en 1000 unidades de combustible
14 110-117 F8.0 Costo take or pay del contrato en $/unidad de
combustible
4.14 Datos de configuración de reservorio de combustible
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado CFUEREXX.DAT contiene los datos de los reservorios de combustible para el sistema XX.
El primer registro es un comentario. Los demás tienen el siguiente formato:
4.14.1 Registro tipo 1
Este registro identifica los datos de configuración del reservorio de combustible.
Campo Columna Tipo Descripción
1 1-4 I4 Número del reservorio de combustible
67

SDDP MANUAL DE ARCHIVOS
| 2   | 6-17   | A12  Nombre del reservorio de combustible        |
| --- | ------ | ------------------------------------------------ |
| 3   | 19-22  | I4  Número del combustible asociado              |
| 4   | 24-31  | F8.0  Volumen máximo de almacenamiento, en 1000  |
unidades de combustible. Valor default = 0.
5  33-40  F8.0  Volumen inicial de almacenamiento, en p.u. Va-
lor default = 0.
6  42-49  F8.0  Límite máximo de inyección en el reservorio, en
unidades de combustible/hora
7  51-58  F8.0  Límite máximo de retirada del reservorio, en uni-
dades de combustible/hora
4.15  Dados de modificación de reservorio de combustible
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado MFUEREXX.DAT contiene modificaciones de la configuración de reservorio de combus-
tible del sistema XX. El programa solamente lee estas informaciones se fue indicado que la
configuración es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 3 tipos de registros:
4.15.1 Registro tipo 1
Este registro identifica la etapa (día/mes/año) de la modificación.

| Campo  | Columna  | Tipo  Descripción                    |
| ------ | -------- | ------------------------------------ |
| 1      | 1-4      | A  Debe contener la palabra "MOD:".  |
| 2      | 6-7      | I2  Día de la modificación.          |
| 3      | 9-10     | I2  Número del mes                   |
| 4      | 12-15    | I4  Año                              |
4.15.2 Registro tipo 2
Es un header que contiene la palabra " NUM" en las 4 primeras columnas.
4.15.3 Registro tipo 3
Contiene los datos del reservorio de combustible a ser modificados en la etapa indicada en el
registro tipo 1. E formato de este registro es idéntico al formato del registro de los archivos
CFUEREXX.DAT. Los únicos campos reconocidos por el programa son:

| Campo  | Columna  | Tipo  Descripción                          |
| ------ | -------- | ------------------------------------------ |
| 1      | 1-4      | I4  Número del reservorio de combustible   |
| 2      | 6-17     | A12  Nombre del reservorio de combustible  |
68

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| ...    | ...      | ...  ...           |
4  24-31  F8.0  Volumen máximo de almacenamiento, en 1000 unida-
des de combustible. Valor default = 0.
Observaciones:
Se coloca un registro tipo 3 para cada dato de reservorio de combustible modificado en esa
etapa.
4.16  Relación contrato de combustible x térmica
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado FCTERMXX.DAT contiene la relación entre plantas térmicas y contratos de combustibles
para el sistema XX.
El primer registro es un comentario. Los demás tienen el siguiente formato:
4.16.1 Registro tipo 2
Este registro identifica los grupos de térmicas por contrato de combustible.

| Campo  | Columna  | Tipo  Descripción                       |
| ------ | -------- | --------------------------------------- |
| 1      | 1-4      | I4  Número del contrato de combustible  |
| 2      | 6-9      | I4  Número de la planta térmica         |
4.17  Relación contrato x reservorio de combustible
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado FCFRESXX.DAT contiene la relación entre reservorios y contratos de combustibles para
el sistema XX.
El primer registro es un comentario. Los demás tienen el siguiente formato:
4.17.1 Registro tipo 2
Este registro identifica los grupos de embales por contrato de combustible.

| Campo  | Columna  | Tipo  Descripción                         |
| ------ | -------- | ----------------------------------------- |
| 1      | 1-4      | I4  Número del contrato de combustible    |
| 2      | 6-9      | I4  Número del reservorio de combustible  |
69

SDDP MANUAL DE ARCHIVOS
4.18  Relación reservorio de combustible x térmica
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado FRTERMXX.DAT contiene la relación entre usinas térmicas y reservorios de combustible
para el sistema XX.
El primer registro es un comentario. Los demás tienen el siguiente formato:
4.18.1 Registro tipo 2
Este registro identifica los grupos de térmicas por reservorio de combustible.

| Campo  | Columna  | Tipo  Descripción                         |
| ------ | -------- | ----------------------------------------- |
| 1      | 1-4      | I4  Número del reservorio de combustible  |
| 2      | 6-9      | I4  Número de la planta térmica           |
4.19  Costos de contrato de combustible
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo deno-
minado FCCSYYXX.DAT contiene los datos de costo de contrato de combustible por etapa (YY =
ME para etapas mensuales; YY = SE para etapas semanales) del sistema XX.
Más específicamente estos datos tienen el siguiente formato.
1.1.1  Registro tipo 1
Este registro identifica el contrato de combustible con variación de costo:

| Campo  | Columna  | Tipo  Descripción                        |
| ------ | -------- | ---------------------------------------- |
| 1      | 14-17    | I4  Número del contrato de combustible   |
| 2      | 19-30    | A12  Nombre del contrato de combustible  |
4.19.1 Registro tipo 2
Es un header que es colocado enseguida del registro tipo 1.
4.19.2 Registro tipo 3
Contiene los datos de costo de contrato de combustible por etapa. Cada registro está asociado
a un año y cada columna a una etapa.

| Campo  | Columna  | Tipo  Descripción                                 |
| ------ | -------- | ------------------------------------------------- |
| 1      | 1-4      | I4  Año                                           |
| 2      | 5-12     | A8  Costo del contrato de combustible ($/unidad)  |
de la etapa 1
70

SDDP MANUAL DE ARCHIVOS
| 3   | 13-20  | A8  Costo del contrato de combustible ($/unidad)  |
| --- | ------ | ------------------------------------------------- |
de la etapa 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
4.20  Disponibilidad de contrato de combustible
Conjunto de archivos ASCII denominados CCZZYYXX.DAT (donde ZZ=ME para etapas mensuales
y ZZ= SE para etapas semanales; YY es el número de bloques; XX es el identificador del sistema
definido en el campo 3 del registro del archivo SISTEM.DAT). Contiene la disponibilidad (Mil
unidades de combustible) de los contratos de combustible para cada etapa y bloque del estu-
dio de mediano plazo. El programa solamente lee estas informaciones si fue indicado que la
configuración es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 2 tipos de registros:
4.20.1 Registro tipo 1
Este registro identifica o contrato de combustible.

| Campo  | Columna  | Tipo  Descripción                        |
| ------ | -------- | ---------------------------------------- |
| 1      | 14-17    | I4  Código del contrato de combustible   |
| 2      | 19-30    | A12  Nombre del contrato de combustible  |
4.20.2 Registro tipo 2
Contiene la disponibilidad para cada etapa. Se debe incluir un registro para cada año y para
cada bloque. Cada registro contiene los valores de disponibilidad de combustible para cada
mes o semana del estudio. Sólo es necesario llenar los campos donde existe una alteración de
dato en relación a la etapa anterior.

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 1      | 1-4      | I4  Año            |
| 2      | 5-8      | I4  Bloque         |
3  9-16  F8.0  Disponibilidad (unidades de combustible/hora)
en el mes o semana 1
4  17-24  F8.0  Disponibilidad (unidades de combustible/hora)
en el mes o semana 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que los datos son los mismos de la etapa anterior.
•  El conjunto de registros 1, 2 e 3 es informado para cada contrato de combustible con datos
de disponibilidad.
71

SDDP MANUAL DE ARCHIVOS
4.21  Límites de inyección de reservorio de combustible
Conjunto de archivos ASCII denominados RIZZYYXX.DAT (donde ZZ=ME para etapas mensuales y
ZZ= SE para etapas semanales; YY es el número de bloques; XX es el identificador del sistema
definido en el campo 3 del registro del archivo SISTEM.DAT). Contiene los límites de inyección
(Mil unidades de combustible) de los reservorios de combustible para cada etapa y bloque del
estudio de mediano plazo. El programa solamente lee estas informaciones se fue indicado que
la configuración es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 2 tipos de registros:
4.21.1 Registro tipo 1
Este registro identifica el reservorio de combustible.

| Campo  | Columna  | Tipo  Descripción                          |
| ------ | -------- | ------------------------------------------ |
| 1      | 14-17    | I4  Código del reservorio de combustible   |
| 2      | 19-30    | A12  Nombre del reservorio de combustible  |
4.21.2 Registro tipo 2
Contiene el límite de inyección en el reservorio de combustible para cada etapa. Se debe in-
cluir un registro para cada año y para cada bloque. Cada registro contiene los valores de límite
de inyección para cada mes o semana del estudio. Sólo es necesario llenar los campos donde
existe una alteración de dato en relación a la etapa anterior.

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 1      | 1-4      | I4  Año            |
| 2      | 5-8      | I4  Bloque         |
3  9-16  F8.0  Límite  de  inyección  (unidades  de  combusti-
ble/hora) en el mes o semana 1
4  17-24  F8.0  Límite  de  inyección  (unidades  de  combusti-
ble/hora) en el mes o semana 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que los datos son los mismos de la etapa anterior.
•  El conjunto de registros 1, 2 e 3 es informado para cada reservorio de combustible con
datos de límite de inyección.
72

SDDP MANUAL DE ARCHIVOS
4.22  Límites de retirada de reservorio de combustible
Conjunto de archivos ASCII denominados ROZZYYXX.DAT (donde ZZ=ME para etapas mensuales
y ZZ= SE para etapas semanales; YY es el número de bloques; XX es el identificador del sistema
definido en el campo 3 del registro del archivo SISTEM.DAT). Contiene los límites de retirada
(Mil unidades de combustible) de los reservorios de combustible para cada etapa y bloque del
estudio de mediano plazo. El programa solamente lee estas informaciones se fue indicado que
la configuración es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 2 tipos de registros:
4.22.1 Registro tipo 1
Este registro identifica el reservorio de combustible.

| Campo  | Columna  | Tipo  Descripción                          |
| ------ | -------- | ------------------------------------------ |
| 1      | 14-17    | I4  Código del reservorio de combustible   |
| 2      | 19-30    | A12  Nombre del reservorio de combustible  |
4.22.2 Registro tipo 2
Contiene el límite de retirada del reservorio de combustible para cada etapa. Se debe incluir
un registro para cada año y para cada bloque. Cada registro contiene los valores de límite de
retirada para cada mes o semana del estudio. Sólo es necesario llenar los campos donde existe
una alteración de dato en relación a la etapa anterior.

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 1      | 1-4      | I4  Año            |
| 2      | 5-8      | I4  Bloque         |
3  9-16  F8.0  Límite  de  retirada  (unidades  de  combusti-
ble/hora) en el mes o semana 1
4  17-24  F8.0  Límite  de  retirada  (unidades  de  combusti-
ble/hora) en el mes o semana 2
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que los datos son los mismos de la etapa anterior.
•  El conjunto de registros 1, 2 e 3 es informado para cada reservorio de combustible con
datos de límite de retirada.
73

SDDP MANUAL DE ARCHIVOS
4.23  Restricciones operativas
Conjunto de archivos ASCII denominados OPECTRXX.DAT (donde XX es el identificador del sis-
tema definido en el campo 3 del registro del archivo SISTEM.DAT). Contienen las restricciones
operativas cronológicas de las centrales térmicas, utilizadas en ejecuciones horarias. Las res-
tricciones representadas son: rampa de subida/bajada, mínimo uptime/downtime e número
máximo de arranques/paradas.
El primer registro indica la versión del archivo. En este punto, debe venir con el texto "$versión
1". El segundo registro es un header. Los restantes tienen formato CSV (delimitado por co-
mas):

| Columna  Tipo  Descripción               |     |     |     |
| ---------------------------------------- | --- | --- | --- |
| 1  Entero  Código de la central térmica  |     |     |     |
| 2  String  Nombre de la central térmica  |     |     |     |
| 3  Real  Rampa de subida (MW/min)        |     |     |     |
| 4  Real  Rampa de bajada (MW/min)        |     |     |     |
| 5  Real  Mínimo uptime (hora)            |     |     |     |
| 6  Real  Mínimo downtime (hora)          |     |     |     |
| 7  Entero  Número máximo de arranques    |     |     |     |
| 8  Entero  Número máximo de paradas      |     |     |     |
| 9  Real  Costo de parada (k$)            |     |     |     |
4.24  Datos de emisión
Archivo ASCII denominado CEMIGAS.DAT ubicado en el directorio de datos del estudio. Contiene
el registro básico de emisiones, como CO  SO , NO , PM, entre otras. Los registros de este
|     | 2 2 | x   |     |
| --- | --- | --- | --- |
archivo tienen formato CSV (delimitado por comas):

| Columna  Tipo  | Descripción            |     |     |
| -------------- | ---------------------- | --- | --- |
| 1  Entero      | Código de la emisión   |     |     |
| 2  String      | Nombre de la emisión:  |     |     |
Límite = 12 caracteres.
| 3  String  | Unidad de la emisión:  |     |     |
| ---------- | ---------------------- | --- | --- |
Límite = 7 caracteres.
| 4  Real  | Costo  por  | unidad  | de  emisión  |
| -------- | ----------- | ------- | ------------ |
($/unid)
74

SDDP MANUAL DE ARCHIVOS
4.25  Coeficientes de emisión térmica
Archivo ASCII denominado EMITER.DAT ubicado en el directorio de datos del estudio. Contiene
los coeficientes de emisión de las centrales térmicas para cada tipo de emisión. Los coeficien-
tes de emisión pueden variar con el tiempo. Los registros de este archivo tienen formato CSV
(delimitado por comas):

|     | Columna  | Tipo    | Descripción           |               |         |
| --- | -------- | ------- | --------------------- | ------------- | ------- |
|     | 1        | Entero  | Dia inicial           |               |         |
|     | 2        | Entero  | Mes inicial           |               |         |
|     | 3        | Entero  | Año inicial           |               |         |
|     | 4        | Entero  | Código de la emisión  |               |         |
|     | 5        | String  | Identificador         | del  sistema  | de  la  |
central térmica
Tamaño = 2 caracteres.
|     | 6   | Entero  | Código de la central térmica  |     |     |
| --- | --- | ------- | ----------------------------- | --- | --- |
|     | 7   | Real    | Coeficiente de emisión        |     |     |
(unid/MWh)
4.26  Costos cronológicos de emisión
Archivo ASCII denominado EMICOSZZ.DAT ubicado en el directorio de datos del estudio. Contiene
los costos de emisión semanales (se ZZ= "SE") o mensuales (se ZZ= "ZE"), por unidad. El archivo
contiene 3 tipos de registros.
4.26.1 Registro tipo 1
Identifica el tipo de emisión.

| Campo  | Columna  | Tipo  | Descripción                  |     |     |
| ------ | -------- | ----- | ---------------------------- | --- | --- |
| 1      | 1-12     | A4    | Palabra-clave: "**** Code:"  |     |     |
| 2      | 15-17    | I3    | Código de la emisión         |     |     |
| 3      | 19-30    | A12   | Nombre de la emisión         |     |     |
4.26.2 Registro tipo 2
Header de etapas.

| Campo  | Columna  | Tipo  | Descripción  |     |     |
| ------ | -------- | ----- | ------------ | --- | --- |
Palabra-clave: "A~NO".
| 1   | 1-4  | A4  |     |     |     |
| --- | ---- | --- | --- | --- | --- |
75

SDDP MANUAL DE ARCHIVOS
4.26.3 Registro tipo 3
Valores de costo de emisión cronológicos. Hay un registro tipo 3 para cada año del estudio.

| Campo  | Columna  | Tipo  Descripción                   |
| ------ | -------- | ----------------------------------- |
| 1      | 1-4      | I4  Año                             |
| 2      | 5-12     | F8.0  costo en la etapa 1 ($/unid)  |
| 3      | 13-20    | F8.0  costo en la etapa 2 ($/unid)  |
| 4      | 21-28    | F8.0  costo en la etapa 3 ($/unid)  |
| etc.   | etc.     | etc.  etc.                          |
4.27  Restricción de presupuesto de emisión
Archivo ASCII denominado REMISSAO.DAT ubicado en el directorio de datos del estudio. Contiene
los datos de restricción de presupuesto de emisión. Cada línea representa una restricción
distinta. Los registros de este archivo tienen formato CSV (delimitado por comas):

|     | Columna  | Tipo  Descripción                      |
| --- | -------- | -------------------------------------- |
|     | 1        | Entero  Código da la emisión           |
|     | 2        | Entero  Mes inicial de la restricción  |
|     | 3        | Entero  Año inicial de la restricción  |
|     | 4        | Entero  Mes final de la restricción    |
|     | 5        | Entero  Año final de la restricción    |
|     | 6        | Real  Presupuesto de emisión para el   |
período definido (unid)
|     | 7   | Real  Penalidad de violación de la res- |
| --- | --- | --------------------------------------- |
tricción ($/unid)

|     |     |     |
| --- | --- | --- |
76

SDDP MANUAL DE ARCHIVOS
5  RESTRICCIONES MIXTAS
5.1  Restricciones de generación
Conjunto de archivos ASCII en el directorio de datos del estudio. Cada archivo, llamado
RGZZYYXX.DAT, contiene los datos de las restricciones de generación por grupos de generadores
del sistema XX, donde XX es el identificador del sistema definido en el campo 3 del registro del
archivo de sistemas, SISTEM.DAT; YY es el número de bloques; ZZ=ME, para estudios mensuales
y ZZ=SE, para estudios semanales.
Este archivo contiene los siguientes registros
5.1.1  Registro tipo 1

| Campo  | Columna  | Tipo  Descripción   |
| ------ | -------- | ------------------- |
| 1      | 1-4      | A4  Contiene: ****  |
2  5-13  F9.0  Penalización por violación de la restricción de ge-
neración:
= -1, el cálculo es automático
> 0, valor en K$/MWh de la penalidad especifi-
cado por el usuario
| 3   | 14-17  | I4  Número de la restricción   |
| --- | ------ | ------------------------------ |
| 4   | 19-30  | A12  Nombre de la restricción  |
| 5   | 33     | A1  Tipo de restricción:       |
“>”: mayor o igual
“<”: menor o igual
| 6   | 36  | A1  Tipo del generador 1:  |
| --- | --- | -------------------------- |
“H”: hidroeléctrica
“T”: térmica
| 7   | 38-41  | I4  Número del generador 1   |
| --- | ------ | ---------------------------- |
| 8   | 43     | A1  Tipo del generador 2:    |
“H”: hidroeléctrica
“T”: térmica
| 9   | 45-48  | I4  Número del generador 2   |
| --- | ------ | ---------------------------- |
|     |        |   etc.                       |
Se pueden indicar hasta 20 generadores en cada restricción.
5.1.2  Registro tipo 2
Este registro es un header y es ignorado por el programa
77

SDDP MANUAL DE ARCHIVOS
5.1.3  Registro tipo 3
A continuación, se indican los valores de la restricción de generación para etapa (mes o se-
mana) y para año del estudio. Se pueden incluir datos anteriores o posteriores; éstos serán
ignorados por el modelo.

| Campo  | Columna  | Tipo  Descripción                        |
| ------ | -------- | ---------------------------------------- |
| 1      | 1-4      | I4  Año                                  |
| 2      | 5-8      | I4  Bloque                               |
| 3      | 9-16     | F8.0  Valor para el mes o semana 1 (MW)  |
| 4      | 17-24    | F8.0  Valor para el mes o semana 2 (MW)  |
| etc.   | etc.     | etc.  etc.                               |
Para cada restricción se debe incluir un registro tipo 1, un registro tipo 2 y tantos registros tipo
3 como sean necesarios.
5.2  Reserva primaria
Conjunto de archivos ASCII llamados RRZZYYXX.DAT (donde ZZ=ME para etapas mensuales y ZZ=
SE para etapas semanales; YY es el número de bloques; XX es el identificador del sistema defi-
nido en el campo 3 del registro del archivo SISTEM.DAT). Contienen la reserva de generación
(MW) que se substrae de la generación máxima de las centrales térmicas y hidro para cada
etapa y bloque del estudio de mediano plazo. El programa solamente lee estas informaciones
si se indicó que la configuración es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 5 tipos de registros:
5.2.1  Registro tipo 1
Identifica el tipo de reserva y es un registro fijo.

| Campo  | Columna  | Tipo  Descripción                         |
| ------ | -------- | ----------------------------------------- |
| 1      | 1-12     | A4  Contiene las palabras "Tipo Info. :"  |
| 2      | 17-17    | I1  Tipo de Mantenimiento (valor fijo)    |
=2 se informa el valor resultante después del
mantenimiento (Absoluto)
5.2.2  Registro tipo 2
Identifica las unidades de la restricción de reserva.

| Campo  | Columna  | Tipo  Descripción                       |
| ------ | -------- | --------------------------------------- |
| 1      | 1-12     | A4  contiene las palabras "Unidades :"  |
78

SDDP MANUAL DE ARCHIVOS
| 2   | 17-17  | I1  Tipo de unidad de la restricción de reserva:  |
| --- | ------ | ------------------------------------------------- |
= 2 %
= 3 MW
= 14 % de la Potencia disponible
Si la reserva se informa en %, se refiere al porcentaje de la potencia total. Si el usuario indica
que la reserva es en % de la potencia disponible, entonces se aplicará este porcentaje a: po-
tencia total − los MW en mantenimiento.
5.2.3  Registro tipo 3
Este registro identifica una central con reserva primaria.

|     | Campo  Columna  | Tipo  Descripción          |
| --- | --------------- | -------------------------- |
|     | 1  14-17        | I4  Código de la central   |
|     | 2  19-30        | A12  Nombre de la central  |
|     | 3  38-38        | A1  Tipo de la central:    |
h = hidroeléctrica;
t = térmica
5.2.4  Registro tipo 4
Es un header a continuación del registro 3.
5.2.5  Registro tipo 5
Contiene la reserva primaria para cada etapa. Se debe incluir un registro para cada año y para
bloque. Cada registro contiene los valores de reserva para cada mes o semana del estudio.
Solo es necesario llenar los campos donde existe una alteración del dato con respecto a la
etapa antecedente.

| Campo  | Columna  | Tipo  Descripción                                 |
| ------ | -------- | ------------------------------------------------- |
| 1      | 1-4      | I4  Año                                           |
| 2      | 5-8      | I4  Bloque                                        |
| 3      | 9-16     | F8.0  Reserva primaria (MW) en el mes o semana 1  |
| 4      | 17-24    | F8.0  Reserva primaria (MW) en el mes o semana 2  |
| etc.   | etc.     | etc.  etc.                                        |
Observaciones:
•  Un campo vacío indica que los datos son los mismos de la etapa anterior.
•  El conjunto de registros 3, 4 y 5 se informa para cada central con datos de reserva prima-
ria.
79

SDDP MANUAL DE ARCHIVOS
5.3 Configuración restricciones de reserva secundaria
Conjunto de archivos ASCII en el directorio de datos del estudio. Cada archivo, llamado RES-
GERXX.DAT, contiene los datos de las restricciones de reserva secundaria por grupos de gene-
radores del sistema XX, donde XX es el identificador del sistema definido en el campo 3 del
registro del archivo de sistemas, SISTEM.DAT.
Este archivo contiene los siguientes registros
5.3.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-4 header ignorado por el programa
2 5-8 I4 Número de la restricción
3 9-14 header ignorado por el programa
4 15-26 A12 Nombre de la restricción
5 28-28 I1 Tipo de dato de entrada de las restricciones tipo
1
0: factor constante de la demanda
1: datos cronológicos
6 41-50 F10.0 Penalización por violación de la restricción de re-
serva secundaria:
= -1, el cálculo es automático
> 0, valor en K$/MWh de la penalidad especifi-
cado por el usuario
5.3.2 Registro tipo 2
Campo Columna Tipo Descripción
1 1-14 header ignorado por el programa
2 15-19 I5 Restricción tipo 1: reserva como factor de la de-
manda
0: inactiva
1: activa
3 21-25 I5 Restricción tipo 2: reserva en función de los gene-
radores pertenecientes al sistema que no perte-
necen a la restricción
0: inactiva
1: activa
80

SDDP MANUAL DE ARCHIVOS
4 27-31 I5 Restricción tipo 3: reserva en función de los gene-
radores pertenecientes a la restricción
0: inactiva
1: activa
5.3.3 Registro tipo 3
Campo Columna Tipo Descripción
1 1-14 header ignorado por el programa
2 15-19 I5 Número de generadores participantes de la res-
tricción.
5.3.4 Registro tipo 4
A continuación se indica el conjunto de generadores participantes de la restricción de reserva
secundaria.
Campo Columna Tipo Descripción
1 1-3 I3 Contador
2 5-8 I4 Número del generador indicado en los datos
de configuración hidroeléctrica o térmica res-
pectivos.
3 10-10 A1 Tipo de generador:
“T”o “t”: indica generador térmico;
“H”o “h”: indica generador hidroeléctrico.
Para cada restricción se debe incluir un registro tipo 1, un registro tipo 2, un registro tipo 3,
un registro tipo 4 y tantos registros tipo 5 como número de generadores pertenecientes a la
restricción fue indicado.
5.4 Modificación restricciones de reserva secundaria
Conjunto de archivos ASCII llamados RSZZYYXX.DAT (donde ZZ=ME para etapas mensuales y ZZ=
SE para etapas semanales; YY es el número de bloques; XX es el identificador del sistema defi-
nido en el campo 3 del registro del archivo SISTEM.DAT). Contienen los valores de las reservas
para aquellas restricciones definidas como siendo del tipo 1, i.e, reserva como factor de la
demanda (en % o p.u) o como un valor fijo (MW) para cada etapa y bloque del estudio de
mediano plazo. El programa solamente lee estas informaciones si se indicó que la configura-
ción es dinámica (registro 8 del archivo SDDP.DAT).
Este archivo contiene 5 tipos de registro:
81

SDDP MANUAL DE ARCHIVOS
5.4.1  Registro tipo 1
Identifica el tipo de dato.

| Campo  | Columna  | Tipo  Descripción                        |
| ------ | -------- | ---------------------------------------- |
| 1      | 1-12     | A  Contiene las palabras "Tipo Info. :"  |
| 2      | 17-17    | I1  Tipo de dato (valor fijo)            |
=2 se informa el valor resultante después del
mantenimiento (Absoluto)
5.4.2  Registro tipo 2
Identifica la unidad de la reserva.

| Campo  | Columna  | Tipo  Descripción                    |
| ------ | -------- | ------------------------------------ |
| 1      | 1-12     | A  Contiene la palabra "Unidades :"  |
| 2      | 17-18    | I2  Tipo de unidad del dato:         |
= 2 %
= 3 MW
= 12 p.u.
5.4.3  Registro tipo 3
Este registro identifica una restricción de reserva secundaria.

Campo  Columna  Tipo  Descripción
1  1-4  A4  Contiene “****”
2  14-17  I4  Código de la restricción
3  19-30  A12  Nombre de la restricción
5.4.4  Registro tipo 4
Es un header a continuación del registro 3.
5.4.5  Registro tipo 5
Contiene la reserva secundaria para cada etapa. Se debe incluir un registro para cada año y
para bloque. Cada registro contiene los valores de reserva para cada mes o semana del estu-
dio. Sólo es necesario llenar los campos donde existe una alteración del dato con respecto a
la etapa antecedente.

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
| 1      | 1-4      | I4  Año            |
82

SDDP MANUAL DE ARCHIVOS
| 2   | 5-8   | I4  Bloque                                        |
| --- | ----- | ------------------------------------------------- |
| 3   | 9-16  | F8.0  Reserva secundaria (MW) en el mes o semana  |
1
| 4   | 17-24  | F8.0  Reserva secundaria (MW) en el mes o semana  |
| --- | ------ | ------------------------------------------------- |
2
| etc.  | Etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que los datos son los mismos de la etapa anterior.
•  El conjunto de registros 3, 4 y 5 se informa para cada restricción con datos de reserva
secundaria.
83

SDDP MANUAL DE ARCHIVOS
6  DATOS DE TRANSMISIÓN – MODELO DE INTERCAMBIOS
6.1  Configuración de intercambios
El archivo de datos de los intercambios INTERC.DAT (utilizado si no se representa la red de
transmisión detallada) contiene las siguientes informaciones:
6.1.1  Registro tipo 1
| Campo  | Columna  | Tipo  Descripción             |
| ------ | -------- | ----------------------------- |
| 1      | 1-8      | A8  Palabra clave: $version   |
| 2      | 10-13    | I4  Número de la versión      |
Registros que comienzan con el carácter “!” se consideran comentarios y son ignorados
6.1.2  Registro tipo 2
| Campo  | Columna  | Tipo  Descripción                                  |
| ------ | -------- | -------------------------------------------------- |
| 1      | 1-5      | I5  Código identificador del intercambio           |
| 2      | 7-18     | A12  Nombre del intercambio                        |
| 3      | 20-31    | A12  Nombre del sistema Origen                     |
| 4      | 33-44    | A12  Nombre del sistema Destino                    |
| 5      | 49       | A  Tipo: Existente (E o 0) / Futuro (F o 1)        |
| 6      | 56-58    | A3  Unidad monetaria; utilizada solamente si exis- |
ten costos de intercambio
| 7   | 60-69   | F10.0  Capacidad de intercambio From->To (MW)   |
| --- | ------- | ----------------------------------------------- |
| 8   | 71-80   | F10.0  Factor de pérdidas From->To (pu)         |
| 9   | 82-91   | F10.0  Capacidad de intercambio To ->From (MW)  |
| 10  | 93-102  | F10.0  Factor de pérdidas To ->From (pu)        |
6.2  Modificación de los intercambios
Archivo ASCII denominado MINTERCYYY.DAT localizado en el directorio de datos del sistema.
Este archivo contiene las modificaciones de los límites de las capacidades, costos y factores
de pérdidas de los intercambios para un estudio con YYY bloques. Este archivo está organizado
de la siguiente manera:
6.2.1  Registro tipo 1
| Campo  | Columna  | Tipo  Descripción             |
| ------ | -------- | ----------------------------- |
| 1      | 1-8      | A8  Palabra clave: $version   |
| 2      | 10-13    | I4  Número de la versión      |
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
84

SDDP MANUAL DE ARCHIVOS
6.2.2 Registro tipo 2
Campo Columna Tipo Descripción
1 1-10 Fecha Fecha dd/mm/yyyy
2 12-16 I5 Código del agente
3 18-29 A12 Nombre del agente
4 31-40 A10 Atributo a ser modificado
5 42-46 I5 Identificador del bloque (* = todos los bloques)
6 48-57 F10.0 Valor
En este caso los atributos que pueden ser modificados son:
• capacidad de intercambio sentido From -> To (MW)
CAPACFT–
• capacidad de intercambio sentido To -> From (MW)
CAPACTF–
• factor de pérdidas sentido From -> To (pu)
LOSSFT–
• factor de pérdidas sentido To -> From (pu)
LOSSTF–
• costo de intercambio sentido From -> To (UM/MWh)
CINTFT –
• costo de intercambio sentido To -> From (UM/MWh)
CINTTF –
6.3 Configuración de suma de intercambios
El archivo CSUMINT.DAT contiene los datos de las restricciones de suma de intercambios. Una
restricción de suma de se define como la combinación lineal (con coeficientes +1 o -1) de hasta
20 líneas de intercambio. Este archivo está organizado de la siguiente manera:
6.3.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-8 A8 Palabra clave: $version
2 10-13 I4 Número de la versión
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
6.3.2 Registro tipo 2
Campo Columna Tipo Descripción
1 1-5 I5 Código de la restricción de suma de intercam-
bios
2 7-18 A12 Nombre de la restricción de suma de intercam-
bios
3 20-29 F10.0 Límite inferior (se considera el mismo valor para
todos los bloques)
4 31-40 F10.0 Límite superior (se considera el mismo valor
para todos los bloques)
5 42-47 F6.0 Coeficiente 1
6 49-60 A12 Nombre del intercambio 1
85

SDDP MANUAL DE ARCHIVOS
| 7    | 62-67  F6.0  Coeficiente 2            |     |
| ---- | ------------------------------------- | --- |
| 8    | 69-80  A12  Nombre del intercambio 2  |     |
| ...  | ...  ...                              | …   |
7  422-427  F6.0  Coeficiente 20
8  429-440  A12  Nombre del intercambio 20
6.4  Modificación de restricciones de suma de intercambios
Archivo ASCII denominado MSUMINTYYY.DAT localizado en el directorio de datos el sistema.
Este archivo contiene las modificaciones de los límites de las restricciones de suma de inter-
cambios para un estudio con YYY bloques. Este archivo está organizado de la siguiente ma-
nera:
6.4.1  Registro tipo 1
Campo  Columna  Tipo  Descripción
| 1   | 1-8  A8  Palabra clave: $version   |     |
| --- | ---------------------------------- | --- |
| 2   | 10-13  I4  Número de la versión    |     |
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
6.4.2  Registro tipo 2
Campo  Columna  Tipo  Descripción
| 1   | 1-10  Fecha  Fecha dd/mm/yyyy          |     |
| --- | -------------------------------------- | --- |
| 2   | 12-16  I5  Código del agente           |     |
| 3   | 18-29  A12  Nombre del agente          |     |
| 4   | 31-40  A10  Atributo a ser modificado  |     |
5  42-46  I5  Identificador del bloque (* = todos los bloques)
| 6   | 48-57  F10.0  Valor  |     |
| --- | -------------------- | --- |
En este caso los atributos que pueden ser modificados son:
•   – límite superior de la restricción de suma de intercambios (MW)
UB
•   – límite inferior de la restricción de suma de intercambios (MW)
LB
6.5  Costos de intercambio
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo lla-
mado CINTZZYY.DAT contiene los costos de intercambio variables (ZZ = ME para etapas mensuales;
ZZ = SE para etapas semanales y YY indica el número de bloques). El programa solamente lee
estas informaciones si se indicó que la configuración es dinámica (registro 8 del archivo
SDDP.DAT). Si este archivo no existe entonces, entonces se asume que el costo de intercambio
es el indicado en el archivo de configuración INTERC.DAT para todas las etapas y bloques del
estudio.
86

SDDP MANUAL DE ARCHIVOS
Este archivo contiene 3 tipos de registro:
6.5.1  Registro tipo 1
Este registro identifica la línea de intercambio.

| Campo  | Columna  | Tipo  Descripción                            |
| ------ | -------- | -------------------------------------------- |
| 1      | 1-12     | A12  Palabra clave: Contiene "**** Planta:"  |
| 2      | 14-17    | I4  Número de la línea de intercambio        |
| 3      | 19-30    | A12  Nombre de la línea de intercambio       |
| 4      | 41-43    | A3  Palabra clave:                           |
“-->” indica el sentido DE→PARA
“<--” indica el sentido PARA→DE
6.5.2  Registro tipo 2
Es un header a continuación del registro tipo 1. Es ignorado por el programa.
6.5.3  Registro tipo 3
Contiene los datos de los costos de intercambio por etapa y por bloque. Cada registro está
asociado a un año y a un bloque y cada columna a una etapa (mes o semana). Solo es necesario
llenar los campos donde el costo de intercambio se alteró con respecto a la etapa anterior.

| Campo  | Columna  | Tipo  Descripción                               |
| ------ | -------- | ----------------------------------------------- |
| 1      | 1-4      | I4  Año                                         |
| 2      | 5-8      | i4  Bloque de demanda                           |
| 3      | 9-16     | A8  Costo de intercambio para la primera etapa  |
(mes o semana) en $/MWh
| 4   | 17-24  | A8  Costo de intercambio para la segunda etapa  |
| --- | ------ | ----------------------------------------------- |
(mes o semana) en $/MWh
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que no hay cambios con respecto al campo antecedente
•  Se coloca un registro tipo 3 para cada año y bloque del estudio
87

SDDP MANUAL DE ARCHIVOS
7  DATOS DE TRANSMISIÓN – MODELO DE FLUJO DE POTENCIA
Estos datos incluyen:
•  configuración de barras
•  modificación de las barras
•  configuración de circuitos
•  modificación de los circuitos
•  configuración de enlaces CC
•  modificación de los enlaces CC
•  configuración de áreas eléctricas
•  modificación de los límites de exportación e importación por área
•  límites de suma de flujo en circuitos
•  modificación de los límites de suma de flujo en circuitos
7.1  Configuración de barras
El archivo DBUS.DAT contiene los datos de barras del sistema. El primer registro es un comen-
tario. Los demás registros tienen el siguiente formato:

| Campo  | Columna  Formato  | Valores Válidos  | Descripción                         |
| ------ | ----------------- | ---------------- | ----------------------------------- |
| 1      | 1-5  I5           | 1 .. ZNEB(1)     | Número de la barra                  |
| 2      | 10-21  A12        | -                | Nombre de la barra                  |
| 3      | 23-24  A2         | -                | Identificador del sistema           |
| 4      | 25-27  I3         | ≥ 0              | Numero secuencial del generador co- |
nectado a la barra.
| 5   | 30-30  I1  | 1, 2  | Tipo de la central:  |
| --- | ---------- | ----- | -------------------- |
= 1 hidroeléctrica;
= 2 térmica.
| 6   | 32-35  I4  | ≥ 0  | Código de la central definido en el  |
| --- | ---------- | ---- | ------------------------------------ |
campo 1 del registro 2 de los archivos
CHIDROXX.DAT y CTERMIXX.DAT.
| 7   | 37-48  A12  | -   | Nombre de la central (Opcional)         |
| --- | ----------- | --- | --------------------------------------- |
| 8   | 50-53  I4   | >0  | Número del área eléctrica. Sólo se uti- |
liza si existen datos de restricciones de
exportación e importación por áreas
| 9   | 61-65  F5.0  | ≥ 0  | Demanda en la barra (MW) en el blo- |
| --- | ------------ | ---- | ----------------------------------- |
que 1.(2)
| 10  | 67-71  F5.0  | ≥ 0  | Demanda industrial en la barra en el  |
| --- | ------------ | ---- | ------------------------------------- |
bloque 1 (2)
| 11  | 73-77  F5.0  | ≥ 0  | Pérdidas fijas en el bloque 1 (MW)  |
| --- | ------------ | ---- | ----------------------------------- |
| 12  | 85-89  F5.0  | ≥ 0  | Demanda en la barra (MW) en el blo- |
que 2 (2)
88

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  Formato  | Valores Válidos  | Descripción                           |
| ------ | ----------------- | ---------------- | ------------------------------------- |
| 13     | 91-95  F5.0       | ≥ 0              | Demanda industrial en la barra en el  |
bloque 2 (2)
| 14  | 97-101  F5.0   | ≥ 0  | Pérdidas fijas en el bloque 2 (MW)  |
| --- | -------------- | ---- | ----------------------------------- |
| 15  | 109-113  F5.0  | ≥ 0  | Demanda en la barra (MW) en el blo- |
que 3 (2)
≥ 0
| 16  | 115-119  F5.0  |     | Demanda industrial en la barra en el  |
| --- | -------------- | --- | ------------------------------------- |
bloque 3 (2)
| 17  | 121-125  F5.0  | ≥ 0  | Pérdidas fijas en el bloque 3 (MW)  |
| --- | -------------- | ---- | ----------------------------------- |
| 18  | 133-137  F5.0  | ≥ 0  | Demanda en la barra (MW) en el blo- |
que 4 (2)
19  139-143  F5.0  ≥ 0  Demanda industrial en la barra en el
bloque 4 (2)
| 20  | 145-149  F5.0  | ≥ 0  | Pérdidas fijas en el bloque 4 (MW)  |
| --- | -------------- | ---- | ----------------------------------- |
| 21  | 157-161  F5.0  | ≥ 0  | Demanda en la barra (MW) en el blo- |
que 5 (2)
≥ 0
| 22  | 163-167  F5.0  |     | Demanda industrial en la barra en el  |
| --- | -------------- | --- | ------------------------------------- |
bloque 5 (2)
≥ 0
| 23  | 169-173  F5.0  |      | Pérdidas fijas en el bloque 5 (MW)     |
| --- | -------------- | ---- | -------------------------------------- |
| 24  | 175-178  I4    | 0,1  | Caso se utilice “Corte de carga en ba- |
rras seleccionadas” (ver Datos Gene-
rales y Opciones de Ejecución, archivo
SDDP.DAT), este campo indica:
= 1: barra seleccionada para corte de
carga;
= 0: caso contrario.
Si la opción “Corte de carga en barras
seleccionadas”  no  fue  seleccionada,
este campo es ignorado.
(1) ZNEB: parámetro del programa que indica el número máximo de la barra
(2) Estos datos solamente se utilizan para cálculo de los factores de participación de cada barra
de demanda en la demanda total
7.2  Modificación de los datos de barra
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo lla-
mado MBUS.DAT contiene las modificaciones de las demandas por barra. El programa sola-
mente utiliza estas informaciones si se indicó que la configuración es dinámica (registro 8 del
archivo SDDP.DAT).
Este archivo contiene 3 tipos de registro:
89

SDDP MANUAL DE ARCHIVOS
7.2.1  Registro tipo 1
Este registro identifica la etapa (día/mes/año) de la modificación.

| Campo  Columna  | Tipo  | Descripción                      |     |
| --------------- | ----- | -------------------------------- | --- |
| 1  1-4          | A     | Debe contener la palabra "MOD:"  |     |
| 2  6-7          | I2    | Día de la modificación           |     |
| 3  9-10         | I2    | Número del mes                   |     |
| 4  12-15        | I4    | Año                              |     |
7.2.2  Registro tipo 2
Es un header igual al del archivo DBUS.DAT. Contiene la palabra ".NUM" en las 4 primeras co-
lumnas.
7.2.3  Registro tipo 3
Contiene los datos de la barra a ser modificada en la etapa indicada en el registro tipo 1. El
formato de este registro es idéntico al formato del registro del archivo DBUS.DAT. Los campos
que se puede modificar son:

| Campo  Columna  | Formato  | Valores  Váli- | Descripción  |
| --------------- | -------- | -------------- | ------------ |
dos
| 3   61-65  | F5.0  | ≥ 0  | Dem.variable (MW) - bloque 1  |
| ---------- | ----- | ---- | ----------------------------- |
| 4   67-71  | F5.0  | ≥ 0  | Dem.industrial - bloque 1     |
| 5   85-89  | F5.0  | ≥ 0  | Dem.variable (MW) - bloque 2  |
| 6   91-95  | F5.0  | ≥ 0  | Dem.industrial - bloque 2     |
≥ 0
| 7   109-113   | F5.0  |      | Dem.variable (MW) - bloque 3  |
| ------------- | ----- | ---- | ----------------------------- |
| 8   115-119   | F5.0  | ≥ 0  | Dem.industrial - bloque 3     |
| 9   133-137   | F5.0  | ≥ 0  | Dem.variable (MW) - bloque 4  |
| 10   139-143  | F5.0  | ≥ 0  | Dem.industrial - bloque 4     |
| 11   157-161  | F5.0  | ≥ 0  | Dem.variable (MW) - bloque 5  |
| 12   163-167  | F5.0  | ≥ 0  | Dem.industrial - bloque 5     |
Se coloca un registro tipo 3 por cada barra modificada en la etapa.
7.3  Demanda por barra
El archivo DBFYYYXX.DAT contiene el registro de todas las demandas por barra para el sistema
XX, para un estudio con YYY bloques.

90

SDDP MANUAL DE ARCHIVOS
De modo a mantener compatibilidad con los datos de entrada de las versiones anteriores, las
informaciones de demanda por barra contenidas en los archivos DBUS.DAT e MBUS.DAT son
consideradas, caso el archivo DBFYYYXX.DAT no exista.
Este archivo está organizado de la siguiente manera:
7.3.1  Registro tipo 1
Es un header que describe los elementos del registro tipo 2.
7.3.2  Registro tipo 2
Este registro define una nueva demanda por barra, para un determinado bloque.

| Campo  Columna  | Tipo      | Descripción                         |     |     |     |
| --------------- | --------- | ----------------------------------- | --- | --- | --- |
| 1  1-5          | I5        | Número identificador de la barra    |     |     |     |
| 2  7-18         | A12       | Nombre de la barra                  |     |     |     |
| 3  20-23        | I4        | Número identificador de la demanda  |     |     |     |
| 4  25-34        | DD/MM/AAA | Fecha de creación/modificación      |     |     |     |
A
| 5  36-39  | I4    | Número identificador del bloque          |     |     |     |
| --------- | ----- | ---------------------------------------- | --- | --- | --- |
| 6  41-48  | F8.0  | Demanda en la barra relacionada a la de- |     |     |     |
manda y bloque indicados (MW)
7.4  Configuración de circuitos
El archivo DCIRC.DAT contiene los datos de circuitos del sistema. El primer registro indica la
versión del archivo, que debe ser $version=2. El segundo registro es un header. Los demás
registros tienen el siguiente formato:

| Campo  Columna  | Formato  | Valores  Vá- | Descripción  |     |     |
| --------------- | -------- | ------------ | ------------ | --- | --- |
lidos
| 1  1-5    | I5    | -    | Número de la barra de origen               |        |                      |
| --------- | ----- | ---- | ------------------------------------------ | ------ | -------------------- |
| 2  9-13   | I5    | -    | Número de la barra de destino              |        |                      |
| 3  18-23  | F6.0  | -    | Resistencia del circuito (en %)            |        |                      |
| 4  24-29  | F6.0  | ≠ 0  | Reactancia del circuito (en %)             |        |                      |
| 5  31-42  | A12   |      | Nombre del circuito. Si se deja en blanco  |        |                      |
|           |       |      | el  modelo                                 | asume  | el  nombre:  CIRCUI- |
Tnnnn, donde nnnn es el número externo
del circuito (campo 8)
6  59-64  F6.0  > 0  Límite de flujo - situación normal (MW)
| 7  65-68  | F4.0  | > 0  | Límite de flujo - emergencia (MW)  |     |     |
| --------- | ----- | ---- | ---------------------------------- | --- | --- |
| 8  70-74  | I5    | -    | Número del circuito                |     |     |
91

SDDP MANUAL DE ARCHIVOS
9  76-76  I1  0,1  Tipo de circuito: = 0, existente; = 1, futuro
| 10  78-78  | I1  | 0,1  | Representa contingencia? 1 = sí          |
| ---------- | --- | ---- | ---------------------------------------- |
| 11  80-84  | I5  |      | Número externo del circuito monitoreado  |
1
| 12  86-90  | I5  |     | Número externo del circuito monitoreado  |
| ---------- | --- | --- | ---------------------------------------- |
2
| 13  92-96  | I5  |     | Número externo del circuito monitoreado  |
| ---------- | --- | --- | ---------------------------------------- |
3
| 14  98-102  | I5  |     | Número externo del circuito monitoreado  |
| ----------- | --- | --- | ---------------------------------------- |
4
| 15  104-108  | I5  |     | Número externo del circuito monitoreado  |
| ------------ | --- | --- | ---------------------------------------- |
5
16  110-113  I4  0,1  Considera falla: = 1, no considera falla: = 0
| 17  115-121  | F7.0  |     | Probabilidad de falla del circuito  |
| ------------ | ----- | --- | ----------------------------------- |
18  126-126  I1  0,1  Caso  se  utilice  “Monitoración  seleccio-
nada de flujos” (ver Datos Generales y Op-
ciones de Ejecución, archivo SDDP.DAT),
este campo indica:
= 1: seleccionado para monitoración;
= 0: caso contrario.
Si la opción “Monitoración seleccionada
de flujos” no fue seleccionada, este campo
es ignorado.
| 19  128-128  | I1  | 0, 1  | Status del circuito:  |
| ------------ | --- | ----- | --------------------- |
0 : conectado,
1 : desconectado
| 20  140-147  | F8.0  |     | Ángulo mínimo de transformador defasa- |
| ------------ | ----- | --- | -------------------------------------- |
dor (en °)
| 21  149-156  | F8.0  |     | Ángulo máximo de transformador defasa- |
| ------------ | ----- | --- | -------------------------------------- |
dor (en °)
7.5  Modificación de los datos de circuitos
Archivo ASCII llamado MCIRC.DAT, ubicado en el directorio de datos del sistema. El programa
solamente utiliza estas informaciones si se indicó que la configuración es dinámica (registro 8
del archivo SDDP.DAT). Este archivo contiene 4 tipos de registro:
7.5.1  Registro tipo 1
El primer registro indica la versión del archivo, que debe ser $version=2.
7.5.2  Registro tipo 2
Este registro identifica la etapa (día/mes/año) de la modificación.
92

SDDP MANUAL DE ARCHIVOS

| Campo  Columna  | Tipo  | Descripción                      |     |
| --------------- | ----- | -------------------------------- | --- |
| 1  1-4          | A     | Debe contener la palabra “MOD:”  |     |
| 2  6-7          | I2    | Día de la modificación           |     |
| 3  9-10         | I2    | Número del mes                   |     |
| 4  12-15        | I4    | Año                              |     |
7.5.3  Registro tipo 3
Es un header igual al del archivo DCIRC.DAT. Contiene la palabra “.NUM” en las 4 primeras co-
lumnas.
7.5.4  Registro tipo 4
Contiene los datos del circuito a ser modificado en la etapa indicada en el registro tipo 2. El
formato de este registro es idéntico al formato del registro del archivo DCIRC.DAT. Sin em-
bargo, los únicos campos que el programa reconoce son:

| Campo  Columna  | Formato  | Valores  Váli- | Descripción  |
| --------------- | -------- | -------------- | ------------ |
dos
| 1  1-5    | I5    | -   | Número de la barra de origen       |
| --------- | ----- | --- | ---------------------------------- |
| 2  9-13   | I5    | -   | Número de la barra de destinación  |
| 3  18-23  | F6.0  | -   | Resistencia del circuito (en %)    |
≠ 0
| 4  24-29  | F6.0  |     | Reactancia del circuito (en %)  |
| --------- | ----- | --- | ------------------------------- |
6  59-64  F6.0  > 0  Límite de flujo - situación normal (MW)
| 7  65-68     | F4.0  | > 0   | Límite de flujo - emergencia (MW)   |
| ------------ | ----- | ----- | ----------------------------------- |
| 8  70-74     | I4    | -     | Número del circuito                 |
| 17  115-121  | F7.0  |       | Probabilidad de falla del circuito  |
| 19  128-128  | I1    | 0, 1  | Status del circuito:                |
0 : conectado,
1 : desconectado
| 20  140-147  | F8.0  |     | Ángulo mínimo de transformador defa- |
| ------------ | ----- | --- | ------------------------------------ |
sador (en °)
| 21  149-156  | F8.0  |     | Ángulo máximo de transformador de- |
| ------------ | ----- | --- | ---------------------------------- |
fasador (en °)
Se coloca un registro tipo 4 por cada circuito modificado en esa etapa.
7.6  Datos de enlace CC
Archivo ASCII llamado DCLINK.DAT, ubicado en el directorio de datos del sistema (registro 2 del
archivo PATH.DAT). Contiene los datos de los enlaces CC.
93

SDDP MANUAL DE ARCHIVOS
7.6.1 Registro tipo 1
Este registro es un header.
7.6.2 Datos de los enlaces CC
Campo Columna Tipo Descripción
1 1-4 I4 Número de la barra "DE" (origen)
2 6-9 I4 Número de la barra "PARA" (destino)
3 11-17 F7.0 Límite de transferencia DE→PARA
4 19-24 F7.0 Factor de pérdida DE→PARA
5 27-33 F7.0 Límite de transferencia PARA→DE
6 35-41 F7.0 Factor de pérdida PARA→DE
7 43-46 I4 Número del enlace CC
8 48-59 A12 Nombre del enlace CC
9 61-64 I4 Tipo de circuito: = 0, existente; = 1, futuro
10 66-72 F7.0 Límite de emergencia de transferencia DE→PARA
11 74-80 F7.0 Límite de emergencia de transferencia PARA→DE
7.7 Modificación de los enlaces CC
Archivo ASCII llamado MDCLINK.DAT, ubicado en el directorio del sistema (registro 2 del archivo
PATH.DAT). Este archivo no se utiliza si la configuración es estática (registro 8 del archivo
SDDP.DAT). El archivo contiene tres tipos de registro:
7.7.1 Registro tipo 1
Este registro identifica la etapa (día/mes/año) de la modificación.
Campo Columna Tipo Descripción
1 1-4 A Debe contener la palabra "MOD:"
2 6-7 I2 Día de la modificación
3 9-10 I2 Número del mes
4 12-15 I4 Año
7.7.2 Registro tipo 2
Mismo header del archivo DCLINK.DAT. Debe contener la palabra "FROM" en las primeras 4
columnas.
7.7.3 Registro tipo 3
Mismo formato del archivo DCLINK.DAT. Se puede modificar los siguientes campos:
94

SDDP MANUAL DE ARCHIVOS
Campo Columna Tipo Descripción
3 11-17 F7.0 Límite de transferencia DE→PARA
4 19-24 F7.0 Factor de pérdida DE→PARA
5 27-33 F7.0 Límite de transferencia PARA→DE
6 35-41 F7.0 Factor de pérdida PARA→DE
7 43-46 I4 Número del enlace CC
8 48-59 A12 Nombre del enlace CC
9 61-64 I4 Tipo de circuito: = 0, existente; = 1, futuro
10 66-72 F7.0 Límite de emergencia de transferencia DE→PARA
11 74-80 F7.0 Límite de emergencia de transferencia PARA→DE
7.8 Dados de áreas eléctricas
El archivo de datos de áreas eléctricas DAREA.DAT contiene las siguientes informaciones
7.8.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-8 A8 Palabra clave: $version
2 10-13 I4 Número de la versión
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
7.8.2 Registro tipo 2
Campo Columna Tipo Descripción
1 1-5 I5 Código del área
2 7-16 A10 Nombre del área
7.9 Modificación de los límites de exportación e importación por área
Archivo ASCII denominado MAREAYYY.DAT localizado en el directorio de datos del sistema. Este
archivo contiene las modificaciones de los límites de las restricciones de exportación e impor-
tación por área para un estudio con YYY bloques. Este archivo está organizado de la siguiente
manera:
7.9.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-8 A8 Palabra clave: $version
2 10-13 I4 Número de la versión
95

SDDP MANUAL DE ARCHIVOS
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
7.9.2  Registro tipo 2
Campo  Columna  Tipo  Descripción
| 1   | 1-10  Fecha  Fecha dd/mm/yyyy          |     |
| --- | -------------------------------------- | --- |
| 2   | 12-16  I5  Código del agente           |     |
| 3   | 18-29  A12  Nombre del agente          |     |
| 4   | 31-40  A10  Atributo a ser modificado  |     |
5  42-46  I5  Identificador del bloque (* = todos los bloques)
| 6   | 48-57  F10.0  Valor  |     |
| --- | -------------------- | --- |
En este caso los atributos que pueden ser modificados son:
•
 – limite de exportación (MW)
EXPORT
•
 – limite de importación (MW)
IMPORT
7.10  Configuración de suma de flujo en circuitos
El archivo CSUMCIRC.DAT contiene los datos de las restricciones de soma de flujo en circuitos.
Una restricción de soma de flujo en circuitos se define como la combinación lineal de hasta 25
circuitos. Este archivo es organizado de la siguiente manera:
7.10.1 Registro tipo 1
Campo  Columna  Tipo  Descripción
| 1   | 1-8  A8  Palabra clave: $version   |     |
| --- | ---------------------------------- | --- |
| 2   | 10-13  I4  Número de la versión    |     |
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
7.10.2 Registro tipo 2
Campo  Columna  Tipo  Descripción
| 1   | 1-5  I5  Código de la restricción de soma de circuitos    |     |
| --- | --------------------------------------------------------- | --- |
| 2   | 7-18  A12  Nombre de la restricción de soma de circuitos  |     |
3  20-29  F10.0  Límite inferior (será considerado el mismo valor
parar todos los bloques)
4  31-40  F10.0  Límite superior (será considerado el mismo va-
lor parar todos los bloques)
| 5    | 42-47  F6.0  Coeficiente 1         |     |
| ---- | ---------------------------------- | --- |
| 6    | 49-60  A12  Nombre del circuito 1  |     |
| 7    | 62-67  F6.0  Coeficiente 2         |     |
| 8    | 69-80  A12  Nombre del circuito 2  |     |
| ...  | ...  ...                           | …   |
96

SDDP MANUAL DE ARCHIVOS
7 522-527 F6.0 Coeficiente 25
8 529-540 A12 Nombre del circuito 25
7.11 Modificación de restricciones de suma de flujo en circuitos
Archivo ASCII denominado MSUMCIRCYYY.DAT localizado en el directorio de datos del sistema.
Este archivo contiene las modificaciones de los límites de las restricciones de suma de circuitos
para un estudio con YYY bloques. Este archivo está organizado de la siguiente manera:
7.11.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-8 A8 Palabra clave: $version
2 10-13 I4 Número de la versión
Registros que comienzan con el carácter “!” son comentarios y son ignorados.
7.11.2 Registro tipo 2
Campo Columna Tipo Descripción
1 1-10 Fecha Fecha dd/mm/yyyy
2 12-16 I5 Código del agente
3 18-29 A12 Nombre del agente
4 31-40 A10 Atributo a ser modificado
5 42-46 I5 Identificador del bloque (* = todos los bloques)
6 48-57 F10.0 Valor
En este caso los atributos que pueden ser modificados son:
• – limite superior de la restricción de suma de circuitos (MW)
UB
• – limite inferior de la restricción de suma de circuitos (MW)
LB
7.12 Costos en circuitos internacionales
Conjuntos de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo lla-
mado CCIRZZYY.DAT contiene los costos variables en los flujos de los circuitos internacionales (ZZ
= ME para etapas mensuales; ZZ = SE para etapas semanales y YY indica el número de bloques).
El programa solamente lee estas informaciones si se indicó que la configuración es dinámica
(registro 8 del archivo SDDP.DAT). Si este archivo no existe entonces se asume que el costo en
los circuitos internacionales es nulo para todas las etapas y bloques del estudio.
Este archivo contiene 3 tipos de registro:
7.12.1 Registro tipo 1
Este registro identifica el circuito.
97

SDDP MANUAL DE ARCHIVOS

| Campo  | Columna  | Tipo  Descripción                            |
| ------ | -------- | -------------------------------------------- |
| 1      | 1-12     | A12  Palabra clave: Contiene "**** Planta:"  |
| 2      | 14-17    | I4  Número del circuito                      |
| 3      | 19-30    | A12  Nombre del circuito                     |
| 4      | 41-43    | A3  Palabra clave:                           |
“-->” indica el sentido DE→PARA

“<--” indica el sentido PARA→DE

5  45-47  A3  Identificador de la unidad monetaria del circuito
internacional
7.12.2 Registro tipo 2
Es un header a continuación del registro tipo 1. Es ignorado por el programa.
7.12.3 Registro tipo 3
Contiene los datos de los costos en los flujos de los circuitos internacionales por etapa y por
bloque. Cada registro está asociado a un año y a un bloque y cada columna a una etapa (mes
o semana). Solo es necesario llenar los campos donde el costo de los circuitos se alteró con
respecto a la etapa anterior.

| Campo  | Columna  | Tipo  Descripción                                   |
| ------ | -------- | --------------------------------------------------- |
| 1      | 1-4      | I4  Año                                             |
| 2      | 5-8      | i4  Bloque de demanda                               |
| 3      | 9-16     | A8  Costo de circuito para la primera etapa (mes o  |
semana) en $/MWh
4  17-24  A8  Costo de circuito para la segunda etapa (mes o
semana) en $/MWh
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
Observaciones:
•  Un campo vacío indica que no hay cambios con respecto al campo antecedente
•  Se coloca un registro tipo 3 para cada año y bloque del estudio
98

SDDP MANUAL DE ARCHIVOS
8 DEMANDA
8.1 Configuración de demanda
El archivo CLOADSXX.DAT contiene el registro de todas las demandas para el sistema XX. A él
corresponden los siguientes datos:
8.1.1 Registro tipo 1
Es un header que describe los elementos del registro tipo 2.
8.1.2 Registro tipo 2
Este registro define una nueva demanda en el sistema XX.
Campo Columna Tipo Descripción
1 1-4 I4 Número identificador de la demanda
2 6-17 A12 Nombre de la demanda
3 19-23 I5 Número de segmentos de la demanda
4 25-29 I5 Tipo del primer segmento:
0 : inelástico
1: elástico
8.2 Demanda de energía
Conjunto de archivos ASCII ubicado en el directorio de datos del estudio. Cada archivo llamado
DEZZYYXX.DAT contiene los valores de las demandas en GHz para el sistema XX, considerando
YY bloques, donde ZZ indica lo siguiente:
ZZ = ME, si las demandas son mensuales,
ZZ = SE, si las demandas son semanales.
Observación: XX es el identificador del sistema definido en el campo 3 del registro del archivo
SISTEM.DAT.
Por ejemplo, el archivo DEME01XX.DAT contiene los datos de demanda mensuales conside-
rando 1 bloque de demanda para el sistema XX.
8.2.1 Registro tipo 1
Campo Columna Tipo Descripción
1 1-9 A9 Palabra clave: $version=
2 10-13 I4 Número de la versión
99

SDDP MANUAL DE ARCHIVOS
8.2.2 Registro tipo 2
Este registro identifica la demanda y el segmento para los cuales se informará la demanda. Él
tiene el siguiente formato.
Campo Columna Tipo Descripción
1 1-12 A12 Indica que un nuevo segmento será creado, a
partir de la instrucción: **** Load :
2 14-17 I4 Número identificador de la demanda a la cual el
segmento está asociado
3 19-30 A12 Nombre de la demanda
4 39-42 I4 Número identificador del nuevo segmento de
demanda
8.2.3 Registro tipo 3
Este registro es un comentario.
8.2.4 Registro tipo 4
Este registro contiene los valores de las demandas en el siguiente formato:
Campo Columna Tipo Descripción
1 1-4 I4 Año del dato de duración variable.
2 6-8 I3 Número del bloque de demanda.
3 9-14 F6.0 Demanda del primer mes o semana (GWh).
4 15-20 F6.0 Demanda del segundo mes o semana (GWh).
5-53 etc. etc. etc.
54 315-320 F6.0 Demanda de la semana 52 (GWh).
8.3 Precios de energía
Conjunto de archivos ASCII ubicados en directorio de datos del estudio. Cada archivo denomi-
nado CDYYXX.DAT contiene los datos de los precios de energía para el sistema XX, conside-
rando YY bloques. A él corresponden los siguientes datos:
8.3.1 Registro tipo 1
Este registro define los datos básicos del segmento de demanda al cual los precios están aso-
ciados.
Campo Columna Tipo Descripción
100

SDDP MANUAL DE ARCHIVOS
1 1-12 A12 Indica que un nuevo segmento será leído a partir
de la instrucción: **** Load :
2 14-17 I4 Número identificador de la demanda al cual el
segmento está asociado
3 19-30 A12 Nombre de la demanda
4 39-42 I4 Número identificador del segmento de la de-
manda
8.3.2 Registro tipo 2
Este registro es un header.
8.3.3 Registro tipo 3
Este registro define, para un determinado bloque, los valores de precios asociados a las ener-
gías, para todas las etapas de un año.
Campo Columna Tipo Descripción
1 1-4 I4 Año
2 6-8 I3 Bloque
3 10-14 F5.0 Precio del segmento ($/MWh) asociado al valor
máximo de energía para la primera etapa
etc. etc. etc. Etc.
14 76-80 F5.0 Precio del segmento ($/MWh) asociado al valor
máximo de energía para la última etapa
101

SDDP MANUAL DE ARCHIVOS
9  DÉFICIT
9.1  Modificación curva costo de déficit
Conjuntos de archivos ASCII ubicados en el directorio de datos del estudio. El archivo llamado
MCDEF.DAT contiene modificaciones de la curva de costo de déficit a lo largo del tiempo. El
programa sólo lee estas informaciones si se indicó que la configuración es dinámica (registro
8 del archivo SDDP.DAT).
Este archivo contiene 3 tipos de registro:
9.1.1  Registro tipo 1
Este registro identifica la etapa (día/mes/año) de la modificación.

| Campo  | Columna  | Tipo  Descripción                    |     |     |     |
| ------ | -------- | ------------------------------------ | --- | --- | --- |
| 1      | 1-4      | A  Debe contener la palabra "MOD:".  |     |     |     |
| 2      | 6-7      | I2  Día de la modificación.          |     |     |     |
| 3      | 9-10     | I2  Número del mes                   |     |     |     |
| 4      | 12-15    | I4  Año                              |     |     |     |
9.1.2  Registro tipo 2
Es un header ignorado por el programa.
9.1.3  Registro tipo 3
Contiene los datos del costo de déficit variables en el tiempo. El formato de este registro es
definido a seguir:

| Campo  | Columna  | Tipo  Descripción  |     |     |     |
| ------ | -------- | ------------------ | --- | --- | --- |
1  1-6  F6.0  Valor del primer segmento de la energía no suminis-
|     |     | trada  (%).  | Debe  ser  | igual  al  definido  | no  archivo  |
| --- | --- | ------------ | ---------- | -------------------- | ------------ |
sddp.dat.
| 2   | 8-15  | F8.0  Primer segmento del costo de la ENS ($/MWh).  |     |     |     |
| --- | ----- | --------------------------------------------------- | --- | --- | --- |
3  17-22  F6.0  Valor del segundo segmento de la ENS (%).Debe ser
igual al definido no archivo sddp.dat.
4  24-31  F8.0  Segundo segmento del costo de la ENS ($/MWh).
5  33-38  F6.0  Valor del ercer segmento de la ENS (%).Debe ser igual
al definido no archivo sddp.dat.
6  40-47  F8.0  Tercer segmento del costo de la ENS ($/MWh).
7  49-54  F6.0  Valor del cuarto segmento de la ENS (%).Debe ser igual
al definido no archivo sddp.dat.
102

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
8  56-63  F8.0  Cuarto segmento del costo de la ENS ($/MWh).
103

SDDP MANUAL DE ARCHIVOS
10  DISPONIBILIDAD Y TRANSPORTE DE GAS NATURAL
Conjunto de archivos donde se define la estructura de producción, consumo y logística de
transporte de gas natural.
Sea UV la unidad volumétrica utilizada por el usuario (puede ser m3 o pies cúbicos). Los datos
asociados a la red de gas, como capacidad de producción y capacidad de transporte en los
gasoductos deben ser informados en MUV/día (millones de unidades volumétricas por día).
Para las unidades térmicas que están asociadas a la red de gas, el consumo específico debe
ser informado en UV/MWh (unidades volumétricas por MWh).
10.1  Nodos de la red de gas
Archivo ASCII ubicado en el directorio de datos del estudio. Este archivo llamado SISGAS.DAT con-
tiene la identificación de los nodos que representan las áreas de producción y consumo de gas
natural, o también los nodos de pasaje. Estos nodos o sistemas son independientes de aque-
llos definidos en el SISTEM.DAT.
El primer registro es apenas un comentario y es ignorado por el programa. Los demás registros
tienen el siguiente formato:

| Campo  | Columna  | Tipo  Descripción                     |                |      |
| ------ | -------- | ------------------------------------- | -------------- | ---- |
| 1      | 1-4      | I4  Número del sistema                |                |      |
| 2      | 6-17     | A12  Nombre del sistema               |                |      |
| 3      | 19-20    | A2  Identificador del sistema de gas  |                |      |
| 4      | 22-28    | F7.0  Producción                      | mínima  local  | (en  |
MUV/día)
| 5   | 30-36  | F7.0  Producción  | máxima  local  | (en  |
| --- | ------ | ----------------- | -------------- | ---- |
MUV/día)
| 6   | 38-44  | F7.0  Costo de producción (en $/UV)  |     |     |
| --- | ------ | ------------------------------------ | --- | --- |
| 7   | 46-49  | I4  Tipo de fuente de producción     |     |     |
= 0: existente
= 1: futura
| 8   | 51-52  | A2  Identificador  | del  sistema  | eléc- |
| --- | ------ | ------------------ | ------------- | ----- |
trico
10.1.1 Modificación de los sistemas de gas
Archivo ASCII llamado MSISGAS.DAT, ubicado en el directorio de datos del estudio. Este archivo
contiene las modificaciones a lo largo del estudio de los datos informados en el archivo SIS-
GAS.DAT.
El primer registro es un comentario, los demás tienen el siguiente formato:

104

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción           |               |        |
| ------ | -------- | --------------------------- | ------------- | ------ |
| 1      | 1-2      | I2  Día de la modificación  |               |        |
| 2      | 4-5      | I2  Mes de la modificación  |               |        |
| 3      | 7-10     | I4  Año de la modificación  |               |        |
| 4      | 12-15    | I4  Número del sistema      |               |        |
| 5      | 17-28    | A12  Nombre del sistema     |               |        |
| 6      | 30-31    | A2  Identificador           | del  sistema  | (este  |
campo es ignorado)
| 7   | 33-39  | F7.0  Producción  | mínima  local  | (en  |
| --- | ------ | ----------------- | -------------- | ---- |
MUV/día)
| 8   | 41-47  | F7.0  Producción  | máxima  local  | (en  |
| --- | ------ | ----------------- | -------------- | ---- |
MUV/día)
| 9   | 49-55  | F7.0  Costo de producción (en $/UV)  |     |     |
| --- | ------ | ------------------------------------ | --- | --- |
10.2  Costos cronológicos de producción de gas
Los datos de costo de producción en $/UV para un estudio de NN bloques deben ser informa-
dos en un archivo denominado DATCGYYNN.DAT, donde YY indica se los datos son mensua-
les (YY=me) o semanales (YY=se). Este archivo solamente será leído caso haya sido definida
la opción de lectura de datos cronológicos de producción de gas, código RGAS, en el archivo
sddp.dat. Este archivo contiene 2 tipos de registros:
10.2.1 Registro tipo 1
Este registro identifica los agentes asociados a los datos de costo de producción definidos en
el archivo sisgas.dat.

| Campo  | Columna  | Tipo  Descripción                    |                |          |
| ------ | -------- | ------------------------------------ | -------------- | -------- |
| 1      | 1-6      | A6  Dependiendo del tipo de estudio  |                |          |
|        |          | contiene                             | la  siguiente  | palabra  |
clave:
Estudio mensual: ‘!Month”
Estudio semanal: “!Week “
| 2   | 8-11  | A4  Comentario ignorado por el pro- |     |     |
| --- | ----- | ----------------------------------- | --- | --- |
grama
| 3   | 13-13  | A1  Comentario ignorado por el pro- |     |     |
| --- | ------ | ----------------------------------- | --- | --- |
grama
| 4   | 15-26  | A12  Nombre del primer sistema   |     |     |
| --- | ------ | -------------------------------- | --- | --- |
Nombre del segundo sistema
| 5     | 28-39  | A12         |     |     |
| ----- | ------ | ----------- | --- | --- |
| etc.  | etc.   | etc.  etc.  |     |     |
105

SDDP MANUAL DE ARCHIVOS
10.2.2 Registro tipo 2
Contienen los datos de costo de producción. El formato de este registro es definido a seguir:

| Campo  | Columna  | Tipo  Descripción                    |
| ------ | -------- | ------------------------------------ |
| 1      | 5-6      | I2  Indica el mes o semana del estu- |
dio.
| 2   | 8-11   | I4  Indica el año del estudio.          |
| --- | ------ | --------------------------------------- |
| 3   | 13-13  | I1  Indica el bloque de demanda         |
| 4   | 15-26  | F12.0  Costo de producción para el pri- |
mer agente ($/UV)
| 5   | 28-39  | F12.0  Costo de producción para el se- |
| --- | ------ | -------------------------------------- |
gundo agente ($/UV)
| etc.  | etc.  | etc.  etc.  |
| ----- | ----- | ----------- |
10.3  Demanda no-termoeléctrica de gas
Archivo ASCII ubicado en el directorio de datos del estudio, llamado DEMGAS.DAT. Este ar-
chivo contiene las demandas de gas natural no-termoeléctricas, o sea, aquellas relacionadas
al consumo de los sectores industrial, comercial, automotriz y residencial además del con-
sumo de las refinarías, por ejemplo.
El primer registro es apenas un comentario, los restantes tienen el siguiente formato:

| Campo  | Columna  | Tipo  Descripción                   |
| ------ | -------- | ----------------------------------- |
| 1      | 1-4      | I4  Número de identificación de la  |
demanda
| 2   | 6-17  | A12  Nombre que la demanda de gas  |
| --- | ----- | ---------------------------------- |
no-eléctrica
| 3   | 19-22  | I4  Número del sistema de gas al cual  |
| --- | ------ | -------------------------------------- |
está asociada la demanda
| 4   | 24-30  | F7.0  Penalidad por no suministro de la  |
| --- | ------ | ---------------------------------------- |
demanda en $/UV
10.3.1 Demandas no-termoeléctrica – datos cronológicos
Los datos de demanda no eléctrica en MUV/día para un estudio de NN bloques deben ser
informados en un archivo denominado DATDGYYNN.DAT, donde YY indica se los datos son
mensuales (YY=me) o semanales (YY=se).
Este archivo contiene 2 tipos de registro:
10.3.1.1  Registro tipo 1
106

SDDP MANUAL DE ARCHIVOS
Este registro identifica los agentes asociados a los datos de demanda no-térmica de gas defi-
nidos en el archivo demgas.dat.

| Campo  | Columna  | Tipo  Descripción                    |                |          |
| ------ | -------- | ------------------------------------ | -------------- | -------- |
| 1      | 1-6      | A6  Dependiendo del tipo de estudio  |                |          |
|        |          | contiene                             | la  siguiente  | palabra  |
clave:
Estudio mensual: ‘!Month”
Estudio semanal: “!Week “
| 2   | 8-11  | A4  Comentario ignorado por el pro- |     |     |
| --- | ----- | ----------------------------------- | --- | --- |
grama
| 3   | 13-13  | A1  Comentario ignorado por el pro- |     |     |
| --- | ------ | ----------------------------------- | --- | --- |
grama
| 4   | 15-26  | A12  Nombre de la primera demanda  |     |     |
| --- | ------ | ---------------------------------- | --- | --- |
de gas no-térmica
| 5   | 28-39  | A12  Nombre de la segunda demanda  |     |     |
| --- | ------ | ---------------------------------- | --- | --- |
de gas no-térmica
| etc.  | etc.  | etc.  etc.  |     |     |
| ----- | ----- | ----------- | --- | --- |
10.3.1.2  Registro tipo 2
Contiene los datos de demanda no-térmica de gas. El formato de este registro es definido a
seguir:
| Campo  | Columna  | Tipo  Descripción                    |     |     |
| ------ | -------- | ------------------------------------ | --- | --- |
| 1      | 5-6      | I2  Indica el mes u semana del estu- |     |     |
dio.
| 2   | 8-11   | I4  Indica el año del estudio.          |             |         |
| --- | ------ | --------------------------------------- | ----------- | ------- |
| 3   | 13-13  | I1  Indica el bloque                    |             |         |
| 4   | 15-26  | F12.0  Indica la demanda de gas no-tér- |             |         |
|     |        | mica  para                              | el  primer  | agente  |
(MUV/día)
| 5   | 28-39  | F12.0  Indica la demanda de gas no-tér- |              |         |
| --- | ------ | --------------------------------------- | ------------ | ------- |
|     |        | mica  para                              | el  segundo  | agente  |
(MUV/día)
| etc.  | etc.  | etc.  etc.  |     |     |
| ----- | ----- | ----------- | --- | --- |
10.4  Gasoductos
Archivo ASCII ubicado en el directorio de datos del estudio. Este archivo se llama INTGAS.DAT
y contiene las características de los gasoductos que interconectan los diferentes sistemas de
gas definidos en el archivo SISGAS.DAT.
El primero registro es comentario. Los demás tienen el siguiente formato:
107

SDDP MANUAL DE ARCHIVOS

| Campo  | Columna  | Tipo  Descripción                      |
| ------ | -------- | -------------------------------------- |
| 1      | 1-4      | I4  Número del gasoducto               |
| 2      | 6-17     | A12  Nombre del gasoducto              |
| 3      | 19-22    | I4  Sistema origen                     |
| 4      | 24-27    | I4  Sistema destino                    |
| 5      | 29-35    | F7.0  Capacidad máxima de flujo en el  |
sentido  “origen→destino”  (en
MUV/día)
| 6   | 37-43  | F7.0  Capacidad máxima de flujo en el  |
| --- | ------ | -------------------------------------- |
sentido  “destino→origen”  (en
MUV/día)
| 7   | 45-51  | F7.0  Factor de pérdidas en el sentido  |
| --- | ------ | --------------------------------------- |
“origen→destino”
| 8   | 53-59  | F7.0  Factor de pérdidas en el sentido  |
| --- | ------ | --------------------------------------- |
“destino→origen”
| 9   | 61-67  | F7.0  Costo de transporte (en $/UV)  |
| --- | ------ | ------------------------------------ |
| 10  | 69-72  | I4  Tipo de gasoducto                |
= 0: existente
= 1: futura
| 11  | 81-83  | A3  Identificador de la unidad mone- |
| --- | ------ | ------------------------------------ |
taria del gasoducto
10.4.1 Modificaciones en los datos de gasoductos
Las alteraciones en las características de los gasoductos – aumento o reducción de la capaci-
dad de transporte, modificación de los factores de pérdidas – deben ser indicadas en el archivo
MINTGAS.DAT ubicado en el directorio de datos del estudio.
El primer registro es apenas un comentario, ignorado por el programa. Los registros siguientes
tienen el siguiente formato:

| Campo  | Columna  | Tipo  Descripción                     |
| ------ | -------- | ------------------------------------- |
| 1      | 1-2      | I2  Día de la modificación            |
| 2      | 4-5      | I2  Mes de la modificación            |
| 3      | 7-10     | I4  Año de la modificación            |
| 4      | 12-15    | I4  Número del gasoducto              |
| 5      | 17-28    | A12  Nombre del gasoducto             |
| 6      | 30-33    | I4  Sistema origen (este campo es ig- |
norado)
| 7   | 35-38  | I4  Sistema destino (este campo es  |
| --- | ------ | ----------------------------------- |
ignorado)
108

SDDP MANUAL DE ARCHIVOS
| 8   | 40-46  | F7.0  Capacidad máxima de flujo en el  |
| --- | ------ | -------------------------------------- |
sentido  “origen→destino”  (en
MUV/día)
| 9   | 48-54  | F7.0  Capacidad máxima de flujo en el  |
| --- | ------ | -------------------------------------- |
sentido  “destino→origen”  (en
MUV/día)
| 10  | 56-62  | F7.0  Factor de pérdidas en el sentido  |
| --- | ------ | --------------------------------------- |
“origen→destino”
| 11  | 64-70  | F7.0  Factor de pérdidas en el sentido  |
| --- | ------ | --------------------------------------- |
“destino→origen”
| 12  | 72-78  | F7.0  Costo de transporte (en $/UV)  |
| --- | ------ | ------------------------------------ |
109

SDDP MANUAL DE ARCHIVOS
11  HIDROLOGÍA
Los módulos de cálculo de política operativa y de simulación operativa utilizan cinco archivos
de datos hidrológicos:
•  configuración de las estaciones hidrológicas
•  histórico de caudales
•  parámetros del modelo estocástico
•  archivo externo de secuencias hidrológicas
•  archivo externo de caudales condicionados
11.1  Configuración de las estaciones hidrológicas
Archivos ASCII llamados HTOPOL.DAT (caudales mensuales) y HTOPOL_W.DAT (caudales sema-
nales). Cada archivo contiene 90 registros, que describen las estaciones hidrológicas del ar-
chivo de caudales correspondiente. El contenido de cada registro se presenta a continuación.

| Campo  | Columna  | Tipo  Descripción                                |
| ------ | -------- | ------------------------------------------------ |
| 1      | 3-5      | I2  Número del registro                          |
| 2      | 13-15    | I3  Código de la estación                        |
| 3      | 21-35    | A15  Nombre de la estación                       |
| 4      | 53-55    | I3  Código de la estación aguas abajo            |
| 5      | 56-56    | A1  Indicador de serie incremental nula: '*'     |
| 6      | 62-70    | -  Fecha de la última actualización del archivo  |
de caudales (día/mes/año)(I2,1x,A3,1x,I2)
11.2  Histórico de caudales
Archivos ASCII llamados HINFLW.DAT (caudales mensuales) y HINFLW_W.DAT (caudales semana-
les).
11.2.1 Registro tipo 1

| Campo  | Columna  | Tipo  Descripción                        |
| ------ | -------- | ---------------------------------------- |
| 1      | 1-2      | I2  Mes inicial del archivo de caudales  |
| 2      | 4-7      | I4  Año inicial del archivo de caudales  |
| 3      | 8-14     | i7  Código de la primera estación        |
| 4      | 15-21    | i7  Código de la segunda estación        |
| etc.   | etc.     | etc.  etc.                               |
110

SDDP MANUAL DE ARCHIVOS
11.2.2 Registro tipo 2
Contiene los caudales naturales mensuales (o semanales) asociados a las estaciones, en m3/s.
Campo Columna Tipo Descripción
1 1-2 I2 Mes
2 4-7 I4 Año
3 8-14 F7.0 Caudal natural de la primera estación
4 15-21 F7.0 Caudal natural de la segunda estación
etc. etc. etc. etc.
Los datos no disponibles se representan como -99.0
11.3 Archivos de parámetros
Archivos de acceso directo (con header) llamados HPARAM.DAT (mensual) y HPARAM_W.DAT
(semanal). Cada archivo tiene 90 registros, correspondientes a las estaciones de los archivos
de configuración HTOPOL.DAT y HTOPOL_W.DAT.
Cada registro del archivo de parámetros mensuales contiene los siguientes valores, corres-
pondientes a los meses de Enero hasta Diciembre:
• 12 promedios;
• 12 desviaciones estándar;
• 12 conjuntos de parámetros auto-regresivos. Cada conjunto contiene ocho valores: los
seis primeros son los parámetros del modelo auto-regresivo periódico; el séptimo no se
utiliza en esta versión; el octavo contiene la varianza de los residuos.
Todos los valores están en precisión simple (REAL*4). El tamaño del registro es por lo tanto 12
x 10 x 4 = 480 bytes.
El archivo de parámetros semanales tiene una estructura semejante, pero con 52 promedios,
52 desviaciones estándar etc.
11.4 Archivo externo de secuencias de caudales (FORW.DAT)
Notación:
L número de secuencias en paralelo
N número de aberturas
P orden del modelo
NP número de puestos hidrológicos
T número de etapas del estudio
111

SDDP MANUAL DE ARCHIVOS
Archivo llamado FORW.DAT que contiene las L secuencias de caudales de la simulación "for-
ward" - acceso directo.
El primer registro contiene los números externos de los NP puestos hidrológicos, en el orden
en que las secuencias de caudales son grabadas.
Cada uno de los registros restantes, contiene un vector de dimensión NP (REAL*8), donde NP
es el número de puestos hidrológicos.
El segundo registro contiene los caudales incrementales de la etapa 1-P, primera secuencia,
donde P es el orden máximo del modelo estocástico de caudales (6). El tercero registro con-
tiene los caudales de la etapa 1-P, secuencia 2; el cuarto, de la etapa 1-P, secuencia 3 etc. El
registro L × P + 2 contiene los caudales de la etapa 1 para la primera secuencia. El número de
registros es por lo tanto L × (T + P) + 1, donde T es el número de etapas del estudio.
Los datos están en m3/s. Los caudales incrementales no deben ser negativos, pues esto resulta
en problemas para el balance hídrico de la PDD.
11.5 Archivo externo de caudales condicionados (BACK.DAT)
Contiene las N realizaciones de caudales para cada etapa t del estudio condicionadas a los
caudales observados en las etapas t-1, t-2, ... ,t-P de cada secuencia del archivo FORW.DAT -
acceso directo.
Cada registro contiene un vector de dimensión H (REAL*8). El primer registro contiene la pri-
mera realización de los caudales incrementales de la etapa 1 condicionados a los caudales de
las etapas 0, -1, ... , -P de la secuencia 1 del archivo FORW.DAT. El segundo registro contiene la
realización 2, etapa 1, condicionada a la secuencia 1. El registro N contiene la realización N,
etapa 1, condicionada a la secuencia 1. El registro N + 1 contiene la realización 1, etapa 2,
condicionada a la secuencia 2. El número de registros es por lo tanto T × L × N.
Se observa que el conjunto de ruidos aleatorios que se utiliza para producir las N realizaciones
condicionadas a la secuencia 1 deben ser los mismos que se utilizan en las secuencias 2, 3, ...
hasta la secuencia L. El objetivo es evitar que, debido a variaciones muestrales, el conjunto de
caudales condicionados a una secuencia de caudales secos en el pasado resulte más húmedo
que el mismo conjunto condicionado a caudales más elevados. Se observa también que el
conjunto de ruidos puede ser diferente en cada etapa.
11.6 Incertidumbre reducida
Archivo ASCII llamado INCRED.DAT ubicado en el directorio de datos del estudio, que permite
representar períodos de incertidumbre reducida.
11.6.1 Indicador de uso de períodos de incertidumbre reducida
El primer registro tiene el siguiente formato
112

SDDP MANUAL DE ARCHIVOS
Campo Columna Tipo Descripción
1 27-30 I4 Indicador de uso de períodos de incertidumbre re-
ducida:
0 = no: los datos serán ignorados
1 = sí
11.6.2 Datos de los períodos de incertidumbre reducida
Para cada período de incertidumbre reducida se deberán indicar los siguientes registros:
Registro Columna Tipo Descripción
2 27-30 I4 Etapa inicial del período de incertidumbre redu-
cida
3 27-30 I4 Año inicial del período de incertidumbre reducida
4 27-30 I4 Etapa final del período de incertidumbre reducida
5 27-30 I4 Año final del período de incertidumbre reducida
6 27-40 A12 Nombre del archivo de parámetros asociado a ese
período de incertidumbre reducida.
Se pueden representar varios períodos de incertidumbre reducida. Después del último pe-
ríodo indicado por el usuario el modelo asume el archivo de parámetros estándar: HPARAM.DAT,
para estudios mensuales o HPARAM_W.DAT, para estudios semanales.
11.7 Histórico de variable climática
Archivos ASCII llamados HHISTCLA.DAT (mensuales) e HHISTCLA_W.DAT (semanales). Contienen
el histórico de variable climática para el mismo periodo en que están definidos los caudales.
El primer registro es un header que contiene el nombre de las columnas del archivo. El se-
gundo registro contiene:
Campo Columna Tipo Descripción
1 1-2 I2 Mes/Semana inicial del registro del histórico de
variable climática, que debe ser igual al mes/se-
mana inicial del archivo de caudales
2 4-7 I4 Año inicial del registro del histórico de variable
climática, que debe ser igual al año inicial del ar-
chivo de caudales
3 8-12 A5 Contiene la palabra “class”, sin función especial
Los registros a seguir contienen los valores del histórico de variable climática (mensuales o
semanales). El formato sigue:
113

SDDP MANUAL DE ARCHIVOS
| Campo  | Columna  | Tipo  Descripción                               |
| ------ | -------- | ----------------------------------------------- |
| 1      | 1-2      | I2  Mes/Semana                                  |
| 2      | 4-7      | I4  Año                                         |
| 3      | 8-14     | F7.0  Valor histórico de la variable climática  |
| etc.   | etc.     | etc.  etc.                                      |
11.8  Escenario de previsión de la variable climática
Archivos ASCII llamados HDEFCLA.DAT (mensuales) y HDEFCLA _W.DAT (semanales). Contienen el
escenario previsto de la variable climática para el período en que el modelo de estimación
considerará el efecto de la variable climática en los caudales. El primer registro es un header
que contiene el nombre de las columnas del archivo. El segundo registro contiene:

| Campo  | Columna  | Tipo  Descripción  |
| ------ | -------- | ------------------ |
1  1-2  I2  Mes/Semana inicial del registro del escenario de
previsión de la variable climática
2  4-7  I4  Año inicial del registro del escenario de previsión
de la variable climática
3  8-12  A5  Contiene la palabra “class”, sin función especial
Los registros a seguir contienen los valores de la serie de previsión de variable climática (men-
suales o semanales). El formato sigue:

| Campo  | Columna  | Tipo  Descripción                              |
| ------ | -------- | ---------------------------------------------- |
| 1      | 1-2      | I2  Mes/Semana                                 |
| 2      | 4-7      | I4  Año                                        |
| 3      | 8-14     | F7.0  Valor previsto de la variable climática  |
| etc.   | etc.     | etc.  etc.                                     |
11.9  Parámetros de uso de la variable climática
Archivo ASCII llamado ESTCLASS.DAT. Contiene informaciones sobre el uso de variables climáti-
cas en la estimación de parámetros del modelo hidrológico. Contiene los siguientes registros:

| Registro  | Columna  | Tipo  Descripción                                |
| --------- | -------- | ------------------------------------------------ |
| 1         | 26-29    | I4  Indica si el modelo debe considerar o no el  |
efecto de la variable climática en los caudales
0 = no considera
1 = considera
114

SDDP MANUAL DE ARCHIVOS
| Registro  | Columna  | Tipo  Descripción  |
| --------- | -------- | ------------------ |
2  26-32  F7.0  Factor de ponderación asociado al efecto que la
variable climática exógena provocará en los cau-
dales. El factor es utilizado en la expresión para
la determinación de los pesos de cada observa-
ción.

Archivo ASCII denominado CLIMA.DAT, generado automáticamente cuando se ejecuta la esti-
mación del modelo hidrológico. Cuando la opción del uso de la variable climática se activa, el
estimador generará un archivo de parámetros del modelo hidrológico para cada año del hori-
zonte del estudio para el cual existan previsiones definidas por el usuario para la variable cli-
mática. Consecuentemente, en el archivo CLIMA.DAT se escribe el período (siempre de dura-
ción de un año) asociado a cada archivo de parámetros generado con el efecto de la variable
climática, así como el nombre de este archivo de parámetros (también generado automática-
mente por el estimador).
Para cada año del horizonte del estudio para el cuál existan previsiones definidas por el usua-
rio para la variable climática, deberán ser indicados los siguientes registros:

| Registro  | Columna  | Tipo  Descripción  |
| --------- | -------- | ------------------ |
1  27-30  F7.0  Factor de ponderación (mismo valor que se es-
cribe en el archivo ESTCLASS.DAT), presentado
aquí para informar cual es el factor utilizado en
la estimación.
| 2   | 27-30  | I4  Mes/Semana inicial                            |
| --- | ------ | ------------------------------------------------- |
| 3   | 27-30  | I4  Año inicial                                   |
| 4   | 27-30  | I4  Mes/Semana final                              |
| 5   | 27-30  | I4  Año final                                     |
| 6   | 27-38  | A12  Nombre del archivo de parámetros asociado a  |
ese período que considera el efecto de la varia-
ble climática
  Los próximos años deben venir en secuencia en el archivo, utilizando el mismo formato.

115

SDDP MANUAL DE ARCHIVOS
12  FUENTES RENOVABLES
Conjunto de archivos donde se define la estructura de configuración y escenarios de fuentes
renovables, como plantas eólicas, plantas con biomasa, etc.
12.1  Configuración fuentes renovables
Archivo ASCII ubicado en el directorio de datos del estudio. Este archivo llamado CGNDXX.DAT
contiene la identificación de las plantas asociadas a fuentes renovables para cada sistema XX.
El primer registro es apenas un comentario y es ignorado por el programa. Los demás registros
tienen el siguiente formato:

| Campo  | Columna  | Tipo  Descripción                      |
| ------ | -------- | -------------------------------------- |
| 1      | 1-4      | I4  Número de la planta.               |
| 2      | 6-17     | A12  Nombre de la planta.              |
| 3      | 19-23    | I5  Número de barra a la cual está co- |
nectada (en caso de representa-
ción de la red de transmisión)
| 4   | 25-28  | I4  Tipo de la planta:  |
| --- | ------ | ----------------------- |
0 = Existente;
1 = Futura.
| 5   | 30-33  | I4  Número de unidades            |
| --- | ------ | --------------------------------- |
| 6   | 35-41  | F7.0  Potencia instalada (MW)     |
| 7   | 43-50  | F8.0  Factor de operación (p.u).  |
| 8   | 52-58  | F7.0  Probabilidad de falla (%)   |
| 9   | 60-63  | I4  Sorteo de fallas              |
12.1.1 Modificación fuentes renovables
Archivo ASCII llamado MGNDXX.DAT, ubicado en el directorio de datos del estudio, para el sistema
XX. Este archivo contiene las modificaciones a lo largo del estudio de los datos informados en
el archivo CGNDXX.DAT.
El primer registro es un comentario, los demás tienen el siguiente formato:

| Campo  | Columna  | Tipo  Descripción            |
| ------ | -------- | ---------------------------- |
| 1      | 1-2      | I2  Día de la modificación.  |
| 2      | 4-5      | I2  Mes de la modificación.  |
| 3      | 7-10     | I4  Año de la modificación.  |
| 5      | 12-15    | I4  Número de la planta.     |
| 6      | 17-28    | A12  Nombre de la planta.    |
116

SDDP MANUAL DE ARCHIVOS
| 7   | 36-39  | I4  Tipo de la planta:  |
| --- | ------ | ----------------------- |
0 = Existente;
1 = Futura.
| 8   | 41-44  | I4  Número de unidades            |
| --- | ------ | --------------------------------- |
| 9   | 46-52  | F7.0  Potencia instalada (MW)     |
| 10  | 54-61  | F8.0  Factor de operación (p.u).  |
| 11  | 63-69  | F7.0  Probabilidad de falla (%)   |
12.2  Escenarios de generación de fuentes renovables
Archivo ASCII llamado GNDZZYYXX.DAT, ubicado en el directorio de datos del estudio, donde se
definen los escenarios de generación en p.u. de fuentes renovables, donde ZZ=ME o SE, YY =
número de bloques y XX=sistema.
12.2.1 Registro de identificación
Este registro contiene las siguientes informaciones.

| Campo  | Columna  | Tipo  Descripción                   |
| ------ | -------- | ----------------------------------- |
| 1      | 1-4      | A4  Palabra clave: “!Stg”           |
| 2      | 6-9      | A4  Palabra clave: Scn              |
| 3      | 11-14    | A4  Palabra clave: LBlk             |
| 4      | 16-27    | A12  Nombre de la fuente renovable  |
1(1)
| 5   | 29-40  | A12  Nombre de la fuente renovable  |
| --- | ------ | ----------------------------------- |
2(1)
| ...  | ...  | ...  Etc.  |
| ---- | ---- | ---------- |
 (1) Todos los datos de fuente renovable que están definidos en el archivo CGNDXX.DAT deben
estar contenidos en este archivo. El programa ignora las columnas de datos de fuente reno-
vable que no fueron definidos en el archivo CGNDXX.DAT.
12.2.2 Registro de datos
Este registro contiene los escenarios de generación por etapa y bloque de demanda.

| Campo  | Columna  | Tipo  Descripción                   |
| ------ | -------- | ----------------------------------- |
| 1      | 1-4      | I4  Etapa: mes o semana             |
| 2      | 6-9      | I4  Escenario                       |
| 4      | 11-14    | I4  Bloque                          |
| 5      | 16-27    | F8  Generación de la fuente renova- |
ble 1 (p.u.)
117

SDDP MANUAL DE ARCHIVOS
| 6   | 29-40  | F9  Generación de la fuente renova- |
| --- | ------ | ----------------------------------- |
ble 2 (p.u.)
| ...  | ...  | ...  etc.  |
| ---- | ---- | ---------- |
118

SDDP MANUAL DE ARCHIVOS
13 BATERÍA
Conjunto de archivos donde se define la estructura de configuración de baterías.
13.1 Configuración de batería
Archivo ASCII ubicado en el directorio de datos del estudio. Este archivo llamado CBATTERYXX.DAT
contiene datos de configuración para las baterías en el sistema xx.
El primer registro indica la versión del archivo. En este punto, debe venir con el texto "$versión
1". El segundo registro es un header. Los restantes tienen formato CSV (delimitado por co-
mas):
Columna Tipo Descripción
1 entero Número de la batería
2 string Nombre de la batería:
Límite = 12 caracteres.
3 entero Número de barra a la cual está conectada (en caso
de representación de la red de transmisión)
4 entero Tipo de la batería:
0 = Existente;
1 = Futura.
5 real Almacenamiento mínimo (MWh)
6 real Almacenamiento máximo (MWh)
7 real Almacenamiento inicial (p.u.) en función del alma-
cenamiento útil
8 real Potencia máxima (MW)
9 real Eficiencia de carga (p.u.)
10 real Eficiencia de descarga (p.u.)
11 entero Tiempo máximo de regulación (h)
12 entero Flag para representación de almacenamiento en-
tre etapas:
0 = No representa;
1= Representa.
13 real Rampa de carga (MW/min)
14 real Rampa de descarga (MW/min)
119

SDDP MANUAL DE ARCHIVOS
13.2 Modificación de batería
Archivo ASCII denominado MBATTERYXX.DAT, ubicado en el directorio de datos del estudio, para
el sistema xx. Este archivo contiene las modificaciones a lo largo del estudio de los datos in-
formados en el archivo CBATTERYXX.DAT. El programa solo usa esta información si la configura-
ción es dinámica (registro 8 del archivo SDDP.DAT).
El primer registro indica la versión del archivo. En este punto, debe venir con el texto "$versión
1". El siguiente registro es un header, los restantes tienen el siguiente formato CSV (delimitado
por comas).
El formato de registro es similar a lo del archivo de configuración de la batería con 3 primeras
columnas que identifican la fecha de la modificación. Solo se pueden modificar los siguientes
campos: 1, 2, 3, 4, 5, 9, 12 y 13.
Column Type Description
1 entero Año
2 entero Mes
3 entero Día
4 entero Número de la batería
5 string Nombre de la batería:
Límite = 12 characteres.
6 entero Número de barra a la cual está conectada (en
caso de representación de la red de transmisión)
7 entero Tipo de la batería:
0 = Existente;
1 = Futura.
8 real Almacenamiento mínimo (MWh)
9 real Almacenamiento máximo (MWh)
10 real Almacenamiento inicial (p.u.) en función del al-
macenamiento útil
11 real Potencia máxima (MW)
12 real Eficiencia de carga (p.u.)
13 real Eficiencia de descarga (p.u.)
14 entero Tiempo máximo de regulación (h)
15 entero Flag para representación de almacenamiento
entre etapas:
0 = No representa;
1= Representa.
120

SDDP MANUAL DE ARCHIVOS
13.3  Tablas de carga y descarga de la batería
Conjunto de archivos ASCII ubicados en el directorio de datos del estudio. Cada archivo lla-
mado CHGBATXX.DAT contiene las tablas de consumo versus carga de las baterías que pertenecen
al sistema xx, también en formato CSV.
Cada archivo llamado DSGBATXX.DAT contiene las tablas de inyección versus descarga de las ba-
terías que pertenecen al sistema xx, también en formato CSV.
El primer registro indica la versión del archivo. En este punto, debe venir con el texto "$versión
1". El siguiente registro es un header, los restantes tienen el siguiente formato

| Column  | Type    | Description            |
| ------- | ------- | ---------------------- |
| 1       | entero  | Número de la batería   |
| 2       | string  | Nombre de la batería:  |
Límite = 12 characteres.
| 3   | real  | Consumo / Carga (p.u.)       |
| --- | ----- | ---------------------------- |
| 4   | real  | Inyección / Descarga (p.u.)  |
121

SDDP MANUAL DE ARCHIVOS
14 ANÁLISIS DE SENSIBILIDAD
El modelo puede efectuar análisis de sensibilidad automática con respecto a los siguientes
parámetros:
• variación de la demanda
• variación de los índices de disponibilidad de las térmicas
• variación de la hidrología
• variación de los costos de combustibles
Los datos de sensibilidad se indican en un archivo ASCII ubicado en el directorio de datos del
estudio y llamado SENSIB.DAT.
El primer registro es un header y es ignorado por el programa. El archivo tiene 3 tipos de
registro:
14.1 Registro tipo 1
Utilizado para representar las variaciones de la demanda
Campo Columna Tipo Descripción
1 1-12 A12 Palabra clave:
Load
2 14-17 I4 Número externo del sistema al cual se aplica el
factor de sensibilidad
3 19-22 I4 Ignorado
4 24-33 F10.0 Factor de sensibilidad (p.u.)
Observaciones:
• Si el campo 2 se deja en blanco entonces el factor de sensibilidad se aplica a todos los
sistemas.
• Pueden existir varios registros de este tipo. El último factor de sensibilidad prevalece so-
bre los anteriores.
14.2 Registro tipo 2
Utilizado para representar las variaciones de los índices de sensibilidad de las centrales térmi-
cas.
Campo Columna Tipo Descripción
1 1-12 A12 Palabra clave:
ThermalAvail
2 14-17 I4 Número externo del sistema al cual se aplica el
factor de sensibilidad
122

SDDP MANUAL DE ARCHIVOS
3 19-22 I4 Número externo de la central térmica a la cual se
aplica el factor de sensibilidad
4 24-33 F10.0 Factor de sensibilidad (p.u.)
Observaciones:
• Si los campos 2 y 3 se dejan en blanco entonces el factor de sensibilidad se aplica a todas
las centrales térmicas de todos los sistemas.
• Si el campo 3 se deja en blanco entonces el factor de sensibilidad se aplica a todas las
centrales térmicas del sistema indicado en el campo 2.
• Si se informan el campo 2 y el 3 entonces el factor de sensibilidad se aplica únicamente a
una central térmica.
• Pueden existir varios registros de este tipo. El último factor de sensibilidad prevalece so-
bre los anteriores.
14.3 Registro tipo 3
Utilizado para representar las variaciones de hidrología.
Campo Columna Tipo Descripción
1 1-12 A12 Palabra clave:
Inflow
2 14-17 I4 Ignorado
3 19-22 I4 Número externo de la estación hidrológica a la
cual se aplica el factor de sensibilidad
4 24-33 F10.0 Factor de sensibilidad (p.u.)
Observaciones:
• Si el campo 3 se deja en blanco entonces el factor de sensibilidad se aplica a todas las
estaciones hidrológicas.
• Pueden existir varios registros de este tipo. El último factor de sensibilidad prevalece so-
bre los anteriores.
14.4 Registro tipo 4
Utilizado para representar las variaciones de costo de combustible.
Campo Columna Tipo Descripción
1 1-12 A12 Palabra clave:
FuelCosts
2 14-17 I4 Número externo del sistema al cual se aplica el
factor de sensibilidad
123

SDDP MANUAL DE ARCHIVOS
3 19-22 I4 Número externo del combustible a l cual se aplica
el factor de sensibilidad
4 24-33 F10.0 Factor de sensibilidad (p.u.)
Observaciones:
• Si se dejan en blanco los campos 2 y 3 el factor de sensibilidad se aplica a todos los com-
bustibles de todos los sistemas.
• Si se deja en blanco el campo 3, el factor de sensibilidad se aplica a todos los combustibles
del sistema indicado en el campo 2.
124

SDDP MANUAL DE ARCHIVOS
15  FUNCIÓN DE COSTO FUTURO
Los archivos de Función de Costo Futuro (FCF) son archivos de acceso directo, producidos du-
rante el proceso de convergencia y denominados COSTYYXX.PSR. La extensión YY representa el
tipo de etapa, siendo YY = ME para etapas mensuales e YY = SE para etapas semanales. La se-
gunda extensión XX está asociada al tipo de estudio. Para estudios aislados y coordenados se
produce una FCF para cada sistema seleccionado, donde XX corresponde al identificador del
sistema como definido en el archivo SISTEM.DAT. Para estudios integrados se produce un único
archivo de FCF y la extensión XX se mantiene como parte de su nombre.
El contiene los siguientes registros.
15.1  Registro 1

| Campo  | Tipo  | Descripción                                |
| ------ | ----- | ------------------------------------------ |
| 1      | I*4   | Tamaño del registro del archivo de cortes  |
| 2      | I*4   | Número total de registros del archivo de   |
cortes
| 3   | I*4  | Campo que permite identificar con que ver- |
| --- | ---- | ------------------------------------------ |
sión fue salvado el archivo de FCF. En la ver-
sión corriente las siguientes opciones están
disponibles:
= 0: indica que fue utilizada precisión R*8
para salvar el archivo de FCF;
= 1: indica que fue utilizada precisión R*4
para salvar el archivo de FCF.
| 4   | I*4  | Número de plantas                       |
| --- | ---- | --------------------------------------- |
| 5   | I*4  | Número de embalses                      |
| 6   | I*4  | Número de embalses equivalentes         |
| 7   | I*4  | Orden máxima del modelo auto-regresivo  |
de caudales
| 8   | I*4  | Mes inicial del estudio donde fue creada la  |
| --- | ---- | -------------------------------------------- |
función de costo futuro
| 9   | I*4  | Año inicial del estudio donde fue creada la  |
| --- | ---- | -------------------------------------------- |
función de costo futuro
| 10  | I*4  | Numero de etapas                              |
| --- | ---- | --------------------------------------------- |
| 11  | R*8  | Límite inferior de la función objetivo de la  |
primera iteración
| 12  | I*4  | Número de la iteración                     |
| --- | ---- | ------------------------------------------ |
| 13  | R*8  | Valor del límite inferior en la iteración  |
| 14  | R*8  | Valor del límite superior en la iteración  |
125

SDDP MANUAL DE ARCHIVOS
| 15  | I*4  | Número de la iteración del mejor límite su- |     |     |
| --- | ---- | ------------------------------------------- | --- | --- |
perior
| 16  | R*8  | Valor del mejor límite superior             |     |     |
| --- | ---- | ------------------------------------------- | --- | --- |
| 17  | I*4  | Registro donde empiezan los cortes del pri- |     |     |
mer período
| 18  | I*4  | Registro donde empiezan los cortes del se- |     |     |
| --- | ---- | ------------------------------------------ | --- | --- |
gundo período
|          | ...  | ...                                        |     |     |
| -------- | ---- | ------------------------------------------ | --- | --- |
| 18+NPER  | I*4  | Registro donde empiezan los cortes del úl- |     |     |
timo período
15.2  Registro 2
Este registro contiene la información de las plantas/embalses en el siguiente formato.

| Campo  | Tipo  | Descripción                                  |     |     |
| ------ | ----- | -------------------------------------------- | --- | --- |
| 1      | I*4   | Número externo de la planta asociada al pri- |     |     |
mer embalse;
| 2   | I*4  | Número externo de la planta asociada al se- |     |     |
| --- | ---- | ------------------------------------------- | --- | --- |
gundo embalse;
| ...  | ...  | ...                                      |     |     |
| ---- | ---- | ---------------------------------------- | --- | --- |
| NR   | I*4  | Número externo de la planta asociada al  |     |     |
NR-ésimo embalse;
| NR+1     | I*4  | Número externo de la primera planta;    |     |     |
| -------- | ---- | --------------------------------------- | --- | --- |
| NR+2     | I*4  | Número externo de la segunda planta;    |     |     |
| ...      | ...  | ...                                     |     |     |
| NR+NP    | I*4  | Número externo de la NP-ésima planta.   |     |     |
| NR+NP+1  | I*4  | Número externo del primer embalse equi- |     |     |
valente;
| NR+NP+2  | I*4  | Número externo del segundo embalse equi- |     |     |
| -------- | ---- | ---------------------------------------- | --- | --- |
valente;
| ...       | ...  | ...              |                |          |
| --------- | ---- | ---------------- | -------------- | -------- |
| NR+NP+NE  | I*4  | Número  externo  | del  NE-ésimo  | embalse  |
equivalente.
15.3  Registro 3 en adelante...

| Campo  | Tipo  | Descripción                                 |     |     |
| ------ | ----- | ------------------------------------------- | --- | --- |
| 1      | I*4   | Pointer para el registro conteniendo el si- |     |     |
guiente corte de la etapa.
126

SDDP MANUAL DE ARCHIVOS
| 2   | I*4  | Número de la iteración donde el corte fue  |
| --- | ---- | ------------------------------------------ |
generado;
| 3   | I*4  | Este campo tiene de los informaciones:  |
| --- | ---- | --------------------------------------- |
Maxrev: apunta para el cluster del corte;
Caso contrario: indica la serie asociada al
corte.
| 4   | I*4  | Número de la serie hidrológica             |
| --- | ---- | ------------------------------------------ |
| 5   | I*4  | Número de iteraciones sucesivas en que el  |
corte está inactivo
| 6          | R*8  | RHS del corte                              |
| ---------- | ---- | ------------------------------------------ |
| ND campos  | R*8  | Coeficientes de los volúmenes por embalse  |
NP campos  R*8  Coeficientes de los caudales anteriores lag 1
por hidroeléctrica
NP campos  R*8  Coeficientes de los caudales anteriores lag 2
por hidroeléctrica
| ...  | ...  | ...  |
| ---- | ---- | ---- |
NP campos  R*8  Coeficientes de los caudales anteriores lag 6
por hidroeléctrica
| NE campos  | R*8  | Coeficientes de las energías almacenadas  |
| ---------- | ---- | ----------------------------------------- |
por embalses equivalente
| NE campos  | R*8  | Coeficientes de las energías afluentes por  |
| ---------- | ---- | ------------------------------------------- |
embalse equivalente lag 1
| NE campos  | R*8  | Coeficientes de las energías afluentes por  |
| ---------- | ---- | ------------------------------------------- |
embalse equivalente lag 2
| ...        | ...  | ...                                         |
| ---------- | ---- | ------------------------------------------- |
| NE campos  | R*8  | Coeficientes de las energías afluentes por  |
embalse equivalente lag 6
127

SDDP MANUAL DE ARCHIVOS
16 VOLUMEN INICIAL
El archivo VOLINI.DAT es un archivo CSV (Comma Separated Values) con su formato coincidente
con el formato de la salida de volumen final producido por el programa (VOLINI.CSV).
Las siguientes consideraciones deben ser observadas:
• Cuando el archivo de volumen inicial es dato de entrada para una recursión backward es
necesario la existencia de por lo menos un año completo de datos;
• Caso no existan datos para todas las series se hace un carrusel de las series dentro de una
misma etapa;
• Caso no existan datos para algunos años se repiten los datos del último año llevando en
consideración la estacionalidad;
• Para aquellos embalses con ausencia de datos en el archivo de volumen inicial se consi-
deran los datos de configuración.
Para una descripción detallada de sus funcionalidades referirse al Manual de Usuario.
Este archivo contiene los siguientes registros.
16.1 Registro 1
Registro de identificación del tipo de etapa y condición inicial del estudio.
Campo Descripción
1 Ignorado por el programa
2 Ignorado por el programa
3 Ignorado por el programa
4 Ignorado por el programa
5 Tipo de estudio:
= 1: semanal
= 2: mensual
6 Etapa inicial del estudio
7 Año inicial del estudio
16.2 Registro 2
Registro ignorado por el programa.
16.3 Registro 3
Registro de identificación del número total de embalses.
Campo Descripción
128

SDDP MANUAL DE ARCHIVOS
1 Ignorado por el programa
2 Número total de embalses
16.4 Registro 4
Registro de identificación de los embales.
Campo Descripción
1 Ignorado por el programa
2 Ignorado por el programa
3 Ignorado por el programa
4 Nombre de la planta hidroeléctrica asociada al primer embalse
5 Nombre de la planta hidroeléctrica asociada al segundo embalse
.. ….
N+3 Nombre de la planta hidroeléctrica asociada al N-ésimo embalse
16.5 Registro 5
Registro de identificación de datos de volúmenes iniciales.
Campo Descripción
1 Número de la etapa
2 Número de la serie
3 Número del bloque de demanda
4 Volumen inicial del primer embalse
5 Volumen inicial del segundo embalse
.. ….
N+3 Volumen inicial del N-ésimo embalse
129