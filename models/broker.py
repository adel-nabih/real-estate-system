class Broker:
    def __init__(self, id, name, years_experience):
        self.id = id
        self.name = name
        self.years_experience = years_experience

    @classmethod
    def from_dict(cls, row):
        return cls(
            id=row['id'],
            name=row['name'],
            years_experience=row['years_experience']
        )
