import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.common import producers_by_type

def customizeHLTforMHT(process):
  # find automatically all HLT HT/MHT producers
  for prod in producers_by_type(process, "HLTHtMhtProducer"):
    prod.minEtaFwdJetMht = cms.double(4.7)
    prod.minPtFwdJetMht = cms.double(30.)

  return process
