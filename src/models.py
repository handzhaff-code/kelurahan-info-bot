

class Article:
    def __init__(self, id, category, question, keywords, answer):
        self.id = id
        self.category = category
        self.question = question
        self.keywords = keywords
        self.answer = answer

    @classmethod
    def from_dict(cls, Data):
        return cls(
            Data["id"],
            Data["category"],
            Data["question"],
            Data["keywords"],
            Data["answer"]
        )
        