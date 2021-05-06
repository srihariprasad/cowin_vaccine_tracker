import sys
import datetime 
from cowin_api import CoWinAPI
import subprocess                                                                
import os.path                                                                   
import smtplib                                                                   
import getpass  
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

global toString
toString = "username@company.com"

def send_report_mail(report,subject,tostring):
    sender = "xyz@xyz.com"
    receivers_str = tostring
    receivers_list = tostring.split(",")
  
    filep = open(report,"r")
    lines_list = filep.readlines()
    data_lines = ""
    for line in lines_list:
        data_lines = data_lines + line.strip();
    filep.close()

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = tostring
    message['Subject'] = subject
 
    message.attach(MIMEText(data_lines,"html"))

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers_list, message.as_string())
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")

def prepare_report(centers):
   global toString
   report  = "report_vaccine.html"
   subject = "Vaccine Availability in Bangalore"
                                                                                
   HTML = open(report,"w")
   HTML.write(" \
           <html> \
           <head> \
           <title>"+subject+"</title> \
	   <style>\
        	table, th, td {\
            		border: 1px solid black;\
            		border-collapse: collapse;\
                } \
		th, td { \
            		padding: 5px;\
            		text-align: left;\
        	}\
    	   </style>\
           </head> \
           <body> \
           <p>")
   HTML.write("Hi,")
   HTML.write("<br>  \
           <br>  \
           Latest vaccine availability...\
           <br> \
           <div> \
           <table style=\"width:100%\"> \
           <tr><td><b>Center</b></td><td><b>Address</b></td><td><b>Pincode</b></td><td><b>Availability</b></td><td><b>Vaccine</b></td><td><b>Slots</B></td></tr>")

   for each_center in centers:
        c_name = each_center['name']
        c_address = each_center['address']
        c_pincode = each_center['pincode']
        c_feetype = each_center['fee_type']
        c_sessions = each_center['sessions'] 
        for each_session in c_sessions: 
            if each_session['available_capacity'] > 0: 
               print("center: "+c_name+"  date: "+each_session['date']+"  availability: "+str(each_session['available_capacity'])+ "  age: "+str(each_session['min_age_limit'])+" vaccine: "+each_session['vaccine']+" slots: "+str(each_session['slots'])) 
               HTML.write("<font color=\"blue\"><tr><td><b>"+c_name+"</b></td><td>"+c_address+"</td><td>"+str(c_pincode)+"</td><td>"+str(each_session['available_capacity'])+"</td><td>"+each_session['vaccine']+"</td><td>"+str(each_session['slots'])+"</td></tr></font>")
   HTML.write(" \
           </table> \
           </div> \
           <div><p> \
           <br> \
           </p> \
           </div> \
           </body> \
           </html>")
   HTML.close()

   tostring = toString
   send_report_mail(report,subject,tostring)

if __name__ == "__main__" :

    if len(sys.argv) > 2:
        print("INVALID Arguments passed !!!")
        print("Correct usage :-> python cowin_tracker.py <pincode>")
        print("For whole bangalore: -> python cowin_tracker.py")
        sys.exit(1)

    cowin = CoWinAPI()

    #states = cowin.get_states()

    current_time = datetime.datetime.now() 
    date_t = str(current_time.day)+"-"+str(current_time.month)+"-"+str(current_time.year)

    print("today is :"+date_t)

    min_age_limit = 45  # Optional. By default returns centers without filtering by min_age_limit 

    if len(sys.argv) == 2:
        pin_code = sys.argv[1]
        date_t = "07-05-2021"
        print("Getting data for pincode:"+str(pin_code))
        available_centers = cowin.get_availability_by_pincode(pin_code, date_t, min_age_limit)
    else:
        district_id = 265
        available_centers = cowin.get_availability_by_district(district_id, date_t, min_age_limit)

    centers = available_centers['centers']

    prepare_report(centers)

