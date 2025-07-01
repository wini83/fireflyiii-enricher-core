"""Moduł przetwarzający i interaktywnie aktualizujący dane w Firefly."""
from fireflyiii_enricher_core.matcher import TransactionMatcher


class TransactionProcessor:
    def __init__(self, firefly_client, bank_records):
        self.firefly_client = firefly_client
        self.bank_records = bank_records

    def process(self, filter_text, exact_match=True):
        raw = self.firefly_client.fetch_transactions()
        single = self.firefly_client.filter_single_part(raw)
        uncategorized = self.firefly_client.filter_without_category(single)
        filtered = self.firefly_client.filter_by_description(uncategorized, filter_text, exact_match)
        firefly_transactions = self.firefly_client.simplify_transactions(filtered)

        for tx in firefly_transactions:
            print(f"\n📌 Firefly: ID {tx['id']} | {tx['date']} | {tx['amount']} PLN | {tx['description']}")
            print("   🔍 Możliwe dopasowania z danymi:")

            matches = TransactionMatcher.match(tx, self.bank_records)

            if not matches:
                print("   ⚠️ Brak dopasowań.")
                continue

            for i, record in enumerate(matches, start=1):
                sender = record.get("sender", "–")
                recipient = record.get("recipient", "–")
                details = record.get("details", "–")
                print(f"\n   💬 Dopasowanie #{i}")
                print(f"      📅 Data: {record['date']}")
                print(f"      💰 Kwota: {record['amount']} PLN")
                print(f"      👤 Nadawca: {sender}")
                print(f"      🏷️ Odbiorca: {recipient}")
                print(f"      📝 Szczegóły: {details}")
                print(f"          Nowy opis: {tx['description']};{recipient}")
                choice = input("      ❓ Czy zaktualizować opis? (t/n/q): ").strip().lower()
                if choice == 't':
                    new_description = f"{tx['description']};{recipient}"
                    self.firefly_client.update_transaction_description(tx["id"], new_description)
                    break
                if choice == 'q':
                    print("🔚 Zakończono.")
                    return
                print("      ⏩ Pominięto.")
