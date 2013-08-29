import AbstractClasses
import ROOT
import os
import AbstractClasses.Helper.BetterConfigParser 
import AbstractClasses.Helper.HtmlParser
import AbstractClasses.Helper.environment
#as BetterConfigParser
import AbstractClasses.Helper.testchain
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
  
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_TestResult'
        self.NameSingle='QualificationGroup'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = self.Attributes['QualificationType'] + " " + self.Attributes['ModuleID']
        if self.Attributes['TestType'] == 'automatic':
            self.ResultData['SubTestResultDictList'] = self.extractTests()
        elif self.Attributes['TestType'] == 'singleFulltest':
            print 'add singleFulltest subTestResults'
            self.ResultData['SubTestResultDictList'] = [
                {
                    'Key':'singleFulltest',
                    'Module':'Fulltest',
                    'InitialAttributes':{
                        'StorageKey':    'Fulltest_p17_1',
                        'TestResultSubDirectory': '.',
                        'IncludeIVCurve':False,
                        'IVCurveSubDirectory':    '',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'p17',
                        'TestTemperature':17,
                        'ChipNo':0,
                    },
                    'DisplayOptions':{
                        'Order':1        
                    }
                },
                                                        ]
#        elif self.Attributes['TestType'] == 'FullQualification':
#            self.ResultData['SubTestResultDictList'] = [
#                {
#                    'Key':'ModuleFulltest_p17',
#                    'Module':'Module',
#                    'InitialAttributes':{
#                        'StorageKey':    'ModuleFulltest_p17',
#                        'TestResultSubDirectory': '004_Fulltest_p17',
#                        'IncludeIVCurve':True,
#                        'IVCurveSubDirectory':    '005_IV_p17',
#                        'ModuleID':self.Attributes['ModuleID'],
#                        'ModuleVersion':self.Attributes['ModuleVersion'],
#                        'ModuleType':self.Attributes['ModuleType'],
#                        'TestType':'p17',
#                        'TestTemperature':17,
#                    },
#                    'DisplayOptions':{
#                        'Order':3        
#                    }
#                },
#                {
#                    'Key':'ModuleFulltest_m10_1',
#                    'Module':'Module',
#                    'InitialAttributes':{
#                        'StorageKey':    'ModuleFulltest_m10_1',
#                        'TestResultSubDirectory': '001_Fulltest_m10',
#                        'IncludeIVCurve':False,
#                        'ModuleID':self.Attributes['ModuleID'],
#                        'ModuleVersion':self.Attributes['ModuleVersion'],
#                        'ModuleType':self.Attributes['ModuleType'],
#                        'TestType':'m10_1',
#                        'TestTemperature':-10,
#                    },
#                    'DisplayOptions':{
#                        'Order':1        
#                    }
#                },
#                {
#                    'Key':'ModuleFulltest_m10_2',
#                    'Module':'Module',
#                    'InitialAttributes':{
#                        'StorageKey':    'ModuleFulltest_m10_2',
#                        'TestResultSubDirectory': '002_Fulltest_m10',
#                        'IncludeIVCurve':True,
#                        'IVCurveSubDirectory':    '003_IV_m10',
#                        'ModuleID':self.Attributes['ModuleID'],
#                        'ModuleVersion':self.Attributes['ModuleVersion'],
#                        'ModuleType':self.Attributes['ModuleType'],
#                        'TestType':'m10_2',
#                        'TestTemperature':-10,
#                        'recalculateCurrentTo': 17
#                    },
#                    'DisplayOptions':{
#                        'Order':2        
#                    }
#                },
#            ]
#
#        elif self.Attributes['TestType'] == '2TempQualification':
#            self.ResultData['SubTestResultDictList'] = [
#                {
#                    'Key':'TemperatureCycle',
#                    'Module':'TemperatureCycle',
#                    'InitialAttributes':{
#                        'StorageKey':    'ModuleFulltest_TemperatureCycle',
#                        'TestResultSubDirectory': 'configfiles',
#                        'ModuleID':self.Attributes['ModuleID'],
#                        'ModuleVersion':self.Attributes['ModuleVersion'],
#                        'ModuleType':self.Attributes['ModuleType'],
#                        'TestType':'TemperatureCycle',
#                    },
#                    'DisplayOptions':{
#                        'Order':1        
#                    }
#                },
#                {
#                    'Key':'ModuleFulltest_p17_1',
#                    'Module':'Module',
#                    'InitialAttributes':{
#                                         #Storage Key is needed to identify the 
#                        'StorageKey':    'ModuleFulltest_p17_1',
#                        'TestResultSubDirectory': '000_Fulltest_p17',
#                        'IncludeIVCurve':True,
#                        'IVCurveSubDirectory':    '001_IV_p17',
#                        'ModuleID':self.Attributes['ModuleID'],
#                        'ModuleVersion':self.Attributes['ModuleVersion'],
#                        'ModuleType':self.Attributes['ModuleType'],
#                        'TestType':'p17_1',
#                        'TestTemperature':17,
#                    },
#                    'DisplayOptions':{
#                        'Order':3        
#                    }
#                },
#                {
#                    'Key':'ModuleFulltest_m10_1',
#                    'Module':'Module',
#                    'InitialAttributes':{
#                        'StorageKey':    'ModuleFulltest_m10_1',
#                        'TestResultSubDirectory': '002_Fulltest_m10',
#                        'IncludeIVCurve':True,
#                        'IVCurveSubDirectory':    '003_IV_m10',
#                        'ModuleID':self.Attributes['ModuleID'],
#                        'ModuleVersion':self.Attributes['ModuleVersion'],
#                        'ModuleType':self.Attributes['ModuleType'],
#                        'TestType':'m10_1',
#                        'TestTemperature':-10,
#                        'recalculateCurrentTo': 17
#                    },
#                    'DisplayOptions':{
#                        'Order':2        
#                    }
#                },
#                
#            ]
   
    def extractTests(self):
        print 'Extract Tests from config file'
        absPath = self.TestResultEnvironmentObject.TestResultsPath+'/configfiles'
        testList = []
        if not os.path.isdir(absPath):
            print 'dir: %s does not exist'%absPath
            pass
        self.initParser = AbstractClasses.Helper.BetterConfigParser.BetterConfigParser()
        fileName = absPath+'/elComandante.ini'
        if os.path.isfile(fileName):
