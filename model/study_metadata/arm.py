from model import Study


class Arm:
    def __init__(self, study: Study):
        self.study = study

    study: Study
    def to_dict(self):
        return {
            "arms": [arm.to_dict() for arm in self.study.study_arm],
            "study_type": self.study.study_design.study_type,
        }



