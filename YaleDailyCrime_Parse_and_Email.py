from datetime import datetime, timedelta
import os
import requests
from tika import parser
import smtplib
import kbnasettings

# create url for recent crime report PDF
# use yesterday's date
date = datetime.now() - timedelta(days=1)
formatted_date = datetime.strftime(date, "%m%d%y")
url = "https://your.yale.edu/sites/default/files/daily-crime-log/" + \
    formatted_date + ".pdf"

# create local save path
save_dir = r"C:\Users\Carson J Bryant\Desktop\Py Scripts\YaleDailyCrime"
pdf_path = os.path.join(save_dir, formatted_date + ".pdf")

# request url to see if it exists
# if so, open the file and write it into "path"
response = requests.get(url)
if response.status_code == 200:
    with open(pdf_path, 'wb') as output_file:
        output_file.write(response.content)
else:
    # if file does not exist, quit
    print("Response Code: " + response.status_code)
    # rewrite as main() function return
    raise SystemExit(0)

# parse PDF text and print it
parsed = parser.from_file(pdf_path)
content = parsed['content']
# strip leading newlines
content = content.lstrip('\n')
print(content)

# save text locally
txt_path = os.path.join(save_dir, formatted_date + ".txt")
with open(txt_path, 'w') as output_file:
    output_file.write(content)
    output_file.close()

# send email
email_address = kbnasettings.SENDER_ADDRESS
email_password = kbnasettings.SENDER_PASS
target_address = "carson.bryant@yale.edu"
try:
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(email_address, email_password)
except RuntimeError:
    print("Login failed.")
else:
    print("Login successful.")
    subject = "{} Yale Daily Crime Log".format(
        datetime.strftime(date, "%Y-%m-%d"))
    message = "Subject: {}\n\n{}".format(subject, content)
    smtpserver.sendmail(from_addr=email_address, to_addrs=target_address,
                        msg=message)
    print("Sent message with subject \"{}\"".format(subject))
    smtpserver.quit()
    # if email was sent, delete tmp file
    os.remove(txt_path)

# delete files
#os.remove(pdf_path)
