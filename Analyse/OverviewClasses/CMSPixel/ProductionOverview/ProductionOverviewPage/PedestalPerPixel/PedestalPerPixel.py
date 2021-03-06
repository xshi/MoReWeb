import ROOT
import AbstractClasses
import glob
import json
import copy

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='PedestalPerPixel'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Pedestal per pixel {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)

    def GenerateOverview(self):
        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        HTML = ""

        # define for which grades to plot histogram
        HistogramDict = {
            '0-All': {
                'Histogram': None,
                'Title': 'All',
            },
            '1-A': {
                'Histogram': None,
                'Grades': [1],
                'Color': self.GetGradeColor('A'),
                'Title': 'A',
            },
            '2-B': {
                'Histogram': None,
                'Grades': [2],
                'Color': self.GetGradeColor('B'),
                'Title': 'B',
            },
            '3-C': {
                'Histogram': None,
                'Grades': [3],
                'Color': self.GetGradeColor('C'),
                'Title': 'C',
            },
            '4-AB': {
                'Histogram': None,
                'Grades': [1, 2],
                'Title': 'A/B',
                'Show': False,
            }
        }

        # set histogram options
        HistogramOptions = {
            'RootFileHistogramName': 'PHCalibrationGain',
            'GradeJsonPath': ['Chips','Chip{Chip}', 'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value'],
            'RootFilePath': ['Chips' ,'Chip{Chip}', 'PHCalibrationPedestal', '*.root'],
            'StatsPosition': [0.60,0.88,0.80,0.88],
            'LegendPosition': [0.2, 0.88],
            'XTitle': "Vcal offset",
            'YTitle': "No. of Entries",
            'Range': [-150, 300],
        }

        # draw histogram
        self.DrawPixelHistogram(Rows, ModuleIDsList, HistogramDict, HistogramOptions)

        # save plot and add to .html
        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)