#            print 'read configParser'
            self.initParser.read(fileName)
            tests = self.initParser.get('Tests','Test')
#            print tests
            testList = self.analyseTestList(tests)
#            print tests
        else:
            print "file %s doesn't exist"%fileName
#        print 'done with extraction'
        return testList
        pass
    
    def analyseTestList(self,testList):
        tests =[]
        testchain = AbstractClasses.Helper.testchain.parse_test_list(testList)
        test = testchain.next()
        while test:
            env = AbstractClasses.Helper.environment.environment(test.test_str, self.initParser)
            test.environment = env
            test.testname = test.test_str.split("@")[0]
            test = test.next()
        index = 0
        test = testchain.next()
        while test:
            if 'Fulltest' in test.testname:
                tests,test,index = self.appendFulltest(tests,test,index)
            elif 'Cycle' in test.testname:
                tests,test,index = self.appendTemperatureCycle(tests, test, index)
            elif 'XraySpectrum' in test.testname:
                tests,test,index = self.appendXraySpectrum(tests,test,index)
            else:
                index += 1
                test = test.next()
                
#        print '\n'
#        for item in tests:
#            for key in item:
#                print key,": ",item[key]
            
#            for key, value in item:
#                print key, value
#            print '\n'
#        for item in testchain:
#            print item
#        for item in testList:
#            item.
#            pass
        
        return tests
    
    def appendTemperatureCycle(self,tests,test,index):
#         print  '%03d'%index, test.testname, test.environment
         tests.append(
                      {
                    'Key':'TemperatureCycle',
                    'Module':'TemperatureCycle',
                    'InitialAttributes':{
                        'StorageKey':    'ModuleFulltest_TemperatureCycle',
                        'TestResultSubDirectory': 'configfiles',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'TemperatureCycle',
                    },
                    'DisplayOptions':{
                        'Order':len(tests)+1        
                    }
                })
         test = test.next()
         index += 1
         return tests,test,index
     
    def appendFulltest(self,tests,test,index):
#        print  '%03d'%index, test.testname, test.environment
        environment = test.environment
        key = 'Module%s_%s'%(test.testname,test.environment.name)
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys +=1
        key+='_%s'%(nKeys)        
        directory = '%03d'%index+'_%s_%s'%(test.testname,test.environment.name)
        tests.append( {
            'Key': key,
            'Module':'Fulltest',
            'InitialAttributes':{
                'StorageKey':    key,
                'TestResultSubDirectory': directory,
                'IncludeIVCurve':False,
                'ModuleID':self.Attributes['ModuleID'],
                'ModuleVersion':self.Attributes['ModuleVersion'],
                'ModuleType':self.Attributes['ModuleType'],
                'TestType': '%s_%s'%(test.environment.name,nKeys),
                'TestTemperature':test.environment.temperature,
            },
            'DisplayOptions':{
                'Order':len(tests)+1        
            }
           })
        if test.environment.temperature != 17:
            tests[-1]['InitialAttributes']['recalculateCurrentTo'] = 17
        test = test.next()
        index += 1
        if test and 'IV' in test.testname and test.environment.name == environment.name:
