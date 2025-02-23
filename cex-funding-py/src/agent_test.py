from forta_agent import create_transaction_event, FindingSeverity
import agent
from web3_mock import Web3Mock, NEW_EOA, OLD_EOA, NEW_CONTRACT

w3 = Web3Mock()


class TestDEXFunding:

    def test_not_transfer_to_cex(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': NEW_EOA,
                'from': "0x4e5b2e1dc63f6b91cb6cd759936495434c7e0000",
                'value': "1000000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_dex_funding(w3, tx_event)
        assert len(findings) == 0, "this should have not triggered a finding as the from is not a CEX"

    def test_transfer_to_contract(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': NEW_CONTRACT,
                'from': "0x4e5b2e1dc63f6b91cb6cd759936495434c7e0000",
                'value': "1000000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_dex_funding(w3, tx_event)
        assert len(findings) == 0, "this should have not triggered a finding is to a contract"

    def test_transfer_to_old_eoa(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': OLD_EOA,
                'from': "0x4e5b2e1dc63f6b91cb6cd759936495434c7e0000",
                'value': "1000000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_dex_funding(w3, tx_event)
        assert len(findings) == 0, "this should have not triggered a finding is to an old EOA"

    def test_transfer_excessive_amount(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': NEW_EOA,
                'from': "0x4e5b2e1dc63f6b91cb6cd759936495434c7e0000",
                'value': "3000000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_dex_funding(w3, tx_event)
        assert len(findings) == 0, "this should have not triggered a finding as funding amount is too large"


    def test_cex_funding(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': NEW_EOA,
                'from': "0x4e5b2e1dc63f6b91cb6cd759936495434c7e972f",
                'value': "1000000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_dex_funding(w3, tx_event)
        assert len(findings) == 1, "this should have triggered a finding"
