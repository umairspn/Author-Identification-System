#!/usr/bin/python
import re
import string
import os
import sys
import glob
import tkinter.messagebox 
from tkinter import *
from tkinter.filedialog import askopenfilename
import shutil
from time import sleep
from difflib import SequenceMatcher
from nltk.stem.lancaster import LancasterStemmer
from scipy import spatial
import numpy as np
from collections import defaultdict 
from nltk.corpus import stopwords
import math
import operator
import time

gui = tkinter.Tk()
gui.title('Author Identification System')
gui.geometry('1000x600')
gui.state('zoomed')
temp = [] 
temp2 = []
dest='Training Data/test'
s_word = 'AUTHOR IDENTIFICATION SYSTEM'
color_temp=0
test_filename='a'
counterx=0
st = LancasterStemmer()

t_time_folder=0
t_time_testfile=0
t_files_per_author=0
tested_file='none'
t_files = t_folders = -1
t_path='Training Data./'


vscrollbar = tkinter.Scrollbar(gui)
c2= tkinter.Canvas(gui,background = "#D2D2D5",yscrollcommand=vscrollbar.set)
vscrollbar.config(command=c2.yview)
vscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y) 
f2=tkinter.Frame(gui)
#c2.pack(side="left", fill="both", expand=True)
c2.pack(expand=True,  fill="y")
c2.create_window(-200,0,window=f2, anchor='nw')
c = Canvas(f2, width=750, height=500)



    
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)   
        self.master = master
        self.init_window()

    def init_window(self):
        
        self.master.title("AUTHOR IDENTIFICATION SYSTEM")
        self.pack(fill=BOTH, expand=0)
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        edit = Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)
        aboutmenu=Menu(menu)
        menu.add_cascade(label="About", menu=aboutmenu )
        aboutmenu.add_command(label="About Developers", command=self.aboutfunc)
        aboutmenu.add_command(label="How To", command=self.how_to)

        running = Menu(menu)
        menu.add_cascade(label="Run", menu=running)
        running.add_command(label="Stop Debugging", command=self.stopdebug)
        extras = Menu(menu)
        menu.add_cascade(label="Options", menu=extras)
        extras.add_command(label="Change Color", command=self.changecolor)
        
    def client_exit(self):
        exit()

    def aboutfunc(self):
        tkinter.messagebox.showinfo ( "ABOUT", "\t***AUTHOR IDENTIFICATION SYSTEM***\n\n*THIS SYSTEM"
                                      "IS DESIGNED BY MOHAMMAD UMAIR\n AND BASIT SALEEM\n*IT SERVES AS"
                                      "OUR FINAL YEAR PROJECT\n*TRAINING DATASET IS ATTACHED ALONGWITH "
                                      "THE PROJECT.\n*MORE THAN 80% ACCURACY HAS BEEN ACHEIVED ON N AUTHORS" )


    def how_to(self):
        tkinter.messagebox.showinfo ( "HOW TO !", "\t***AUTHOR IDENTIFICATION SYSTEM***\n\n*TRAIN THE SYSTEM"
                                      "IS DESIGNED BY MOHAMMAD UMAIR\n AND BASIT SALEEM\n*IT SERVES AS"
                                      "OUR FINAL YEAR PROJECT\n*TRAINING DATASET IS ATTACHED ALONGWITH "
                                      "THE PROJECT.\n*MORE THAN 80% ACCURACY HAS BEEN ACHEIVED ON N AUTHORS" )


    def stopdebug(self):
        raise SystemExit(0)

    def changecolor(self):
        
        global color_temp
        color_temp=color_temp+1
        if color_temp>3:
            color_temp=1
            
        if color_temp==1:
            gui.configure(background='grey')
            l.configure(foreground='grey')
            btn0.configure(foreground='grey')
            btn1.configure(foreground='grey')
        elif color_temp==2:
            gui.configure(background='lightyellow')
            l.configure(foreground='green')
            btn0.configure(foreground='green')
            btn1.configure(foreground='green')

        else:
            gui.configure(background='SystemButtonFace')
            l.configure(foreground='black')
            btn0.configure(foreground='green')
            btn1.configure(foreground='green')
        
        
