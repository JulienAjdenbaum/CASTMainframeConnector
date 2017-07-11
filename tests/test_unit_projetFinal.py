import unittest
import cast.analysers.test
from cast.analysers import filter
from cast.analysers import log

class TestUnit(unittest.TestCase):
    
    def test_annotation_inheritance_one_table(self):
        analysis = cast.analysers.test.DotNetTestAnalysis()
         
        analysis.add_selection('V2/StudentRecordsManager/BusinessProcessor/BusinessProcessor.csproj')
        analysis.add_selection('V2/StudentRecordsManager/DataProcessor/DataProcessor.csproj')
        analysis.add_selection('V2/StudentRecordsManager/DbEntities/DbEntities.csproj')
        #table_student_info = analysis.add_database_table('StudentInfo','TSQL')
        
        analysis.set_verbose()
        analysis.run()
 
        #student_class = analysis.get_object_by_fullname('SchoolDomainClasses.Student', filter.classes)
        #self.assertTrue(analysis.get_link_by_caller_callee('useLink', student_class, table_student_info))
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
