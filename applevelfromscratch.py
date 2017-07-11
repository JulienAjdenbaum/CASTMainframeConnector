'''
Created on Jun 23, 2017

@author: JAJ
'''
import logging
from cast.application import ApplicationLevelExtension, create_link, Bookmark
import sys
import re
def testifsql(h):
        try:
            codea = h.split("\n")
        except:
            codea = h
        a = 1
        for code in codea:    
#             try:
#                 b = code.split("SELECT COUNT")[1]
# #                 print("SELECT COUNT")
#                 a = 0
#                 return "select",b
#                 break
#             except:
            try:
                b = code.split("UPDATE")[1]
#                     print("UPDATE")
                a = 0
                return "update",b
                break
            except:
                try:
                    b = re.split("INSERT +INTO",h)[1]
#                         print("INSERT")
                    a = 0
                    return "insert into",b
                    break
                except:
                    try:
                        b = code.split("SELECT")[1]
#                             print("SELECT")
                        a = 0
                        return "select",b
                        break
                    except:
                        pass
        if(a==1):
            return "nothing",0
        
        
        
class AppLevel(ApplicationLevelExtension):
    
    def end_application(self, application):
        #print('Yo')
        qwe = 0
        variables = application.objects().has_type("CAST_DotNet_MethodCSharp") #get all the variables
        #
        #
        #
        t = 0
        for link in application.links().has_callee(variables).load_positions():
#             print(link.get_caller().get_name())
            try:
                
                code = link.get_code(3)
#                 #print("test11")
#                 print(link.get_caller().get_name())
#                 print(code)
#                 print()
                sql,b = testifsql(code)
                
#                 print(sql)
                if(sql=="nothing"):
                    continue
                try:
                    c,a = b.split("=")
                    b = c
                except:
                    pass
#                 print("test1 = ",b)
                objettemp = b.split("\\\"") #split at /"
#                 #print(link.get_caller().get_name()+ " : type SELECT")
                

                objet = [""]*len(objettemp)
                
                t = 0
                motsinterdits = {" FROM ",".",", ","\");","\");\n"," "," WHERE "," ORDER BY ","(",") FROM ",""}
                for x in range(len(objettemp)):
#                     #print("objettemp[x] =" + objettemp[x] , end = " ")
                    h = 0
                    for y in motsinterdits:
                        if(objettemp[x] == y):
                            h = 1
                    if(h == 0):
#                   
                        objet[t] = objettemp[x]
                        t += 1
#                 print(objet)
                for obj in objet:    
                    for f in application.objects():
#                         #print("name =" + f.get_name() + "<=>" + objet[t] + "!")
                        if(f.get_name() == obj and f.get_type() == "SQLScriptTable"):
#                                 print(f.get_name()+ "        " +f.get_type())
                            try:
    #                     #print("getting positions")
                                
                                positions = str(link.get_caller().get_positions())
                                #print(positions)
                                pos = ""
                                for i in range(len(positions)-2):
                                    pos += positions[i+1]
                                #print("testa")
                                arr = pos.split(",")
                                file = arr[0].split("(")
                                #print("testb")
                                line = int(arr[2])+2
                                
                                for ds in application.objects():
                                    if (ds.get_name() == file[2]):
                                        #print("file found")
                                        asd = ds
                                
                                hg = 0
                                tes = 0
                                if(sql == "select"):
                                    code = code.split("{")[1]
#                                     print("done")
                                for lo in range(len(code)):
#                                     try:
#                                         print(str(hg)+"    "+obj[hg]+"    "+str(lo)+"    "+code[lo])
#                                     except:
#                                         print("fail:", sys.exc_info()[0])
                                    if(hg<len(obj)):
                                        if(code[lo] == obj[hg]):
                                            hg += 1
                                            continue
                                        else:
                                            hg = 0
                                    else:
                                        tes = 1
                                        column = lo-len(obj)
                                        break              
                                    
                            except:
                                print("Unexpected error:", sys.exc_info()[0])
                                
                            #print("test1")
                            print("creating a link from" + link.get_caller().get_name() + " to "+ f.get_name())
                            
                            bookmark = Bookmark(asd,line, column, line, column+len(obj))
                            
                            #print("test1")
                            print("type : ",end="")
                            if(sql == "insert"):
                                create_link("useInsertLink",link.get_caller(),f,bookmark)
                                print("insert") 
                            if(sql == "insert into"):
                                create_link("useInsertLink",link.get_caller(),f,bookmark)
                                print("insert into")                           #print("test2")
                            if(sql == "select"):
                                create_link("useSelectLink",link.get_caller(),f,bookmark)
                                print("select")  
                            if(sql == "update"):
                                create_link("useUpdateLink",link.get_caller(),f,bookmark)
                                print("update")                            #print("test3")
                            if(sql == "select count"):
                                create_link("useSelectLink",link.get_caller(),f,bookmark)
                                print("select")
                            qwe = 1    
                        
                    if(qwe == 1):
                        qwe = 0
                        break    
            except:
                print("Unexpected error 2:", sys.exc_info()[0])
            t += 1  
            #
    def end_application2(self, application):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    # 
        #print("finished")
        
    