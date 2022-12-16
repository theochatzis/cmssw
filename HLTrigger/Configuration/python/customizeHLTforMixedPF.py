import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.common import producers_by_type

def customizeHLTForMixedPF(process):

    #Not affecting the other seed producers
    for producer in producers_by_type(process, "SeedGeneratorFromProtoTracksEDProducer"):
        producer.produceComplement = cms.bool(False)

    # Customization for the iter0 seeds
    process.hltIter0PFLowPixelSeedsFromPixelTracks.produceComplement = cms.bool(True)

    # Merging Iter0 tracks with the complement of pixel tracks
    process.hltPFTracks = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        MinPT = cms.double( 0.05 ),
        Epsilon = cms.double( -0.001 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        MinFound = cms.int32( 3 ),
        TrackProducers = cms.VInputTag( 'hltIter0PFLowPixelSeedsFromPixelTracks','hltMergedTracks' ),
        hasSelector = cms.vint32( 0, 0 ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        selectedTrackQuals = cms.VInputTag( 'hltIter0PFLowPixelSeedsFromPixelTracks','hltMergedTracks' ),
        setsToMerge = cms.VPSet(
          cms.PSet(  pQual = cms.bool( False ),
            tLists = cms.vint32( 0, 1 )
          )
        ),
        trackAlgoPriorityOrder = cms.string( "hltESPTrackAlgoPriorityOrder" ),
        allowFirstHitShare = cms.bool( True ),
        newQuality = cms.string( "confirmed" ),
        copyExtras = cms.untracked.bool( True ),
        writeOnlyTrkQuals = cms.bool( False ),
        copyMVA = cms.bool( False )
    )

    # Using these mixed tracks as input for hltPFTracks
    process.hltParticleFlowBlock.elementImporters.source = cms.InputTag("hltPFTracks")

    return process
