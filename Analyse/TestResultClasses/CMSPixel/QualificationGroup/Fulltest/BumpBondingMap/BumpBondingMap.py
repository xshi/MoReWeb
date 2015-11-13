import ROOT
import AbstractClasses
import ROOT
from ROOT import kRed, gStyle
from FPIXUtils.moduleSummaryPlottingTools import *

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle='BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

            
    def PopulateResultData(self):
        if 'QualificationType' in self.Attributes and self.Attributes['QualificationType'] == 'PurdueTest':
            return self.PopulateResultDataPurdueTest()
        
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        # initialize data
        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins);  # mBumps

        # fill plot
        SpecialBumpBondingTestNamesROC = []
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]

            # take the same bb map that has been used in the grading
            SpecialBumpBondingTestName = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SpecialBumpBondingTestName']
            if SpecialBumpBondingTestName == 'BB4':
                histo = ChipTestResultObject.ResultData['SubTestResults']['BB4'].ResultData['Plot']['ROOTObject']
                self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB4'
            elif SpecialBumpBondingTestName == 'BB2':
                histo = ChipTestResultObject.ResultData['SubTestResults']['BB2Map'].ResultData['Plot']['ROOTObject']
                self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB2'
            else:
                histo = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingMap'].ResultData['Plot']['ROOTObject']

            SpecialBumpBondingTestNamesROC.append(SpecialBumpBondingTestName)
                
            if not histo:
                print 'cannot get BumpBondingProblems histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            for col in range(self.nCols):
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.UpdatePlot(chipNo, col, row, result)

        UniqueBBTestNames = list(set(SpecialBumpBondingTestNamesROC))
        if len(UniqueBBTestNames) == 1:
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = UniqueBBTestNames[0]
        elif len(UniqueBBTestNames) > 1:
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = '/'.join(UniqueBBTestNames)
        else:
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = ''

        # draw
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')


        boxes = []
        startChip = self.ParentObject.Attributes['StartChip']
        endChip = self.ParentObject.Attributes['NumberOfChips'] + startChip - 1
        if self.verbose:
            print 'Used chips: %2d -%2d' % (startChip, endChip)
        for i in range(0,16):
            if i < startChip or endChip < i:
                if i < 8:
                    j = 15 - i
                else:
                    j = i - 8
                beginX = (j % 8) * self.nCols
                endX = beginX + self.nCols
                beginY = int(j / 8) * self.nRows
                endY = beginY + self.nRows
                if self.verbose:
                    print 'chip %d not used.' % i, j, '%d-%d , %d-%d' % (beginX, endX, beginY, endY)
                newBox = ROOT.TPaveText(beginX, beginY, endX, endY)
#                 newBox.AddText('%2d' % i)
                newBox.SetFillColor(29)
                newBox.SetLineColor(29)
                newBox.SetFillStyle(3004)
                newBox.SetShadowColor(0)
                newBox.SetBorderSize(1)
                newBox.Draw()
                boxes.append(newBox)
                # (beginX, beginY, endX, endY)
#         if self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 0:
#             box.SetFillColor(29);
#             box.DrawBox( 0, 0,  8*self.nCols,  self.nRows);
#         elif self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 8:
#             box.SetFillColor(29);
#             box.DrawBox(0, self.nRows, 8 * self.nCols, 2 * self.nRows);
#         elif self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 8:
#             box.SetFillColor(29);
#             box.DrawBox( 0, 0,  8*self.nCols,  2*self.nRows);

        self.ResultData['Plot']['Format'] = 'png'

        self.Title = 'Bump Bonding Map' + (' (%s)'%self.ResultData['HiddenData']['SpecialBumpBondingTestName']) if 'SpecialBumpBondingTestName' in self.ResultData['HiddenData'] and len(self.ResultData['HiddenData']['SpecialBumpBondingTestName']) > 0 else ''
        self.SaveCanvas()        
    def UpdatePlot(self, chipNo, col, row, value):
        result = value
        if chipNo < 8:
            tmpCol = 8 * self.nCols - 1 - chipNo * self.nCols - col
            tmpRow = 2 * self.nRows - 1 - row
        else:
            tmpCol = (chipNo % 8 * self.nCols + col)
            tmpRow = row
        # Get the data from the chip sub test result bump bonding

        if result and self.verbose:
            print chipNo, col, row, '--->', tmpCol, tmpRow, result
#         self.ResultData['Plot']['ROOTObject'].SetBinContent(tmpCol + 1, tmpRow + 1, result)
        self.ResultData['Plot']['ROOTObject'].Fill(tmpCol, tmpRow, result)

    def PopulateResultDataPurdueTest(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)
        plots = []
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get PixelMap histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            histoName = 'BumpBonding_ROC%s' %chipNo
            histo.SetName(histoName)
            plots.append(histo)

        # sort the plot from ROC0 to ROC15, in order to be used for merging
        plots = sorted(plots, key=lambda h:int(h.GetName().split('ROC')[1]))
        summaryPlot = makeMergedPlot(plots)
        zRange = findZRange(plots)
        setZRange(summaryPlot,zRange)

        colors = array("i",[51+i for i in range(40)] + [kRed])
        gStyle.SetPalette(len(colors), colors);
        zMin=summaryPlot.GetMinimum()
        zMax=summaryPlot.GetMaximum()
        step=(zMax-zMin)/(len(colors)-1)
        levels = array('d',[zMin + i*step for i in range(len(colors)-1)]+[4.9999999])

        summaryPlot.SetContour(len(levels),levels)
        
        self.Canvas = setupSummaryCanvas(summaryPlot)

        self.ResultData['Plot']['Format'] = 'png'

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
            print 'Saved ', self.GetPlotFileName()
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding Map'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()

