import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import smtplib, ssl

url = #<Some-web-site>
username = #<Email> #Username for login to the website
password = #<Password>
msg = ''

#Use Firefox as a driver to open the website and login
#1: modify it to do logging in without openning the browser
options = Options()
options.add_argument("--headless")

#2: Specify Firefox path
binary = FirefoxBinary(r'Path\To\Firefox\Mozilla Firefox\firefox.exe')

#3: Adding parameters to init the driver, in addition to 
#Path to geckodriver, you can download it from here:
#https://github.com/mozilla/geckodriver/releases
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'Path\To\geckodriver.exe', options=options)
log = driver.get(url)

#Find the IDs of the user and passwd using Inspect Element
user = driver.find_element_by_id("username")
passwd = driver.find_element_by_id("password")
#Add the above parameters (username & password) to the fields
user.send_keys(username)
passwd.send_keys(password)
#Find the ID of the submit button and click on it
driver.find_element_by_name("login").click()
#Wait some time to load the page (depending on your bandwidth) 
time.sleep(15)
#Click on some navigation button using the XPath on the page 
driver.find_element_by_xpath("/html/body/div[1]/div").click()
time.sleep(10)
#Now grab a table in the page 
mytable = driver.find_element_by_css_selector('table.<Selector>')

#Loop over rows and columns of the table
for row in mytable.find_elements_by_css_selector('tr'):
    c = 0
    row = []
    for cell in row.find_elements_by_tag_name('td'):
        c = c + 1
        #Add each cell of the row 
        row.append(cell.text)
        #Match the columns to print each row in a line 
        if c == #<No. of columns per row>:
            #row[7] is a #Date for a row in a table
            date = row[7].format().split()[0]
            day = int(date.split('/')[1])
            month = int(date.split('/')[0])
            year = int(date.split('/')[2])
            time = row[7].format().split()[1]
            hour = int(time.split(':')[0])
            min = time.split(':')[1]
            mid = row[7].format().split()[2]
            #Match the row that has today's date
            if int(datetime.datetime.now().strftime("%Y")) == year and int(datetime.datetime.now().strftime("%m")) == month and int(datetime.datetime.now().strftime("%d")) == day:
                #Match the row that is initiated since less than 15 minutes 
                if int(datetime.datetime.now().strftime("%I")) - hour < 1 and int(datetime.datetime.now().strftime("%M")) - min < 15:
                    name = row[0].format()
                    No = row[1].format()
                    project = row[5].format()
                    date = row[6].format()
                    priority = row[8].format()
                    #Add the row to message structure
                    msg = msg + 'Title:  ' + name + '\nProject:  ' + project + '\nPriority: ' + priority + '\nDate:  ' + date + '\n===============================================================================\n'

#Initiate an email and send it using a gmail account
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = #<Sender-mail>
receivers = #<Some-Receiver>, <Some-Receiver>
message = "\r\n".join(["Subject: #<Subject>", '', msg])
#Use SSL 
context = ssl.create_default_context()
#Send the message
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receivers, message)
