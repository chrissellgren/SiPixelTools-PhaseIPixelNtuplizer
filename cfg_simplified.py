# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: RECO -s RAW2DIGI,L1Reco,RECO --data --scenario pp --conditions auto:run3_data --era Run3 --process RERECO --eventcontent RECO --datatier RECO --filein dummy.root --secondfilein dummy.root --python_filename=test/run_PhaseIPixelNtuplizer_Data_2022_123X_cfg.py --runUnscheduled -n 10 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.outputFile = 'ntuple.root'

process = cms.Process('RERECO',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
)

# Input source
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('/store/data/Run2023D/Muon0/ALCARECO/SiPixelCalSingleMuonLoose-PromptReco-v2/000/370/664/00000/fca88e0f-0a16-4a28-8eb2-5bbfd8ec39b5.root')
    fileNames = cms.untracked.vstring('/store/data/Run2023D/Muon0/ALCARECO/SiPixelCalSingleMuonLoose-PromptReco-v1/000/369/869/00000/c1f8f13a-49be-493e-b59b-38af908719a5.root')
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('RECO nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '132X_dataRun3_Prompt_v4', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Fix problem with default config
process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound'), wantSummary = cms.untracked.bool(True)
)

# Refitter
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")

# Load and confiugre the plugin you want to use
#---------------------------
#  PhaseIPixelNtuplizer
#---------------------------
process.PhaseINtuplizerPlugin = cms.EDAnalyzer("PhaseIPixelNtuplizer",
    trajectoryInput = cms.InputTag('TrackRefitter'),
    outputFileName = cms.untracked.string(options.outputFile),
    # Global muon collection
    muonCollection                 = cms.InputTag("muons"),
    keepAllGlobalMuons             = cms.untracked.bool(True),
    keepAllTrackerMuons            = cms.untracked.bool(True),
    # information to save
    eventSaveDownscaleFactor       = cms.untracked.int32(1),
    trackSaveDownscaleFactor       = cms.untracked.int32(1),
    clusterSaveDownscaleFactor     = cms.untracked.int32(10),
    saveDigiTree                   = cms.untracked.bool(False),
    saveTrackTree                  = cms.untracked.bool(True),
    saveNonPropagatedExtraTrajTree = cms.untracked.bool(False),
    clusterCollection              = cms.InputTag("siPixelClusters"),
    )

process.MeasurementTrackerEvent.pixelClusterProducer = 'ALCARECOSiPixelCalSingleMuonLoose'
process.MeasurementTrackerEvent.stripClusterProducer = 'ALCARECOSiPixelCalSingleMuonLoose'
process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag()
process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag()
process.TrackRefitter.src = 'ALCARECOSiPixelCalSingleMuonLoose'
process.TrackRefitter.TrajectoryInEvent = True
process.PhaseINtuplizerPlugin.clusterCollection = cms.InputTag("ALCARECOSiPixelCalSingleMuonLoose")

# myAnalyzer Path
process.TrackRefitter_step = cms.Path(process.offlineBeamSpot*process.MeasurementTrackerEvent*process.TrackRefitter)
process.PhaseIPixelNtuplizer_step = cms.Path(process.PhaseINtuplizerPlugin)

#---------------------------
#  Schedule
#---------------------------

process.schedule = cms.Schedule(
	process.TrackRefitter_step,
	process.PhaseIPixelNtuplizer_step,
	process.endjob_step
	)


























# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
