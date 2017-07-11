'''
Created on Jun 22, 2017
 
@author: JAJ
'''
import cast.analysers.dotnet
from cast.analysers import log , create_link, external_link
from random import randint
import re
from cast.application import ApplicationLevelExtension, create_link, Bookmark
import sys
from cast import analysers

class DotNetAnnotation(cast.analysers.dotnet.Extension):
    
    i = [""]
    currenttype = None
    def start_analysis(self,option):
        log.debug("analysis started")

    def start_type(self, _type):
        log.warning("visiting _type --> " + _type.get_name())
#         posi = _type.get_position()
#         name = AppLevel.takecode(self,posi.get_file(),posi.get_begin_line(),posi.get_begin_column(),posi.get_end_line(),posi.get_end_column) # get the code
#         ligne = re.search("\w+\.ExecuteNonQuery\(\)", name)
#         if (ligne != None): #si la commande existe
#             result = cast.analysers.CustomObject()
#             result.set_type('APIConnect_myobject')
#             nom = "toto" + _type.get_name()
#             result.set_name(nom)
#             wsname = _type.get_name() + nom
#             asdfghjkl = 0
#             for existingObject in self.i: #checks if the object dosn't already exist
#                 if(existingObject == wsname):
#                     asdfghjkl = 1
#             if(asdfghjkl == 0): # if the object doesn't exist, create it 
#                 self.i.append(wsname)
#                 result.set_fullname(wsname)
#                 result.set_parent(_type)
#                 result.set_guid(wsname)
#                 result.save()
# #                 log.warning("fullname ="+result.fullname)
# #                 log.warning("name = "+result.name)
# #                 log.warning(result.typename)
# #                 log.warning(result.guid)
#      
#                 create_link('callLink',_type,result) # create the link
#             else:
#                 log.warning("??????????skiped???????????") #if the link alreqady exists, skip it
# #             log.warning(str(link))
#     #     def introducing__type(self,_type)
#     #         log.warning('analysis ended! ')
# #             log.warning("")
#         else:
#             log.debug("pas trouve")
#             log.debug(name)
    #         for x in _type.get_children():
    #             try:
    #                 log.debug(x.is_variable)
    #             except:
    #                 log.debug("except")
    #         log.debug("")
#     def end_analysis(self):
#         log.warning('analysis ended! ')   
#         log.warning("start type -->" + _type)
#         a = _type.get_source_files()
#         log.warning(a)
#         for annotation in _type.get_annotations():
#             log.warning(str(annotation))
class AppLevel(ApplicationLevelExtension):
    def takecode(self,fi,a,b,c,d): #get the code of the bookmark
        book = Bookmark(fi,a,b,c,d)
        return book.get_code()