"""DashScope embedder using Alibaba's text-embedding models.

DashScope provides multilingual embedding models including strong Chinese support
via text-embedding-v3.
"""

"""DashScope embedder using Alibaba's text-embedding models.

DashScope provides multilingual embedding models including strong Chinese support
via text-embedding-v3.
"""

import os
from typing import List, Optional

import numpy as np
from openai import OpenAI

from tau2.knowledge.embedders.base import BaseEmbedder

# DashScope limits batch size to 10 texts per request.
_MAX_BATCH_SIZE = 10


class DashScopeEmbedder(BaseEmbedder):
    """Embedder using DashScope's text-embedding models.

    Supported models:
        - text-embedding-v3 (multilingual, 1024 dimensions)
        - text-embedding-v2 (multilingual, 1536 dimensions)
    """

    SUPPORTED_MODELS = {
        "text-embedding-v3": {"dimension": 1024},
        "text-embedding-v2": {"dimension": 1536},
    }

    def __init__(
        self,
        model: str = "text-embedding-v3",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        dimensions: Optional[int] = None,
    ):
        self.model = model
        self.dimensions = dimensions or self.SUPPORTED_MODELS.get(model, {}).get(
            "dimension"
        )

        self.client = OpenAI(
            api_key=api_key or os.getenv("DASHSCOPE_API_KEY", os.getenv("OPENAI_API_KEY")),
            base_url=base_url or os.getenv(
                "DASHSCOPE_API_BASE",
                "https://dashscope.aliyuncs.com/compatible-mode/v1",
            ),
        )

    def embed(self, texts: List[str]) -> np.ndarray:
        if not texts:
            raise ValueError("No text to embed.")

        all_embeddings: List[np.ndarray] = []
        for i in range(0, len(texts), _MAX_BATCH_SIZE):
            batch = texts[i : i + _MAX_BATCH_SIZE]
            kwargs = {"input": batch, "model": self.model}
            if self.dimensions and self.model == "text-embedding-v3":
                kwargs["dimensions"] = self.dimensions

            response = self.client.embeddings.create(**kwargs)
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.append(np.array(batch_embeddings))

        return np.concatenate(all_embeddings, axis=0)

    def get_name(self) -> str:
        return f"dashscope_{self.model}"

    def get_dimension(self) -> Optional[int]:
        return self.dimensions
