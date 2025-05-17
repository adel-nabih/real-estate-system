class Property:
    def __init__(self, id, location, type_, size, price, status="available", broker_id=None):
        self.id = id
        self.location = location
        self.type = type_
        self.size = size
        self.price = float(price) if price else 0.0
        self.status = status
        self.broker_id = broker_id

    @classmethod
    def from_dict(cls, row):
        return cls(
            id=row['id'],
            location=row['location'],
            type_=row['type'],
            size=row['size'],
            price=row['price'],
            status=row['status'],
            broker_id=row.get('broker_id')
        )
