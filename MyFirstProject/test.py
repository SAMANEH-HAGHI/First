import tkinter
import re
import sqlite3
import time
import datetime
#---------------functions-------------------


def signup():


    def saveSignup(user,pas,addr): 
        sqlSignup=f'''
                    INSERT INTO users(username,password,address,grade)
                    VALUES ("{user}","{pas}","{addr}",0)
        '''
        try:
            cnt.execute(sqlSignup)
            cnt.commit()
            return True
        except:
            return False
    

    def submitVal(user,pas,pasCon):
        if user=='' or pas=='' or pasCon=='':
            return False,'none of the fields shoul be empty!'
        if pas!=pasCon:
            return False,'password and its confirmation missmatch!'
        pattern=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not re.match(pattern,pas):
            return False,' invalid password form! '
        sqlCode=f'SELECT * FROM users WHERE username="{user}"'
        result=cnt.execute(sqlCode)
        data=result.fetchall()
        if len(data)>0:
            return False,'this username already exists!'   
        return True,''

    def submit():
        user=txtuser.get()
        pas=txtpass.get()
        pasCon=txtpasscon.get()
        address=txtaddr.get()
        result,msg=submitVal(user,pas,pasCon)
        if not result:
            lblmsg.configure(text=msg,fg='red')
            txtuser.delete(0,'end')
            txtpass.delete(0,'end')
            txtpasscon.delete(0,'end')
            txtaddr.delete(0,'end')
            return # in this line,program exits from submit function, and 
                   # doesn't execute the rest of the codes in submit function;
                   # when it gets out, it is still in sign up function and the
                   # program executes codes of the start of signup function
                   # which is creating window2 and redoing the different lines.
        result=saveSignup(user,pas,address)
        if not result:
            lblmsg.configure(text='something went wrong while connecting database!',fg='red')
        else: #here we have else so we don't need return
            lblmsg.configure(text='sign up done successfully!',fg='green')
            txtuser.delete(0,'end')
            txtpass.delete(0,'end')
            txtpasscon.delete(0,'end')
            txtaddr.delete(0,'end')

        

    window2=tkinter.Toplevel(window1)
    window2.title('sign up here!')
    window2.geometry('400x400')

    lbluser=tkinter.Label(window2,text='enter your username: ')
    lbluser.pack()

    txtuser=tkinter.Entry(window2,width=18)
    txtuser.pack()

    lblpass=tkinter.Label(window2,text='enter your password: ')
    lblpass.pack()

    txtpass=tkinter.Entry(window2,width=18)
    txtpass.pack()

    lblpasscon=tkinter.Label(window2,text='enter password confirmation: ')
    lblpasscon.pack()

    txtpasscon=tkinter.Entry(window2,width=18)
    txtpasscon.pack()

    lbladdr=tkinter.Label(window2,text='enter your address: ')
    lbladdr.pack()

    txtaddr=tkinter.Entry(window2,text='enter your address: ')
    txtaddr.pack()

    submitbtn=tkinter.Button(window2,width=18,text='submit now',command=submit)
    submitbtn.pack()

    lblmsg=tkinter.Label(window2,text='')
    lblmsg.pack()



    window2.mainloop()


def check(username,password):
    sqlCheck=f'''SELECT password FROM users WHERE username="{username}"'''
    result=cnt.execute(sqlCheck)
    data=result.fetchall()
    if password!=data[0][0]:
        return False
    else:
        return True

def allowed(mistakeTime):
    duration=datetime.timedelta(weeks=1)
    endTime=mistakeTime+duration
    now=datetime.datetime.now()
    remainTime=endTime-now
    if now<endTime:
        return False,f'account locked.try after {remainTime}'
    else:
        return True,''
    
def refresh():
    global mistakeTime
    if mistakeTime is not None:
        duration = datetime.timedelta(weeks=1)
        endTime = mistakeTime + duration
        now = datetime.datetime.now()
        if now >= endTime:
            btnLogin.configure(state='normal')
            lblmessage.configure(text='Account unlocked. You can try to log in again.', fg='green')
            mistakeTime = None


