from model import Study


class Identifiers:
    def __init__(self, study: Study):
        self.study = study

    study: Study
    def to_dict(self):
        return {
            "primary": [identifier for identifier in self.study.study_identification if not identifier.secondary][0].to_dict(),
            "secondary": [identifier.to_dict() for identifier in self.study.study_identification if identifier.secondary],
        }

