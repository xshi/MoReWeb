# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import time
import glob
import json


class ModuleSummaryValues(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def MakeArray(self,p):

        
        Numbers = {
        'nA' : 0,
        'nB' : 0,
        'nC' : 0,
        'nM' : 0,
        'BrokenROC' : 0,
        'BrokenROCX' : 0,
        'nAtoB' : 0,
        'nAtoC' : 0,
        'nBtoC' : 0,
        'nBtoA' : 0,
        'nCtoA' : 0,
        'nCtoB' : 0,
        'nAtoBX' : 0,
        'nAtoCX' : 0,
        'nBtoCX' : 0,
        'nBtoAX' : 0,
        'nCtoAX' : 0,
        'nCtoBX' : 0,
        'nHDI' : 0,
        'nlcstartupB': 0, 
        'nlcstartupC' : 0,
        'nIV150B' : 0,
        'nIV150C' : 0,
        'nIV150m20B' : 0,
        'nIV150m20C' : 0,
        'nIVSlopeB' : 0,
        'nIVSlopeC' : 0,
        'nRecCurrentB' : 0,
        'nRecCurrentC' : 0,
        'nCurrentRatioB' : 0,
        'nCurrentRatioC' : 0,
        'ntotDefectsB' : 0,
        'ntotDefectsC' : 0,
        'ntotDefectsXrayB' : 0,
        'ntotDefectsXrayC' : 0,
        'nBBFullB' : 0,
        'nBBFullC' : 0,
        'nBBXrayB' : 0,
        'nBBXrayC' : 0,
        'nAddressdefB' : 0,
        'nAddressdefC' : 0,
        'nTrimbitdefB' : 0,
        'nTrimbitdefC' : 0,
        'nMaskdefB' : 0,
        'nMaskdefC' : 0,
        'ndeadpixB' : 0,
        'ndeadpixC' : 0,
        'nuniformityB' : 0,
        'nuniformityC' : 0,
        'nNoiseB' : 0,
        'nNoiseC' : 0,
        'nNoiseXrayB' : 0,
        'nNoiseXrayC' : 0,
        'nPedSpreadB' : 0,
        'nPedSpreadC' : 0,
        'nRelGainWB' : 0,
        'nRelGainWC' : 0,
        'nVcalThrWB' : 0,
        'nVcalThrWC' : 0,
        'nLowHREfB' : 0,
        'nLowHREfC' : 0,
        'nBrokenROCFull' : 0,
        'nBrokenROCXray' : 0
}

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort(reverse=True)

        FullTests = ['m20_1','m20_2','p17_1'][::-1]
        TestTypeLeakageCurrentPON = ['LeakageCurrentPON']
        Final_Grades = []

        FTMinus20BTC_Grades = []
        FTMinus20ATC_Grades = []
        FT17_Grades = []
        XrayCal_Grades = []
        XrayHR_Grades = []
        Final_Grades = []
        brokenrocs = []
        brokenrocsx = []
        totdef = []
        totdefx = []

        for ModuleID in ModuleIDsList:

            FTMinus20BTC = ''
            FTMinus20ATC = ''
            FT17 = ''
            XrayCal = ''
            XrayHR = ''
            Complete = ''

            ModuleGrades = []

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'm20_1':
                        FTMinus20BTC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'm20_2':
                        FTMinus20ATC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'p17_1':
                        FT17 =  RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XRayHRQualification':
                        XrayHR = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])


            if self.ModuleQualificationIsComplete(ModuleID, Rows):
                FinalGrade = self.GetFinalGrade(ModuleID, Rows)
                Final_Grades.append(FinalGrade)
        

        Numbers['nA'] = len([x for x in Final_Grades if x=='A'])
        Numbers['nB'] = len([x for x in Final_Grades if x=='B'])
        Numbers['nC'] = len([x for x in Final_Grades if x=='C'])
        Numbers['nM'] = len(ModuleIDsList) - len(Final_Grades)

        DefectROCs = 0
        DefectROCsX = 0


        for ModuleID in ModuleIDsList:

            grades = [0]*16
            Pixdefects = [0]*16
            gradesX = [0]*16
            PixdefectsX = [0]*16
            Nuniformity = [0]*16
            initialF = [0]*3
            finalF = [0]*3
            initialX = 0 
            finalX = 0
            initial = 0
            final = 0

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:

                    TestType = RowTuple['TestType']
                    if TestType != 'TemperatureCycle':

                        #Number of broken ROCs
                        if TestType in FullTests:
                            for i in range (0,16):
                                Pixdefects[i] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%i, 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
              
                        elif TestType == 'XRayHRQualification':
                            for i in range (0,16):
                                PixdefectsX[i] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%i, 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            	Nuniformity[i] = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%i,'Grading' ,'KeyValueDictPairs.json', 'NumberOfNonUniformColumns','Value'])
                                
                        for  i, v in enumerate(Pixdefects):
                            if v is not None and float(v) > 3000:
                                grades[i] = 1
                                brokenrocs.append(ModuleID)

                        for  i, v in enumerate(PixdefectsX):
                            if v is not None and float(v) > 3000:
                                gradesX[i] = 1
                                brokenrocsx.append(ModuleID)
                        for i, v in enumerate(Nuniformity):
                            if v is not None and float(v) > 20:
                                gradesX[i] = 1
                                brokenrocsx.append(ModuleID)

                        #Number of manual regradings
                        reg = str(self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'GradeComment', 'Value']))
                        
                        try: 
                            if (reg!=''):
                                if (TestType == "XRayHRQualification"):
                                    initialX=reg[28]
                                    finalX=reg[33]
                                elif (TestType == 'm20_1'):
                                    initialF[0] = reg[28]
                                    finalF[0] = reg[33]
                                elif (TestType == 'm20_2'):
                                    initialF[1] = reg[28]
                                    finalF[1] = reg[33]
                                elif (TestType == "p17_1"):
                                    initialF[2] = reg[28]
                                    finalF[2] = reg[33]

                                if 'C' in initialF:
                                    initial = 'C'
                                elif 'B' in initialF:
                                    initial = 'B'
                                elif 'A' in initialF:
                                    initial = 'A'

                                if 'C' in finalF:
                                    final = 'C'
                                elif 'B' in finalF:
                                    final = 'B'
                                elif 'A' in finalF:
                                    final = 'A'

                               
                        except:
                            pass

                    #Get number of modules with an HDI problem
                    if (TestType == "XRayHRQualification"):
                        try: 
                            hdicomment = str(self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], 'QualificationGroup', 'KeyValueDictPairs.json', 'Comment', 'Value']))
                            if ("HDI Problem" in hdicomment):
                                Numbers['nHDI'] += 1   
                        except:
                            pass



                    
            if (initialX=='A' and finalX=='B'):
                Numbers['nAtoBX'] += 1
            elif (initialX=='A' and finalX=='C'):
                Numbers['nAtoCX'] += 1
            elif (initialX=='B' and finalX=='A'):
                Numbers['nBtoAX'] += 1
            elif (initialX=='B' and finalX=='C'):
                Numbers['nBtoCX'] += 1
            elif (initialX=='C' and finalX=='A'):
                Numbers['nCtoAX'] += 1
            elif (initialX=='C' and finalX=='B'):
                Numbers['nCtoBX'] += 1

            if (initial=='A' and final=='B'):
                Numbers['nAtoB'] += 1
            elif (initial=='A' and final=='C'):
                Numbers['nAtoC'] += 1
            elif (initial=='B' and final=='A'):
                Numbers['nBtoA'] += 1
            elif (initial=='B' and final=='C'):
                Numbers['nBtoC'] += 1
            elif (initial=='C' and final=='A'):
                Numbers['nCtoA'] += 1
            elif (initial=='C' and final=='B'):
                Numbers['nCtoB'] += 1




            if (grades.count(1)>0):
                DefectROCs += 1

            if (gradesX.count(1)>0):
                DefectROCsX += 1

      


        Numbers['BrokenROC'] = DefectROCs
        Numbers['BrokenROCX'] = DefectROCsX

        Path = p

        filename = "{}/ProductionOverview/ProductionOverviewPage_Total/ModuleFailuresOverview/KeyValueDictPairs.json".format(Path)
        #print filename
    	data = open(filename, 'r')
        moduledefects = json.load(data)

       

        for mod, defects in moduledefects.iteritems():


            for d, grade in defects.iteritems():

            	if (d == 'TotalDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['ntotDefectsB'] += 1
                    elif tag == "C" and not mod in brokenrocs:
                        Numbers['ntotDefectsC'] += 1
                        totdef.append(mod)

                if (d == 'TotalDefects_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['ntotDefectsXrayB'] += 1
                    elif grade == "C" and not mod in brokenrocsx:
                        Numbers['ntotDefectsXrayC'] += 1
                        totdefx.append(mod)
                        

        for mod, defects in moduledefects.iteritems():


            for d, grade in defects.iteritems():

                if (d == 'AddressDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B":
                        Numbers['nAddressdefB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['nAddressdefC'] += 1

                if (d == 'BB_Fulltest' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nBBFullB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['nBBFullC'] += 1

                if (d == 'BB_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['nBBXrayB'] += 1
                    elif grade == "C" and not mod in brokenrocsx  and not mod in totdefx:
                        Numbers['nBBXrayC'] += 1

                if (d == 'IV150' and grade!=""):
                    for test, g in grade.iteritems():
                        if g != "" :
                            if test == "m20_2" and g == "B":
                                Numbers['nIV150m20B'] += 1
                            elif test == "m20_2" and g == "C":
                                Numbers['nIV150m20C'] += 1
                            elif test == "p17_1" and g == "B":
                                Numbers['nIV150B'] += 1
                            elif test == "p17_1" and g == "C":
                            	for ModuleID in ModuleIDsList:
	                                for RowTuple in Rows:
	                                    if RowTuple['ModuleID'] == ModuleID:
	                                    	if ModuleID==mod and RowTuple['TestType'] in TestTypeLeakageCurrentPON:
	                                            GradeC = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_C']*1e-6
	                                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'KeyValueDictPairs.json', 'LeakageCurrent', 'Value'])
	                                            if Value is not None and float(Value) > GradeC:
	                                                Numbers['nlcstartupC'] += 1
	                                            else:
	                                                Numbers['nIV150C'] += 1
	                                           
	                                            

                if (d == 'IVRatio150' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nCurrentRatioB'] += 1
                    elif tag == "C":
                        Numbers['nCurrentRatioC'] += 1

                if (d == 'IVSlope' and grade!=""):
                    if grade == "B" :
                        Numbers['nIVSlopeB'] += 1
                    elif grade == "C":
                        Numbers['nIVSlopeC'] += 1

                if (d == 'LCStartup' and grade!=""):
                    if grade == "B" :
                        Numbers['nlcstartupB'] += 1
                    elif grade == "C":
                        Numbers['nlcstartupC'] += 1

                if (d == 'Noise' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nNoiseB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['nNoiseC'] += 1

                if (d == 'Noise_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['nNoiseXrayB'] += 1
                    elif grade == "C" and not mod in brokenrocsx and not mod in totdefx:
                        Numbers['nNoiseXrayC'] += 1

                if (d == 'PedestalSpread' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nPedSpreadB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['nPedSpreadC'] += 1

                if (d == 'RelativeGainWidth' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nRelGainWB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['nRelGainWC'] += 1


                if (d == 'UniformityProblems' and grade!=""):
                    if grade == "B" :
                        Numbers['nuniformityB'] += 1
                    elif grade == "C" and not mod in brokenrocsx and not mod in totdefx:
                        Numbers['nuniformityC'] += 1

                if (d == 'VcalThrWidth' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nVcalThrWB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['nVcalThrWC'] += 1

                if (d == 'deadPixels' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['ndeadpixB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['ndeadpixC'] += 1

                if (d == 'lowHREfficiency' and grade!=""):
                    if grade == "B" :
                        Numbers['nLowHREfB'] += 1
                    elif grade == "C" and not mod in brokenrocsx and not mod in totdefx:
                        Numbers['nLowHREfC'] += 1

                if (d == 'maskDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nMaskdefB'] += 1
                    elif tag == "C" and not mod in brokenrocs and not mod in totdef:
                        Numbers['nMaskdefC'] += 1

                if (d == 'trimbitDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nTrimbitdefB'] += 1
                    elif tag == "C" and mod not in brokenrocs and mod not in totdef:
                        Numbers['nTrimbitdefC'] += 1

       
        Numbers['nLowHREfC'] -= Numbers['nHDI']


       
        return Numbers

