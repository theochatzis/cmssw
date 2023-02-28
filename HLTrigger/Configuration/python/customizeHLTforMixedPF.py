import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.common import producers_by_type

def customizeHLTForMixedPF(process):

    # Not affecting the other seed producers
    for producer in producers_by_type(process, "SeedGeneratorFromProtoTracksEDProducer"):
        producer.produceComplement = cms.bool(False)

    # Customization for the iter0 seeds
    process.hltIter0PFLowPixelSeedsFromPixelTracks.produceComplement = cms.bool(True)
    
    # Apply cuts for pixel tracks complement
    process.hltPixelTracksLowPT = cms.EDProducer( "TrackWithVertexSelector",
        normalizedChi2 = cms.double( 999999.0 ),
        numberOfValidHits = cms.uint32( 0 ),
        zetaVtx = cms.double( 0.3 ),
        etaMin = cms.double( 0.0 ),
        rhoVtx = cms.double( 0.2 ),
        ptErrorCut = cms.double( 5.0 ),
        dzMax = cms.double( 999.0 ),
        etaMax = cms.double( 5.0 ),
        quality = cms.string( "loose" ), ##loose, tight, highPurity
        copyTrajectories = cms.untracked.bool( False ),
        nSigmaDtVertex = cms.double( 0.0 ),
        timesTag = cms.InputTag( "" ),
        ptMin = cms.double( -1.0 ), # minimum pT cut
        ptMax = cms.double( 6.0 ), # maximum pT cut
        d0Max = cms.double( 999.0 ),
        copyExtras = cms.untracked.bool( False ),
        nVertices = cms.uint32( 2 ),
        vertexTag = cms.InputTag( "hltPixelVertices" ),
        src = cms.InputTag( "hltIter0PFLowPixelSeedsFromPixelTracks" ), # the complement reco::TrackCollection
        vtxFallback = cms.bool( True ),
        numberOfLostHits = cms.uint32( 999 ),
        numberOfValidPixelHits = cms.uint32( 3 ),
        timeResosTag = cms.InputTag( "" ),
        useVtx = cms.bool( False ) ## Turning off vertex selection
    )



    process.HLTIterativeTrackingIteration0 = cms.Sequence(process.hltIter0PFLowPixelSeedsFromPixelTracks+process.hltPixelTracksLowPT+process.hltIter0PFlowCkfTrackCandidates+process.hltIter0PFlowCtfWithMaterialTracks+process.hltIter0PFlowTrackCutClassifier+process.hltMergedTracks)


    # Merging Iter0 tracks with the complement of pixel tracks
    process.hltPFTracks = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        MinPT = cms.double( 0.05 ),
        Epsilon = cms.double( -0.001 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        MinFound = cms.int32( 3 ),
        TrackProducers = cms.VInputTag( 'hltPixelTracksLowPT','hltMergedTracks' ),
        hasSelector = cms.vint32( 0, 0 ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        selectedTrackQuals = cms.VInputTag( 'hltPixelTracksLowPT','hltMergedTracks' ),
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

    # Merging these tracks with muons for final mixed tracks collection
    process.hltPFMuonMerging.selectedTrackQuals = cms.VInputTag("hltIterL3MuonTracks", "hltPFTracks")
    process.hltPFMuonMerging.TrackProducers = cms.VInputTag("hltIterL3MuonTracks", "hltPFTracks")
    
    process.HLTTrackReconstructionForPF = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTRecopixelvertexingSequence+process.HLTDoLocalStripSequence+process.HLTIterativeTrackingIter02+process.hltPFTracks+process.hltPFMuonMerging+process.hltMuonLinks+process.hltMuons)

    # Customize the full hlt vertices such that they do not use the complement tracks by requiring at least 1 valid strip hit
    process.hltVerticesPF.TkFilterParameters.minValidStripHits = cms.int32(1)

    return process
