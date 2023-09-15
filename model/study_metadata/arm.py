from model import Study


class Arm:
    def __init__(self, study: Study):
        self.study = study

    study: Study

    def to_dict(self):
        sorted_study_arms = sorted(self.study.study_arm, key=lambda arm: arm.created_at)
        return {
            "arms": [arm.to_dict() for arm in sorted_study_arms],
            "study_type": self.study.study_design.study_type,
        }
