from forta_agent import Finding, FindingType, FindingSeverity


class MaliciousContractFindings:

    @staticmethod
    def malicious_contract_creation(from_address: str, contract_address: str, contained_addresses: set, model_score: float, model_threshold: float) -> Finding:
        metadata = {"address_contained_in_created_contract_" + str(i): address for i, address in enumerate(contained_addresses, 1)}
        metadata["model_score"] = str(model_score)
        metadata["model_threshold"] = str(model_threshold)

        return Finding({
            'name': 'Suspicious Contract Creation',
            'description': f'{from_address} created contract {contract_address}',
            'alert_id': 'SUSPICIOUS-CONTRACT-CREATION',
            'type': FindingType.Suspicious,
            'severity': FindingSeverity.High,
            'metadata': metadata
        })
