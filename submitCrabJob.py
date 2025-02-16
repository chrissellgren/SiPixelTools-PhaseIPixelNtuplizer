import sys, os, time, re
import numpy as np
#from common_functions import *
from optparse import OptionParser
parser = OptionParser(usage="Usage: python %prog codeVersion")
(opt,args) = parser.parse_args()

datasetList = [
"/Muon/Run2023E-SiPixelCalSingleMuonLoose-PromptReco-v1/ALCARECO",
#"/Muon0/Run2023A-SiPixelCalSingleMuonLoose-PromptReco-v2/ALCARECO",
#"/Muon0/Run2023B-SiPixelCalSingleMuonLoose-PromptReco-v1/ALCARECO",
]

if not os.path.exists("submittedConfigs"): os.makedirs("submittedConfigs")

if not os.path.exists("4crab_Template_maxStat.py"):
  TEMPLATE = '''
from CRABClient.UserUtilities import config
config = config()

config.section_('General')
config.General.requestName = 'calib_ROVIDMINTA'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'cfg_simplified.py'
config.JobType.allowUndistributedCMSSW = True
#config.JobType.maxJobRuntimeMin = 4000
#config.JobType.maxMemoryMB = 4000
#config.JobType.inputFiles = ['SUSYBSMAnalysis/HSCP/data/template_2018MC_v5.root','SUSYBSMAnalysis/HSCP/data/MuonTimeOffset.txt']

config.section_('Data')
config.Data.inputDataset = 'MINTA'
#config.Data.inputDBS = 'phys03'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'LumiBased'
    #config.Data.unitsPerJob = 1 #20
#config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 100 
#config.Data.totalUnits = config.Data.unitsPerJob * 2000
config.Data.outputDatasetTag = config.General.requestName
config.Data.outLFNDirBase = '/store/user/csellgre'
config.Data.ignoreLocality = True
config.Data.publication = False
config.Data.partialDataset = True

config.section_('Site')
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
config.Site.blacklist = ['T2_US_Nebraska']
config.Site.storageSite = 'T3_CH_CERNBOX'
  '''

  with open("4crab_Template_maxStat.py", "w") as text_file:
      text_file.write(TEMPLATE)

for i in datasetList:
  print("Submit for sample "+i)
  os.system("cp 4crab_Template_maxStat.py 4crab_toSubmit_calib.py")
  shortSampleName = i[(i.find('Run2023E')):(i.find('ALCARECO'))-1]
  replaceROVIDMINTA = "sed -i 's/ROVIDMINTA/"+shortSampleName+"/g' 4crab_toSubmit_calib.py"
  os.system(replaceROVIDMINTA)
  replaceMINTA = "sed -i 's/MINTA/"+i.replace("/","\/")+"/g' 4crab_toSubmit_calib.py"
  os.system(replaceMINTA)
  os.system("crab submit -c 4crab_toSubmit_calib.py")
  os.system("mv 4crab_toSubmit_calib.py submittedConfigs/.")

os.system("rm 4crab_Template_maxStat.py")

