import pandas as pd
from tkinter import*
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

#Database Connection
import mysql.connector
conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='patient_report'
    )
cursor = conn.cursor()

#Load Dataset
stone=pd.read_csv('kidney-stone-dataset.csv')

#Split
from sklearn.model_selection import train_test_split

x=stone.iloc[:, :-1]
y=stone.iloc[:,-1]

x_train, x_test, y_train, y_test=train_test_split(x, y, test_size=0.2, random_state=1)

#Train Model
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
model.fit(x_train, y_train)

#prediction

root=Tk()
root.geometry("895x380")
root.title("KIDNEY-STONE-PREDICTION")
root.configure(bg='white smoke')
stone_prediction=""
def info():
      global stone_prediction
      Result=pd.DataFrame(
           [[float(gravityvalue.get()), float(phvalue.get()) ,float(osmovalue.get()),float(condvalue.get()) ,float(ureavalue.get()),float(calcvalue.get()) ]],
           columns=x.columns)
      
      stone_prediction=model.predict(Result)
      messagebox.showinfo("Details:",f"Patient Name: {namevalue.get()}\nPatient Age: {agevalue.get()}\nPatient Address: {addvalue.get()}\nStone Pratiction=> {stone_prediction[0]}\n")

      #Convert values into other variable to sent MYSQL
      gravity=gravityvalue.get()
      ph=phvalue.get()
      osmo=osmovalue.get()
      cond=condvalue.get()
      urea=ureavalue.get()
      calc=calcvalue.get()
      result=float(stone_prediction[0])
      #Send details to MYSQL
      query = "INSERT INTO test (gravity, ph, osmo, cond, urea, calc, result) VALUES (%s, %s, %s, %s, %s, %s, %s)"
      values = (gravity, ph, osmo, cond, urea, calc, result)
      cursor.execute(query, values)
      conn.commit()
      
f=Frame(root,bg="gainsboro",padx=15,pady=15)
f.grid(row=0,column=0,padx=10,pady=10)

name=Label(f,bg="#243B7A",fg="#EAF4FF",text=" Enter Patient Full Name:",padx=8)
name.grid(row=0,column=0,sticky="w")
namevalue=StringVar()
nameentry=Entry(f,textvariable=namevalue,width=40,bg="RoyalBlue4",fg="white")
nameentry.grid(row=0,column=1,sticky="w",padx=5,pady=5)

age=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter Patient Age:",padx=25)   
age.grid(row=1,column=0)
agevalue=StringVar()
ageentry=Entry(f,textvariable=agevalue,width=40,bg="RoyalBlue4",fg="white")
ageentry.grid(row=1,column=1,sticky="w",padx=5,pady=5)

add=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter Patient Address:",padx=15)   
add.grid(row=2,column=0)
addvalue=StringVar()
addentry=Entry(f,textvariable=addvalue,width=40,bg="RoyalBlue4",fg="white")
addentry.grid(row=2,column=1,sticky="w",padx=5,pady=5)

gravity=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter Gravity Value:",padx=21)   
gravity.grid(row=3,column=0)
gravityvalue=StringVar()
gravityentry=Entry(f,textvariable=gravityvalue,width=40,bg="RoyalBlue4",fg="white")
gravityentry.grid(row=3,column=1,sticky="w",padx=5,pady=5)

ph=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter PH Value:",padx=31)   
ph.grid(row=4,column=0)
phvalue=StringVar()
phentry=Entry(f,textvariable=phvalue,width=40,bg="RoyalBlue4",fg="white")
phentry.grid(row=4,column=1,sticky="w",padx=5,pady=5)

osmo=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter OSMO Value:",padx=22)   
osmo.grid(row=5,column=0)
osmovalue=StringVar()
osmoentry=Entry(f,textvariable=osmovalue,width=40,bg="RoyalBlue4",fg="white")
osmoentry.grid(row=5,column=1,sticky="w",padx=5,pady=5)

cond=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter COND Value:",padx=22)   
cond.grid(row=6,column=0)
condvalue=StringVar()
condentry=Entry(f,textvariable=condvalue,width=40,bg="RoyalBlue4",fg="white")
condentry.grid(row=6,column=1,sticky="w",padx=5,pady=5)

