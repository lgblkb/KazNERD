import re
from typing import List

import numpy as np
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from app.utils import tokenizer, model, convert_ids_to_name

app = FastAPI()


class RecognizedEntities(BaseModel):
    word_label_pairs: List[str]


response_example = {
    200: {
        "description": "Return list of (word, label) pairs.",
        "content": {
            "application/json": {
                "examples": {
                    "Example": {
                        "word_label_pairs":
                            [
                                ["Word 1", "Label 1"],
                                ["Word 2", "Label 2"],
                                ["Word ...", "Label ..."],
                                ["Word N", "Label N"],
                            ]

                    }
                }
            }
        }
    },
}


def get_labels(text: str):
    tokenized_inputs = tokenizer(text, return_tensors="pt")
    # Predict
    output = model(**tokenized_inputs)
    predictions = np.argmax(output.logits.detach().numpy(), axis=2)
    labels = convert_ids_to_name(tokenized_inputs, predictions)
    return labels


@app.get("/recognize_entities", response_model=RecognizedEntities, responses=response_example)
def recognize_entities(text: str):
    logger.debug("text: {}", text)
    labels = get_labels(text)

    # # Print tokens and predicted labels
    # if model_name == "roberta":
    #     input_sent_tokens = tokenizer.decode(tokenized_inputs['input_ids'][0], skip_special_tokens=True).split()
    # else:
    input_sent_tokens = re.findall(r"[\w’]+|[-.,#?!)(\]\[;:–—\"«№»/%&']", text)
    assert len(input_sent_tokens) == len(labels), "Mismatch between input token and label sizes!"

    return dict(word_label_pairs=list(zip(input_sent_tokens, labels)))