def login():
    global mistakeTime,counting
    username = txt1.get()
    if mistakeTime is not None:
        result, Msg = allowed(mistakeTime)
        if not result:
            lblmessage.configure(text=Msg, fg='red')
            btnLogin.configure(state='disabled')
            return  
    password = txt2.get()
    result = check(username, password)
    if not result:
        counting += 1  
        if counting > 1: 
            mistakeTime = datetime.datetime.now()  
            lblmessage.configure(text='one more try.', fg='red')
            return
    else:
        counting = 0  
        mistakeTime = None       
    sqlLog=f'''SELECT * FROM users WHERE username="{username}" AND password="{password}"'''
    result=cnt.execute(sqlLog)
    data=result.fetchall()
    if len(data)<1:
        lblmessage.configure(text='wrong username or password!',fg='red')
    else:
        global session
        session=data[0][0]
        lblmessage.configure(text='welcome to your account!',fg='green')
        txt1.delete(0,'end')
        txt2.delete(0,'end')
        btnLogin.configure(state='disabled')
        btnShop.configure(state='active')



def shop():
    def buyVal(id,number):
        products=getAllProducts()
        lst=[]
        for product in products:
            lst.append(product[0])
        if id not in lst:
            return False,'not any specific product with this id!!!'
        dct={}
        for product in products:
            dct[product[0]]=product[2]
        for k,v in dct.items():
            if id==k and number>v:
                return False,"we don't have this amount of this product in our shop"
        return True,''
            
    def buy():
        currentT=time.ctime()
        id=int(txtid.get())
        number=int(txtnum.get())
        result,msg=buyVal(id,number)
        if not result:
            lblmsg3.configure(text=msg,fg='red')
            return
        sqlCart=f'''
                INSERT INTO cart(Userid,Productid,purchaseNum,date)
                VALUES({session},{id},{number},"{currentT}")
        '''
        cnt.execute(sqlCart)
        cnt.commit()
        sqlT=f'''SELECT numbers FROM products WHERE id={id}'''
        result=cnt.execute(sqlT)
        data=result.fetchall()
        totalNum=data[0][0]
        NewNum=totalNum-number
        sqlChange=f'''
                    UPDATE products
                    SET numbers={NewNum}
                    WHERE id={id}
        '''
        cnt.execute(sqlChange)
        cnt.commit()
        lstbox.delete(0,'end')
        products=getAllProducts()
        for product in products:
            text=f'ID={product[0]},Name={product[1]},Numbers={product[2]},price={product[3]}'
            lstbox.insert('end',text)
        lblmsg3.configure(text='Thank you for your purchase! Your order has been successfully processed ',fg='green')
    window3=tkinter.Toplevel(window1)
    window3.title('**shop now**')
    window3.geometry('400x400')
    lstbox=tkinter.Listbox(window3,width=50)
    lstbox.pack(pady=5)
    products=getAllProducts()
    for product in products:
        text=f'ID={product[0]},Name={product[1]},Numbers={product[2]},price={product[3]}'
        lstbox.insert('end',text)
    lblid=tkinter.Label(window3,text='Product id:')
    lblid.pack()
    txtid=tkinter.Entry(window3)
    txtid.pack()
    lblnum = tkinter.Label(window3, text='Product Numbers:')
    lblnum.pack()
    txtnum = tkinter.Entry(window3)
    txtnum.pack()
    lblmsg3=tkinter.Label(window3,text='')
    lblmsg3.pack()
    btnbuy=tkinter.Button(window3,text='BUY!',width=20,command=buy)
    btnbuy.pack()


    window3.mainloop()

def getAllProducts():
    sqlGet='''SELECT * FROM products'''
    result=cnt.execute(sqlGet)
    data=result.fetchall()
    return data




#------------------main----------------------
cnt=sqlite3.connect('samanehShop.db')
session=False
counting=0
mistakeTime=None
window1=tkinter.Tk()

window1.title('samaneh shop')
window1.geometry('300x300')

lbl1=tkinter.Label(window1,text='enter your username: ')
lbl1.pack()
txt1=tkinter.Entry(window1,width=18)
txt1.pack()

lbl2=tkinter.Label(window1,text='enter your password: ')
lbl2.pack()
txt2=tkinter.Entry(window1,width=18)
txt2.pack()

btnSignup=tkinter.Button(window1,text='sign up',width=18,command=signup)
btnSignup.pack()

btnLogin=tkinter.Button(window1,text='login',width=18,command=login)
btnLogin.pack()

btnShop=tkinter.Button(window1,text='shop now!',width=18,state='disabled',command=shop)
btnShop.pack()

btnRefresh=tkinter.Button(window1,text='refresh',width=18,command=refresh)
btnRefresh.pack()

lblmessage=tkinter.Label(window1,text='')
lblmessage.pack()


window1.mainloop()


