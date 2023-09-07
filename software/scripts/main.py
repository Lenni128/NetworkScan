import nmap
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration for the SMTP server
smtp_server = 'smtp.web.de'
smtp_port = 587  # TLS port
smtp_username = 'YOUR USERNAME'  # Your username
smtp_password = 'YOUR PASSWORD'  # Your password

# Sender and receiver email addresses along with subject
sender_email = 'SENDER_EMAIL'
receiver_email = 'RECEIVER_EMAIL'
subject = 'Found IPs'

# Network interface and IP information
interface = "wlp2s0"  # normal is "eth0" by raspberry pi 4
eth0_ip = subprocess.check_output("ip addr show " + interface + "| grep 'inet ' | awk '{print $2}' | cut -d'/' -f1",
                                  shell=True)
eth0_ip = eth0_ip.decode("utf-8").strip()
subnet_mask = "/24"

# IP address of the router on the network (Gateway)
parts = eth0_ip.split('.')
parts[-1] = '1'
router_ip = '.'.join(parts)

# Create the network address by combining the router IP address and the subnet mask
network_address = router_ip + subnet_mask
print("Network address:", network_address)

# Create a new Nmap scanner
scanner = nmap.PortScanner()

# Scan the network for hosts
scanner.scan(hosts=network_address, arguments="-sn")

# Open a file to write the found IP addresses
with open("../../found_ips.txt", "w") as file:
    file.write("Interface: " + interface + "\n")
    file.write("Network address: " + network_address + "\n")
    file.write("Router IP: " + router_ip + "\n\n")
    for host in scanner.all_hosts():
        file.write(host + "\n")
        print("Found IPs:", host)

print("Scan completed.")

# Check if the email has been sent already
email_sent = False


def send_data():
    global email_sent
    # Create an email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Read the content of the file
    with open("../../found_ips.txt", "r") as file:
        file_content = file.read()

    # Attach the file content to the email
    message.attach(MIMEText(file_content, 'plain'))

    # Connect to the web.de SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully")
        email_sent = True  # Set the flag to indicate that the email has been sent
    except Exception as e:
        print("Error sending the email:", str(e))


# Check if the email has already been sent before sending it again
if not email_sent:
    send_data()
