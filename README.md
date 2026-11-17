# 役割分担
- 平山
Update,Delete
- marin-412
Read,List
- Tsuruhana0819
Create

## データ構造
``` SQL
assignment{
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 課題識別用のidとりあえずは連番
    lectureName TEXT NOT NULL, -- 講義名
    taskName TEXT NOT NULL, -- 課題名
    deadLine TEXT NOT NULL, -- 締め切り "yyyy/mm/dd/hh/mm"など
    memo TEXT, -- 課題関連のメモ
    classification TEXT NOT NULL, -- 講義の分類 必修、選択必修、一般教養、教職、その他など
    isSubmitted BOOLEAN, -- 提出済かどうか
    createdAt TEXT NOT NULL -- 作成日時
}
```
## 希望などがあればここに追記してdevにREADME.mdだけpushしてください
- 出来れば機能ごとにブランチ分けてdevにプルリク出してほしいです。 (平山)