-- 課題のデータ構造のイメージ
    -- id : string, //UUID
    -- lecutureName : string, //講義名
    -- taskName : string, //課題名
    -- deadline : string, //締め切り日時(yyyymmddhhmmss)
    -- memo : string, //メモ
    -- classification : '必修'|'選択必修'|'一般教養'|'その他', //科目区分
    -- isSubmitted : true|false, //提出したか否か
    -- createdAt : string, //作成日時
CREATE TABLE IF NOT EXISTS task(
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 課題識別用のidとりあえずは連番
    lectureName TEXT NOT NULL, -- 講義名
    taskName TEXT NOT NULL, -- 課題名
    deadLine TEXT NOT NULL, -- 締め切り "yyyy/mm/dd/hh/mm"など
    memo TEXT, -- 課題関連のメモ
    classification TEXT NOT NULL, -- 講義の分類 必修、選択必修、一般教養、教職、その他など
    isSubmitted BOOLEAN, -- 提出済かどうか
    createdAt TEXT NOT NULL -- 作成日時
)