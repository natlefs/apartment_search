from dataclasses import dataclass

@dataclass
class Article:
    finn_id: int
    title: str

    @classmethod
    def parse(cls, url):
        pass

    @staticmethod
    def testIsWorking(source, expected) -> bool:
        raise NotImplementedError()

    @staticmethod
    def score(scoring_method) -> int:
        raise NotImplementedError()