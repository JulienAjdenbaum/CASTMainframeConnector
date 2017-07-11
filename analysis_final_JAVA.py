'''
Created on Jun 22, 2017
 
@author: JAJ
'''
import cast.analysers.jee
from cast.analysers import log
import re
from cast.application import ApplicationLevelExtension,  Bookmark, create_link, logging
# class JEEAnnotation(cast.analysers.JEEExecutionUnit):
#     
# #     i = [""]
# #     currenttype = None
#     def start_analysis(self,option):
#         cast.analysers.log.warning("analysis started")
#         cast.analysers.log.warning("option 1 : " + option)
        
class JEEAnnotation(cast.analysers.jee.Extension):
    
    i = [""]
#     currenttype = None
    def start_analysis(self,options):
        cast.analysers.log.warning("analysis started")
        
    def objetcreation(self,parent,limpor,programme,fonction,callee,typedobj):
        posi = parent.get_position()
        cast.analysers.log.warning(posi.get_file().get_name())
        classcode = AppLevel.takecode(self,posi.get_file(),posi.get_begin_line(),posi.get_begin_column(),posi.get_end_line(),posi.get_end_column) # get the code
        classcodeperline = re.split("\n",classcode)
        ligne = False
        linenumber = None
        for x in range(len(classcodeperline)):
            if (re.search(programme+"\(\)", classcodeperline[x])!=None):
                cast.analysers.log.warning(classcodeperline[x])
                ligne = True
                linenumber = x + posi.get_begin_line()
                collonnenumber = len(classcodeperline[x])
        if(str(linenumber)!=None):
            cast.analysers.log.warning("linenumber"+str(linenumber))
        else:
            cast.analysers.log.warning("No Line Number")

        if (ligne): #si la commande existe
            cast.analysers.log.warning(fonction+" Found")
            impors = AppLevel.takecode(self,posi.get_file(),0,0,posi.get_end_line(),posi.get_end_column)
            impor = re.split("import",impors)
            importfound = False
            limpors = limpor.split(".")
            imporfinal = " "
            for x in range(len(limpors)-1):
#                 cast.analysers.log.warning()
                imporfinal += limpors[x]
                imporfinal += "\."
            imporfinal += limpors[len(limpors)-1]
            cast.analysers.log.warning("imporfinal est "+ imporfinal)
            for imp in range(len(impor)-2):
                
#                 cast.analysers.log.warning(impor[imp+1])
                if(re.match(imporfinal,impor[imp+1])!= None):
                    importfound = True
                cast.analysers.log.warning("t"+impor[imp+1]+"        "+str(importfound))
            if importfound:
                cast.analysers.log.warning("l'immport cics a ete trouve")
                ligne = re.search(fonction+"\((.+)\)", classcode)
                if (ligne!= None):
                    cast.analysers.log.warning(fonction+" found")
                ligne = ligne.group(1)
                stringoupas = re.match("\"",ligne)
                if(stringoupas == None):
                    cast.analysers.log.warning("C'est une variable. Son nom est : "+ligne)
                    lastring = re.search(ligne+" *= *\"(\w*)", classcode).group(1)
                    
                    cast.analysers.log.warning("sa valeur est : "+lastring)
                else:
                    lastring = re.split("\"",ligne)
                    cast.analysers.log.warning("C'est une string : "+ lastring)
                result = cast.analysers.CustomObject()
                result.set_type(typedobj)
#                 result.set_type('JV_METHOD')
                nom = parent.get_name()+" Cobol prgm " + lastring + "cherche" + callee
                cast.analysers.log.warning(nom)
                result.set_name(nom)
                wsname = nom + parent.get_name()
                asdfghjkl = 0
                for existingObject in self.i: #checks if the object dosn't already exist
                    if(existingObject == wsname):
                        asdfghjkl = 1
                if(asdfghjkl == 0): # if the object doesn't exist, create it 
                    self.i.append(wsname)
                    result.set_fullname(wsname)
                    result.set_parent(parent)
                    result.set_guid(wsname)
                    result.save()
                    
#                     result.save_property("Callee", lastring)
                    cast.analysers.log.warning("fullname ="+result.fullname)
                    cast.analysers.log.warning("name = "+result.name)
                    cast.analysers.log.warning(result.typename)
                    cast.analysers.log.warning(result.guid)
