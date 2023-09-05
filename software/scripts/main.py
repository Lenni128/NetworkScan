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
    with open("../../found_ips.txt", "r") as file:
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
        print("Send e-mail successfully")
    except Exception as e:
        print("Error by sending the e-mail:", str(e))


# Config for web.de
smtp_server = 'smtp.web.de'
smtp_port = 587  # TLS-Port
smtp_username = 'YOUR_USERNAME'  # YOUR USERNAME
smtp_password = 'YOUR_PASSWORD'  # YOUR PASSWORD

sender_email = 'YOUR_EMAIL'  # YOUR_EMAIL
receiver_email = 'RECEIVER_EMAIL'  # RECEIVER_EMAIL
subject = 'Found IPs'  # Betreff Ihrer E-Mail

interface = "eth0"

eth0_ip = subprocess.check_output("ip addr show " + interface + "| grep 'inet ' | awk '{print $2}' | cut -d'/' -f1",
                                  shell=True)

eth0_ip = eth0_ip.decode("utf-8").strip()

subnet_mask = "/24"

# The IP address of the router on the network (Gateway)
# in the Rule the Router is the first IP-Address in the Subnet (xxx.xxx.xxx.1)
parts = eth0_ip.split('.')
parts[-1] = '1'
router_ip = '.'.join(parts)

# create a network address by combining the router IP address and the subnet mask
network_address = router_ip + subnet_mask
print("Networkadress:", network_address)

#create a new nmap scanner
scanner = nmap.PortScanner()

# scan the network for hosts
scanner.scan(hosts=network_address, arguments="-sn")

# open a file to write the found IP addresses to
with open("../../found_ips.txt", "w") as file:
    file.write("Interface: " + interface + "\n")
    file.write("  Networkadress: " + network_address + "\n")
    file.write("  IP from the router: " + router_ip + "\n\n")
    for host in scanner.all_hosts():
        file.write(host + "\n")
        print("Found IPs:", host)

print("Scan Completed.")

sendData()
