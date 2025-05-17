class Sale:
    def __init__(self, id, property_id, client_id, broker_id, date, final_price):
        self.id = id
        self.property_id = property_id
        self.client_id = client_id
        self.broker_id = broker_id
        self.date = date
        self.final_price = float(final_price)

    @classmethod
    def from_dict(cls, row):
        return cls(
            id=row['id'],
            property_id=row['property_id'],
            client_id=row['client_id'],
            broker_id=row['broker_id'],
            date=row['date'],
            final_price=row['final_price']
        )