#                     parent = AppLevel.findparent(AppLevel,parent,self)
                    objetfinal = None
                    cast.analysers.log.warning("parser        "+str(linenumber))
                    for o in parent.get_children():
                        pos = o.get_position()
                        beginline = pos.get_begin_line()
                        endline = pos.get_end_line()
                        logging.debug(o.get_name()+ "        "+str(beginline)+"        "+str(endline))
                        cast.analysers.log.warning(str(beginline)+"        "+str(endline))
                        if (beginline<=linenumber and endline>=linenumber):
                            cast.analysers.log.warning("appartient")
                            objetfinal = o
#                             mybookmark = Bookmark(pos.get_file(),linenumber,1,linenumber,collonnenumber)
#                             cast.analysers.log.warning(str(pos))
                            result.save_position(pos)
                    if(objetfinal != None):
                        cast.analysers.log.warning("parent name = "+objetfinal.get_name())
                        cast.analysers.create_link('callLink',objetfinal,result,posi)
                        
                    else:
                        cast.analysers.create_link('callLink',parent,result,posi)
                        cast.analysers.log.warning("Program n'est pas dans une fonction")
                    JEEAnnotation.creerobjet(self, "thereisnoprogram"+parent.get_name(), "APIConnect_unknownqueue", parent)
                else:
                    cast.analysers.log.warning("??????????skiped???????????") #if the link alreqady exists, skip it
            else:
                cast.analysers.log.warning("l'immport cics n'a pas ete trouve")
        else:
            cast.analysers.log.warning("Program Not Found")
            
    def start_type(self,_type):
        cast.analysers.log.warning("visiting _type --> " + _type.get_name())
        logging.debug(str(_type))
        self.objetcreation(_type,"com.ibm.cics","Program","setName","CAST_COBOL_SavedProgram",'APIConnect_myobject')
        self.objetcreation(_type,"com.ibm.cics","TDQ","setName","CAST_COBOL_SavedProgram",'APIConnect_myobject')
    def creerobjet(self,name,type1,parent):
        wsname = name + parent.get_name()
        monobjet = cast.analysers.CustomObject()
        monobjet.set_type(type1)
        monobjet.set_name(name)
        monobjet.set_fullname(wsname)
        monobjet.set_guid(wsname)
        monobjet.set_parent(parent)
        monobjet.save()
        cast.analysers.log.debug("objet special cree")
class AppLevel(ApplicationLevelExtension):
    objetscrees = [[]]
    def end_application(self, application):
        
        logging.debug("end_application1")
        for o in application.objects():
#             for o in application.objects().has_type('APIConnect_myobject'):
#                 logging.debug(o.get_name())
                a = re.search("Cobol prgm (\w+)", o.get_name())
                
                if(a!=None):
                    logging.debug("oui1")
                    logging.debug(o.get_name())
                    nolinkcreated = True
                    a = a.group(1)
                    logging.debug(a)
                    b = a.split("cherche")
                    logging.debug(b)
#                     try:
                    logging.debug(b[1])
                    print(o.get_name()+" o.get_name()")
#                     logging.debug(ob.get_name())
                   
                    for ob in application.objects().has_type(b[1]):
#                         logging.debug("ob = "+ob.get_name()+"        "+b[0])
                        if (ob.get_name() == b[0]):
                            logging.debug(ob.get_type()+"        "+ob.get_name()+"    "+o.get_type()+"    "+o.get_name() )
                            logging.debug("qqqqqqqqqqqqqqqqqqq")
                            create_link("callLink",o,ob)
                            logging.debug("link created")
                            nolinkcreated = False
                    if(nolinkcreated):
                        logging.debug("oui")
                        ab = re.search("(.+) Cobol", o.get_name()).group(1)
                        logging.debug("a = "+ab)
                        for ob in application.objects().has_type("APIConnect_unknownqueue"):
                            print(ob.get_name())
                            a = re.search("thereisnoprogram"+ab,ob.get_name())
                            if(a != None):
#                                 logging.debug(a)                            
                                create_link("callLink", o, ob)
                                logging.debug("lien de type et objets crees")
            
            #                     except:
#                         logging.debug("pas cherche")            
    def takecode(self,fi,a,b,c,d): #get the code of the bookmark
        book = Bookmark(fi,a,b,c,d)
        return book.get_code()