import re

class BusinessContextExtractor:
    SKU_PATTERN = re.compile(r"[A-Z]\d{2}[A-Z]\d{5,}[A-Z0-9]*")
    ORDER_PATTERN = re.compile(r"\bO\d+\b")

    def extract(self, text: str) -> dict:
        sku_match = self.SKU_PATTERN.search(text)
        order_match = self.ORDER_PATTERN.search(text)
        return {
            "sku": sku_match.group(0) if sku_match else None,
            "order_id": order_match.group(0) if order_match else None,
        }
