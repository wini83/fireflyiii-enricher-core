"""Match bank transactions with records retrieved from Firefly."""
from datetime import date


class TransactionMatcher:
    """Helper for aligning CSV records with Firefly transactions."""

    @staticmethod
    def compare_amounts(amount1, amount2):
        """Return True if the amounts are equal ignoring their sign."""
        return abs(float(amount1)) == abs(float(amount2))

    @staticmethod
    def match(tx, records):
        """Return CSV records that correspond to the provided transaction."""
        firefly_date:date = tx["date"]
        firefly_amount:float = tx["amount"]
        matches = []

        for record in records:
            csv_date:date = record["date"]
            csv_amount:float = record["amount"]
            if (csv_date == firefly_date
                    and TransactionMatcher.compare_amounts(csv_amount, firefly_amount)):
                matches.append(record)

        return matches
