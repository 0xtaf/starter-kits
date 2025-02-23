import forta_agent
from hexbytes import HexBytes
from forta_agent import Finding, FindingType, FindingSeverity, get_json_rpc_url
from src.constants import CEXES
from web3 import Web3

web3 = Web3(Web3.HTTPProvider(get_json_rpc_url()))


def initialize():
    """
    this function initializes the state variables that are tracked across tx and blocks
    it is called from test to reset state between tests
    """

def is_contract(w3, address) -> bool:
    """
    this function determines whether address is a contract
    :return: is_contract: bool
    """
    if address is None:
        return True
    code = w3.eth.get_code(Web3.toChecksumAddress(address))
    return code != HexBytes('0x')

def detect_dex_funding(w3, transaction_event: forta_agent.transaction_event.TransactionEvent) -> list:
    findings = []

    # alert on funding tx from CEXes
    value = transaction_event.transaction.value
    for chainId, address, name, threshold in CEXES:
        if (not is_contract(w3, transaction_event.transaction.to) and chainId == w3.eth.chainId and 
            address == transaction_event.transaction.from_ and value < threshold and 
            w3.eth.get_transaction_count(Web3.toChecksumAddress(transaction_event.transaction.to), transaction_event.block.number) == 0):
            findings.append(Finding(
                {
                    "name": "CEX Funding",
                    "description": f"CEX Funding from {name} of {value} wei to {transaction_event.transaction.to}",
                    "alert_id": "CEX-FUNDING-1",
                    "type": FindingType.Suspicious,
                    "severity": FindingSeverity.Low,
                    "metadata": {"CEX_name": name, "to": transaction_event.transaction.to, "value": value}
                }
            ))

    return findings


def provide_handle_transaction(w3):
    def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent) -> list:
        return detect_dex_funding(w3, transaction_event)

    return handle_transaction


real_handle_transaction = provide_handle_transaction(web3)


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    return real_handle_transaction(transaction_event)