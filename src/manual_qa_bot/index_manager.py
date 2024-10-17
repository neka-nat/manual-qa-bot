from pathlib import Path

from byaldi import RAGMultiModalModel


class IndexManager:
    def __init__(self, index_root: str = ".byaldi") -> None:
        self.index_root = Path(index_root)

    def list_indexes(self) -> list[str]:
        return [index.name for index in self.index_root.glob("*") if index.is_dir()]

    def index_exists(self, index_name: str) -> bool:
        return (self.index_root / index_name).exists()

    def get_file_list(self, path: str) -> list[Path]:
        return list(Path(path).iterdir())

    def create_index(
        self, index_name: str, input_path: str = "data/", overwrite: bool = True
    ) -> RAGMultiModalModel:
        if self.index_exists(index_name):
            return RAGMultiModalModel.from_index(index_name)
        file_list = self.get_file_list(input_path)
        rag = RAGMultiModalModel.from_pretrained("vidore/colqwen2-v0.1")
        rag.index(
            input_path=input_path,
            index_name=index_name,
            metadata=[[{"file_path": str(file_path)} for file_path in file_list]],
            overwrite=overwrite,
        )
        return rag
