import FWCore.ParameterSet.Config as cms

generalTracksMtdTrackQualityMVA = cms.EDProducer("MTDTrackQualityMVAProducer",
  tracksSrc = cms.InputTag('generalTracks'),
  btlMatchChi2Src = cms.InputTag('generalTracksWithMTD:btlMatchChi2'),
  btlMatchTimeChi2Src = cms.InputTag('generalTracksWithMTD:btlMatchTimeChi2'),
  etlMatchChi2Src = cms.InputTag('generalTracksWithMTD:etlMatchChi2'),
  etlMatchTimeChi2Src = cms.InputTag('generalTracksWithMTD:etlMatchTimeChi2'),
  mtdTimeSrc = cms.InputTag('generalTracksWithMTD:generalTracktmtd'),
  pathLengthSrc = cms.InputTag('generalTracksWithMTD:generalTrackPathLength'),
  npixBarrelSrc = cms.InputTag('generalTracksWithMTD:npixBarrel'),
  npixEndcapSrc = cms.InputTag('generalTracksWithMTD:npixEndcap'),
)