urea=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter UREA Value:",padx=25)   
urea.grid(row=7,column=0)
ureavalue=StringVar()
ureaentry=Entry(f,textvariable=ureavalue,width=40,bg="RoyalBlue4",fg="white")
ureaentry.grid(row=7,column=1,sticky="w",padx=5,pady=5)

calc=Label(f,bg="#243B7A",fg="#EAF4FF",text="Enter CALCIUM Value:",padx=14)   
calc.grid(row=8,column=0)
calcvalue=StringVar()
calcentry=Entry(f,textvariable=calcvalue,width=40,bg="RoyalBlue4",fg="white")
calcentry.grid(row=8,column=1,sticky="w",padx=5,pady=5)

Button(root,bg="#00A8FF",fg="white",text="SUBMIT DETAILS",width=18,command=info,borderwidth=5,activebackground="#0077FF").grid(row=1,column=0)
def restart_app():
   namevalue.set("")
   agevalue.set("")
   addvalue.set("")
   gravityvalue.set("")
   phvalue.set("")
   osmovalue.set("")
   condvalue.set("")
   ureavalue.set("")
   calcvalue.set("")
Button(root,text='Recheck',bg='#6C63FF',fg="white",command=restart_app,borderwidth=5,width=18,activebackground="#5145CD").grid(row=2,column=0)
    
#Visualization
import matplotlib.pyplot as plt
def chart():
      total=stone['target'].value_counts()
      total.plot(kind='bar',color='red')
      plt.title("Kidney-Stone-Analysis")
      plt.xlabel('0 vs 1')
      plt.ylabel('counts')
      plt.show()
Button(root,text='Visualization',bg="#00A8FF",fg="white",command=chart,borderwidth=5,width=18,activebackground="#0077FF").grid(row=1,column=1)

#Load Image
from PIL import Image, ImageTk

image = Image.open(r"C:\Users\HP\OneDrive\Pictures\WhatsApp Image 2026-05-29 at 6.39.23 PM.jpeg")
image = image.resize((430, 280))
photo = ImageTk.PhotoImage(image)
label = Label(root,image=photo)
label.grid(row=0,column=1)

#Print

from reportlab.pdfgen import canvas
from datetime import date
def report():
     patient_name=namevalue.get().strip()
     if patient_name=="":
           patient_name="Unknown Patient"
     file_name=f"{patient_name}_Kidney_Stone_Report.pdf"      
     pdf=canvas.Canvas(file_name)
     pdf.setFont("Helvetica-Bold", 18)
     pdf.drawString(150, 800, "Kidney Stone Report")
     pdf.line(50, 790, 550, 790)
     pdf.setFont("Helvetica", 12)

     today=date.today()
     pdf.drawString(50, 750, f"Date: {today}")
     pdf.setFont("Helvetica", 12)
     pdf.drawString(50, 730, f"Patient Name: {namevalue.get()}")
     pdf.drawString(50, 710, f"Patient Age: {agevalue.get()}")
     pdf.drawString(50, 690, f"Patient Address: {addvalue.get()}")
     pdf.setFont("Helvetica", 12)
     pdf.drawString(50, 670, f"Stone Prediction: {stone_prediction}")
     if stone_prediction==[0]:
            pdf.drawString(50, 650, "You don't have kidney stone")
            pdf.drawString(50, 500, "")
            pdf.line(50, 590, 550, 590)
            pdf.setFont("Helvetica-Bold", 14)
            
     else:
            pdf.drawString(50, 650, "You have kidney stone!!!")
            pdf.drawString(50, 600, "Please Follow This Diet Plan:")

            pdf.drawString(50, 580, "1.Drink 4 to 5 liters of water daily ")
            pdf.drawString(50, 560, "2.Limit salt intake ")
            pdf.drawString(50, 540, "3.Eat calcium rich foods ")
            pdf.drawString(50, 520, "4.Avoide sugar drinks ")
            pdf.line(50, 490, 550, 490)
            pdf.setFont("Helvetica", 12)
            
     pdf.save()
     messagebox.showinfo("File_Saved:",f"PDF Generated Successfully For: {file_name}")
Button(root,text='Make Print',bg='#6C63FF',fg="white",command=report,borderwidth=5,width=18,activebackground="#5145CD").grid(row=2,column=1)

root.mainloop()

                                
