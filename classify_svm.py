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

import numpy as np
from sklearn.svm import SVC

from nltk.tokenize import wordpunct_tokenize
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()

gui = tkinter.Tk()
gui.title('Author Identification System')
gui.geometry('1000x600')
gui.state('zoomed')
temp = [] 
temp2 = []
topthree = ''
dest='Training Data/test'
s_word = 'AUTHOR IDENTIFICATION SYSTEM'
color_temp=0
test_filename='a'
counterx=0
st = LancasterStemmer()
total_test=0
n_top1=0
n_top2=0
n_top3=0
n_none=0

t_time_folder=0
t_time_testfile=0
t_files_per_author=0
tested_file='none'
t_files = t_folders = -1
t_path='Training Data./'

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


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

        
if __name__ == '__main__':

    for _, dirnames, filenames in os.walk(t_path):
        t_files += len(filenames)
        t_folders += len(dirnames)
    #print(t_files)
    #print(t_folders)
        
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def go(counter=1):
        l.config(text=s_word[:counter])
        f2.after(80, lambda: go(counter+1))

    def aboutgo(counter=1):
        l.config(text=s_word_about[:counter])
        window2.after(80, lambda: go(counter+1))
        

#####################################################################################################################


    def func(text):
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences


    def temp_DF(inp1):

        sentence_arr=[]
        n_words=0
        t_words=0
        n_character=0
        t_word_length=0
        spaces=0
        n_semicolon=0
        n_colon=0
        n_comma=0
        n_1=0
        n_2=0
        n_3=0
        n_4=0
        n_5=0
        n_period=0
        t0=0
        n_sentences=0
        t_sentences=0
        n_words2=0
        n_words_in_sent=0
        
        t0=time.time()

        auth_counter = len(glob.glob1('Training Data./',"*.txt"))                             #number of authors    
      #  print(auth_counter)

        doccounter = len(glob.glob1('Training Data./'+inp1,"*.txt"))                          #number of documents    
       # print('\nNAME OF DOCUMENTS:   '  +  str(glob.glob1('Training Data./'+inp1,"*.txt")))
       # print('NUMBER OF DOCUMENTS:    ' +  str(doccounter) + '\n\n\n')

        global t_files_per_author

        if counterx==0:
            t_files_per_author=doccounter
            

     #   print('\n<--------NUMBER OF WORDS IN EACH DOCUMENTS-------->\n')
        DF = defaultdict(int)                                                   
        CF = defaultdict(int)
        for filename in glob.glob(os.path.join('Training Data./'+inp1, '*.txt')):                 
            words = re.findall(r'\w+', open(filename).read().lower())           
            #words2= re.finditer(r'\w+', open(filename).read().lower())                                      #return all strings (for number of words)
            
            stop_words = stopwords.words('english')
            filtered_words = [word for word in words if word not in stop_words]                             #stopwords removal
            stems = [st.stem(word) for word in filtered_words]                                              #stemming. (lancaster)
            #print(stems)
            
            sentence = open(filename).read().splitlines()                                                   #sentences
            sad=str(sentence)
            f_func=func(sad)
            for sents in f_func:
                words = re.findall(r'\w+', sents)
                t_sentences+=1
                n_sentences+=1    
                n_words2+=len(words)


            #print(n_words2)
            #print(n_sentences)
            n_words_in_sent+=(n_words2/n_sentences)
            #print('No of words in a sentence'+ str(n_words_in_sent))

            n_sentences=0    
            n_words2=0


            charactar= open(filename)
           
            for line in stems:                                                                          #number of characters (for Avg word length)
                n_words+=1                                                                              #this n_words is for after stemming words.  
                t_words+=1
                for ch in line:
                   n_character+=1
                   if ch==' ':
                       spaces+=1

            t_word_length+=(n_character/n_words)
            n_character=0
            n_words=0
        



           # print('word_length: '+str(t_word_length))

            
            for line in charactar:                                                                      #feature 5,6,7,8
                for ch in line:
                   if ch==';':
                       n_semicolon+=1
                   if ch==':':
                       n_colon+=1
                   if ch==',':
                       n_comma+=1
                   if ch=='.':
                       n_period+=1
                   if ch=="'":
                       n_1+=1
                   if ch=='”' or ch=='“':
                       n_2+=1               
                   if ch=='(' or ch==')':
                       n_3+=1
                   if ch=="-":
                       n_4+=1
                   if ch=="[" or ch ==']':
                       n_5+=1


                       
            #print(n_1)

            for word in set(stems):                                                                     # DF
                if len(word) >= 1 and word.isalpha():
                    DF[word] +=1                                                
                                    
            
        f = open('Author/'+inp1+'_trained_data_11_features.txt', 'w')
        
        feature_arr=[None]*13
        
        #print(doccounter)
        a1=t_words/doccounter
        #print('\nAvg <number of words>                : ' + str(a1) )                                              # Avg <number of words>

        a2=t_sentences/doccounter
        #print('\nAvg <number of Sentences>            : ' +  str(a2))                                              # Avg <number of sentences>

        a3=n_words_in_sent/doccounter
        #print('\nAvg <number of words in a Sentence>  : ' + str(a3) )                                              # Avg <number words in a sentences>
        
        a4=t_word_length/doccounter
        #print('\nAvg <word length>                    : ' + str(a4) )                                              # Avg <word length>
        

        a5=n_semicolon/doccounter
       # print('\nAvg <number of semicolons>           : ' + str(a5) )                                             # Avg <number of semicolons>
        

        a6=n_colon/doccounter
       # print('\nAvg <number of colons>               : ' + str(a6) )                                             # Avg <number of colons>
        

        a7=n_comma/doccounter
        #print('\nAvg <number of comma>                : ' + str(a7) )                                             # Avg <number of commas>
                

        a8=n_period/doccounter
        #print('\nAvg <number of periods >             : ' + str(a8) )                                             # Avg <number of periods> *same as no of sentences*

        a9=n_1/doccounter
        #print('\nAvg <number of unn >             : ' + str(a9) )                                                 # Avg <number of ' >*

        a10=n_2/doccounter
        #print('\nAvg <number of " >             : ' + str(a10) )                                                  # Avg <number of " >*

        a11=n_3/doccounter
        #print('\nAvg <number of parenthesis >             : ' + str(a11) )                                        # Avg <number of parenthesis >*

        a12=n_4/doccounter
        #print('\nAvg <number of - >             : ' + str(a12) )                                          # Avg <number of parenthesis >*

        a13=n_5/doccounter
       # print('\nAvg <number of - >             : ' + str(a13) )                                          # Avg <number of [] >*


        feature_arr[0]=a1
        feature_arr[1]=a2
        feature_arr[2]=a3
        feature_arr[3]=a4
        feature_arr[4]=a5
        feature_arr[5]=a6
        feature_arr[6]=a7
        feature_arr[7]=a8
        feature_arr[8]=a9
        feature_arr[9]=a10
        feature_arr[10]=a11
        feature_arr[11]=a12
        feature_arr[12]=a13
        
        for x in feature_arr:
            xx = (x-min(feature_arr))/(max(feature_arr)-min(feature_arr))                       #normalization. 
            #print(xx)
            f.write(str(xx) + '\n')

        f.close()
        
        t1 = time.time()
        total = t1-t0



                                                                    ####### COMMENT SECTION ######

        '''
        f2 = open('Author/'+inp1.upper()+'_DF-TDF.txt', 'w')
        
        print('\n\n\n<--------DOCUMENT FREQUENCY AND IDF-------->\n')
        inp5=int(input("\nEnter max DF size:    "))
        f2.write('DATA OF ' + str("FILE") + ' words \n\n' )


        filtered_words = [word for word in DF if word not in stopwords.words('english')]

        max_idf=abs(0.01*doccounter) 
        print('\n'+ 'Max IDF Size:   '+str(max_idf)+'\n') 
        
        IDF = dict()
        for word in filtered_words:
            if max_idf>doccounter:
                print('Size Exceeded')
                break;
            elif DF[word]>max_idf:
                IDF[word] = math.log(doccounter / float(DF[word]))
                
                print(str(word) + '\t' + str(DF[word]) +  '\t' + str(IDF[word]))                                 # Document frequency
                f2.write(str(word) + '\t' + str(DF[word]) +  '\t' + str(IDF[word]))
                f2.write('\n')

        f2.close()
        
       '''

        #print('TOTAL RUN TIME OF ALGORITHM:  '+str(total))
        '''
        global t_time_folder, t_time_testfile
 
        if counterx==1:
            t_time_testfile=total
        else:
            t_time_folder=total
        '''
        
        #print('\n\n--------------------------------------------------\n\n')

                                                                                ####### COMMENT SECTION ######
        
        
