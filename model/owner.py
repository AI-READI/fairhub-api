from . import db
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
