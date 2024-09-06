import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Check for command line arguments
if len(sys.argv) < 2:
    print("Usage: python send_email.py '<alert_message>'")
    sys.exit(1)

# Email credentials and recipient
sender_email = "honeyfilealert@gmail.com"
receiver_email = 'abdulrahmanyusuf2002@gmail.com' #"ummukulthum2710@gmail.com"
password = "stfnqyiijcpgctka"

# Email body from command line argument
alert_message = sys.argv[1]

# Setup the MIME
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = "Decoy File Access Alert"
message.attach(MIMEText(alert_message, 'plain'))

# Create secure connection with server and send email
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")
