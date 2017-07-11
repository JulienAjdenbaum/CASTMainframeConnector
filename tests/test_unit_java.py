import unittest
import cast.analysers.test
from cast.analysers import filter
from cast.analysers import log
from cast.application.test import run


class TestUnit(unittest.TestCase):
    
    def test_annotation_inheritance_one_table(self):
        analysis = cast.analysers.test.JEETestAnalysis()
         
        analysis.add_selection('CobolFromJava\cics-java-jzosprog-master\projects\com.ibm.cicsdev.jzostest\src\com\ibm\cicsdev\jzostest\JZOSprog.java')


        #table_student_info = analysis.add_database_table('StudentInfo','TSQL')
        
        analysis.set_verbose()
        analysis.run()
        run(kb_name='finalplugin_local', application_name='Final') 
        #student_class = analysis.get_object_by_fullname('SchoolDomainClasses.Student', filter.classes)
        #self.assertTrue(analysis.get_link_by_caller_callee('useLink', student_class, table_student_info))
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
