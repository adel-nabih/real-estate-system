class Client:
    def __init__(self, id, name, contact, preferences, broker_id=None):
        self.id = id
        self.name = name
        self.contact = contact
        self.preferences = preferences
        self.broker_id = broker_id

    @classmethod
    def from_dict(cls, row):
        return cls(
            id=row['id'],
            name=row['name'],
            contact=row['contact'],
            preferences=row['preferences'],
            broker_id=row['broker_id']
        )