#            print '\tFound corresponding', test.testname, test.environment
            tests[-1]['InitialAttributes']['IncludeIVCurve'] =True
            tests[-1]['InitialAttributes']['IVCurveSubDirectory'] = '%03d_%s_%s'%(index,test.testname,test.environment.name)
            test = test.next()
            index += 1
        return tests,test,index
    
    def appendXraySpectrum(self,tests,test,index):
        print 'ADDING XraySpectrumMethod'
        environment = test.environment
        key = 'XraySpectrumMethod'
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys +=1
        key+='_%s'%(nKeys)        
        directory =  "."
        tests.append( {
            'Key': key,
            'Module':'XrayCalibrationSpectrum',
            'InitialAttributes':{
                'StorageKey':    key,
                'TestResultSubDirectory': directory,
                'IncludeIVCurve':False,
                'ModuleID':self.Attributes['ModuleID'],
                'ModuleVersion':self.Attributes['ModuleVersion'],
                'ModuleType':self.Attributes['ModuleType'],
                'TestType': 'XraySpectrum',
                'TestTemperature':test.environment.temperature,
            },
            'DisplayOptions':{
                'Order':len(tests)+1,
                #'Width':1
            }
           })
        while test and 'XraySpectrum' in test.testname:
            tests,test,index = self.appendFluorescenceTarget(tests,test,index)
        
        print'\n'
        for i in  tests[-1]['InitialAttributes']['SubTestResultDictList']:
            print i
            print '\n'
        return tests,test,index

    # Hard coded initial guess for signal position based on element name
    def GetEnergy(self,elementName):
        if "Fe" in elementName:
            return 6391.02
        elif "Ni" in elementName:
            return 7461.03
        elif "Cu" in elementName:
            return 8027.84
        elif "Br" in elementName:
            return 11877.75
        elif "Mo" in elementName:
            return 17374.29
        elif "Ag" in elementName:
            return 21990.30
        elif "Sn" in elementName:
            return 25044.04
        elif "Ba" in elementName:
            return 31816.615
        else:
            return 0

    def appendFluorescenceTarget(self,tests,test,index):
        environment = test.environment
        print 'ADDING FluorescenceTarget @ %s'%environment.name
        key = 'Module%s_%s'%(test.testname,test.environment.name)
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys +=1
        key+='_%s'%(nKeys)        
        directory = '%03d'%index+'_%s_%s'%(test.testname,test.environment.name)
        print 'XRAY Spectrum @ %s in dir %s:"%s"'%(environment,directory,key)
        TargetEnergy= self.GetEnergy(environment.name)
        TargetNElectrons = TargetEnergy / 3.6
        if not tests[-1].has_key('InitialAttributes'):
            tests[-1]['InitialAttributes'] = {}
        if not tests[-1]['InitialAttributes'].has_key('SubTestResultDictList'):
            tests[-1]['InitialAttributes']['SubTestResultDictList']=[]
        tests[-1]['InitialAttributes']['SubTestResultDictList'].append({
               'Key': key,
               'Module':'FluorescenceSpectrum',
               'InitialAttributes':{
                         'StorageKey':    key,
                        'TestResultSubDirectory': directory,
                        'IncludeIVCurve':False,
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType': '%s_%s'%(test.environment.name,nKeys),
                        'TestTemperature':test.environment.temperature,
                        'Target': environment.name,
                        'TargetEnergy': TargetEnergy,
                        'TargetNElectrons': TargetNElectrons
                },
                'DisplayOptions':{
                        'Order':len(tests[-1]['InitialAttributes']['SubTestResultDictList'])+1        
                }
           })
        test = test.next()
        index +=1
        return tests,test,index 
    
    def PopulateResultData(self):
        
        ModuleResultOverviewObject = AbstractClasses.ModuleResultOverview.ModuleResultOverview(self.TestResultEnvironmentObject)
        ModuleResultOverviewObject.StoragePath = self.StoragePath
        self.ResultData['Table'] = ModuleResultOverviewObject.TableData(self.Attributes['ModuleID'],self.Attributes['TestDate'],ShrinkedList = False)
        
    def PostWriteToDatabase(self):
        self.PopulateResultData();