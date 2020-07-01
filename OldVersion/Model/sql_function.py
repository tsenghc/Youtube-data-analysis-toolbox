import MySQLdb
import time
import json
import datetime

class SQLFunction():
    def __init__(self,DBsetting):
        self.DBsetting=DBsetting
        
        

    def log(self,text):
        with open('./sql.txt','a') as e:
            e.write("[ %s ] : %s\n"%(time.strftime("%Y-%m-%d %H:%M:%S"),text))

    def raw_Input(self,SQL_text):
        db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
        cursor = db.cursor()
        cursor.execute(SQL_text)
        db.commit()
        db.close()

    def raw_Search(self,SQL_text):
        db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
        cursor = db.cursor()
        cursor.execute(SQL_text)
        data = cursor.fetchall()

        #db.commit()
        db.close()
        return data

    def Inst(self,Table,Field=[],Value=[]):
        
        if len(Field) != len(Value):
            return {'error':101}
        else:
            Field = str(Field)[1:len(str(Field))-1]
            Value = str(Value)[1:len(str(Value))-1]
            db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
            cursor = db.cursor()
            SQL_text = "INSERT INTO `%s`.`%s` (%s) VALUES (%s);"%(self.DBsetting['DateBase'],Table,Field.replace("'",""),Value)
            #cursor.execute(SQL_text)
            print(str(Field)+str(Value))
            try:
                cursor.execute(SQL_text)
                db.commit()
            except:
                self.log(text="error insert : "+Field+" "+Value)
                #print(SQL_text)
                db.rollback()
                db.close()
                return {'error':102}
            #data = cursor.fetchone()    for single line 
            # data = cursor.fetchall()  for all data 
            db.close()
        return {'error':0}

    def BatchChannelInst(self,Table,Field=[],filekey=[],filevalue=[]):        
        
        db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
        cursor = db.cursor()
        Field = str(Field)[1:len(str(Field))-1]

        Pstart=time.time()
        Tstart=time.time()
        
        for i in range(len(filevalue)):
            Value=[filekey[i],filevalue[i]]
            Value = str(Value)[1:len(str(Value))-1]  
            print(Value) 
            try:                
                SQL_text = "INSERT INTO `%s`.`%s` (%s) VALUES (%s);"%(self.DBsetting['DateBase'],Table,Field.replace("'",""),Value)                
                cursor.execute(SQL_text)
                db.commit()
            except Exception as identifier:
                #self.log(text="error insert : "+Field+" "+Value)                                         
                print(identifier)
            
            Tend=time.time()
            if ((Tend-Tstart)>5):
                print('寫入資料庫進度: %.2f' %(i/len(filekey)*100))
                Tstart=time.time()

        Pend=time.time()
        print('寫入總耗時：%.2f s 平均每秒比數：%.2f /s' %((Pend-Pstart),len(filekey)/(Pend-Pstart)))

        db.close()
            
    def BatchChannelInfoInst(self,Table,Field=[],Value=[]):
        db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
        cursor = db.cursor()
        Field = str(Field)[1:len(str(Field))-1]
        Value = str(Value)[1:len(str(Value))-1]  
        try:                
            SQL_text = "INSERT INTO `%s`.`%s` (%s) VALUES (%s);"%(self.DBsetting['DateBase'],Table,Field.replace("'",""),Value)                
            cursor.execute(SQL_text)
            db.commit()
        except Exception as identifier:
            #self.log(text="error insert : "+Field+" "+Value)                                                  
            print(identifier)
        db.close()

    def SquenVideoListInst(self,Table,Field=[],Value=[]):
        db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
        cursor = db.cursor()
        Field = str(Field)[1:len(str(Field))-1]
        Value = str(Value)[1:len(str(Value))-1]  
        
        try:                
            SQL_text = "INSERT INTO `%s`.`%s` (%s) VALUES (%s);"%(self.DBsetting['DateBase'],Table,Field.replace("'",""),Value)                
            cursor.execute(SQL_text)
            db.commit()
        except Exception as identifier:
            #self.log(text="error insert : "+Field+" "+Value)                                                  
            print(identifier)
        db.close()

    def BatchVideoListInst(self,Table,Field=[],filekey=[],filevalue=[]):

        db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
        cursor = db.cursor()
        Field = str(Field)[1:len(str(Field))-1]
        ProcessStart = time.time()
        Pstart=time.time()
        Tstart=time.time()
        RunCount=0
        BeforeRunCount=0
        
        for i in range(len(filevalue)):
            
            RunCount+=1
            Value=[filekey[i],filevalue[i]]
            Value = str(Value)[1:len(str(Value))-1]  
            
            try:                  
                SQL_text = "INSERT INTO `%s`.`%s` (%s) VALUES (%s);"%(self.DBsetting['DateBase'],Table,Field.replace("'",""),Value)                
                cursor.execute(SQL_text)
                db.commit()                
            except Exception as identifier:
                #SQLFunction.log(self,text="error insert : "+Field+" "+Value)                                         
                print(identifier)

            Tend=time.time()
            
            if ((Tend-Tstart)>self.DBsetting['RefreshTime']):                
                print('Progress status: %.2f' %(i/len(filekey)*100))
                print('Speed: %.f /s' % ((RunCount-BeforeRunCount)/self.DBsetting['RefreshTime']))
                print('NeedTime:%.2f /min  already: %d s' % ((((len(filevalue)/(((RunCount-BeforeRunCount))/self.DBsetting['RefreshTime']))-((Tend-ProcessStart)))/60),(Tend-ProcessStart)))
                print()
                Tstart=time.time()
                BeforeRunCount=RunCount

        Pend=time.time()
        print('寫入總耗時：%.2f s 平均每秒比數：%.2f /s' %((Pend-Pstart),len(filekey)/(Pend-Pstart)))

        db.close()

    def Update(self,Table,dic={},Where={}):
        
        db = MySQLdb.connect(self.DBsetting['IP'], self.DBsetting['Account'], self.DBsetting['Password'], self.DBsetting['DateBase'], charset='utf8' )
        cursor = db.cursor()
        Where_key = list(Where.keys())[0]
        Where_val = list(Where.values())[0]
        for key,val in dic.items():
            try:
                SQL_text = "UPDATE `%s`.`%s` SET `%s`='%s' WHERE `%s`='%s' LIMIT 1;"%(self.DateBase,Table,key,val,Where_key,Where_val)
                #print(SQL_text)
                cursor.execute(SQL_text)
            except:
                self.log(text="error update : "+key+" "+val)
                db.close()
                return {'error':201}
        try:
            db.commit()
        except:
            self.log('error commit in update')
            db.rollback()
            db.close()
            return {'error':202}
        db.close()
        return {'error':0}



