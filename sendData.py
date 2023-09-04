




# Erstellen Sie eine E-Mail
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

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
