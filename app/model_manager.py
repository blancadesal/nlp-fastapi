import logging
# import pickle

# import mwparserfromhell
# from annoy import AnnoyIndex
# from mwedittypes.utils import wikitext_to_plaintext
# from sentence_transformers import SentenceTransformer
# from transformers import pipeline
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline


from app.config import settings


log = logging.getLogger("uvicorn")


class ModelManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        emb_model_name="sentence-transformers/all-mpnet-base-v2",
        qa_model_name="deepset/tinyroberta-squad2",
        emb_dir=settings.emb_dir,
    ):
        if not hasattr(self, "initialized"):
            self.index_path = "/code/app/all-mpnet-base-v2.faiss"
            self.config_path = "/code/app/all-mpnet-base-v2.json"
            self.emb_model_name = emb_model_name
            self.qa_model_name = qa_model_name
            self.document_store = FAISSDocumentStore(faiss_index_path=self.index_path, faiss_config_path=self.config_path)
            self.retriever=EmbeddingRetriever(document_store=self.document_store, embedding_model=self.emb_model_name)
            self.reader = FARMReader(model_name_or_path=self.qa_model_name, use_gpu=False)
            self.pipe = ExtractiveQAPipeline(self.reader, self.retriever)
            self.initialized = True


    def get_model_info(self):
        return {"q&a": self.qa_model_name, "emb": self.emb_model_name}

    def get_result(self, query, num_results=5):
        results = []
        prediction = self.pipe.run(
            query=query, params={"Retriever": {"top_k": num_results*2},
                                "Reader": {"top_k": num_results}}
        )
        try:
            answer = prediction['answers'][0].answer  # take first answer
        except Exception:
            answer = None

        for a in prediction['answers']:
            results.append({
                'title':a.meta['section_title'],
                'score':a.score,
                'text':self.document_store.get_document_by_id(a.document_ids[0]).content})

        return {'query': query, 'search_results':results, 'answer':answer}


def get_model_manager():
    return ModelManager()
