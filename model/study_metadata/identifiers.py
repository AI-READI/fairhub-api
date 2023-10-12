from model import Study


class Identifiers:
    def __init__(self, study: Study):
        self.study = study

    study: Study

    def to_dict(self):
        sorted_study_identifications = sorted(
            self.study.study_identification,
            key=lambda identifier: identifier.created_at,
        )
        return {
            "primary": [
                identifier
                for identifier in sorted_study_identifications
                if not identifier.secondary
            ][0].to_dict()
            if len(
                [
                    identifier
                    for identifier in sorted_study_identifications
                    if not identifier.secondary
                ]
            )
            != 0  # noqa: W503
            else [],
            "secondary": [
                identifier.to_dict()
                for identifier in sorted_study_identifications
                if identifier.secondary
            ],
        }
        # sorted_study_reference = sorted(study_reference_, key=lambda x: x.created_at, reverse=True)
        # return [s.to_dict() for s in sorted_study_reference]
