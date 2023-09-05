import os
from pathlib import Path

from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForTokenClassification, PreTrainedTokenizerFast

from settings import settings

load_dotenv()
# storage_path = Path(os.environ['STORAGE_DIR'])
# assert storage_path.exists()

model_checkpoint_path = settings.storage_folder / 'bert-base-multilingual-cased-finetuned-ner-9,10,11,13,14' / 'checkpoint-1128'
assert model_checkpoint_path.exists()

# Tokenize input sentence for BERT
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint_path)
assert isinstance(tokenizer, PreTrainedTokenizerFast)

# Load model
model = AutoModelForTokenClassification.from_pretrained(model_checkpoint_path)

labels_info = {0: "O", 1: "B-ADAGE", 2: "I-ADAGE", 3: "B-ART", 4: "I-ART", 5: "B-CARDINAL",
               6: "I-CARDINAL", 7: "B-CONTACT", 8: "I-CONTACT", 9: "B-DATE", 10: "I-DATE", 11: "B-DISEASE",
               12: "I-DISEASE", 13: "B-EVENT", 14: "I-EVENT", 15: "B-FACILITY", 16: "I-FACILITY",
               17: "B-GPE", 18: "I-GPE", 19: "B-LANGUAGE", 20: "I-LANGUAGE", 21: "B-LAW", 22: "I-LAW",
               23: "B-LOCATION", 24: "I-LOCATION", 25: "B-MISCELLANEOUS", 26: "I-MISCELLANEOUS",
               27: "B-MONEY", 28: "I-MONEY", 29: "B-NON_HUMAN", 30: "I-NON_HUMAN", 31: "B-NORP",
               32: "I-NORP", 33: "B-ORDINAL", 34: "I-ORDINAL", 35: "B-ORGANISATION", 36: "I-ORGANISATION",
               37: "B-PERCENTAGE", 38: "I-PERCENTAGE", 39: "B-PERSON", 40: "I-PERSON", 41: "B-POSITION",
               42: "I-POSITION", 43: "B-PRODUCT", 44: "I-PRODUCT", 45: "B-PROJECT", 46: "I-PROJECT",
               47: "B-QUANTITY", 48: "I-QUANTITY", 49: "B-TIME", 50: "I-TIME"}


def convert_ids_to_name(tokenized_inputs, predictions):
    # Convert label IDs to label names
    word_ids = tokenized_inputs.word_ids(batch_index=0)
    previous_word_idx = None
    labels = []
    for i, p in zip(word_ids, predictions[0]):
        # Special tokens have a word id that is None. We set the label to -100 so they are
        # automatically ignored in the loss function.
        if i is None or i == previous_word_idx:
            continue
        elif i != previous_word_idx:
            labels.append(labels_info[p])
        previous_word_idx = i
    return labels
