"""Embedding 接口 - MiniMax API + pgvector 存储

优先使用 MiniMax Embedding API（已有 MINIMAX_API_KEY），
降级到 hash mock。
"""
import os
import hashlib
import json
import logging
from typing import List, Optional

import requests

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_EMBED_DIM = 1024  # MiniMax embo-01 输出 1024 维


def _call_minimax_embed(texts: List[str]) -> Optional[List[List[float]]]:
    """调用 MiniMax Embedding API（embo-01）"""
    api_key = os.environ.get('MINIMAX_API_KEY', '') or os.environ.get('LLM_API_KEY', '')
    if not api_key:
        return None

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        resp = requests.post(
            "https://api.minimaxi.com/v1/embeddings",
            headers=headers,
            json={"model": "embo-01", "input": texts},
            timeout=15,
        )
        if resp.status_code != 200:
            logger.warning(f"MiniMax Embedding API 返回 {resp.status_code}: {resp.text[:100]}")
            return None
        data = resp.json()
        # 按传入顺序排序
        items = sorted(data.get("data", []), key=lambda x: x.get("index", 0))
        return [item["embedding"] for item in items]
    except Exception as e:
        logger.error(f"MiniMax Embedding 调用失败: {e}")
        return None


def _hash_embed(text: str, dim: int = 256) -> List[float]:
    """Hash-based mock embedding - 兜底方案"""
    text = (text or "").strip()
    if not text:
        return [0.0] * dim
    vec = [0.0] * dim
    for i, ch in enumerate(text):
        h = int(hashlib.md5(ch.encode()).hexdigest()[:8], 16)
        idx = h % dim
        weight = 1.0 / (1 + i * 0.1)
        vec[idx] += weight
    norm = sum(v * v for v in vec) ** 0.5
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def embed(text: str) -> Optional[List[float]]:
    """生成单条文本 embedding

    Args:
        text: 输入文本

    Returns:
        List[float] 向量（1024 维），失败时返回 None
    """
    if not text or not text.strip():
        return None

    # 1. MiniMax API
    result = _call_minimax_embed([text])
    if result and len(result) > 0:
        return result[0]

    # 2. Mock 兜底（保不挂）
    logger.info("MiniMax Embedding 不可用，使用 hash mock")
    return _hash_embed(text, dim=_EMBED_DIM)


def embed_batch(texts: List[str]) -> Optional[List[List[float]]]:
    """批量生成 embedding（MiniMax 支持批量）"""
    if not texts:
        return None
    texts = [t.strip() for t in texts if t.strip()]
    if not texts:
        return None

    # 1. MiniMax API 批量
    result = _call_minimax_embed(texts)
    if result and len(result) == len(texts):
        return result

    # 2. 逐个 mock 降级
    logger.info("MiniMax Embedding 批量不可用，逐个使用 hash mock")
    return [_hash_embed(t, dim=_EMBED_DIM) for t in texts]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """余弦相似度"""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def get_embedder_info() -> dict:
    """获取当前 embedder 信息"""
    has_key = bool(os.environ.get('MINIMAX_API_KEY', '') or os.environ.get('LLM_API_KEY', ''))
    return {
        "type": "minimax_api" if has_key else "hash_mock",
        "dim": _EMBED_DIM,
        "api_key_available": has_key,
    }


if __name__ == "__main__":
    info = get_embedder_info()
    print(f"Embedder: {info}")

    texts = ["运输费", "物流费", "计算机", "computer"]
    vecs = [embed(t) for t in texts]
    for t, v in zip(texts, vecs):
        print(f"  {t}: dim={len(v) if v else 0}")

    if vecs[0] and vecs[1]:
        sim = cosine_similarity(vecs[0], vecs[1])
        print(f"\n'运输费' vs '物流费' 相似度: {sim:.3f}")
    if vecs[0] and vecs[2]:
        sim = cosine_similarity(vecs[0], vecs[2])
        print(f"'运输费' vs '计算机' 相似度: {sim:.3f}")
    if vecs[2] and vecs[3]:
        sim = cosine_similarity(vecs[2], vecs[3])
        print(f"'计算机' vs 'computer' 相似度: {sim:.3f}")
