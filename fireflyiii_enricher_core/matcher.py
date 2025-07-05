"""Match bank transactions with records retrieved from Firefly."""
from datetime import datetime


class TransactionMatcher:
    @staticmethod
    def match(tx, records):
        firefly_date = datetime.fromisoformat(tx["date"]).date()
        firefly_amount = float(tx["amount"])
        matches = []

        for record in records:
            csv_date = datetime.strptime(record["date"], "%d-%m-%Y").date()
            csv_amount = float(record["amount"])
            if csv_date == firefly_date and abs(csv_amount) == abs(firefly_amount):
                matches.append(record)

        return matches
