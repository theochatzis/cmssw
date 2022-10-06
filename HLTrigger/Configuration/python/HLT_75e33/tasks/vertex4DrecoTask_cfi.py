import FWCore.ParameterSet.Config as cms

from ..modules.unsortedOfflinePrimaryVertices4D_cfi import *
from ..modules.offlinePrimaryVertices4D_cfi import *

vertex4DrecoTask = cms.Task(
  unsortedOfflinePrimaryVertices4D,
  offlinePrimaryVertices4D
)