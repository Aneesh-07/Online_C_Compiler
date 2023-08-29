from flask import Flask,redirect,url_for,render_template,request
import subprocess,os
from subprocess import PIPE

app=Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


def run(code,inp,chk):
    
    # creating a file for code if not already
    if not os.path.exists('program.c'):
        os.open('program.c',os.O_CREAT)
        
    # creating a file descriptor
    fd = os.open('program.c',os.O_WRONLY)
    
    # clearing whatever written previously
    os.truncate(fd,0)
    
    encoded_program = str.encode(code)
    
    os.write(fd,encoded_program)
    
    os.close(fd)
    
    s = subprocess.run(['gcc','-o','new','program.c'],stderr=PIPE,)
    
    #checking whether code ran successfully or not
    check = s.returncode
    
    if check==0:
        if chk == '1':
            r = subprocess.run(['new.exe'],input=inp.encode(),stdout=PIPE)
        else:
            r = subprocess.run(['new.exe'],stdout=PIPE)
        
        return r.stdout.decode("utf-8")
    return s.stderr.decode("utf-8")
        
        
        
@app.route("/compiler",methods = ['GET','POST'])
def compiler():
    if request.method == 'POST':
        code = request.form['code']
        inp = request.form['input']
        chk = request.form.get('check')
        
        if not chk == '1':
            inp = ""
            check = ''
        else:
            check ='checked'
        
        output = run(code,inp,chk)
        print(output)
        return render_template('compiler.html',code=code,input=inp,output=output,check = check)
    else:
        return render_template('compiler.html')



if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run()