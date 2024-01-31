#include "CommonTools/RecoAlgos/interface/PFJetsMerger.h"
#include "Math/GenVector/VectorUtil.h"
#include "FWCore/Utilities/interface/EDMException.h"
//
// class decleration
//
using namespace reco;
using namespace std;
using namespace edm;

PFJetsMerger::PFJetsMerger(const edm::ParameterSet& iConfig)
    : jetSrc(iConfig.getParameter<vtag>("JetSrc")) {
  for (vtag::const_iterator it = jetSrc.begin(); it != jetSrc.end(); ++it) {
    edm::EDGetTokenT<PFJetCollection> aToken = consumes<PFJetCollection>(*it);
    jetSrc_token.push_back(aToken);
  }

  produces<PFJetCollection>();
}

PFJetsMerger::~PFJetsMerger() {}

void PFJetsMerger::produce(edm::StreamID iSId, edm::Event& iEvent, const edm::EventSetup& iES) const {
  using namespace edm;
  using namespace std;
  using namespace reco;

  // Defining collection of merged jets
  std::unique_ptr<PFJetCollection> mergedJets(new PFJetCollection);
  //PFJetCollection mergedJets;
  
  // Iterate over jets collections to merge
  for (vtoken_cjets::const_iterator iJetCollection = jetSrc_token.begin(); iJetCollection != jetSrc_token.end(); ++iJetCollection) {
    edm::Handle<PFJetCollection> subCollJets;
    iEvent.getByToken(*iJetCollection, subCollJets);
    // For each jet collection push to the merged jet collection the jets
    for (PFJetCollection::const_iterator iJet = subCollJets->begin(); iJet != subCollJets->end(); ++iJet) {
      mergedJets->push_back(*iJet);
    }
  }
  iEvent.put(std::move(mergedJets));
}

void PFJetsMerger::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  std::vector<edm::InputTag> inputTags;
  desc.add<std::vector<edm::InputTag> >("JetSrc", inputTags)->setComment("PFJet collections to merge");
  descriptions.add("PFJetsMerger", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PFJetsMerger);