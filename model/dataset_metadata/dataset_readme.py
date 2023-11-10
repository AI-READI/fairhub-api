from ..db import db


class DatasetReadme(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.content = ""

    __tablename__ = "dataset_readme"
    content = db.Column(db.String, nullable=False)

    dataset_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False
    )
    dataset = db.relationship("Dataset", back_populates="dataset_readme")

    def to_dict(self):
        return {
            "id": self.dataset_id,
            "content": self.content,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_readme = DatasetReadme(dataset)
        dataset_readme.update(data)
        return dataset_readme

    def update(self, data: dict):
        self.content = data["content"]
        self.dataset.touch_dataset()
