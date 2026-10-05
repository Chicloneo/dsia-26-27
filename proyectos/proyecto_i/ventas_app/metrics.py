from .validator import SalesRecord


def total_by_region(records: list[SalesRecord]):
    """Devuelve el importe total por región, de mayor a menor."""

    return records.groupby("product").amount().sum().sort_values(ascending=False)

class SalesMetrics:
    """Open/Closed: se pueden añadir métricas sin tocar el validador."""

    def total_by_region(self, records: list[SalesRecord]) -> dict[str, float]:
        totals: dict[str, float] = {}
        for record in records:
            totals[record.region] = totals.get(record.region, 0.0) + record.amount
        return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))