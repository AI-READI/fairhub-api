import dataclasses


@dataclasses.dataclass
class Owner:
    ORCID: str
    name: str
    email: str

    def to_dict(self):
        return {
            "ORCID": self.ORCID,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_data(data):
        owner=Owner('ORCID', 'name', 'email')
        owner.ORCID = data['ORCID']
        owner.name=data['name']
        owner.email = data['email']
        return owner