#####################################################################################################################
        
    

    def DF_PY():
        if counterx==1:         
            temp_DF('test')
        else:
            for file in glob.glob1('Training Data./',"*"):
                if file !='test':
                    print(file)
                    temp_DF(file)

                    
            
        
#####################################################################################################################

                

    def disp_result_btn():
        print('\n----------------------------')
        print('TOTAL FILES TESTED: '+ str(total_test) )
        print('% OF 1st matches: '+ str((n_top1/total_test)*100) + '...' + '('+str(n_top1)+')')
        print('% OF 2nd matches: '+ str((n_top2/total_test)*100) + '...' + '('+str(n_top2)+')')
        print('% OF 3rd matches: '+ str((n_top3/total_test)*100) + '...' + '('+str(n_top3)+')')
        print('% OF no matche: '+ str((n_none/total_test)*100) + '...' + '('+str(n_none)+')')
        print('% coming in top 3: '+ str(((n_top1+n_top2+n_top3)/total_test)*100))




#####################################################################################################################

        
    #shit
    def test_folder_btn():
        
        for file in glob.glob('untrainedTest/'+"*.txt"):
          #  print(file)
            foldarr=file
            textbox1.insert(END, foldarr , 'tag2')

            print('\n\n..................................\n\n')
            global total_test
            total_test=total_test+1
            
            global counterx
            counterx=1
            filename = foldarr
            file_str=filename
            file_str=file_str[file_str.find('\\')+1 : file_str.find('_')]

            global topthree
            topthree=file_str
            print('FILENAME: ' + str(filename)) 
            print('AUTHOR:   ' + str(file_str))

            
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
                
                head, tail = os.path.split(test_filename)
              #  print(tail)
                global tested_file
                tested_file=tail

                counterx=0
                check_author_btn()
                


    def CLEAR():
        #os.system('check_author.py')
        os._exit(0)



