import re
from app.main import get_labels


def main():
    text = 'Қалпына келтіру жұмыстары жазушы Мұхтар Әуезовтің 125 жылдық мерейтойына орайластырылған. Шыңғыстаудағы ' \
           'кесене алғаш рет 60 жыл бұрын жөнделген. Осы жолы да зираттың ауласы абаттандырылып, қос ғашыққа арналған ' \
           'ескерткішке қалпына келтіру жұмыстары жүргізілді. Сондай-ақ жүрек формасындағы арт кескіндеме орнатылды. ' \
           'Нысанның ашылу рәсіміне келген көпшілік назарына театрландырылған көрініс ұсынылды. '
    text = 'Сондай-ақ жүрек формасындағы арт кескіндеме орнатылды.'
    labels = get_labels(text)
    print(labels)
    input_sent_tokens = re.findall(r"[\w’]+|[-.,#?!)(\]\[;:–—\"«№»/%&']", text)
    print(input_sent_tokens)
    assert len(input_sent_tokens) == len(
        labels), f"Mismatch between input token and label sizes! {len(input_sent_tokens)} and {len(labels)}"
    out = dict(word_label_pairs=list(zip(input_sent_tokens, labels)))
    print(out)
    pass


if __name__ == '__main__':
    main()
