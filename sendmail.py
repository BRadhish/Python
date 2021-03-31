import smtplib 
import sys

subject = "no subject"
message = "no message"
if len(sys.argv) > 1:
	subject = sys.argv[1]

if len(sys.argv) > 2:
	message = sys.argv[2]

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
 
# Authentication 
password = "TODO" 
s.login("radhish401@gmail.com", password) 
  
# message to be sent 
subject = "mail subject"
text = "text"
message = 'Subject: {}\n\n{}'.format(subject, text)
  
# sending the mail 
s.sendmail("Mention service account", "radhish401@gmail.com", message) 
  
# terminating the session 
s.quit() 
