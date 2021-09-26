import hashlib
from typing import List

import aioredis
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

from mutants.dna import identify


class Dna(BaseModel):
    dna: List


app = FastAPI()
redis = aioredis.from_url("redis://redis", decode_responses=True)
# redis = aioredis.from_url("redis://1.1.1.1", decode_responses=True)


@app.post("/mutant")
async def identify_mutant(dna: Dna, response: Response):
    dna_string = ''.join(dna.dna)
    dna_hash = hashlib.sha1(dna_string.encode()).hexdigest()
    dna_info = await redis.hgetall(dna_hash)

    if not dna_info:
        is_mutant = identify(dna.dna)
        pipeline = await redis.pipeline()
        if is_mutant:
            await pipeline.incr('count_mutant_dna')
        else:
            await pipeline.incr('count_human_dna')
        await pipeline.hset(dna_hash, 'dna', dna_string)
        await pipeline.hset(dna_hash, 'is_mutant', str(is_mutant))
        await pipeline.execute()
    else:
        is_mutant = False if dna_info['is_mutant'].lower() == "false" else True

    response.status_code = status.HTTP_200_OK if is_mutant else status.HTTP_403_FORBIDDEN
    return {"is_mutant": is_mutant}


@app.get("/stats")
async def dna_count():
    count_mutant_dna = await redis.get('count_mutant_dna')
    if not count_mutant_dna or count_mutant_dna == '0':
        count_mutant_dna = 0
    count_mutant_dna = int(count_mutant_dna)

    count_human_dna = await redis.get('count_human_dna')
    if not count_human_dna or count_human_dna == '0':
        count_human_dna = 0
    count_human_dna = int(count_human_dna)

    ratio = 0 if not count_human_dna or not count_mutant_dna else round(count_mutant_dna / count_human_dna, 2)

    return {"count_human_dna": count_human_dna, "count_mutant_dna": count_mutant_dna, "ratio": ratio}
