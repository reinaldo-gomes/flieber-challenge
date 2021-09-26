import fakeredis.aioredis
import nest_asyncio
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from mutants.api import app

nest_asyncio.apply()

client = TestClient(app)
redis = fakeredis.aioredis.FakeRedis(decode_responses=True)


@pytest.mark.asyncio
@patch('mutants.api.redis', redis)
@pytest.mark.parametrize(
    'dna, expected_status, is_mutant, dna_hash',
    [(["mock_dna1"], 403, False, ''),
     (["mock_dna2"], 200, True, ''),
     (["mock_dna3"], 200, True, '7ab3bb121b21e009594e7ba4db7ebac517cebf9c')]
)
async def test_identify_mutant(mocker, dna, expected_status, is_mutant, dna_hash):
    mocker.patch('mutants.api.identify', return_value=is_mutant)
    await redis.hset(dna_hash, 'dna', 'dna_string')
    await redis.hset(dna_hash, 'is_mutant', str(is_mutant))

    response = client.post("/mutant", json={"dna": dna})

    assert response.status_code == expected_status
    assert response.json() == {"is_mutant": is_mutant}


@pytest.mark.asyncio
@patch('mutants.api.redis', redis)
@pytest.mark.parametrize(
    'count_mutant_dna, count_human_dna, expected_json',
    [(0, 0, {"count_human_dna": 0, "count_mutant_dna": 0, "ratio": 0}),
     (0, 1, {"count_human_dna": 1, "count_mutant_dna": 0, "ratio": 0}),
     (1, 0, {"count_human_dna": 0, "count_mutant_dna": 1, "ratio": 0}),
     (1, 1, {"count_human_dna": 1, "count_mutant_dna": 1, "ratio": 1.0})]
)
async def test_dna_count(count_mutant_dna, count_human_dna, expected_json):
    await redis.set('count_mutant_dna', int(count_mutant_dna))
    await redis.set('count_human_dna', int(count_human_dna))

    response = client.get("/stats")

    assert response.json() == expected_json
