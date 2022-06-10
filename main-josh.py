# -*- coding: utf-8 -*-
"""

@author:Dilip Nikhil 
"""
import logging
from datetime import datetime,date
logging.basicConfig(filename="log.txt",
                    level='INFO',
                    filemode='w',
                    format='%(asctime)s--%(levelname)s--%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logfile = open("log.txt","w")

try:
    from PIL import Image,ImageTk
    from pymongo import MongoClient
    import urllib
    import time
    import keyboard
    from tkinter import *
    import tkinter.messagebox as tkmb
    import cv2
    import face_recognition
    import os
    import sys
    import numpy as np
    import tkinter.messagebox as tkmb
    import time
    import datetime
    from ctypes import windll
    import bcrypt
    import smtplib,ssl
    import getpass
    from email.message import EmailMessage
    import os
    import urllib
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    from yolo_helper import YoloV3, load_darknet_weights, draw_outputs
    yolo = YoloV3()
    load_darknet_weights(yolo, 'yolov3.weights')
    logging.info("Import Successful")
    
except Exception as ex:
    logfile.write("Package Import Error"+str(ex))


def read_config(key):
    try:
        fp = open(os.path.join(os.getcwd(), "configuration.txt"))
        RawContent = fp.readlines()
        Content = [i.strip("\n") for i in RawContent]
        for line in Content:
            if line.split(";")[0] == key:
                value = line.split(";")[1]
        fp.close()
        return value
    except Exception as ex:
        logfile.write("Config File Error"+str(ex))

password="cssJavascript"
mongo_uri=(read_config("mongo_uri").replace("<password>",password))
taskbar = windll.user32.FindWindowA(b'Shell_TrayWnd', None)

try:
    cluster = MongoClient(mongo_uri)
    db=cluster[str(read_config("db"))]
except Exception as ex:
    logfile.write("MongoDB Connection:"+str(ex))



global user_data,login_time,today,project_name,project_id

try :
    def user_login():
        windll.user32.ShowWindow(taskbar, 0)   ## hide the taskbar
        #windll.user32.ShowWindow(taskbar, 9) # show 
        login_window=Tk()
        login_window['bg'] = '#0059b3'
        login_window.attributes('-alpha',0.90)
        login_window.attributes('-toolwindow', True)
        login_window.withdraw()
        login_window.attributes('-topmost',True)
        login_window.eval('tk::PlaceWindow . center')
        login_window.title(read_config("login_Window"))
        windowWidth = 200
        windowHeight = 200
        positionRight = int(login_window.winfo_screenwidth()/2.7 - windowWidth/2)
        positionDown = int(login_window.winfo_screenheight()/2 - windowHeight/2)
        login_window.geometry('600x250+{}+{}'.format(positionRight, positionDown))
        login_window.resizable(width=False, height=False)
        l1=Label(login_window,text="User ID:",font=('Times New Roman', 20, 'bold'), bg="#0059b3", fg='White')
        l2=Label(login_window,text='Password:',font=('Times New Roman', 20, 'bold'), bg="#0059b3", fg='White')
        l1.grid(row=1,column=0,padx=30,pady=15)
        l2.grid(row=2,column=0,padx=60,pady=15)
        global user_id,password,violation
        user_id=StringVar()
        password=StringVar()
        t1=Entry(login_window,textvariable=user_id,font=3)
        t1.focus()
        t2=Entry(login_window,textvariable=password,font=3,show='*')
        t1.grid(row=1,column=1,padx=30,pady=15)
        t2.grid(row=2,column=1,padx=30,pady=15)
        def on_closing():
            if tkmb.askokcancel("Quit", "Do you really want to quit the application?"):
                login_window.destroy()
                windll.user32.ShowWindow(taskbar, 9)

        def validate_creds():  
            global user_id,pwd
            # Function to validate the user credentials
            user_id=user_id.get()
            pwd=password.get().encode("utf-8")
            credentials = db.master.find_one({"user_id": user_id})
            if credentials != None:
                stored_password=db.master.find_one({"user_id":user_id},{"password":1})
                if bcrypt.checkpw(pwd,stored_password["password"]):
                    try:
                        tkmb.showinfo(title="Authentication ", message="User Authentication Successfull")
                        logging.info("User Authentication Successful")
                        login_window.destroy()
                        agreement()
                    except Exception as ex:
                        logfile.write("validate_creds  "+str(ex))
                else:
                    tkmb.showerror(title='Login Error', message="Please check your User-ID/Password!!")
            else:
                tkmb.showerror(title='Error', message="Please Check your User-ID/Password!!")
       
        def on_cancel():
            status=tkmb.askyesno(title="Question",message="Do you really want to close the window")
            if status==True:
                login_window.destroy()
                windll.user32.ShowWindow(taskbar, 9)
            else:
                tkmb.showwarning("Warning ","Please login again")   
        login_window.protocol("WM_DELETE_WINDOW", on_closing)
        b1=Button(login_window,command=validate_creds,text='Login',font=('Times New Roman', 15, 'bold'), fg='Green', height = 1, width = 13)
        b2=Button(login_window,command=on_cancel,text='Cancel',font=('Times New Roman', 15, 'bold'), fg='Blue', height = 1, width = 13)
        b1.grid(row=3,column=0,sticky=W, padx=60,pady=30)
        b2.grid(row=3,column=1,sticky=E, padx=60,pady=30)
        login_window.mainloop()
    
except Exception as ex:
    logfile.write("User Login"+str(ex))
    windll.user32.ShowWindow(taskbar, 9)
    sys.exit()

def agreement():
    agree_window = Tk()
    agree_window.attributes('-toolwindow', True)
    agree_window['bg'] = 'dark gray'
    var = StringVar()
    label = Label(agree_window , textvariable = var,font=('Times New Roman',10),bg='dark gray')
    var.set("\n\n I hereby provide Hexaware Technologies the permission to collect process and store my live monitoring \n activities during my official working hours for the sole purpose of verifying my identity.\
            \n\n Your collected information will only be shared with your organization or firm.\
                \n\n By pressing Agree, I confirm my consent, agreement and acknowledgment as described above.")
    agree_window.title(read_config("Agreement"))
    windowWidth = 720
    windowHeight = 180
    global width, height
    width=agree_window.winfo_screenwidth()
    height=agree_window.winfo_screenheight()
    positionRight = int(width/2 - windowWidth/2)
    positionDown = int(height/2 - windowHeight/2)
    agree_window.geometry('740x200+{0}+{1}'.format(positionRight, positionDown))
    agree_window.resizable(width=False, height=False)
    def on_agree():
        tkmb.showinfo(title="Facial Authentication",message=" Routing to Facial Authentication.\n\nNote: Please make sure there is optimum lighting in the room before proceeding to Facial Authentication.")
        agree_window.destroy()
        facial_recognition()
    def on_cancel():
        status=tkmb.askyesno(title="Question",message="Do you really want to close the application?")
        if status==True:
            agree_window.destroy()
            windll.user32.ShowWindow(taskbar, 9)
        else:
            tkmb.showwarning("Warning Message","Please accept agreement policy to continue further.")
    # Create Buttons in the frame
    button1 = Button(agree_window, command=on_agree,text="Agree",font=('Times New Roman', 12, 'bold'), width=15, height=1)
    button1.place(x=125, y=150)
    button2 = Button(agree_window, command=on_cancel,text="Deny",font=('Times New Roman', 12, 'bold'), width=15, height=1)
    button2.place(x=480, y=150)
    label.pack()
    agree_window.mainloop()


def facial_recognition():
    try:
        facial_data = []
        names = []
        for x in db["master"].find({"role":"agent"}, {"_id": 0, "user_id": 1, "facial_data": 1}):
            facial_data.append(np.array(x["facial_data"]))
            names.append(x["user_id"])
        cap = cv2.VideoCapture(0)
        winname = "Facial Authentication"
        # present time + 15 seconds
        close_time = time.time() + 15
        flag = True
        while True:
            while flag:
                # if faical registration doesnt happen withing 15 seconds, exit the loop
                if time.time() < close_time: 
                    success, img = cap.read()
                    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                    faces_in_frame = face_recognition.face_locations(imgS)
                    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
                    # Move it to (40,30)
                    cv2.namedWindow(winname, cv2.WINDOW_KEEPRATIO)  # Create a named window
                    cv2.moveWindow(winname, 470, 160)
                    cv2.imshow(winname, img)
                    cv2.resizeWindow(winname, 600, 520)
                    for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
                        matches = face_recognition.compare_faces(facial_data, encode_face)
                        faceDist = face_recognition.face_distance(facial_data, encode_face)
                        matchIndex = np.argmin(faceDist)
                        if matches[matchIndex]:
                            agent_name = names[matchIndex].upper().lower()
                            if agent_name == user_id.upper().lower():
                                y1, x2, y2, x1 = faceloc
                                # since we scaled down by 4 times
                                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                                # Throw a pop up if facial registration is successful
                                for i in matches:
                                    if i == True:
                                        time.sleep(1)
                                        flag = False
                                        cv2.destroyAllWindows()
                                        Face_rec_Window = Tk()
                                        Face_rec_Window.withdraw()
                                        tkmb.showinfo(title="Authentication Successful",
                                                      message=" Facial Authentication Successful !!\n Hello " + str(
                                                          user_id.upper()) + " , you will now be logged into Live Monitoring.")
                                        logging.info("Facial Authentication Successful")
                                        windll.user32.ShowWindow(taskbar, 9)
                                        Face_rec_Window.destroy()
                                        daily_session_login(user_id)
                                        break
                            else:
                                Face_err_Window = Tk()
                                Face_err_Window.withdraw()
                                tkmb.showerror(title='Authentication Unsuccesful',
                                               message="Terminating the application")
                                windll.user32.ShowWindow(taskbar, 9)
                                Face_err_Window.destroy()
                                sys.exit()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        windll.user32.ShowWindow(taskbar, 9)
                        break
                # Throw a pop up if its not successful
                else:
                    cv2.destroyAllWindows()
                    flag = False
                    Face_auth_Window = Tk()
                    Face_auth_Window.withdraw()
                    tkmb.showerror(title='Authentication Unsuccesful',
                                   message="Please make sure there is optimum lighting for the facial authentication to work")
                    windll.user32.ShowWindow(taskbar, 9)
                    Face_auth_Window.destroy()
                    user_login()
                    break
            break
    except Exception as ex:
        logfile.write("facial_recognition-->"+str(ex))
        windll.user32.ShowWindow(taskbar, 9)
        #print(ex)
        sys.exit()


def daily_session_login(user_id):
    try:
        windll.user32.ShowWindow(taskbar, 9)
        global user_data,login_time,today,project_name,project_id,violation_filter,time_nopersons,user_name,manager_id
        user_data=db.master.find_one({"user_id": user_id,"role":"agent"},{"facial_img":0})
        #print (user_data)
        project_name=user_data["project_name"]
        project_id=user_data["project_id"]
        time_nopersons=user_data["time_nopersons"]
        violation_filter=user_data["violation_filter"]
        user_name=user_data["user_name"]
        manager_id=user_data["manager_id"]
        today = datetime.datetime.combine(date.today(), datetime.datetime.min.time())
        login_time=datetime.datetime.now()
        if db.dailySession.count_documents({"user_id":user_id,"session_date_string":str(today)}, limit=1):
            db.dailySession.update_one(
                                { "user_id": user_id ,
                                 "user_name":user_name,
                                "session_date_string": str(today)},
                                { "$set":{
                                            "login_time":login_time,
                                            "session_status":"live"
                                }
                                },
                                )
        else:
            data={
            "user_id": user_id,
            "user_name":user_name,
            "login_time":login_time,
            "logout_time":"Currently logged in",
            "session_status":"live",
            "session_date":today,
            "session_date_string":str(today),
            "project_name":project_name,
            "project_id":project_id,
            "billable_hours":0.0, 
            "total_hours":9.0,
            "non_billable_hours":0.0
            }
            db.dailySession.insert_one(data)
        logging.info("Daily Session Login Successfull")
    except Exception as ex:
        logfile.write("Session Update-->"+str(ex))
        windll.user32.ShowWindow(taskbar, 9)
        sys.exit()
    count_people_and_phones()
    
def count_people_and_phones():
    windll.user32.ShowWindow(taskbar, 9)
    no_person_time=0
    global cap
    try:
        from PIL import Image,ImageTk
        root=Tk()
        root.title(read_config("Title"))
        #root.attributes('-alpha',0.5)
        root.attributes('-toolwindow', True)
        root.attributes('-topmost',True)
        def Logoff():
            status=tkmb.askyesno(title="Logout",message="Do you really want to exit the application")
            if status==True:
                cap.release()
                root.destroy()
                daily_session_update(user_id,today,login_time) 
                logging.info("user successfully logged out")
        window_w = 250
        window_h = 180
        R = int(width/1.12 - window_w/2)
        D = int(height/1.25- window_h/2)
        root.geometry('250x180+{}+{}'.format(R, D))
        l1=Label(root,text=read_config("Title"), font=('Times New Roman', 10, 'bold'))
        f1=LabelFrame(root)
        f1.pack()
        l1=Label(f1)
        l1.pack()
        l1=Label(root, font=3)
        l1.place(x=1, y=1)
        root.protocol("WM_DELETE_WINDOW", Logoff)
        img = Image.open("logout.png")
        img = img.resize((50,30), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)
        b1=Button(root,image=photoImg, command=Logoff, width=50)
        b1.place(x=190, y=1)
        cap=cv2.VideoCapture(0)
        flag=True
        while flag:
            ret, image = cap.read()
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            tk_frame = cv2.resize(frame, (250, 180))
            frame = cv2.resize(frame, (320, 320))
            tkint_img=ImageTk.PhotoImage(Image.fromarray(tk_frame))
            l1["image"]=tkint_img
            root.update()
            frame = frame.astype(np.float32)
            frame = np.expand_dims(frame, 0)
            frame = frame / 255
            class_names = [c.strip() for c in open("classes.txt").readlines()]
            boxes, scores, classes, nums = yolo(frame)
            count = 0
            # image = draw_outputs(image, (boxes, scores, classes, nums), class_names)
            for i in range(nums[0]):
                if int(classes[0][i] == 0):
                    count += 1
                if (int(classes[0][i] == 67) and violation_filter["mobile"]=="on"):
                    cv2.destroyAllWindows()
                    root.destroy()
                    violation(image, "Suspicious Activity : Mobile Phone",user_id,project_id,project_name)
                    daily_session_update(user_id,today,login_time)
                    flag = False
                    violation_popup("MobilePhone usage Detected !!")
                    break
                if int(classes[0][i] == 73 and violation_filter["book"]=="on"):
                    cv2.destroyAllWindows()
                    root.destroy()
                    violation(image, "Suspicious Activity : Book",user_id,project_id,project_name)
                    daily_session_update(user_id,today,login_time)
                    flag = False
                    violation_popup("Book usage detected!!")
                    break
            if count == 0 and violation_filter["no_person"]=="on":
                time.sleep(1)
                no_person_time=no_person_time +1
                if no_person_time<int(time_nopersons):
                    continue
                else:
                    n_p=0
                    cv2.destroyAllWindows()
                    root.destroy()
                    violation(image, "No Agent Detected",user_id,project_id,project_name)
                    daily_session_update(user_id,today,login_time)
                    flag = False
                    violation_popup("No person detected !!")
                    break
            elif count > 1 and violation_filter["multiple_persons"]=="on":
                cv2.destroyAllWindows()
                root.destroy()
                violation(image, "Suspicious background Activity : Multiple Person",user_id,project_id,project_name)
                daily_session_update(user_id,today,login_time)
                flag = False
                violation_popup("More than one person detected!!")
                break
            else:
                no_person_time=0
            if cv2.waitKey(1) & 0xFF == ord('q'):
                windll.user32.ShowWindow(taskbar, 9)
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as ex:
        logfile.write("violation"+str(ex))
        #print(ex)
        windll.user32.ShowWindow(taskbar, 9)
        sys.exit()


def daily_session_update(user_id,today,login_time):
    try:
        windll.user32.ShowWindow(taskbar, 9)
        logout_time=datetime.datetime.now()
        additional_hours=round(((logout_time-login_time).total_seconds()/3600),2)
        data=db.dailySession.find_one({"user_id":user_id,"session_date_string":str(today)})
        billable_hours=data["billable_hours"]
        total_billable_hours=round(billable_hours+additional_hours,2)
        db.dailySession.update_one(
                        { "user_id": user_id,
                            "session_date_string": str(today)},
                        { "$set":{
                                    "billable_hours": total_billable_hours,
                                    "logout_time":logout_time,
                                    "session_status":"offline",
                                    "non_billable_hours":9.0-total_billable_hours
                        }
                        },
                        )
        logging.info("Daily Session update Successfull")
    except Exception as ex:
        logfile.write("facial_recognition-->"+str(ex))
        windll.user32.ShowWindow(taskbar, 9)
        

def violation(image,violation,user_id,project_id,project_name):     #store violation images
    #store violation images
    try:
        windll.user32.ShowWindow(taskbar, 9)
        global violation_name
        violation_name=violation
        im = cv2.imencode('.jpg', image)[1].tobytes()
        data = {"user_id": user_id,
                "user_name":user_name,
                "project_id":project_id,
                "project_name":project_name,
                "marked_as":"TBM",
                "reviewed by":"TBR",
                "escalated_by":"TBE",
                "created_date": datetime.datetime.now(),
                "violation_type":violation,
                "violation_image":im
                }
        db.violation.insert_many([data])
        logging.info("Violation update Successfull")
    except Exception as ex:
        logfile.write("violation"+str(ex))
        windll.user32.ShowWindow(taskbar, 9)
        sys.exit()
# Volations Pop up

def violation_popup(status):
    Violation_Window =Tk()
    Violation_Window.title(read_config("violation_popup"))
    Violation_Window.attributes('-fullscreen', True)
    Violation_Window.configure(background='black')
    windll.user32.ShowWindow(taskbar, 0)   ## hide th1e taskbar
    for i in range(104):  #block the keyboard
        keyboard.block_key(i)  
    root1=Tk()
    root1.withdraw()
    status=tkmb.showerror(status, "Please wait for 5 seconds and login again to continue !!")
    def send_mail(violation):
        try:
            agent_name=user_name
            email_data=list(db.master.find({"emp_id":manager_id},{"user_name":1,"email_id":1}))
            email_id=email_data[0]["email_id"]
            created_date=datetime.datetime.now()
            message = "Hello "+email_data[0]["user_name"]+"," +"\n\nThis is to inform you that a violation has been detected from your agent. \
                \nPlease refer below for more information.\n\nAgent Name: "\
                +agent_name+"\nViolation Type: "+violation+"\nDate&Time: "+str(created_date)
            smtpsrv = "smtp.office365.com"
            smtpsrver = smtplib.SMTP(smtpsrv,587,timeout=3)
            smtpsrver.connect(smtpsrv,587)
            msg = EmailMessage()
            msg['Subject'] = "Agent Violation"
            msg['From'] = 'BPS_WFM@hexaware.com'
            msg['To'] = email_id
            msg.set_content(message)
            smtpsrver.ehlo()
            smtpsrver.starttls()
            smtpsrver.login('BPS_WFM@hexaware.com',"Mumbai@12345")  # user & password
            smtpsrver.send_message(msg)
            smtpsrver.quit()
            logging.info("Mail sent Successfull")
        except Exception as ex:
            logfile.write("Unable to send email : "+str(ex))
            windll.user32.ShowWindow(taskbar, 9) # show 
            pass
    send_mail(violation_name)
    if status==True:
        root1.destroy()
        Violation_Window.destroy()
    else:
        root1.destroy()
        Violation_Window.destroy()    
    Violation_Window.mainloop()
    for i in range(104):   #unblock the keys
        keyboard.unblock_key(i)
    return(user_login())

if __name__ == "__main__" : 
    user_login()
    sys.exit()
    
    
