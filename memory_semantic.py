"""Explicit, digest-bound embeddings from a local Ollama runtime."""

import http.client
import json
import math
import re


class EmbeddingError(ValueError):
    pass


def bounded_vector(value):
    if (not isinstance(value, list) or not 1 <= len(value) <= 4096
            or any(type(x) not in (float, int) or not -1e10 <= x <= 1e10 for x in value)):
        raise EmbeddingError('invalid-local-embedding')
    if not any(value):
        raise EmbeddingError('empty-local-embedding')
    return value


def cosine(left, right):
    if len(left) != len(right):
        raise EmbeddingError('local-embedding-dimensions-changed')
    return math.fsum(a * b for a, b in zip(left, right)) / (math.hypot(*left) * math.hypot(*right))


class Ollama:
    def __init__(self, port, model, digest):
        if (type(port) is not int or not 1024 <= port <= 65535
                or not isinstance(model, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}:[a-zA-Z0-9._-]{1,40}', model)
                or 'cloud' in model.casefold()
                or not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest)):
            raise EmbeddingError('choose-a-local-model-and-full-digest')
        self.port = port
        self.model = model
        self.digest = digest
        self.settings = {'port': port, 'model': model, 'digest': digest}

    @classmethod
    def from_settings(cls, settings):
        if not isinstance(settings, dict) or set(settings) != {'port', 'model', 'digest'}:
            raise EmbeddingError('invalid-local-semantic-settings')
        return cls(**settings)

    def request(self, path, value=None):
        # An explicit loopback socket avoids remote endpoints, proxies and redirects.
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=45)
        try:
            if value is None:
                conn.request('GET', path)
            else:
                conn.request('POST', path, json.dumps(value), {'Content-Type': 'application/json'})
            response = conn.getresponse()
            if response.status != 200:
                raise EmbeddingError('local-embedding-service-refused')
            payload = response.read(4_000_001)
            if len(payload) > 4_000_000:
                raise EmbeddingError('local-embedding-response-too-large')
            result = json.loads(payload)
            if not isinstance(result, dict):
                raise EmbeddingError('invalid-local-embedding-response')
            return result
        except EmbeddingError:
            raise
        except (OSError, ValueError, http.client.HTTPException) as error:
            raise EmbeddingError('local-embedding-service-unavailable') from error
        finally:
            conn.close()

    def verify(self):
        rows = self.request('/api/tags').get('models')
        if not isinstance(rows, list):
            raise EmbeddingError('invalid-local-model-list')
        for row in rows:
            if not isinstance(row, dict) or row.get('name') != self.model or row.get('digest') != self.digest:
                continue
            details = row.get('details')
            if isinstance(details, dict) and details.get('format') == 'gguf' and not (row.get('remote_host') or row.get('remote_model')):
                return
        raise EmbeddingError('local-model-missing-or-changed')

    def embed(self, texts):
        self.verify()
        result = self.request('/api/embed', {'model': self.model, 'input': texts, 'truncate': False})
        rows = result.get('embeddings')
        if (result.get('model') != self.model or not isinstance(rows, list) or len(rows) != len(texts)):
            raise EmbeddingError('invalid-local-embedding-response')
        self.verify()
        return [bounded_vector(vector) for vector in rows]
