from operator import inv
from time import strftime
from forta_agent import Finding, FindingType, FindingSeverity, Label, EntityType, LabelType
from datetime import datetime


class AlertCombinerFinding:

    @staticmethod
    def alert_combiner(attacker_address: str, start_date: datetime, end_date: datetime, involved_addresses: set, involved_alerts: set, alert_id: str, hashes: set) -> Finding:
        involved_addresses = list(involved_addresses)[0:500]
        hashes = list(hashes)[0:10]

        attacker_address_md = {"attacker_address": attacker_address}
        start_date = {"start_date": start_date.strftime("%Y-%m-%d")}
        end_date = {"end_date": end_date.strftime("%Y-%m-%d")}
        involved_addresses = {"involved_addresses_" + str(i): address for i, address in enumerate(involved_addresses, 1)}
        involved_alert_ids = {"involved_alert_id_" + str(i): alert_id for i, alert_id in enumerate(involved_alerts, 1)}
        involved_alert_hashes = {"involved_alert_hashes_" + str(i): alert_id for i, alert_id in enumerate(hashes, 1)}
        meta_data = {**attacker_address_md, **start_date, **end_date, **involved_addresses, **involved_alert_ids, **involved_alert_hashes}

        labels = []
        if alert_id == "ATTACK-DETECTOR-ICE-PHISHING":
            labels = [Label({
    		    'entity_type': EntityType.Address,
    		    'label_type': LabelType.Scam,
    		    'entity': attacker_address,
                'confidence': 0.99,
                'custom_value': ""
    	    })]

        return Finding({
            'name': 'Attack detector identified an EOA with past alerts mapping to attack behavior',
            'description': f'{attacker_address} likely involved in an attack ({alert_id})',
            'alert_id': alert_id,
            'type': FindingType.Exploit,
            'severity': FindingSeverity.Critical,
            'metadata': meta_data,
            'labels': labels
        })
