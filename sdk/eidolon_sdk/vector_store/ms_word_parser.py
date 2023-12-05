from typing import Sequence

from eidolon_sdk.vector_store.base_parser import BaseParser, DataBlob
from eidolon_sdk.vector_store.document import Document


class MsWordParser(BaseParser):
    def parse(self, blob: DataBlob) -> Sequence[Document]:
        try:
            from unstructured.partition.doc import partition_doc
            from unstructured.partition.docx import partition_docx
        except ImportError as e:
            raise ImportError(
                "Could not import unstructured, please install with `pip install "
                "unstructured`."
            ) from e

        mime_type_parser = {
            "application/msword": partition_doc,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": (
                partition_docx
            ),
        }
        if blob.mimetype not in (
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ):
            raise ValueError("This blob type is not supported for this parser.")
        with blob.as_bytes_io() as word_document:
            elements = mime_type_parser[blob.mimetype](file=word_document)
            text = "\n\n".join([str(el) for el in elements])
            metadata = {"source": blob.source}
            yield Document(page_content=text, metadata=metadata)