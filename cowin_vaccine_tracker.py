########################################################################################
#
#   Srihari
#   05/05/2021
#
#######################################################################################

import sys
import datetime 
from cowin_api import CoWinAPI

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

    for each_center in centers:
        c_name = each_center['name']
        c_address = each_center['address']
        c_pincode = each_center['pincode']
        c_feetype = each_center['fee_type']
        c_sessions = each_center['sessions']
        for each_session in c_sessions:
            if each_session['available_capacity'] > 0:
                print("center: "+c_name+"  date: "+each_session['date']+"  availability: "+str(each_session['available_capacity'])+ "  age: "+str(each_session['min_age_limit'])+" vaccine: "+each_session['vaccine']+" slots: "+str(each_session['slots']))

