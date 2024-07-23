import FWCore.ParameterSet.Config as cms

def customizeHLTforTrimmedTrackingVertexing(process):
  ''' define the modules needed for producing the trimmed pixel vertex collection
  '''
  process.HLTPSetPvClusterComparerForIT = cms.PSet( 
    track_chi2_max  = cms.double(20.0),
    track_pt_max    = cms.double(20.0),
    track_prob_min  = cms.double(-1.0),
    track_pt_min    = cms.double(1.0)
  )
  process.hltTrimmedPixelVertices = cms.EDProducer("PixelVertexCollectionTrimmer",
    src             = cms.InputTag("hltPhase2PixelVertices"),
    maxVtx          = cms.uint32(100),
    fractionSumPt2  = cms.double(0.3),
    minSumPt2       = cms.double(0.0),
    PVcomparer      = cms.PSet(refToPSet_=cms.string("HLTPSetPvClusterComparerForIT"))
  )
  process.HLTTrackingV61Sequence.insert(process.HLTTrackingV61Sequence.index(process.hltPhase2PixelVertices)+1, process.hltTrimmedPixelVertices)
  return process

def customizeHLTforTrimmedTrackingInitialStep(process):
  ''' modify the initialStep to select only tracks compatible with a pixel vertex
  from the trimmed collection
  '''
  process.initialStepSeeds.InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices")
  return process

def customizeHLTforTrimmedTrackingHighPtTripletStep(process):
  ''' modify the highPtTripletStep to select only doublets compatible with a pixel vertex
  from the trimmed collection.
  '''
  process.hltTrackingRegionFromTrimmedVertices = cms.EDProducer('GlobalTrackingRegionWithVerticesEDProducer',
    RegionPSet = cms.PSet(
      ptMin                   = cms.double(0.5),
      beamSpot                = cms.InputTag('hltOnlineBeamSpot'),
      pixelClustersForScaling = cms.InputTag('siPixelClusters'),
      VertexCollection        = cms.InputTag('hltTrimmedPixelVertices'),
    ),
    mightGet = cms.optional.untracked.vstring,
  )
  process.highPtTripletStepHitDoublets.trackingRegions = cms.InputTag('hltTrackingRegionFromTrimmedVertices')
  process.highPtTripletStepSequence.insert(0, process.hltTrackingRegionFromTrimmedVertices)
  return process

def HLTTrackingPath(process):
    ''' Create a tracking-only path
    '''
    process.HLT_TrackingPath = cms.Path()
    process.HLT_TrackingPath.insert(item=process.HLTBeginSequence       , index=len(process.HLT_TrackingPath.moduleNames()))
    process.HLT_TrackingPath.insert(item=process.HLTTrackingV61Sequence , index=len(process.HLT_TrackingPath.moduleNames()))
    process.HLT_TrackingPath.insert(item=process.HLTEndSequence         , index=len(process.HLT_TrackingPath.moduleNames()))
    process.outputmodule = cms.EndPath(process.FEVTDEBUGHLToutput)
    process.schedule.insert(-4, process.HLT_TrackingPath)
    return process

def customizeHLTforTrimmedTracking(process):
  ''' main function for trimmed tracking (run the full menu)
  '''
  process = customizeHLTforTrimmedTrackingVertexing(process)
  process = customizeHLTforTrimmedTrackingInitialStep(process)
  process = customizeHLTforTrimmedTrackingHighPtTripletStep(process)
  return process

def customizeHLTforTrimmedTrackingTrackingOnly(process):
  ''' main function for trimmed tracking (run only the tracking sequence)
  '''
  process = customizeHLTforTrimmedTracking(process)
  process = HLTTrackingPath(process)
  process.schedule = cms.Schedule(*[
    process.HLT_TrackingPath,
    process.endjob_step,
    process.outputmodule
  ])
  return process