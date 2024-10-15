from pathlib import Path

from byaldi import RAGMultiModalModel


class IndexManager:
    def __init__(self, index_root: str = ".byaldi") -> None:
        self.index_root = Path(index_root)

    def list_indexes(self) -> list[str]:
        return [index.name for index in self.index_root.glob("*") if index.is_dir()]

    def index_exists(self, index_name: str) -> bool:
        return (self.index_root / index_name).exists()

    def create_index(
        self, index_name: str, input_path: str = "data/", overwrite: bool = True
    ) -> RAGMultiModalModel:
        if self.index_exists(index_name):
            return RAGMultiModalModel.from_index(index_name)
        return RAGMultiModalModel.from_pretrained("vidore/colqwen2-v0.1").index(
            input_path=input_path,
            index_name=index_name,
            overwrite=overwrite,
        )
