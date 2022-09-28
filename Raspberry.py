import sys              
import Adafruit_DHT     # Biblioteca do DHT22
import mhz_19           # Biblioteca do sensor de CO2
import csv              # Biblioteca de arquivos csv
import time             # Biblioteca de tempo
import adafruit_ccs811  # Biblioteca do CCS811
import board            # Biblioteca de pinos do Raspberry
import busio            # Biblioteca de entrada serial
import locale           # Biblioteca de Data
import picamera         # Biblioteca exclusiva do Raspberry usada para a Camera
import RPi.GPIO as GPIO # Biblioteca do Raspberry para GPIos

# Balanças
EMULATE_HX711=False     # relacionado ao HX711
referenceUnit = 1
if not EMULATE_HX711:
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

hx = HX711(5, 6)                        # Portas conectas ao raspberry
hx.set_reading_format("MSB", "MSB")     # Como será feita a leitura
hx.set_reference_unit(referenceUnit)    # Referencia da tara
hx.reset()                              # inicia as balanças
hx.tare_A()                             # Tara da balança A
hx.tare_B()                             # Tara da balança B

# TEMT 6000
GPIO.setmode(GPIO.BCM)                  # Seta a entrada Usb para leitura
GPIO.setup(12, GPIO.IN)                 # 

# DATA
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')                  # Modificando o Formato da Data

# CCS811
i2c_bus = busio.I2C(board.SCL, board.SDA)                       # SCL GPIO3 e SDA GPIO 2
ccs811 = adafruit_ccs811.CCS811(i2c_bus)
while not ccs811.data_ready:                                    # Espera o Sensor ficar pronto
    pass

# Camera
camera = picamera.PiCamera()                                    # Atribui uma variavel para praticidade
camera.start_preview()                                          # abre  uma visualização da Camera
time.sleep(30)                                                  # Tempo para visualizar
camera.stop_preview()                                           # Fecha a visualização

cabecalho = ['NumF', 'Temp', 'Umid', 'ECO2', 'TVOC','mhz_co2','peso','Data']  # Simplificando a o arquivo CSV
NumFoto = 0                                                                   # Zera um auxiliar para nomear/contar as fotos

while True:
    NumFoto = NumFoto + 1  # Contador de fotos
    # Coleta dos dados
    Ultimafoto = camera.capture('Foto_{}.bmp'.format(NumFoto), 'bmp')       # Captura a imagem
    umidade, temperatura = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 17)  # Umidade e Temperautra - DHT 22 e GPIO 17 (pino 11)
    Carbonico = ccs811.eco2                                                 # Equivalente CO2
    Organico = ccs811.tvoc                                                  # Total Volatile Organic Composture
    Data = time.strftime('%c', time.localtime())                            # Data
    co2mhz = mhz_19.read()                                                  
    co2mhz = co2mhz['co2']                                                  # CO2 
    peso_A = hx.get_weight_A(5)                                             # Peso Balança A
    peso_B = hx.get_weight_B(5)                                             # Peso Balança B
    
    # Abre o arquivo csv para escrita
    with open('Medicao.csv', 'a+') as arquivo_csv:                            
        escrever = csv.DictWriter(arquivo_csv, fieldnames=cabecalho, delimiter=';', lineterminator='\n')    # Parâmetros do arquivo csv
        escrever.writerow({                                                                                 # Escrevendo os Dados
            'NumF': '{0}'.format(NumFoto),                                                                  # Número da foto
            'Temp': '{0:0.2f}C'.format(temperatura),                                                        # Temperatura
            'Umid': '{0:0.2f}%'.format(umidade),                                                            # Umidade
            'ECO2': '{0:0.2f}'.format(Carbonico),                                                           # CO2
            'TVOC': '{0:0.2f}'.format(Organico),                                                            # TVOC
            'mhz_co2': '{0:0.2f}'.format(co2mhz),                                                           # CO2
            'peso': '{0:0.2f}'.format(peso_A),                                                              # Peso A
            'peso': '{0:0.2f}'.format(peso_B),                                                              # Peso B
            'Data': '{0}'.format(Data)})                                                                    # Data
    arquivo_csv.close()                                                                                     # Fecha o arquivo csv
    
    hx.power_down()           # Desliga e Liga a Balança
    hx.power_up()
    time.sleep(1800)          # 30 min Entre Amostras