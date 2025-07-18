"""Match bank transactions with records retrieved from Firefly."""
from typing import List

from fireflyiii_enricher_core.firefly_client import SimplifiedItem, SimplifiedTx


class TransactionMatcher:
    """Helper for aligning CSV records with Firefly transactions."""

    @staticmethod
    def match(tx: SimplifiedTx,records: List[SimplifiedItem])->List[SimplifiedItem]:
        matches:List[SimplifiedItem] = []
        for record in records:
            if tx == record:
                matches.append(record)
        return matches
