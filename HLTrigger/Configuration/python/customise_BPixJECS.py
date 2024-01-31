import FWCore.ParameterSet.Config as cms

def customise_BPixJECS(process):
    ## ----- spit the PF Jets based on the BPix region
    process.hltAK4PFJetsBPix = cms.EDFilter( "PFJetSelector",
        src = cms.InputTag("hltAK4PFJets"),
        filter = cms.bool(False),
        cut = cms.string("abs(eta)<1.0")
    )
    
    
    process.hltAK4PFJetsNoBPix = cms.EDFilter( "PFJetSelector",
        src = cms.InputTag("hltAK4PFJets"),
        filter = cms.bool(False),
        cut = cms.string("abs(eta)>1.0")
    )

    process.HLTAK4PFJetsReconstructionSequence += process.hltAK4PFJetsBPix
    process.HLTAK4PFJetsReconstructionSequence += process.hltAK4PFJetsNoBPix

    process.hltAK8PFJetsBPix = cms.EDFilter( "PFJetSelector",
        src = cms.InputTag("hltAK8PFJets"),
        filter = cms.bool(False),
        cut = cms.string("(eta>-1.5 && eta<0.) && (phi<-0.8 && phi>-1.2)")
    )
    
    process.hltAK8PFJetsNoBPix = cms.EDFilter( "PFJetSelector",
        src = cms.InputTag("hltAK8PFJets"),
        filter = cms.bool(False),
        cut = cms.string("!((eta>-1.5 && eta<0.) && (phi<-0.8 && phi>-1.2))")
    )

    process.HLTAK8PFJetsReconstructionSequence += process.hltAK8PFJetsBPix
    process.HLTAK8PFJetsReconstructionSequence += process.hltAK8PFJetsNoBPix
    

    ## ----- For each split create new corrected Jets
    # introduce new corrector modules for BPix jets only.
    # for the NoBPix jets using the existing corrector modules.

    # AK4
    bpix_corrections_tag_AK4 = 'AK4PFHLT'

    process.hltAK4PFBPixFastJetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK4),
        level = cms.string('L1FastJet'),
        srcRho = cms.InputTag("hltFixedGridRhoFastjetAll")
    )
    
    process.hltAK4PFBPixRelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK4),
        level = cms.string('L2Relative')
    )

    process.hltAK4PFBPixAbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK4),
        level = cms.string('L3Absolute')
    )

    process.hltAK4PFBPixResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK4),
        level = cms.string('L2L3Residual')
    )
    

    process.hltAK4PFBPixCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
        correctors = cms.VInputTag("hltAK4PFBPixFastJetCorrector", "hltAK4PFBPixRelativeCorrector", "hltAK4PFBPixAbsoluteCorrector", "hltAK4PFBPixResidualCorrector")
    )
    
    process.HLTAK4PFCorrectorProducersSequence += process.hltAK4PFBPixFastJetCorrector
    process.HLTAK4PFCorrectorProducersSequence += process.hltAK4PFBPixRelativeCorrector
    process.HLTAK4PFCorrectorProducersSequence += process.hltAK4PFBPixAbsoluteCorrector
    process.HLTAK4PFCorrectorProducersSequence += process.hltAK4PFBPixResidualCorrector
    process.HLTAK4PFCorrectorProducersSequence += process.hltAK4PFBPixCorrector

    # NoBPix
    process.hltAK4PFJetsNoBPixCorrected = cms.EDProducer("CorrectedPFJetProducer",
        correctors = cms.VInputTag("hltAK4PFCorrector"),
        src = cms.InputTag("hltAK4PFJetsNoBPix")
    )
    
    # BPix
    process.hltAK4PFJetsBPixCorrected = cms.EDProducer("CorrectedPFJetProducer",
        correctors = cms.VInputTag("hltAK4PFBPixCorrector"),
        src = cms.InputTag("hltAK4PFJetsBPix")
    )

    process.HLTAK4PFJetsCorrectionSequence.insert(process.HLTAK4PFJetsCorrectionSequence.index(getattr(process, 'HLTAK4PFCorrectorProducersSequence'))+1, process.hltAK4PFJetsBPixCorrected)
    process.HLTAK4PFJetsCorrectionSequence.insert(process.HLTAK4PFJetsCorrectionSequence.index(getattr(process, 'HLTAK4PFCorrectorProducersSequence'))+1, process.hltAK4PFJetsNoBPixCorrected)

    # AK8
    bpix_corrections_tag_AK8 = 'AK8PFHLT'

    process.hltAK8PFBPixFastJetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK8),
        level = cms.string('L1FastJet'),
        srcRho = cms.InputTag("hltFixedGridRhoFastjetAll")
    )
    
    process.hltAK8PFBPixRelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK8),
        level = cms.string('L2Relative')
    )

    process.hltAK8PFBPixAbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK8),
        level = cms.string('L3Absolute')
    )

    process.hltAK8PFBPixResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
        algorithm = cms.string(bpix_corrections_tag_AK8),
        level = cms.string('L2L3Residual')
    )
    

    process.hltAK8PFBPixCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
        correctors = cms.VInputTag("hltAK8PFBPixFastJetCorrector", "hltAK8PFBPixRelativeCorrector", "hltAK8PFBPixAbsoluteCorrector", "hltAK8PFBPixResidualCorrector")
    )
    
    process.HLTAK8PFCorrectorProducersSequence += process.hltAK8PFBPixFastJetCorrector
    process.HLTAK8PFCorrectorProducersSequence += process.hltAK8PFBPixRelativeCorrector
    process.HLTAK8PFCorrectorProducersSequence += process.hltAK8PFBPixAbsoluteCorrector
    process.HLTAK8PFCorrectorProducersSequence += process.hltAK8PFBPixResidualCorrector
    process.HLTAK8PFCorrectorProducersSequence += process.hltAK8PFBPixCorrector

    # NoBPix
    process.hltAK8PFJetsNoBPixCorrected = cms.EDProducer("CorrectedPFJetProducer",
        correctors = cms.VInputTag("hltAK8PFCorrector"),
        src = cms.InputTag("hltAK8PFJetsNoBPix")
    )

    # BPix
    process.hltAK8PFJetsBPixCorrected = cms.EDProducer("CorrectedPFJetProducer",
        correctors = cms.VInputTag("hltAK8PFBPixCorrector"),
        src = cms.InputTag("hltAK8PFJetsBPix")
    )
    
    process.HLTAK8PFJetsCorrectionSequence.insert(process.HLTAK8PFJetsCorrectionSequence.index(getattr(process, 'HLTAK8PFCorrectorProducersSequence'))+1, process.hltAK8PFJetsBPixCorrected)
    process.HLTAK8PFJetsCorrectionSequence.insert(process.HLTAK8PFJetsCorrectionSequence.index(getattr(process, 'HLTAK8PFCorrectorProducersSequence'))+1, process.hltAK8PFJetsNoBPixCorrected)

    ## ----- Redefine Corrected PF Jets as merges of the splitted corrected collections
    # AK4
    process.hltAK4PFJetsCorrected = cms.EDProducer( "PFJetsMerger",
      JetSrc = cms.VInputTag( "hltAK4PFJetsNoBPixCorrected" , "hltAK4PFJetsBPixCorrected" )
    )
    
    #AK8
    process.hltAK8PFJetsCorrected = cms.EDProducer( "PFJetsMerger",
      JetSrc = cms.VInputTag( "hltAK8PFJetsNoBPixCorrected" , "hltAK8PFJetsBPixCorrected" )
    )

    return process

