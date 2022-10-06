import FWCore.ParameterSet.Config as cms

generalTracksTOFPIDProducer = cms.EDProducer('TOFPIDProducer',
  tracksSrc    = cms.InputTag('generalTracks'),
  t0Src        = cms.InputTag('generalTracksWithMTD:generalTrackt0'),
  tmtdSrc      = cms.InputTag('generalTracksWithMTD:generalTracktmtd'),
  sigmat0Src   = cms.InputTag('generalTracksWithMTD:generalTracksigmat0'),
  sigmatmtdSrc = cms.InputTag('generalTracksWithMTD:generalTracksigmatmtd'),
  tofkSrc      = cms.InputTag('generalTracksWithMTD:generalTrackTofK'),
  tofpSrc      = cms.InputTag('generalTracksWithMTD:generalTrackTofP'),
  vtxsSrc      = cms.InputTag('unsortedOfflinePrimaryVertices'),
  vtxMaxSigmaT      = cms.double(0.025),
  maxDz             = cms.double(0.1),
  maxDtSignificance = cms.double(5.0),
  minProbHeavy      = cms.double(0.75),
  fixedT0Error      = cms.double(0.0),
)