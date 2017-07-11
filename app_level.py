'''
Created on Jun 23, 2017

@author: JAJ
'''
import cast.analysers.dotnet
from cast.analysers import log , create_link
from random import randint
import re
from cast.application import ApplicationLevelExtension, create_link, Bookmark
import sys
from cast.application.internal import application

        
def testifsql(h): # search if it is a SQL command, and if it is 
        try:
            codea = h.split("\n")
        except:
            codea = h
        a = 1
        for ligneCode in codea:    
            try:
                b = ligneCode.split("UPDATE")[1]
#                     print("UPDATE")
                a = 0
                return "update",b
                break
            except:
                try:
                    b = re.split("INSERT +INTO",ligneCode)[1]
#                         print("INSERT")
                    a = 0
                    return "insert into",b
                    break
                except:
                    try:
                        b = ligneCode.split("SELECT")[1]
#                             print("SELECT")
                        a = 0
                        return "select",b
                        break
                    except:
                        pass
        if(a==1):
            return "nothing",0
        
        
        
class AppLevel(ApplicationLevelExtension):
    
    def end_application4(self,application):
#         for o in application.objects():
#             print(o.get_type(*))
        ttypes = []
        tobjects  = []
        for objet in application.objects():
            mytype = objet.get_type()
            myname = objet.get_name()
            print(mytype+"        "+myname)
#             if(re.match("JV\w+",mytype)!= None):
#                 bool = True
#                 count = 0
#                 for append in ttypes:
#                     if(append == mytype):
#                         bool = False
#                         num = count
#                     count += 1
#                 if(bool):
#                     num = len(ttypes)
#                     ttypes.append(mytype)
#                     tobjects.append([])        
#                 tobjects[num].append(myname)
#         for x in range(len(tobjects)):
#             print("")
#             tobjects[x].sort()
#             for y in tobjects[x]:
#                 print(ttypes[x] + "        "+y)
#             print("")        
#          
# #             print()""
    def end_application3(self, application):
        variables = application.objects().has_type("CAST_DotNet_MethodCSharp") #get all the variables
        for link in application.links().has_callee(variables).load_positions():
#             print(link.get_caller().get_name())
            try:
                
                code = link.get_code(3) #get the multiline code
#                 #print("test11")
#                 print(link.get_caller().get_name())
#                 print(code)
#                 print()
                sql,b = testifsql(code)
                
#                 print(sql)
                if(sql=="nothing"):
                    continue
                try:
                    c,a = b.split("=") # if there is an equal, take everything before it
                    b = c
                except:
                    pass
#                 print("test1 = ",b)
                print("b = "+b)
                
                objet = re.split("[^\w]+",b) #split at \"


                for obj in objet:
#                     print("objet         = "+ obj)    
                    if (obj != ""):
                        for f in application.objects():
    #                         #print("name =" + f.get_name() + "<=>" + objet[t] + "!")
                            try:
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
                                    print("creating a link from " + link.get_caller().get_name() + " to "+ f.get_name())
                                    
                                    bookmark = Bookmark(asd,line, column, line, column+len(obj))
                                    
                                    #print("test1")
                                    print("type : ",end="")
                                    print(sql)
                                    if(sql == "insert"):
                                        create_link("useInsertLink",link.get_caller(),f,bookmark)
    
                                    if(sql == "insert into"):
                                        create_link("useInsertLink",link.get_caller(),f,bookmark)
    
                                    if(sql == "select"):
                                        create_link("useSelectLink",link.get_caller(),f,bookmark)
    
                                    if(sql == "update"):
                                        create_link("useUpdateLink",link.get_caller(),f,bookmark)
    
                                    if(sql == "select count"):
                                        create_link("useSelectLink",link.get_caller(),f,bookmark)
                                    qwe = 1    
                            except:
                                print("error get_name")
                                pass
            except:
                print("Unexpected error 2:", sys.exc_info()[0])
            #
    def end_application2(self, application):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    # 
        #print("finished")
        
    