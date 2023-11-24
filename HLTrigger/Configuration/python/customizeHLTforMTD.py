import FWCore.ParameterSet.Config as cms

def customizeHLTforMTD(process):
    ## event setup
    process.Chi2EstimatorForRefit = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
        ComponentName = cms.string('Chi2EstimatorForRefit'),
        MaxChi2 = cms.double(100000.0),
        MaxDisplacement = cms.double(0.5),
        MaxSagitta = cms.double(2),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000000000),
        MinimalTolerance = cms.double(0.5),
        appendToDataLabel = cms.string(''),
        nSigma = cms.double(3.0)
    )

    process.Chi2MeasurementEstimatorForInOut = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
        ComponentName = cms.string('Chi2ForInOut'),
        MaxChi2 = cms.double(100.0),
        MaxDisplacement = cms.double(100),
        MaxSagitta = cms.double(-1),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000000000),
        MinimalTolerance = cms.double(0.5),
        appendToDataLabel = cms.string(''),
        nSigma = cms.double(3)
    )

    process.KFSmootherForRefitOutsideIn = cms.ESProducer("KFTrajectorySmootherESProducer",
        ComponentName = cms.string('KFSmootherForRefitOutsideIn'),
        Estimator = cms.string('Chi2EstimatorForRefit'),
        Propagator = cms.string('SmartPropagatorAnyRKOpposite'),
        RecoGeometry = cms.string('GlobalDetLayerGeometry'),
        Updator = cms.string('KFUpdator'),
        appendToDataLabel = cms.string(''),
        errorRescaling = cms.double(100.0),
        minHits = cms.int32(3)
    )

    process.KFTrajectoryFitterForInOut = cms.ESProducer("KFTrajectoryFitterESProducer",
        ComponentName = cms.string('KFFitterForInOut'),
        Estimator = cms.string('Chi2ForInOut'),
        Propagator = cms.string('alongMomElePropagator'),
        RecoGeometry = cms.string('GlobalDetLayerGeometry'),
        Updator = cms.string('KFUpdator'), 
        appendToDataLabel = cms.string(''),
        minHits = cms.int32(3)
    )
    
    process.MTDCPEESProducer = cms.ESProducer("MTDCPEESProducer",
        appendToDataLabel = cms.string('')
    )


    process.MTDTimeCalibESProducer = cms.ESProducer("MTDTimeCalibESProducer",
        BTLTimeOffset = cms.double(0.0115),
        ETLTimeOffset = cms.double(0.0066),
        BTLLightCollTime = cms.double(0.2),
        BTLLightCollSlope = cms.double(0.075),
        appendToDataLabel = cms.string('')
    )

    process.MTDTransientTrackingRecHitBuilder = cms.ESProducer("MTDTransientTrackingRecHitBuilderESProducer",
        ComponentName = cms.string('MTDRecHitBuilder')
    )

    process.PropagatorWithMaterialForMTD = cms.ESProducer("PropagatorWithMaterialESProducer",
        ComponentName = cms.string('PropagatorWithMaterialForMTD'),
        Mass = cms.double(0.13957018),
        MaxDPhi = cms.double(1.6),
        PropagationDirection = cms.string('anyDirection'),
        ptMin = cms.double(0.1),
        useOldAnalPropLogic = cms.bool(False),
        useRungeKutta = cms.bool(False)
    )

    process.RungeKuttaTrackerPropagatorOpposite = cms.ESProducer("PropagatorWithMaterialESProducer",
        ComponentName = cms.string('RungeKuttaTrackerPropagatorOpposite'),
        Mass = cms.double(0.105),
        MaxDPhi = cms.double(1.6),
        PropagationDirection = cms.string('oppositeToMomentum'),
        SimpleMagneticField = cms.string(''),
        ptMin = cms.double(-1.0),
        useRungeKutta = cms.bool(True)
    )

    process.SmartPropagatorAnyRKOpposite = cms.ESProducer("SmartPropagatorESProducer",
        ComponentName = cms.string('SmartPropagatorAnyRKOpposite'),
        Epsilon = cms.double(5.0),
        MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
        PropagationDirection = cms.string('oppositeToMomentum'),
        TrackerPropagator = cms.string('RungeKuttaTrackerPropagatorOpposite')
    )

    process.alongMomElePropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
        ComponentName = cms.string('alongMomElePropagator'),
        Mass = cms.double(0.000511),
        MaxDPhi = cms.double(1.6),
        PropagationDirection = cms.string('alongMomentum'),
        SimpleMagneticField = cms.string(''),
        ptMin = cms.double(-1.0),
        useRungeKutta = cms.bool(False)
    )
    
    ## modules
    
    # mtd rec hits    
    _barrelAlgo = cms.PSet(
        algoName = cms.string("MTDRecHitAlgo"),
        thresholdToKeep = cms.double(1.),          # MeV
        calibrationConstant = cms.double(0.03125), # MeV/pC
    )


    _endcapAlgo = cms.PSet(
        algoName = cms.string("MTDRecHitAlgo"),
        thresholdToKeep = cms.double(0.005),    # MeV
        calibrationConstant = cms.double(0.015), # MeV/MIP
    )

    from Configuration.Eras.Modifier_phase2_etlV4_cff import phase2_etlV4
    phase2_etlV4.toModify(_endcapAlgo, thresholdToKeep = 0.005, calibrationConstant = 0.015 )

    process.mtdRecHits = cms.EDProducer(
        "MTDRecHitProducer",
        barrel = _barrelAlgo,
        endcap = _endcapAlgo,
        barrelUncalibratedRecHits = cms.InputTag('mtdUncalibratedRecHits:FTLBarrel'),
        endcapUncalibratedRecHits = cms.InputTag('mtdUncalibratedRecHits:FTLEndcap'),
        BarrelHitsName = cms.string('FTLBarrel'),
        EndcapHitsName = cms.string('FTLEndcap'),
    )

    # mtd clusters
    process.mtdClusters = cms.EDProducer("MTDClusterProducer",
        srcBarrel = cms.InputTag('mtdRecHits:FTLBarrel'),
        srcEndcap = cms.InputTag('mtdRecHits:FTLEndcap'),
        BarrelClusterName = cms.string('FTLBarrel'),
        EndcapClusterName = cms.string('FTLEndcap'),
        ClusterMode = cms.string('MTDThresholdClusterizer')  
    )

    # mtd tracking rec hits
    process.mtdTrackingRecHits = cms.EDProducer("MTDTrackingRecHitProducer",
        barrelClusters = cms.InputTag("mtdClusters","FTLBarrel"),
        endcapClusters = cms.InputTag("mtdClusters","FTLEndcap"),
    )
    
    # mtd uncalibrated rec hits
    # take values parameters from offline cfis
    from SimFastTiming.FastTimingCommon.mtdDigitizer_cfi import mtdDigitizer


    _barrelAlgo = cms.PSet(
        algoName = cms.string("BTLUncalibRecHitAlgo"),
        adcNbits = mtdDigitizer.barrelDigitizer.ElectronicsSimulation.adcNbits,
        adcSaturation = mtdDigitizer.barrelDigitizer.ElectronicsSimulation.adcSaturation_MIP,
        toaLSB_ns = mtdDigitizer.barrelDigitizer.ElectronicsSimulation.toaLSB_ns,
        timeResolutionInNs = cms.string("0.308*pow(x,-0.4175)"), # [ns]
        timeCorr_p0 = cms.double( 2.21103),
        timeCorr_p1 = cms.double(-0.933552),
        timeCorr_p2 = cms.double( 0.),
        c_LYSO = cms.double(13.846235)     # in unit cm/ns
    )


    _endcapAlgo = cms.PSet(
        algoName      = cms.string("ETLUncalibRecHitAlgo"),
        adcNbits      = mtdDigitizer.endcapDigitizer.ElectronicsSimulation.adcNbits,
        adcSaturation = mtdDigitizer.endcapDigitizer.ElectronicsSimulation.adcSaturation_MIP,
        toaLSB_ns     = mtdDigitizer.endcapDigitizer.ElectronicsSimulation.toaLSB_ns,
        tofDelay      = mtdDigitizer.endcapDigitizer.DeviceSimulation.tofDelay,
        timeResolutionInNs = cms.string("0.039") # [ns]
    )


    process.mtdUncalibratedRecHits = cms.EDProducer(
        "MTDUncalibratedRecHitProducer",
        barrel = _barrelAlgo,
        endcap = _endcapAlgo,
        barrelDigis = cms.InputTag('mix:FTLBarrel'),
        endcapDigis = cms.InputTag('mix:FTLEndcap'),
        BarrelHitsName = cms.string('FTLBarrel'),
        EndcapHitsName = cms.string('FTLEndcap')
    )

    from Configuration.ProcessModifiers.premix_stage2_cff import premix_stage2
    premix_stage2.toModify(process.mtdUncalibratedRecHits,
        barrelDigis = 'mixData:FTLBarrel',
        endcapDigis = 'mixData:FTLEndcap',
    )




    # keep tranjectories in tracks
    # these are the tracks used for generalTracks
    process.initialStepTracks.TrajectoryInEvent = cms.bool(True)
    process.highPtTripletStepTracks.TrajectoryInEvent = cms.bool(True)
    
    process.initialStepTrackSelectionHighPurity.copyTrajectories = cms.untracked.bool(True)
    process.highPtTripletStepTrackSelectionHighPurity.copyTrajectories = cms.untracked.bool(True)

    process.generalTracksWithMTD = cms.EDProducer("TrackExtenderWithMTD",
        tracksSrc = cms.InputTag('generalTracks'),
        trjtrkAssSrc = cms.InputTag('generalTracks'),
        hitsSrc = cms.InputTag('mtdTrackingRecHits'),
        beamSpotSrc = cms.InputTag('offlineBeamSpot'),
        genVtxPositionSrc = cms.InputTag('genParticles', 'xyz0'),
        genVtxTimeSrc = cms.InputTag('genParticles', 't0'),
        vtxSrc = cms.InputTag('unsortedOfflinePrimaryVertices'), 
        updateTrackTrajectory = cms.bool(True),
        updateTrackExtra = cms.bool(True),
        updateTrackHitPattern = cms.bool(True),
        TransientTrackBuilder = cms.string('TransientTrackBuilder'),
        MTDRecHitBuilder = cms.string('MTDRecHitBuilder'),
        Propagator = cms.string('PropagatorWithMaterialForMTD'),
        TrackTransformer = cms.PSet(
            DoPredictionsOnly = cms.bool(False),
            #Fitter = cms.string('KFFitterForRefitInsideOut'), 
            #Smoother = cms.string('KFSmootherForRefitInsideOut'),
            Fitter = cms.string('KFFitterForInOut'),
            Smoother = cms.string('KFSmootherForRefitOutsideIn'),
            Propagator = cms.string('PropagatorWithMaterialForMTD'),
            RefitDirection = cms.string('alongMomentum'),
            RefitRPCHits = cms.bool(True),
            TrackerRecHitBuilder = cms.string('WithTrackAngle'),
            #MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            MTDRecHitBuilder = cms.string('MTDRecHitBuilder')
        ),
        estimatorMaxChi2 = cms.double(500),
        estimatorMaxNSigma = cms.double(10),
        btlChi2Cut = cms.double(50),
        btlTimeChi2Cut = cms.double(10),
        etlChi2Cut = cms.double(50),
        etlTimeChi2Cut = cms.double(10),
        useVertex = cms.bool(False),
        useSimVertex = cms.bool(False),
        dZCut = cms.double(0.1),
        bsTimeSpread = cms.double(0.2),
    )

    process.generalTracksTOFPIDProducer = cms.EDProducer("TOFPIDProducer",
        tracksSrc    = cms.InputTag("generalTracks"),
        t0Src        = cms.InputTag("generalTracksWithMTD:generalTrackt0"),
        tmtdSrc      = cms.InputTag("generalTracksWithMTD:generalTracktmtd"),
        sigmat0Src   = cms.InputTag("generalTracksWithMTD:generalTracksigmat0"),
        sigmatmtdSrc = cms.InputTag("generalTracksWithMTD:generalTracksigmatmtd"),
        tofkSrc      = cms.InputTag("generalTracksWithMTD:generalTrackTofK"),
        tofpSrc      = cms.InputTag("generalTracksWithMTD:generalTrackTofP"),
        vtxsSrc      = cms.InputTag("unsortedOfflinePrimaryVertices4D"),
        vtxMaxSigmaT      = cms.double(0.025),
        maxDz             = cms.double(0.1),
        maxDtSignificance = cms.double(5.0),
        minProbHeavy      = cms.double(0.75),
        fixedT0Error      = cms.double(0.0),
    )

    process.generalTracksMtdTrackQualityMVA = cms.EDProducer("MTDTrackQualityMVAProducer",
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
    

    ## Vertices
    
    process.unsortedOfflinePrimaryVertices4DnoPID = cms.EDProducer("PrimaryVertexProducer",
        TkClusParameters = cms.PSet(
            TkDAClusParameters = cms.PSet(
                Tmin = cms.double(4.0),
                Tpurge = cms.double(4.0),
                Tstop = cms.double(2.0),
                convergence_mode = cms.int32(0),
                coolingFactor = cms.double(0.6),
                d0CutOff = cms.double(3.0),
                delta_highT = cms.double(0.01),
                delta_lowT = cms.double(0.001),
                dtCutOff = cms.double(4.0),
                dzCutOff = cms.double(3.0),
                t0Max = cms.double(1.0),
                tmerge = cms.double(0.1),
                uniquetrkminp = cms.double(0.0),
                uniquetrkweight = cms.double(0.8),
                vertexSize = cms.double(0.006),
                vertexSizeTime = cms.double(0.008),
                zmerge = cms.double(0.01),
                zrange = cms.double(4.0)
            ),
            algorithm = cms.string('DA2D_vect')
        ),
        TkFilterParameters = cms.PSet(
            algorithm = cms.string('filter'),
            maxD0Error = cms.double(1.0),
            maxD0Significance = cms.double(4.0),
            maxDzError = cms.double(1.0),
            maxEta = cms.double(4.0),
            maxNormalizedChi2 = cms.double(10.0),
            minPixelLayersWithHits = cms.int32(2),
            minPt = cms.double(0.0),
            minSiliconLayersWithHits = cms.int32(5),
            trackQuality = cms.string('any')
        ),
        TrackLabel = cms.InputTag("generalTracks"),
        TrackTimeResosLabel = cms.InputTag("generalTracksWithMTD","generalTracksigmat0"),
        TrackTimesLabel = cms.InputTag("generalTracksWithMTD","generalTrackt0"),
        beamSpotLabel = cms.InputTag("offlineBeamSpot"),
        isRecoveryIteration = cms.bool(False),
        recoveryVtxCollection = cms.InputTag(""),
        verbose = cms.untracked.bool(False),
        vertexCollections = cms.VPSet(
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string(''),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(0.0),
                useBeamConstraint = cms.bool(False)
            ),
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string('WithBS'),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(2.0),
                useBeamConstraint = cms.bool(True)
            )
        )
)
    
    process.tofPID4DnoPID = cms.EDProducer("TOFPIDProducer",
        fixedT0Error = cms.double(0),
        maxDtSignificance = cms.double(5),
        maxDz = cms.double(0.1),
        mightGet = cms.optional.untracked.vstring,
        minProbHeavy = cms.double(0.75),
        sigmat0Src = cms.InputTag("generalTracksWithMTD","generalTracksigmat0"),
        sigmatmtdSrc = cms.InputTag("generalTracksWithMTD","generalTracksigmatmtd"),
        t0Src = cms.InputTag("generalTracksWithMTD","generalTrackt0"),
        tmtdSrc = cms.InputTag("generalTracksWithMTD","generalTracktmtd"),
        tofkSrc = cms.InputTag("generalTracksWithMTD","generalTrackTofK"),
        tofpSrc = cms.InputTag("generalTracksWithMTD","generalTrackTofP"),
        tracksSrc = cms.InputTag("generalTracks"),
        vtxMaxSigmaT = cms.double(0.025),
        vtxsSrc = cms.InputTag("unsortedOfflinePrimaryVertices4DnoPID")
    )
        
    process.unsortedOfflinePrimaryVertices4D = cms.EDProducer("PrimaryVertexProducer",
        TkClusParameters = cms.PSet( # clustering parameters
            TkDAClusParameters = cms.PSet(
                Tmin = cms.double(4.0),
                Tpurge = cms.double(4.0),
                Tstop = cms.double(2.0),
                convergence_mode = cms.int32(0),
                coolingFactor = cms.double(0.6),
                d0CutOff = cms.double(3.0),
                delta_highT = cms.double(0.01),
                delta_lowT = cms.double(0.001),
                dtCutOff = cms.double(4.0),
                dzCutOff = cms.double(3.0),
                t0Max = cms.double(1.0),
                tmerge = cms.double(0.1),
                uniquetrkminp = cms.double(0.0),
                uniquetrkweight = cms.double(0.8),
                vertexSize = cms.double(0.006),
                vertexSizeTime = cms.double(0.008),
                zmerge = cms.double(0.01),
                zrange = cms.double(4.0)
            ),
            algorithm = cms.string('DA2D_vect') # if use this option insted of DA_vect which was default it activates the 4D vertex reco
            # note: for 4D also needs the maps for tracks times and resolution labels (see bellow)
        ),
        TkFilterParameters = cms.PSet(
            algorithm = cms.string('filter'),
            maxD0Error = cms.double(1.0),
            maxD0Significance = cms.double(4.0),
            maxDzError = cms.double(1.0),
            maxEta = cms.double(4.0),
            maxNormalizedChi2 = cms.double(10.0),
            minPixelLayersWithHits = cms.int32(2),
            minPt = cms.double(0.0),
            minSiliconLayersWithHits = cms.int32(5),
            trackQuality = cms.string('any')
        ),
        TrackLabel = cms.InputTag("generalTracks"),
        beamSpotLabel = cms.InputTag("offlineBeamSpot"),
        # TrackTimesLabel = cms.InputTag("generalTracksTOFPIDProducer:t0"),
        # TrackTimeResosLabel = cms.InputTag("generalTracksTOFPIDProducer:sigmat0"),
        TrackTimeResosLabel = cms.InputTag("tofPID4DnoPID","sigmat0safe"),
        TrackTimesLabel = cms.InputTag("tofPID4DnoPID","t0safe"),
        #TrackTimesLabel = cms.InputTag("generalTracksTOFPIDProducer:t0safe"),
        #TrackTimeResosLabel = cms.InputTag("generalTracksTOFPIDProducer:sigmat0safe"),   
        verbose = cms.untracked.bool(False),
        vertexCollections = cms.VPSet(
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string(''),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(0.0),
                useBeamConstraint = cms.bool(False)
            ),
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string('WithBS'),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(2.0),
                useBeamConstraint = cms.bool(True)
            )
        )
    )
    
    process.trackWithVertexRefSelectorBeforeSorting.vertexTag = cms.InputTag("unsortedOfflinePrimaryVertices4D") 

    process.offlinePrimaryVertices4D = cms.EDProducer("RecoChargedRefCandidatePrimaryVertexSorter",
        assignment = cms.PSet(
            DzCutForChargedFromPUVtxs = cms.double(0.2),
            EtaMinUseDz = cms.double(-1),
            NumOfPUVtxsForCharged = cms.uint32(0),
            OnlyUseFirstDz = cms.bool(False),
            PtMaxCharged = cms.double(-1),
            maxDistanceToJetAxis = cms.double(0.07),
            maxDtSigForPrimaryAssignment = cms.double(3),
            maxDxyForJetAxisAssigment = cms.double(0.1),
            maxDxyForNotReconstructedPrimary = cms.double(0.01),
            maxDxySigForNotReconstructedPrimary = cms.double(2),
            maxDzErrorForPrimaryAssignment = cms.double(0.05),
            maxDzForJetAxisAssigment = cms.double(0.1),
            maxDzForPrimaryAssignment = cms.double(0.1),
            maxDzSigForPrimaryAssignment = cms.double(5),
            maxJetDeltaR = cms.double(0.5),
            minJetPt = cms.double(25),
            preferHighRanked = cms.bool(False),
            useTiming = cms.bool(True),
            useVertexFit = cms.bool(True)
        ),
        jets = cms.InputTag("ak4CaloJetsForTrk"),
        particles = cms.InputTag("trackRefsForJetsBeforeSorting"), # in this we have used the unsortedOfflinePrimaryVertices4D
        produceAssociationToOriginalVertices = cms.bool(False),
        produceNoPileUpCollection = cms.bool(False),
        producePileUpCollection = cms.bool(False),
        produceSortedVertices = cms.bool(True),
        qualityForPrimary = cms.int32(3),
        sorting = cms.PSet(

        ),
        trackTimeTag = cms.InputTag("generalTracksTOFPIDProducer:t0"),
        trackTimeResoTag = cms.InputTag("generalTracksTOFPIDProducer:sigmat0"),
        usePVMET = cms.bool(True),
        vertices = cms.InputTag("unsortedOfflinePrimaryVertices4D")
    )
    
    process.goodOfflinePrimaryVertices4D = cms.EDFilter("VertexSelector",
        cut = cms.string('!isFake && ndof >= 4.0 && abs(z) <= 24.0 && abs(position.Rho) <= 2.0'),
        filter = cms.bool(False),
        src = cms.InputTag("offlinePrimaryVertices4D")
    )

    ## Add MTD in PF Block
    process.particleFlowBlock.elementImporters.append(
    cms.PSet( ## adding TrackTimingImporter
            importerName = cms.string('TrackTimingImporter'),
            timeErrorMap = cms.InputTag("generalTracksTOFPIDProducer","sigmat0"),
            timeErrorMapGsf = cms.InputTag("generalTracksTOFPIDProducer","sigmat0"),
            timeValueMap = cms.InputTag("generalTracksTOFPIDProducer","t0"),
            timeValueMapGsf = cms.InputTag("generalTracksTOFPIDProducer","t0"),
            timeQualityMap = cms.InputTag("generalTracksMtdTrackQualityMVA","mtdQualMVA"),
            timeQualityMapGsf = cms.InputTag("generalTracksMtdTrackQualityMVA","mtdQualMVA"),
            timeQualityThreshold = cms.double(0.5) # MVA quality threshold
        )
    )
    
    ## Change to add maps in PFTICL
    process.pfTICL.trackTimeErrorMap = cms.InputTag("generalTracksTOFPIDProducer","sigmat0")
    process.pfTICL.trackTimeValueMap = cms.InputTag("generalTracksTOFPIDProducer","t0")
    process.pfTICL.trackTimeQualityMap = cms.InputTag("generalTracksMtdTrackQualityMVA","mtdQualMVA")
    process.pfTICL.timingQualityThreshold = cms.double(0.5) # MVA quality threshold
    process.pfTICL.useMTDTiming = cms.bool(True) # uses MTD timing  
    process.pfTICL.useTimingAverage = cms.bool(True) # combined time from both MTD and HGCAL if they both valid time (time error > 0)

    process.ticlTrackstersMerge.useMTDTiming = cms.bool(True)
    process.ticlTrackstersMerge.tracksTime = cms.InputTag("generalTracksTOFPIDProducer","t0")
    process.ticlTrackstersMerge.tracksTimeErr = cms.InputTag("generalTracksTOFPIDProducer","sigmat0")
    process.ticlTrackstersMerge.tracksTimeQual = cms.InputTag("generalTracksMtdTrackQualityMVA","mtdQualMVA")
    
    ## tasks changes
    process.mtdRecoTask = cms.Task(
        process.mtdUncalibratedRecHits,
        process.mtdRecHits,
        process.mtdClusters,
        process.mtdTrackingRecHits,
        process.generalTracksWithMTD,
        process.generalTracksMtdTrackQualityMVA,
        process.generalTracksTOFPIDProducer,
        process.tofPID4DnoPID
    )
    
    process.vertex4DrecoTask = cms.Task(
        process.unsortedOfflinePrimaryVertices4DnoPID,
        process.unsortedOfflinePrimaryVertices4D,
        process.offlinePrimaryVertices4D,
        process.goodOfflinePrimaryVertices4D
    )

    process.HLTParticleFlowTask.add( 
        cms.Task(
        process.mtdRecoTask,
        process.iterTICLTask,
        process.vertex4DrecoTask
        )
    )

    return process

    

  