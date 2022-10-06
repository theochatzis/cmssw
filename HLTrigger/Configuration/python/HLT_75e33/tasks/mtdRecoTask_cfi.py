import FWCore.ParameterSet.Config as cms

from ..modules.mtdUncalibratedRecHits_cfi import *
from ..modules.mtdRecHits_cfi import *
from ..modules.mtdClusters_cfi import *
from ..modules.mtdTrackingRecHits_cfi import *
from ..modules.generalTracksWithMTD_cfi import *
from ..modules.generalTracksMtdTrackQualityMVA_cfi import *
from ..modules.generalTracksTOFPIDProducer_cfi import *

mtdRecoTask = cms.Task(
    mtdUncalibratedRecHits,
    mtdRecHits,
    mtdClusters,
    mtdTrackingRecHits,
    generalTracksWithMTD,
    generalTracksMtdTrackQualityMVA,
    generalTracksTOFPIDProducer
)