import cv2
import numpy as np

# 画像の読み込み
image_path = 'bakery.png'
image = cv2.imread(image_path)

# グレースケール化
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二値化 (閾値は適切に調整)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# 輪郭検出
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 一定面積以下の輪郭を除去 (ノイズ除去)
contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]  # 面積500以上の輪郭のみ

# 輪郭を囲む矩形を取得
bounding_rects = [cv2.boundingRect(cnt) for cnt in contours]

icons = []

for i, rect in enumerate(bounding_rects):
    x, y, w, h = rect
    icon = image[y:y+h, x:x+w]  # アイコン部分を切り出し
    icons.append(icon)

templates = {
    'rabbit': cv2.imread('rabbit.png'),
    'dog': cv2.imread('dog.png'),
    'frog': cv2.imread('frog.png'),
    'risu': cv2.imread('risu.png')
}

results = []
for i, icon in enumerate(icons):
    max_val = 0
    matched_animal = None
    icon = cv2.resize(icon, (100, 100)) 
    for animal, template in templates.items():
        res = cv2.matchTemplate(icon, template, cv2.TM_CCOEFF_NORMED)
        _, max_val_temp, _, _ = cv2.minMaxLoc(res)
        if max_val_temp > max_val:
            max_val = max_val_temp
            matched_animal = animal
    results.append(matched_animal)

# 検出されたアイコンの情報をリストにまとめる
icon_data = []
for i, rect in enumerate(bounding_rects):
    x, y, w, h = rect
    icon = image[y:y+h, x:x+w]
    icon_data.append((x, y, w, h, icon, results[i]))  # 座標、アイコン画像、動物名

# y座標の誤差50px以内のグループごとに配列を作成
sorted_icon_data = []
current_group = []
current_y = icon_data[0][1]  # 最初のアイコンのy座標

for data in icon_data:
    x, y, w, h, icon, animal = data
    if abs(y - current_y) <= 50:  # 誤差50px以内なら同じグループに追加
        current_group.append(data)
    else:  # 新しいグループを作成
        current_group.sort(key=lambda item: item[0])  # x座標でソート
        sorted_icon_data.extend(current_group)
        current_group = [data]
        current_y = y

# 最後のグループも追加
current_group.sort(key=lambda item: item[0])
sorted_icon_data.extend(current_group)

# ソート後の情報をそれぞれのリストに戻す
bounding_rects = [item[:4] for item in sorted_icon_data]
icons = [item[4] for item in sorted_icon_data]
results = [item[5] for item in sorted_icon_data]
for i, rect in enumerate(bounding_rects):
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)  # 矩形を描画
    cv2.putText(image, results[i] + str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)  # 動物名を描画


# パズル探索

# def find_best_move(board, rows, cols):
#     best_move = None
#     max_score = -1

#     for i in range(rows * cols):
#         x, y = i % cols, i // cols

#         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < cols and 0 <= ny < rows:
#                 new_board = swap(board, x, y, nx, ny)
#                 score,chaincounts = evaluate_board(new_board, rows, cols)
#                 if score > max_score:
#                     max_score = score
#                     best_move = (x, y, nx, ny)
#                     print(best_move, score, chaincounts)

#     return best_move

# def swap(board, x1, y1, x2, y2):
#     new_board = copy.deepcopy(board)
#     new_board[y1 * cols + x1], new_board[y2 * cols + x2] = new_board[y2 * cols + x2], new_board[y1 * cols + x1]
#     return new_board

# def evaluate_board(board, rows, cols):
#     score = 0
#     chain_counts = {}  # 各動物の連鎖数を記録

#     # 横方向の連鎖をチェック
#     for y in range(1,rows):
#         count = 1
#         current_animal = board[y * cols]
#         for x in range(1, cols):
#             if board[y * cols + x] == current_animal:
#                 count += 1
#             else:
#                 count = 1
#                 current_animal = board[y * cols + x]
#         chain_counts[current_animal] = chain_counts.get(current_animal, 0) + count

#     # 縦方向の連鎖をチェック (横方向と同様)
#     for x in range(1,cols):
#         count = 1
#         current_animal = board[x]
#         for y in range(0, rows):
#             if board[y * cols + x] == current_animal:
#                 count += 1
#             else:
#                 count = 1
#                 current_animal = board[y * cols + x]
#         chain_counts[current_animal] = chain_counts.get(current_animal, 0) + count

#     # 4つ以上の連鎖にボーナス
#     for animal, count in chain_counts.items():
#         if count >= 4:
#             score += count + 3
#         elif count >= 3:
#             score += count
#     return score, chain_counts

# # 盤面情報
# rows = 7
# cols = 6
# board = results

# # 最適な手を探索
# best_move = find_best_move(board, rows, cols)
# 結果画像の表示
resized_image = cv2.resize(image, (500, 650)) 
cv2.imshow('Result', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()