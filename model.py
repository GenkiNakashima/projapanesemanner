import pandas as pd
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize

# CSVファイルのパス
csv_file_path = 'japanesemanners.csv'

# 読み込む列の名前を指定
target_column_name = 'ルール'

# CSVファイルをDataFrameとして読み込む
data = pd.read_csv(csv_file_path)

# 文章のトークン化とタグ付け
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data[target_column_name])]

# Doc2Vecモデルの学習
model = Doc2Vec(tagged_data, vector_size=110, window=6, min_count=1, epochs=110)

def calculate_similarity(text):
    # 入力テキストをトークン化
    tokenized_text = word_tokenize(text.lower())

    # ベクトルの取得
    vector = model.infer_vector(tokenized_text)

    # 類似度の計算
    similarities = model.docvecs.most_similar([vector], topn=1)

    # 最も類似度の高い文書のインデックスを取得
    max_index = int(similarities[0][0])
    max_rule = data.loc[max_index, target_column_name]
    
    if max_index >= 1 and max_index <= 111:
        result = "適切です"
    elif max_index >= 112 and max_index <= 216:
        result = "やや適切です"
    elif max_index >= 217 and max_index <= 322:
        result = "やや不適切です"
    elif max_index >= 323:
        result = "不適切です"        
    else:
        result = "範囲外です"
    
    return max_index, max_rule,result

# テスト用のテキスト
test_text = input()

# 類似度の計算
most_similar_rule_index, most_similar_rule,max_result = calculate_similarity(test_text)

print("マナー:", test_text)
#print("最も類似度の高いルールのインデックス:", most_similar_rule_index)
#print("該当するルール:", most_similar_rule)
print("適切度:", max_result)
print("アドバイス:", data.iloc[most_similar_rule_index,1])
