from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import ctranslate2
def tranlate_fr_en(query1):
    translator = ctranslate2.Translator("opus-mt-fr-en")
    tokenizer = transformers.AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")

    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(query1))
    results = translator.translate_batch([source])
    target = results[0].hypotheses[0]

    query=tokenizer.decode(tokenizer.convert_tokens_to_ids(target))
    return query
def tranlate_en_fr(query1):
    translator = ctranslate2.Translator("opus-mt-en-fr")
    tokenizer = transformers.AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")

    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(query1))
    results = translator.translate_batch([source])
    target = results[0].hypotheses[0]

    query=tokenizer.decode(tokenizer.convert_tokens_to_ids(target))
    return query