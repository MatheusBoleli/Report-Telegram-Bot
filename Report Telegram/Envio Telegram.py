from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, glob, pandas as pd, os, telegram, matplotlib.pyplot as plt
from datetime import datetime, timedelta

tempo = datetime.now()
timestamp, timestamp_relatorio, timestamp_hist = tempo.strftime('%d-%m-%Y'), tempo.strftime('%d-%m %H:%M'), tempo.strftime('%H:00')

diretorio = "dir/raiz"

#token that can be generated talking with @BotFather on telegram
my_token = 'token do bot do telegram'

SLA = '20'
login_callcenter = 'usuario'
pwd_callcenter = 'senha'

# INICIANDO A BUSCA DO RELATORIO NO SITE
chrome_options = webdriver.ChromeOptions()
chromedriver = diretorio+"driver/chromedriver.exe"
prefs = {"download.default_directory": r"C:\Users\matheus\Desktop\Report Telegram"}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
  
def wait_xpath_click(y):
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, y))).click()
    
def send(msg, chat_id, token=my_token):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)
    
driver.get("callcenter.com.br")

driver.find_element_by_name('nome').send_keys(login_callcenter)
driver.find_element_by_name('pwd').send_keys(pwd_callcenter)

wait_xpath_click('//*[@id="page"]/form/div[2]/input[3]')

wait_xpath_click('//*[@id="Aba_2"]')

wait_xpath_click('//*[@id="menu_lateral"]/ul/li[3]/a')

wait_xpath_click('//*[@id="show_filtro"]')

time.sleep(5)
driver.find_element_by_name('dataIni').clear()
driver.find_element_by_name('dataIni').send_keys(timestamp)

driver.find_element_by_name('sla').clear()
driver.find_element_by_name('sla').send_keys(SLA)

time.sleep(5)
wait_xpath_click('//*[@id="filtro_conteudo"]/table/tbody/tr[5]/td/input[1]')

time.sleep(5)
wait_xpath_click('//*[@id="tabListas_11"]')

time.sleep(5)
wait_xpath_click('//*[@id="listaDetalhes"]/table/tbody/tr[3]/td/a[2]')

time.sleep(10)

teste = glob.glob(diretorio+'*.csv')

for file in teste:
    if file.startswith('RC-Consolidado'):
        file = file

header = ['A','B','C','D','E']
df = pd.read_csv(file, names=header, encoding = "ISO-8859-1", sep=";")
df = df[['A','B']]

ok = '\U00002705'
not_ok = '\U0000274C'
close_ok = '\U000026A0'

#------------------VERIFICA O SLA DO NIVEL DE SERVIÇO
nds = df.values[11][1]
nds = nds.replace(",",".")
nds = float(nds[:-1])
sla_nds = 80
sla_int = 69

if nds > sla_nds:
    nds = ok
elif nds > sla_int and nds < sla_nds:
    nds = close_ok
else:
    nds = not_ok
    
#------------------VERIFICA O SLA DO NIVEL DE ABANDONO
abn = df.values[8][1]
abn = abn.replace(",",".")
abn = float(abn[:-1])
sla_abn = 5
sla_abn_int = 10

if abn < sla_abn:
    abn = ok
elif abn > sla_abn and abn < sla_abn_int:
    abn = close_ok
else:
    abn = not_ok
    
#------------------VERIFICA O SLA DO TMA
def time_sla(campo_df, campo_sla, int_sla):
    tma = datetime.strptime(campo_df, '%H:%M:%S')
    
    tma_sla = datetime.strptime(campo_sla, '%H:%M:%S')
    
    tma_sla_int = datetime.strptime(int_sla, '%H:%M:%S')
    
    if tma < tma_sla:
        return ok
    elif tma > tma_sla and tma < tma_sla_int:
        return close_ok
    else:
        return not_ok
    
    
tma = time_sla(df.values[9][1], '00:07:00','00:09:59')
tme = time_sla(df.values[10][1], '00:00:20','00:30:00')

message = '''Report Atendimento - %s \n
Chamadas recebidas: %s \n
%s Nivel de Serviço/dia: %s \n
%s Abandono: %s              \n
%s Tempo médio de Atendimento/dia: %s  \n
%s Tempo médio de Espera/dia: %s ''' % (timestamp_relatorio, 
                                        df.values[4][1],
                                        nds, df.values[11][1], 
                                        abn, df.values[8][1],  
                                        tma, df.values[9][1], 
                                        tme, df.values[10][1])

send(message, "group or user id")

os.remove(file)
driver.close()
driver.quit() 





# %%
