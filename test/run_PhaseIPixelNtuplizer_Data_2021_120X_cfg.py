# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: -s RAW2DIGI,L1Reco,RECO --data --conditions 120X_dataRun3_Express_v2 --era Run3 --eventcontent RECO --datatier RECO --filein replaceMeRoot --fileout file:PilotRun.root --python_filename=collisionsPilotBeam.py -n 100 --no_exec --scenario pp
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('ReRECO',Run3)

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
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/05d4e531-3560-40bd-ba85-d18f4fa78981.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('-s nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RECO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:PilotRun.root'),
    outputCommands = process.RECOEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '120X_dataRun3_Express_v2', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)

# Schedule definition
#process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.RECOoutput_step)

#=========================================================================================
#                        Main Analysis Module

# HLT Filter
import HLTrigger.HLTfilters.hltHighLevel_cfi

process.HLTFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    HLTPaths = ['HLT_*ZeroBias*'],
    #throw = False #dont throw except on unknown path names
)
#process.hltFilter_step = cms.Path(process.HLTFilter)

# Refitter
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")

# Load and confiugre the plugin you want to use
#---------------------------
#  PhaseIPixelNtuplizer
#---------------------------
process.PhaseINtuplizerPlugin = cms.EDAnalyzer(
        "PhaseIPixelNtuplizer",
        trajectoryInput = cms.InputTag('TrackRefitter'),
        outputFileName = cms.untracked.string('Ntuplizer_346512_0.root'),
        # Global muon collection
        muonCollection                 = cms.InputTag("muons"),
        keepAllGlobalMuons             = cms.untracked.bool(True),
        keepAllTrackerMuons            = cms.untracked.bool(True),
        # information to save
        eventSaveDownscaleFactor       = cms.untracked.int32(1),
        trackSaveDownscaleFactor       = cms.untracked.int32(1),
        clusterSaveDownscaleFactor     = cms.untracked.int32(1),
        saveDigiTree                   = cms.untracked.bool(False),
        saveTrackTree                  = cms.untracked.bool(True),
        saveNonPropagatedExtraTrajTree = cms.untracked.bool(False),
        clusterCollection              = cms.InputTag("siPixelClusters"),
        #clusterSaveDownscaleFactor = cms.untracked.int32(1),
)

# myAnalyzer Path
#process.TrackRefitter_step = cms.Path(process.offlineBeamSpot*process.MeasurementTrackerEvent*process.TrackRefitter)
#process.TrackRefitter_step = cms.Path(process.MeasurementTrackerEvent*process.TrackRefitter)

#process.PhaseIPixelNtuplizer_step = cms.Path(process.PhaseINtuplizerPlugin)

#process.PhaseIPixelNtuplizer_step = cms.Path(process.PhaseINtuplizerPlugin)
process.p = cms.Path(
    process.HLTFilter*
    process.offlineBeamSpot*
    process.MeasurementTrackerEvent*
    process.TrackRefitter*
    process.PhaseINtuplizerPlugin
)
#===============================================================

# Schedule definition
process.schedule = cms.Schedule(process.p)
#===============================================================
from Configuration.DataProcessing.RecoTLR import customiseExpress
process = customiseExpress(process)

#===========================================================================================
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)



# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
