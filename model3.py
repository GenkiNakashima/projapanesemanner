import pandas as pd
from transformers import AlbertTokenizer, AlbertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator

# ALBERTモデルのトークナイザーとモデルのロード
tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
model = AlbertModel.from_pretrained('albert-base-v2')

# CSVファイルのパス
csv_file_path = 'japanesemanners2.csv'

# 読み込む列の名前を指定
target_column_name = 'ルル'

# CSVファイルをDataFrameとして読み込む
data = pd.read_csv(csv_file_path)

def calculate_similarity2(text):
    # 入力テキストをトークン化してエンコード
    # translator = Translator()

    # text_ja=text

    # text_en = translator.translate(text_ja, src='ja', dest='en').text

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    text_embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze().numpy()

    # CSVファイル内の全ての行の文章との類似度を計算
    cosine_scores = []

    for _, row in data.iterrows():
        # 文章をトークン化してエンコード
        row_inputs = tokenizer(row[target_column_name], return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            row_outputs = model(**row_inputs)
        row_embedding = torch.mean(row_outputs.last_hidden_state, dim=1).squeeze().numpy()

        # コサイン類似度の計算
        similarity_score = cosine_similarity([text_embedding], [row_embedding])[0][0]
        cosine_scores.append(similarity_score)

    # 最も類似度の高いインデックスを見つける
    max_index = cosine_scores.index(max(cosine_scores))
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

    return result,data.iloc[max_index,1],data.iloc[max_index,3]

# # テスト用のテキスト
# test_text = input()

# # 類似度の計算
# most_similar_rule_index, most_similar_rule,max_result= calculate_similarity2(test_text)
# print("最も類似度の高いルールのインデックス:", most_similar_rule_index)
# print("最も類似度の高いルール:", most_similar_rule)
# print("適切度:", max_result)
# print("アドバイス:", data.iloc[most_similar_rule_index,1])
