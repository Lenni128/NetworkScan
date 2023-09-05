import nmap
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendData():
    # Erstellen Sie eine E-Mail
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Lesen Sie den Inhalt der Datei
    with open("../../gefundene_ips.txt", "r") as file:
        file_content = file.read()

    # Fügen Sie den Dateiinhalt zur E-Mail hinzu
    message.attach(MIMEText(file_content, 'plain'))

    # Verbindung zum SMTP-Server von web.de herstellen und E-Mail senden
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("E-Mail mit der Datei wurde erfolgreich über web.de gesendet.")
    except Exception as e:
        print("Fehler beim Senden der E-Mail:", str(e))



#E-Mail-Konfiguration für web.de
smtp_server = 'smtp.web.de'
smtp_port = 587  # TLS-Port für web.de
smtp_username = 'megablack1@web.de'  # Ihre web.de-Adresse
smtp_password = '20kons08'  # Ihr web.de-Passwort

sender_email = 'megablack1@web.de'  # Ihre web.de-Adresse
receiver_email = 'peterslennart7@gmail.com'  # E-Mail-Adresse des Empfängers
subject = 'Gefundene IPs'  # Betreff Ihrer E-Mail

# Befehl ausführen, um die IP-Adresse von eth0 zu erhalten
eth0_ip = subprocess.check_output("ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1", shell=True)
eth0_ip = eth0_ip.decode("utf-8").strip()

# Die Netzwerkmaske auf /24 (Standard-Subnetzmaske für die meisten Heimnetzwerke) setzen
subnet_mask = "/24"

# Die IP-Adresse des Routers im Netzwerk ermitteln (Gateway)
# in der Regel ist der Router die erste IP-Adresse im Subnetz (xxx.xxx.xxx.1)
parts = eth0_ip.split('.')
parts[-1] = '1'  # Setzen Sie das letzte Teil der IP-Adresse auf 1, um den Router darzustellen
router_ip = '.'.join(parts)

# Die Netzwerkadresse erstellen, indem Sie die IP-Adresse des Routers und die Subnetzmaske kombinieren
network_address = router_ip + subnet_mask
print("Netzwerkadresse:", network_address)

# Erstellen Sie einen Nmap-Scanner
scanner = nmap.PortScanner()

# Führen Sie den Nmap-Scan durch
scanner.scan(hosts=network_address, arguments="-sn")


# Öffnen Sie eine Datei zum Schreiben der gefundenen IP-Adressen
with open("../../gefundene_ips.txt", "w") as file:
    file.write("  Netzwerkadresse: " + network_address + "\n")
    file.write("  IP-Adresse des Routers: " + router_ip + "\n\n")
    for host in scanner.all_hosts():
        file.write(host + "\n")
        print("Gefundene IP-Adresse:", host)

print("Scan abgeschlossen. Gefundene IP-Adressen wurden in 'gefundene_ips.txt' gespeichert.")

sendData()

