from nomic import embed
import numpy as np

from nomic import embed

clouds = embed.text(
    texts=['It is very cloudy today.'],
    model='nomic-embed-text-v1',
    task_type='search_document'
)



print(output)
