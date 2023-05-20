import logging
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.utils import clean_wiki_text, convert_files_to_docs


logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.INFO)
log = logging.getLogger("pipeline")

doc_dir = '/Users/sstefanova/repos/wikitechsearch/output-plain'

log.info("Initializing ")
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")

docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
document_store.write_documents(docs)

retriever = EmbeddingRetriever(
    document_store=document_store, embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1")

document_store.update_embeddings(retriever)

document_store.save(index_path="../NLP_resources/embeddings/multi-qa-mpnet-base-dot-v1.faiss", config_path="../NLP_resources/embeddings/my_config.json")
