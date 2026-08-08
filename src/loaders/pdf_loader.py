from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document


def load_pdfs(docs_path: str = "docs") -> list[Document]:
    """
    Carrega todos os arquivos PDF da pasta de documentos.

    Retorna uma lista de Documents contendo:
    - conteúdo textual da página;
    - nome do arquivo;
    - número da página.
    """

    documents = []
    docs_directory = Path(docs_path)

    pdf_files = sorted(docs_directory.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"Nenhum arquivo PDF encontrado em: {docs_directory.resolve()}"
        )

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                documents.append(
                    Document(
                        page_content=text.strip(),
                        metadata={
                            "source": pdf_file.name,
                            "page": page_number,
                        },
                    )
                )

    return documents