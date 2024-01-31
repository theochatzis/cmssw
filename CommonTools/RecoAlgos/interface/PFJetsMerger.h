
#ifndef PFJETSMERGER_H
#define PFJETSMERGER_H

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

#include <map>
#include <vector>

class PFJetsMerger : public edm::global::EDProducer<> {
public:
  explicit PFJetsMerger(const edm::ParameterSet&);
  ~PFJetsMerger() override;
  void produce(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  typedef std::vector<edm::InputTag> vtag;
  typedef std::vector<edm::EDGetTokenT<reco::PFJetCollection> > vtoken_cjets;
  const vtag jetSrc;
  vtoken_cjets jetSrc_token;
};

#endif