#####################################################################################################################


        
            
    def check_author_btn():


        np_arr_training = np.zeros([1,13])              #return array with zeros
        np_arr_test = np.array([])
        i=0

        for filename in glob.glob(os.path.join('Author', '*.txt')):
            with open(filename) as f:
                if filename == 'Author\TEST_trained_data_11_features.txt':
                    np_arr_test=(np.loadtxt(filename))
                else:
                    np_arr_training= np.insert(np_arr_training, 1, np.loadtxt(filename),0 )

        np_arr_training=np.delete(np_arr_training, (0), axis=0)
        np_arr_test=np_arr_test.reshape(1, -1)

        #print(np_arr_training)             #using np array, we can perform logical operations and calculations on array

        y = np.array(['WilliamKazer','ToddNissen', 'TimFarrand', 'TheresePoletti', 'TanEeLyn', 'SimonCowell', 'ScottHillis',
                       'SarahDavison', 'SamuelPerry', 'RogerFillion', 'RobinSidel', 'PierreTran', 'PeterHumphrey',
                       'PatriciaCommins', 'NickLouth', 'MureDickie', 'MichaelConnor', 'MatthewBunce', 'MartinWolk', 'MarkBendeich',
                      'MarcelMichelson', 'LynnleyBrowning', 'LynneODonnell',
                       'LydiaZajc', 'KouroshKarimkhany', 'KirstinRidley', 'KevinMorrison', 'KevinDrawbaugh', 'KeithWeir', 'KarlPenhaul',
                      'JoWinterbottom', 'JonathanBirt', 'JohnMastrini',
                       'JoeOrtiz', 'JimGilchrist', 'JanLopatka', 'JaneMacartney', 'HeatherScoffield', 'GrahamEarnshaw', 'FumikoFujisaki',
                      'EricAuchard', 'EdnaFernandes',
                       'DavidLawder', 'DarrenSchuettler', 'BradDorfman', 'BernardHickey', 'BenjaminKangLim', 'AlexanderSmith', 'AlanCrosby', 'AaronPressman'])


        clf=SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
            decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
            max_iter=-1, probability=True, random_state=None, shrinking=True,
            tol=0.001, verbose=False)

        clf.fit(np_arr_training, y) 

        first=clf.predict(np_arr_test)
        print('SVM match: '+str(first))

        #print("1st Match:   "+str(first)+"\n")            
        #print("2nd Match:   "+str(auth2)+"\n")
        #print("3rd Match:   "+str(auth3)+"\n")
 
        if topthree == first:
            print('***1st match***')
            global n_top1
            n_top1=n_top1+1
        else:
            print('***No match***')
            global n_none 
            n_none =n_none +1

        
        '''
        ttl=0
        n=0
        temp=[]
        temp2=[]
      #  print('\n---------------------\nTEST FILE ATTRIBUYTES\n---------------------\n')


        with open('Author/'+'TEST_trained_data_11_features'+'.txt') as f:
            testarr = f.readlines()
        for x in range(0, len(testarr)):           #numerical attributes of each trained file
            #print(testarr[x], end='')
            testarr[x]=float(testarr[x])
            
        #print('\n---------------------\nATTRIBUYTES OF AUTHORS\n---------------------\n')
        for filename in glob.glob(os.path.join('Author', '*.txt')):
            with open(filename) as f:
                if filename !='Author\TEST_trained_data_11_features.txt':
                    arr2 = f.readlines()
                    for xx in range(0, len(arr2)):
                        ttl+=abs(float(testarr[xx])-float(arr2[xx]))
                        arr2[xx]=float(arr2[xx])

                    #result = 1 - (spatial.distance.cosine(testarr,arr2 ))      #cosine similarity
                    #print(result)


                    n+=1    
                    #print('Author '+ str(n) + ' :' +str(ttl) + '   '+str(filename))        #closest matches info
                    #textbox1.insert(END, 'Author '+ str(n) + ' :' + str(ttl) + '   '+str(filename) +'\n' , 'tag2')
                    temp.append(ttl)
                    temp2.append(filename)
                    ttl=0
        
        print('\n')
        kk=temp.index(min(temp))

        l2 = [temp.index(x) for x in sorted(temp)]
        top1=l2[0]
        top2=l2[1]
        top3=l2[2]
        

        auth1=temp2[top1]
        auth1=auth1[auth1.find('\\')+1 : auth1.find('_')]
        auth2=temp2[top2]
        auth2=auth2[auth2.find('\\')+1 : auth2.find('_')]
        auth3=temp2[top3]
        auth3=auth3[auth3.find('\\')+1 : auth3.find('_')]

        print("1st Match:   "+str(auth1)+"\n")            
        print("2nd Match:   "+str(auth2)+"\n")
        print("3rd Match:   "+str(auth3)+"\n")

        
        if topthree == auth1:
            print('***1st match***')
            global n_top1
            n_top1=n_top1+1
        elif topthree == auth2:
            print('***2nd match***')
            global n_top2
            n_top2=n_top2+1
        elif topthree == auth3:
            print('***3rd match***')
            global n_top3
            n_top3=n_top3+1
        else:
            print('***No match***')
            global n_none 
            n_none =n_none +1
        
        textbox1.insert(END, '\n\n1st Match:   '+ str(temp2[top1]) + '\n' , 'color')
        textbox1.insert(END, '2nd Match:   '+ str(temp2[top2]) + '\n' , 'color')
        textbox1.insert(END, '3rd Match:   '+ str(temp2[top3]) + '\n' , 'color')
        
        #textbox1.config(state=DISABLED)

        #tkinter.messagebox.showinfo( "Congragulations ", "Identificaiton Complete !" )


        '''

  #####################################################################################################################

        

         
    space=Label(f2, text="\n\n")
    l = Label(f2,borderwidth=5,    font=('Agency FB', 25, 'bold'), height=3, foreground='#476042')

    btn_train_folder = tkinter.Button(f2, text ="TRAIN FOLDER", command = DF_PY, font=('Agency FB', 11, 'bold'), foreground='#476042', width=12, height=2, bd=3, relief=RIDGE)
    btn_clear = tkinter.Button(f2, text ="RESET", command = CLEAR, font=('Agency FB', 11, 'bold'), foreground='#476042', width=12, height=2, bd=3, relief=RIDGE)
    btn_test_folder = tkinter.Button(f2, text ="INITIALIZE TESTING", command = test_folder_btn, font=('Agency FB', 11, 'bold'), foreground='#476042', width=16, height=2, bd=3, relief=RIDGE)
    
    btn1 = tkinter.Button(f2, text ="DISPLAY RESULTS", command = disp_result_btn, font=('Agency FB', 11, 'bold'), foreground='#476042', width=18, height=2, bd=3, relief=RIDGE)
   # btn_clear_textbox = tkinter.Button(f2, text ="CLEAR", command = CLEAR, font=('Ariel', 11, 'bold'), foreground='#476042', width=18, height=2, bd=3, relief=RIDGE)
    
    textbox1 = Text(f2, height=20, width=90)
    textbox1.tag_configure('color', foreground='#476042', font=('Arial', 12, 'bold'))
    textbox1.tag_configure('tag2', font=('Arial', 10 ))

    app = Window(gui)
    go()   
    l.pack()
    btn_clear.pack()
    btn_train_folder.pack()
    btn_test_folder.pack()
    btn1.pack(pady=2)
    space.pack()
    textbox1.pack()
   # btn_clear_textbox.pack()
    c.pack()
    
    gui.update()
    c2.config(scrollregion=c2.bbox("all"))
    gui.mainloop()



#####################################################################################################################















