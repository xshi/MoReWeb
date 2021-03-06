# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

import ROOT
import datetime
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='Errors'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):

        # lists of strings to search for in .log file
        DetectMessages = {
            'tokenchain': ['Token Chain Length'],
            'eventid': ['Event ID mismatch'],
            'readback': ['Readback start marker'],
            'notokenpass': ['has NoTokenPass but'],
            'datasize': ['Data size does not correspond to'],
            'missingevents': ['Incomplete DAQ data readout'],
            'usbtimeout': ['Timeout reading from USB buffer after'],
            'deser400': ['header reports DESER400 failure'],
            'daqerror': ['Error in DAQ. Aborting test.'],
        }

        # optional: name dictionary of the errors displayed in the summary
        ErrorNames = {
            'tokenchain': 'Token Chain Length',
            'eventid': 'Event ID mismatch',
            'readback': 'Readback start marker',
            'notokenpass': 'has NoTokenPass',
            'datasize': 'Data size criticals',
            'missingevents': 'Missing Event criticals ',
            'usbtimeout': 'USB criticals',
            'deser400': 'DESER400 failure',
            'daqerror': 'DAQ error',
        }

        LogfileErrors = self.AnalyzeLogfiles(self.ParentObject.logfilePath, DetectMessages, ErrorNames)
        self.ResultData['KeyValueDictPairs'] = LogfileErrors['KeyValueDictPairs']
        self.ResultData['KeyList'] = LogfileErrors['KeyList']
