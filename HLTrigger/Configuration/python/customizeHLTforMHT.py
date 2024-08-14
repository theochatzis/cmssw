import FWCore.ParameterSet.Config as cms

def customizeHLTforMHT(process):
  process.hltPFMHTNoMuTightID.minEtaFwdJetMht = cms.double(4.7)
  process.hltPFMHTNoMuTightID.minPtFwdJetMht = cms.double(30.)

  process.hltPFMHTNoMuTightIDHFCleaned.minEtaFwdJetMht = cms.double(4.7)
  process.hltPFMHTNoMuTightIDHFCleaned.minPtFwdJetMht = cms.double(30.)

  process.hltPFMHTTightID.minEtaFwdJetMht = cms.double(4.7)
  process.hltPFMHTTightID.minPtFwdJetMht = cms.double(30.)

  return process
