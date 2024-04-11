import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util


# CSVファイルのパス
csv_file_path = 'japanesemanners.csv'

# 読み込む列の名前を指定
target_column_name = 'ルール'

# CSVファイルをDataFrameとして読み込む
data = pd.read_csv(csv_file_path)

# BERTモデルのロード
model = SentenceTransformer('bert-base-nli-mean-tokens')

def calculate_similarity1(text):
 

    # コサイン類似度を保存するリスト
    cosine_scores = []

    # CSVファイル内の全ての行の文章との類似度を計算
    for idx, row in data.iterrows():
        # 文章をベクトルに変換
        embeddings1 = model.encode(text, convert_to_tensor=True)
        embeddings2 = model.encode(row[target_column_name], convert_to_tensor=True)

        # コサイン類似度の計算
        cosine_score = util.pytorch_cos_sim(embeddings1, embeddings2)[0][0]
        cosine_scores.append(cosine_score)

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
    
    return result,data.iloc[max_index,1]

# # テスト用のテキスト
# test_text = input()

# # 類似度の計算
# most_similar_rule_index, most_similar_rule,max_result = calculate_similarity1(test_text)

# print("マナー:", test_text)
# #print("最も類似度の高いルールのインデックス:", most_similar_rule_index)
# #print("該当するルール:", most_similar_rule)
# print("適切度:", max_result)
# print("アドバイス:", data.iloc[most_similar_rule_index,1])