if __name__ == '__main__':


    for _, dirnames, filenames in os.walk(t_path):
        t_files += len(filenames)
        t_folders += len(dirnames)
    print(t_files)
    print(t_folders)

        
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def go(counter=1):
        l.config(text=s_word[:counter])
        f2.after(80, lambda: go(counter+1))

    def aboutgo(counter=1):
        l.config(text=s_word_about[:counter])
        window2.after(80, lambda: go(counter+1))

    #######################################

    def DF_PY():
        sentence_arr=[]
        n_words=0
        n_sentence=0
        n_character=0
        spaces=0
        n_semicolon=0
        n_colon=0
        n_comma=0
        n_expmark=0
        n_period=0
        t0=0


        if counterx==1:
            inp1='test'
        else:
            inp1= input("\nEnter Folder Name:    ")

        
        while inp1=='':
            inp1= input("\nEnter Folder Name:    ")

        if not os.path.exists('Training Data./'+inp1):
            print('ERROR: FILE DO NOT EXIST ')
        else:
            t0=time.time()

            auth_counter = len(glob.glob1('Training Data./',"*.txt"))                          #number of authors    
            print(auth_counter)
            
            doccounter = len(glob.glob1('Training Data./'+inp1,"*.txt"))                          #number of documents    
            print('\nNAME OF DOCUMENTS:   '  +  str(glob.glob1('Training Data./'+inp1,"*.txt")))
            print('NUMBER OF DOCUMENTS:    ' +  str(doccounter) + '\n\n\n')

            global t_files_per_author

            if counterx==0:
                t_files_per_author=doccounter
                


            print('\n<--------NUMBER OF WORDS IN EACH DOCUMENTS-------->\n')
            DF = defaultdict(int)                                                   
            CF = defaultdict(int)
            for filename in glob.glob(os.path.join('Training Data./'+inp1, '*.txt')):                 
                words = re.findall(r'\w+', open(filename).read().lower())           
                words2= re.finditer(r'\w+', open(filename).read().lower())           #return all strings (for number of words)
                filtered_words = [word for word in words if word not in stopwords.words('english')]
                stems = [st.stem(word) for word in filtered_words]

                #print (len(filtered_words))
                sentence= open(filename).readlines()
                charactar=open(filename)
                
                for line in charactar:                                               #number of characters (for Avg word length)
                    for ch in line:
                       n_character+=1
                       if ch==' ':
                           spaces+=1
                       if ch==';':
                           n_semicolon+=1
                       if ch==':':
                           n_colon+=1
                       if ch==',':
                           n_comma+=1
                       if ch=='!':
                           n_expmark+=1
                       if ch=='.':
                           n_period+=1

                        
                           
                #print(words)
                

                for word in set(stems):                                                                     # DF
                    if len(word) >= 1 and word.isalpha():
                        DF[word] +=1                                                
                        #print(str(word))


                for word in set(stems):                                                                     # <number of words>
                    n_words+=1                                                      

                for word in set(sentence):                                                                  # <number of sentences>
                    sentence_arr.append(word.split("."))
                    
                          
            rows = len(sentence_arr)
            for i in range(rows):
                for j in range(len(sentence_arr[i])):                                                       # <"number of sentences">
                    if sentence_arr[i][j] !='\n':
                        n_sentence+=1


            f = open('Author/'+inp1.upper()+'_trained_data_11_features.txt', 'w')

            a1=n_words/doccounter
            print('\nAvg <number of words>                : ' + str(a1) )                                              # Avg <number of words>
           # norm_a1=
            
            f.write(str(a1) + '\n')

            a2=(n_sentence-doccounter)/doccounter
            print('\nAvg <number of Sentences>            : ' +  str(a2))                                              # Avg <number of sentences>
            f.write(str(a2) + '\n')

            a3=n_words/(n_sentence-doccounter)
            print('\nAvg <number of words in a Sentence>  : ' + str(a3) )                                              # Avg <number words in a sentences>
            f.write(str(a3) + '\n')

            f_char=n_character-spaces
            a4=f_char/n_words
            print('\nAvg <word length>                    : ' + str(a4) )
            f.write(str(a4) + '\n')

            a5=n_semicolon/doccounter
            print('\nAvg <number of semicolons>           : ' + str(a5) )                                             # Avg <number of semicolons>
            f.write(str(a5) + '\n')

            a6=n_colon/doccounter
            print('\nAvg <number of colons>               : ' + str(a6) )                                             # Avg <number of colons>
            f.write(str(a6) + '\n')

            a7=n_comma/doccounter
            print('\nAvg <number of comma>                : ' + str(a7) )                                             # Avg <number of commas>
            f.write(str(a7) + '\n')

            a8=n_expmark/doccounter
            print('\nAvg <number of explanation marks>    : ' + str(a8) )                                             # Avg <number of explanation marks>
            f.write(str(a8) + '\n')

            a9=n_period/doccounter
            print('\nAvg <number of periods >             : ' + str(a9) )                                             # Avg <number of periods> *same as no of sentences*
            f.write(str(a9) + '\n')

            f.close()


            t1 = time.time()
            total = t1-t0

            #f2 = open('Author/'+inp1.upper()+'_DF-TDF.txt', 'w')

    
            
            print('\n\n\n<--------DOCUMENT FREQUENCY AND IDF-------->\n')
            #inp5=int(input("\nEnter max DF size:    "))
           # f2.write('DATA OF ' + str("FILE") + ' words \n\n' )


            '''filtered_words = [word for word in DF if word not in stopwords.words('english')]

            max_idf=abs(0.01*doccounter) 
            print('\n'+ 'Max IDF Size:   '+str(max_idf)+'\n') 
            
            IDF = dict()
            for word in filtered_words:
                if max_idf>doccounter:
                    print('Size Exceeded')
                    break;
                elif DF[word]>max_idf:
                    IDF[word] = math.log(doccounter / float(DF[word]))
                    
                    #print(str(word) + '\t' + str(DF[word]) +  '\t' + str(IDF[word]))                                 # Document frequency
             #       f2.write(str(word) + '\t' + str(DF[word]) +  '\t' + str(IDF[word]))
              #      f2.write('\n')

            #f2.close()
'''



            print('TOTAL RUN TIME OF ALGORITHM:  '+str(total))

            global t_time_folder, t_time_testfile
     
            if counterx==1:
                t_time_testfile=total
            else:
                t_time_folder=total
    
            
        
    ####################################### 

    def train_file_btn():
        global counterx
        counterx=1
        Tk().withdraw()        
        filename = askopenfilename()
        print(filename)
        if filename=='':
            print('nothing')
        else:
            files = glob.glob(dest+'/*')
            for f in files:
                os.remove(f)
            shutil.copy(filename,dest)            
            #os.system('DF.py')
            DF_PY()
            textbox1.insert(END, '\nFILENAME:   '+ str(filename) + '\n' , 'color')
            global test_filename
            test_filename=filename
            #test_filename=test_filename[test_filename.find('/')+1 : test_filename.find(')')]
            #print('123123:   '+ str(test_filename))

            head, tail = os.path.split(test_filename)
            print(tail)
            global tested_file
            tested_file=tail



    def CLEAR():
        #os.system('check_author.py')
        os._exit(0)

            
    def check_author_btn():
        ttl=0
        n=0
        print('\n---------------------\nTEST FILE ATTRIBUYTES\n---------------------\n')
        with open('Author/'+'TEST_trained_data_11_features'+'.txt') as f:
            testarr = f.readlines()
        for x in range(0, len(testarr)):
            print(testarr[x], end='')

        print('\n---------------------\nATTRIBUYTES OF AUTHORS\n---------------------\n')
        for filename in glob.glob(os.path.join('author', '*.txt')):
            with open(filename) as f:
                if filename !='author\TEST_trained_data_11_features.txt':
                    print('shit shit shit')
                    arr2 = f.readlines()
                    for xx in range(0, len(arr2)):
                        ttl+=abs(float(testarr[xx])-float(arr2[xx]))
                        
                    n+=1    
                    print('Author '+ str(n) + ' :' +str(ttl) + '   '+str(filename))
                    textbox1.insert(END, 'Author '+ str(n) + ' :' + str(ttl) + '   '+str(filename) +'\n' , 'tag2')
                    temp.append(ttl)
                    temp2.append(filename)
                    ttl=0
        
        print('\n')
        kk=temp.index(min(temp))

        l2 = [temp.index(x) for x in sorted(temp)]
        top1=l2[0]
        top2=l2[1]
        top3=l2[2]
        
        print("1st Match:   "+str(temp2[top1])+"\n")
        print("2nd Match:   "+str(temp2[top2])+"\n")
        print("3rd Match:   "+str(temp2[top3])+"\n")

        auth1=temp2[top1]
        auth1=auth1[auth1.find('\\')+1 : auth1.find('_')]
        auth2=temp2[top2]
        auth2=auth2[auth2.find('\\')+1 : auth2.find('_')]
        auth3=temp2[top3]
        auth3=auth3[auth3.find('\\')+1 : auth3.find('_')]
        
        
        textbox1.insert(END, '\n\n1st Match:   '+ str(temp2[top1]) + '\n' , 'color')
        textbox1.insert(END, '2nd Match:   '+ str(temp2[top2]) + '\n' , 'color')
        textbox1.insert(END, '3rd Match:   '+ str(temp2[top3]) + '\n' , 'color')
        
        textbox1.config(state=DISABLED)

        tkinter.messagebox.showinfo( "Congragulations ", "Identificaiton Complete !" )



        c.create_rectangle(20, 150, 120, 180, fill="red")
        c.create_text(70, 130, text=str(auth3), font=('Agency FB', 11, 'bold'))
        
        c.create_rectangle(140, 130, 240, 180, fill="blue")
        c.create_text(190, 120, text=str(auth2), font=('Agency FB', 11, 'bold'))
        
        c.create_rectangle(260, 120, 360, 180, fill="green")
        c.create_text(310, 110, text=str(auth1), font=('Agency FB', 11, 'bold'))

        c.create_text(100,70,text='TOP 3 MATCHES', font=('28 Days Later', 18, 'bold'), fill='grey')
        c.create_text(80,270,text='STATISTICS', font=('28 Days Later', 18, 'bold'), fill='grey')
        
        c.create_text(165,385,text=('ALGO USED: \t\tSTYLOMETRY \nTOTAL TIME TO TRAIN(FOLDER): \t'
                                    +str(t_time_folder)+'\nTOTAL TIME TO TRAIN (TEST FILE): \t'
                                    +str(t_time_testfile)+'\nTOTAL FILES OF TRAINED AUTHOR: \t'
                                    + str(t_files_per_author) +'\nFILE TESTED: \t\t'
                                    + str(tested_file) + '\nTOTAL AUTHORS: \t\t'
                                    + str(t_folders) + '\nTOTAL FILES: \t\t' + str(t_files)), font=('Agency FB', 14), fill='blue')   #statistics text

         
    space=Label(f2, text="\n\n")
    l = Label(f2,borderwidth=5,    font=('Agency FB', 25, 'bold'), height=3, foreground='#476042')

    btn00 = tkinter.Button(f2, text ="TRAIN FOLDER", command = DF_PY, font=('Agency FB', 11, 'bold'), foreground='#476042', width=12, height=2, bd=3, relief=RIDGE)
    btn0 = tkinter.Button(f2, text ="TRAIN FILE", command = train_file_btn, font=('Agency FB', 11, 'bold'), foreground='#476042', width=12, height=2, bd=3, relief=RIDGE)
    btn1 = tkinter.Button(f2, text ="CHECK AUTHOR", command = check_author_btn, font=('Agency FB', 11, 'bold'), foreground='#476042', width=18, height=2, bd=3, relief=RIDGE)
   # btn_clear_textbox = tkinter.Button(f2, text ="CLEAR", command = CLEAR, font=('Ariel', 11, 'bold'), foreground='#476042', width=18, height=2, bd=3, relief=RIDGE)
    
    textbox1 = Text(f2, height=20, width=90)
    textbox1.tag_configure('color', foreground='#476042', font=('Arial', 12, 'bold'))
    textbox1.tag_configure('tag2', font=('Arial', 10 ))

    app = Window(gui)
    go()   
    l.pack()
    btn00.pack()
    btn0.pack()
    btn1.pack(pady=2)
    space.pack()
    textbox1.pack()
   # btn_clear_textbox.pack()
    c.pack()
    
    gui.update()
    c2.config(scrollregion=c2.bbox("all"))
    gui.mainloop()



















