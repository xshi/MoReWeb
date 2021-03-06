# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='LeakageCurrent'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Leakage Current 150V {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)


    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(111210)
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogx(1)

        print "    Fulltest: ", self.Attributes['Test']

        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        HTML = ""

        HistogramMin = 1e-7
        HistogramMax = 3e-5
        NBins = 60

        ModuleGrade = {
            'A' : [],
            'B' : [],
            'C' : [],
        }

        Histogram = ROOT.THStack(self.GetUniqueID(),"")

        NModules = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        Factor = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Factor'])
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                        Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary1','KeyValueDictPairs.json','Grade','Value'])

                        if Factor is not None and Value is not None and Grade is not None:
                            ModuleGrade[Grade].append(float(Factor) * float(Value))
                            NModules += 1
                        elif Factor is not None and Value is not None and Grade is None:
                            ModuleGrade['C'].append(float(Value))
                            NModules += 1
                        else:
                            self.ProblematicModulesList.append(ModuleID)

        hA = ROOT.TH1D("vcalslope_A_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hB = ROOT.TH1D("vcalslope_B_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hC = ROOT.TH1D("vcalslope_C_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hAB = ROOT.TH1D("vcalslope_AB_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        h = ROOT.TH1D("vcalslope_all_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)

        hA.SetFillStyle(1001)
        hA.SetFillColor(self.GetGradeColor('A'))
        hA.SetLineColor(self.GetGradeColor('A'))
        hB.SetFillStyle(1001)
        hB.SetFillColor(self.GetGradeColor('B'))
        hB.SetLineColor(self.GetGradeColor('B'))
        hC.SetFillStyle(1001)
        hC.SetFillColor(self.GetGradeColor('C'))
        hC.SetLineColor(self.GetGradeColor('C'))

        for x in ModuleGrade['A']:
            hA.Fill(x)
        for x in ModuleGrade['B']:
            hB.Fill(x)
        for x in ModuleGrade['C']:
            hC.Fill(x)

        Histogram.Add(hA)
        Histogram.Add(hB)
        Histogram.Add(hC)

        hAB.Add(hA,hB)
        h.Add(hAB,hC)

        Histogram.Draw("")

        Histogram.GetXaxis().SetTitle("current [A]")
        Histogram.GetYaxis().SetTitle("# modules")
        Histogram.GetYaxis().SetTitleOffset(1.5)
        
        meanAll = round(h.GetMean()*1.e6,2)
        meanAB = round(hAB.GetMean()*1.e6,2)
        meanC = round(hC.GetMean()*1.e6,2)
        meanerrAll = round(h.GetMeanError()*1.e6,2)
        meanerrAB = round(hAB.GetMeanError()*1.e6,2)
        meanerrC = round(hC.GetMeanError()*1.e6,2)
        RMSAll = round(h.GetRMS()*1.e6,2)
        RMSAB = round(hAB.GetRMS()*1.e6,2)
        RMSC = round(hC.GetRMS()*1.e6,2)
        underAll = int(h.GetBinContent(0))
        underAB = int(hAB.GetBinContent(0))
        underC = int(hC.GetBinContent(0))
        overAll = int(h.GetBinContent(NBins+1))
        overAB = int(hAB.GetBinContent(NBins+1))
        overC = int(hC.GetBinContent(NBins+1))
       
        stats = ROOT.TPaveText(0.6,0.6,0.9,0.8, "NDCNB")
        stats.SetFillColor(ROOT.kWhite)
        stats.SetTextSize(0.025)
        stats.SetTextAlign(10)
        stats.SetTextFont(62)
        stats.SetBorderSize(0)
        stats.AddText("All: #mu = {0} #pm {1}".format(meanAll,meanerrAll))
        stats.AddText(" #sigma = {0}".format(RMSAll))
        stats.AddText("  UF = {0}, OF = {1}".format(underAll,overAll))
        stats.AddText("AB: #mu = {0} #pm {1}".format(meanAB,meanerrAB))
        stats.AddText(" #sigma = {0}".format(RMSAB))
        stats.AddText("  UF = {0}, OF = {1}".format(underAB,overAB))
        stats.AddText("C: #mu = {0} #pm {1}".format(meanC,meanerrC))
        stats.AddText(" #sigma = {0}".format(RMSC))
        stats.AddText("  UF = {0}, OF = {1}".format(underC,overC))
        stats.Draw("same")

        GradeAB = 1.e-6*float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
        GradeBC = 1.e-6*float(self.TestResultEnvironmentObject.GradingParameters['currentC'])

        PM = Histogram.GetMaximum()*1.1
        Histogram.SetMaximum(PM)

        PlotMaximum = Histogram.GetMaximum()*3.0

        try:
            CloneHistogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i <= CloneHistogram.GetXaxis().FindBin(GradeBC) and i >= CloneHistogram.GetXaxis().FindBin(GradeAB):
                    CloneHistogram.SetBinContent(i, PlotMaximum)
              
            CloneHistogram.SetFillColorAlpha(ROOT.kBlue, 0.12)
            CloneHistogram.SetFillStyle(1001)
            CloneHistogram.Draw("same")

            CloneHistogram2 = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i > CloneHistogram.GetXaxis().FindBin(GradeBC):
                    CloneHistogram2.SetBinContent(i, PlotMaximum)
              
            CloneHistogram2.SetFillColorAlpha(ROOT.kRed, 0.15)
            CloneHistogram2.SetFillStyle(1001)
            CloneHistogram2.Draw("same")

            CloneHistogram3 = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i < CloneHistogram.GetXaxis().FindBin(GradeAB):
                    CloneHistogram3.SetBinContent(i, PlotMaximum)
              
            CloneHistogram3.SetFillColorAlpha(ROOT.kGreen+2, 0.1)
            CloneHistogram3.SetFillStyle(1001)
            CloneHistogram3.Draw("same")
        except:
            pass

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        Subtitle = self.Attributes['Test']
        TestNames = {'m20_1' : 'Fulltest -20°C BTC', 'm20_2': 'Fulltest -20°C ATC', 'p17_1': 'Fulltest +17°C'}
        if TestNames.has_key(Subtitle):
            Subtitle = TestNames[Subtitle]
        title.DrawText(0.15,0.965,"%s, modules: %d"%(Subtitle,NModules))

        title4 = ROOT.TText()
        title4.SetNDC()
        title4.SetTextAlign(12)
        title4.SetTextSize(0.03)
        title4.SetTextColor(self.GetGradeColor('A'))
        title4.DrawText(0.72,0.9,"Grade A")

        title2 = ROOT.TText()
        title2.SetNDC()
        title2.SetTextAlign(12)
        title2.SetTextSize(0.03)
        title2.SetTextColor(self.GetGradeColor('B'))
        title2.DrawText(0.72,0.88,"Grade B")

        title3 = ROOT.TText()
        title3.SetNDC()
        title3.SetTextAlign(12)
        title3.SetTextSize(0.03)
        title3.SetTextColor(self.GetGradeColor('C'))
        title3.DrawText(0.72,0.86,"Grade C")

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)

