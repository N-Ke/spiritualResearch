# 音声設計ドキュメント — ElevenLabs

## 使用可能モデル一覧（2026年2月時点）

| モデル | model_id | 言語数 | 特徴 | コスト | 推奨用途 |
|--------|----------|--------|------|--------|---------|
| **★ Eleven v3** | `eleven_v3` | 74言語 | **最新・最高品質**。Audio Tags対応で感情制御可能 | 高 | メイン採用。セリフ・ナレーション全般 |
| Multilingual v2 | `eleven_multilingual_v2` | 29言語 | 安定・高品質。従来のフラッグシップ | 中 | v3がうまくいかない場合のフォールバック |
| Turbo v2.5 | `eleven_turbo_v2_5` | 32言語 | 高品質×低遅延のバランス | 低 | テスト・プレビュー用 |
| Flash v2.5 | `eleven_flash_v2_5` | 32言語 | 75ms以下の超低遅延 | 最低 | リアルタイム用（今回は不要） |

### 採用モデル: **Eleven v3** (`eleven_v3`)

v3を採用する最大の理由は **Audio Tags（感情タグ）** が使えること。

---

## ★ Audio Tags（v3限定の感情制御機能）

v3モデルでは、テキスト内に `[タグ]` を埋め込むことで **声の感情・演技指示** ができる。
これは従来のStability/Style数値調整よりも **はるかに直感的かつ強力**。

### タグ一覧

#### 感情タグ
| タグ | 効果 | 使用例 |
|------|------|--------|
| `[sad]` | 悲しい | `[sad] もう…戻れないのか` |
| `[angry]` | 怒り | `[angry] ふざけんなっ！` |
| `[happily]` | 嬉しい | `[happily] うめぇ！` |
| `[excited]` | 興奮 | `[excited] これだ、この味だ！` |
| `[nervous]` | 緊張 | `[nervous] 俺は…ここにいていいのか` |
| `[frustrated]` | 苛立ち | `[frustrated] なんで分かんねぇんだ` |
| `[sorrowful]` | 哀愁 | `[sorrowful] 5つの時から、ずっとそうだった` |

#### 話し方タグ
| タグ | 効果 | 使用例 |
|------|------|--------|
| `[whispers]` | 囁き | `[whispers] なあ、ンバボ…俺、ここでやっていけるかな` |
| `[shouts]` | 叫び | `[shouts] 逃げろ！` |
| `[quietly]` | 静かに | `[quietly] ありがとう` |
| `[loudly]` | 大声 | `[loudly] いらっしゃい！` |

#### 人間的な反応タグ
| タグ | 効果 | 使用例 |
|------|------|--------|
| `[laughs]` | 笑い | `[laughs] なんだそりゃ` |
| `[sighs]` | ため息 | `[sighs] しょうがねぇな` |
| `[gasps]` | 驚き（息を呑む） | `[gasps] お前…ンバボか？` |
| `[clears throat]` | 咳払い | `[clears throat] えー、本日のメニューは…` |
| `[gulps]` | ゴクリ | `[gulps] あの子…俺に近づいてくる` |

#### テンポ・リズムタグ
| タグ | 効果 | 使用例 |
|------|------|--------|
| `[pauses]` | 間を置く | `俺は [pauses] 料理人だ` |
| `[stammers]` | どもり | `[stammers] お、俺は…その…` |
| `[rushed]` | 早口 | `[rushed] やべぇやべぇやべぇ` |
| `[hesitates]` | 躊躇 | `[hesitates] ここに…いてもいいか？` |

### タグの組み合わせ例

```
[nervous] 俺は…[pauses] [quietly] ここにいていいのか。
[sighs] [sad] 5つの時からずっとだ。「怖い」って言われてきた。
[gasps] お前… [pauses] [whispers] ンバボ…？ お前もここに来たのか…？
[excited] [loudly] うめぇぇぇ！！ なんだこれは！！
```

---

## キャラクター別音声割り振り

### ナレーション（イッテQ風・第三者視点）

#### 設計思想

ナレーターは「1.9」的な声質 — 深く温かいバリトンで、
ドキュメンタリーの信頼感とバラエティの遊び心を兼ね備える。
愛情を込めていじりつつ、感動シーンでは黙ることで効果を最大化。
「笑いと感動の橋渡し」が最大の役割。

#### ★ カスタムボイス生成済み（Voice Design v3）— 3パターン×3候補＝計9候補

| 項目 | 設定 |
|------|------|
| **モデル** | `eleven_v3` |
| **キャラ** | 温かくいじる大人の視点。笑いと感動の橋渡し |
| **声質目標** | 深い東京弁男声。バリトン。自然な笑いの含み。明瞭な滑舌 |
| **フォールバック** | Ishibashi `Mv8AjrYZCBkdsmDHNwcB`（既成ボイス） |

##### パターンA：温かいドキュメンタリー（石橋系）★推奨メイン

| 項目 | 設定 |
|------|------|
| **コンセプト** | 愛情込めていじるが、リスペクトを忘れないプロナレーター |
| **生成プロンプト** | "Deep baritone, rich warm resonance, mature middle-aged, natural to slightly fast pace, perfect articulation, serious documentary to playful humor seamlessly, natural warmth and wit, skilled TV narrator who lovingly teases" |
| **候補1 voice_id** | `zNvHFDRX9PmWUpzbYkzQ` |
| **候補2 voice_id** | `XM3Eh2OHD9Dv36piOhgZ` |
| **候補3 voice_id** | `oeDD6p4BbB1theqS5Alg` |
| **プレビュー音声** | `narrator_voice_A_1.mp3` / `_A_2.mp3` / `_A_3.mp3` |

| パラメータ | 値 | 対応 |
|-----------|-----|------|
| Stability | 0.55 | シリアス↔コミカルの切替に必要な柔軟性 |
| Similarity | 0.80 | 声質の一貫性 |
| Style | 0.30 | 自然な語り口のクセ（いじり感） |
| Speed | 1.05 | やや速め（テンポよく語る） |
| **使用シーン** | ギャグ、ツッコミ、日常の状況説明、次回予告 |

##### パターンB：語り部（Uncle storyteller）

| 項目 | 設定 |
|------|------|
| **コンセプト** | お気に入りのおじさんが信じられない話をしてくれる |
| **生成プロンプト** | "Mid-to-low baritone, smooth engaging, storytelling quality, natural rhythm that draws listeners in, built-in humor, serious things amusing and funny things profound, excellent dynamic range, alive and reactive, like favorite uncle telling incredible story" |
| **候補1 voice_id** | `bLEEUxXNsq7IAteXnaRh` |
| **候補2 voice_id** | `7lOC03TCHsHXVc6OjnAW` |
| **候補3 voice_id** | `L4Ij9rtEnxu1fMtnKFUQ` |
| **プレビュー音声** | `narrator_voice_B_1.mp3` / `_B_2.mp3` / `_B_3.mp3` |

| パラメータ | 値 | 対応 |
|-----------|-----|------|
| Stability | 0.50 | 語りのダイナミクス（引き込む力） |
| Similarity | 0.80 | 同一 |
| Style | 0.35 | 語り部の個性（ストーリーテリング感） |
| Speed | 1.00 | 中速（聞かせるペース） |
| **使用シーン** | 回想語り、状況の深い描写、感動シーンの前振り |

##### パターンC：重厚ブロードキャスター（権威×温度）

| 項目 | 設定 |
|------|------|
| **コンセプト** | プロのアナウンサーだが物語への愛が隠せない |
| **生成プロンプト** | "Full baritone, commanding presence with underlying warmth, measured pace clear diction, commands attention naturally, comedy through timing and subtle tone shifts, professional broadcaster who genuinely cares about the story" |
| **候補1 voice_id** | `D08okKne84HX7qNGdv79` |
| **候補2 voice_id** | `wa1q903obkRt13YtCHQy` |
| **候補3 voice_id** | `yjOOMWJQmTrG2z2eNaLZ` |
| **プレビュー音声** | `narrator_voice_C_1.mp3` / `_C_2.mp3` / `_C_3.mp3` |

| パラメータ | 値 | 対応 |
|-----------|-----|------|
| Stability | 0.60 | 安定した信頼感（ブレない基盤） |
| Similarity | 0.80 | 同一 |
| Style | 0.25 | 控えめだが確かな存在感 |
| Speed | 0.98 | やや落ち着いた語り（権威感） |
| **使用シーン** | 緊迫シーン、シリアスな場面転換、重要な伏線提示 |

#### ナレーションのシーン別Audio Tags設計

```
【ギャグシーン → パターンA】
[laughs] さて、この男── [pauses] 齢35にして人形を命がけで守る
極道の組長、相良仁。[excited] まさかの人形収集家である。

【緊迫シーン → パターンC】
[quietly] 銃声が夜に溶ける。[pauses] 男は…人形を抱いたまま、倒れた。

【感動シーン → パターンB〜C（or 沈黙）】
[pauses] [quietly] ──ナレーション、ここは黙っておきましょう。

【ツッコミ → パターンA】
[laughs] いやいやいやいや。[pauses] 元ヤクザの料理が美味いって、
どういう人生歩んできたらそうなるんですか。

【次回予告 → パターンA】
[excited] 次回！ [pauses] 市場に現れた謎のスリ少年、トール！
仁の財布を狙う！ [laughs] …が、そもそも仁、異世界のお金持ってない。

【状況説明 → パターンB】
[pauses] 異世界の小さな食堂──ヨダマリ亭。
[quietly] この場所が、すべての始まりになるとは、
[pauses] 誰も知らなかった。

【伏線提示 → パターンC】
[quietly] [pauses] ──ちなみに。[pauses]
このぬいぐるみ、後で喋ります。
```

#### 演技テクニック→Audio Tags変換表（ナレーター専用）

| テクニック | v3 Audio Tagsでの実現方法 |
|-----------|------------------------|
| ギャグの"間" | `[pauses]` を一拍入れてから `[laughs]` or `[excited]` |
| ツッコミの自然さ | `[laughs]` を文頭に。中間で `[pauses]` |
| シリアスへの切替 | タグなし→ `[quietly]` で温度を下げる |
| 感動の"引き" | `[pauses]` + `[quietly]` →最終的に沈黙（セリフなし） |
| 次回予告の煽り | `[excited]` + `[pauses]` + `[laughs]` の三段構え |
| 伏線の含み笑い | `[quietly]` + `[pauses]`（笑わない。含みだけ残す） |

#### NG例（ナレーター専用）

| NG | 理由 | 代わりに |
|----|------|---------|
| 常時 `[excited]` | テンション過多→バラエティ感が安っぽくなる | ギャグ＋次回予告のみ |
| `[shouts]` を使う | ナレーターは叫ばない。声量で勝負しない | `[excited]` で代用 |
| `[whispers]` を常用 | 存在感が消える。語りの信頼が崩れる | 緊迫の1場面のみ |
| 感動シーンで語りすぎ | ジンの表情で伝えるべき場面を潰す | 沈黙 or `[quietly]` 一言だけ |
| Speed 1.15以上 | 聞き取れない＋落ち着きが消える | 最大1.05 |

---

### ジン（相良仁）— 主人公

#### ★ カスタムボイス生成済み（Voice Design v3）

テキストプロンプトからジン専用の声を生成。3候補から選定。

| 項目 | 設定 |
|------|------|
| **生成プロンプト** | "Deep low baritone, rich chest resonance, tall large-built man, calm quiet measured, smooth warm, speaks slowly with deliberate pauses, gentle giant, Tokyo Japanese accent" |
| **候補1 voice_id** | `71lZNfF3rm7sqhzCyYMb` |
| **候補2 voice_id** | `gclfjUyRz9ua8r1qYN0u` |
| **候補3 voice_id** | `vWRn5BEi8FfNKCPscV2U` |
| **プレビュー音声** | `jin_voice_preview_1.mp3` / `_2.mp3` / `_3.mp3` |
| **フォールバック** | Otani `3JDquces8E8bkmvbh6Bc`（既成ボイス） |
| **モデル** | `eleven_v3` |

#### 声仕様3パターン（声設計レポート準拠）

レポートの3パターンをv3のパラメータ＋Audio Tagsに変換。
**同一voice_idでパラメータとタグを変えることでシーンに応じた演じ分けを実現。**

##### パターンA：標準ライン（メイン使用）
| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.65 | 低め抑揚（語尾は落とし、角を丸める） |
| Similarity | 0.85 | 声質の一貫性を高く保つ |
| Style | 0.10 | クセを抑え、芯のある低音を維持 |
| Speed | 0.90 | 標準より-10%（信頼性・落ち着き） |
| **使用シーン** | 初対面、料理、日常会話、独白 |

##### パターンB：外面（極道風・威圧寄り）
| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.75 | より安定・無機質（台詞少・1語の重み） |
| Similarity | 0.85 | 同一 |
| Style | 0.05 | クセを最小限に（静かな殺気） |
| Speed | 0.85 | さらに遅く（沈黙を武器に） |
| **使用シーン** | 警告、対立の抑止、敵対者への一言 |

##### パターンC：内面（優しさ・臆病・孤独）
| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.50 | 感情の揺れを許容（心の揺れを小刻みに） |
| Similarity | 0.85 | 同一 |
| Style | 0.20 | 少しだけクセを出す（照れ・泣き） |
| Speed | 0.88 | やや遅め（余韻で感情を滲ませる） |
| **使用シーン** | ンバボとの会話、独白、弱音、感動 |

#### Audio Tags設計（感情→声変化フロー対応）

```
【平常：低い×静か → パターンA】
[quietly] [pauses] ……ああ。

【優しさ提示：語尾の角↓ → パターンA〜C】
[quietly] 怖がらなくていい。[pauses] 俺は、何もしない。

【警戒：無口化・語尾落とし → パターンB】
[quietly] ……その子に触るな。[pauses] 今すぐ、離れろ。

【独白：息温度↑・語尾余韻↑ → パターンC】
[whispers] [sad] なあ、ンバボ。[pauses] 俺、ここでやっていけるかな。

【臆病：短文化・言い切り回避 → パターンC】
[nervous] [stammers] 俺は…[pauses] その…[hesitates] ここにいて…いいのか。

【怒り：音圧↑(短時間)・子音硬化 → パターンB】
[angry] [quietly] ……次はない。

【感動・泣き → パターンC】
[stammers] [whispers] 俺は… [pauses] [gasps] 怖くない…のか…？

【回想・孤独 → パターンC】
[sorrowful] [quietly] 5つの時から…ずっとそうだった。
[sad] [pauses] 「怖い」って言われてきた。

【決意 → パターンA】
[pauses] 俺がここで…飯を作る。[quietly] それだけだ。

【料理中（集中）→ パターンA】
[quietly] [pauses] …火を止めろ。今だ。

【笑い（稀少）→ パターンC】
[laughs] [quietly] …なんだそりゃ。
```

#### 演技テクニック→Audio Tags変換表

| レポートのテクニック | v3 Audio Tagsでの実現方法 |
|-------------------|------------------------|
| 語尾の角を丸める | `[quietly]` + 語尾に「…」を追加 |
| 子音の当たりを弱める | `[whispers]` or `[quietly]`（軽く） |
| 間を"焦りの無さ"として置く | `[pauses]` を文中に挿入 |
| 呼吸の浅さ・短文 | 文を短く区切り、`[pauses]` で接続 |
| 言い切り回避 | `[hesitates]` + 語尾を「…」で濁す |
| 低いまま温度を上げる笑い | `[laughs]` + `[quietly]`（組合せ） |
| ため息は語頭の息に混ぜる | `[sighs]` を文頭に1回だけ |
| 臆病で声が揺れる | `[nervous]` + `[stammers]` |
| 怒り（静かな殺気） | `[angry]` + `[quietly]`（叫ばない） |

#### NG例（v3でも注意）

| NG | 理由 | 代わりに |
|----|------|---------|
| `[shouts] [angry]` を多用 | 怒鳴り→外見の説得力は出るが優しさが崩壊 | `[angry] [quietly]` で静かな殺気 |
| `[whispers]` を常用 | 存在感が消える。ASMR化 | 限定使用（ンバボ相手/独白のみ） |
| `[excited]` をジンに使う | キャラ崩壊（寡黙な男が興奮しない） | 代わりに `[gasps]` で一瞬の驚き |
| Stabilityを0.3以下 | 声がブレすぎて"芯"がなくなる | 最低0.50 |

---

### リーナ — ヒロイン（食堂の少女）

リーナはジンとの「対比」で設計。ジンの低音・静けさ（威圧）に対して、
リーナは「怖さを保持したまま無害さの証拠を積む安全弁」として機能する。

#### ★★ v2 カスタムボイス（高め・若め・初々しさ重視）— 3パターン×3候補＝計9候補 ← NEW

v1の試聴フィードバック「もう少し声が高い方がいい。若さ・初々しさが欲しい」を反映。
→ 声域をソプラノ寄りに引き上げ、「初々しさ」「フレッシュさ」「健気さ」を強化。

##### パターンv2-A：フレッシュソプラノ（透明感×健気さ）★推奨メイン

| 項目 | 設定 |
|------|------|
| **コンセプト** | 一人で店を切り盛りする健気な少女。明るいが少し不器用 |
| **生成プロンプト** | "Light soprano, bright clear crystalline, naturally high and sweet, youthful innocence and slight nervousness, subtle genuine audible smile, occasional slight hesitations" |
| **候補1 voice_id** | `6PXOSbp5RdJiVPGE6iOE` |
| **候補2 voice_id** | `O9dOZ1MLt27BocAYxSQK` |
| **候補3 voice_id** | `e1Jf7UvgK3K52Uv87hsz` |
| **プレビュー音声** | `lina_v2_voice_A_1.mp3` / `_A_2.mp3` / `_A_3.mp3` |

| パラメータ | 値 | 対応 |
|-----------|-----|------|
| Stability | 0.50 | 初々しさの揺れを許容 |
| Similarity | 0.80 | 声質の一貫性 |
| Style | 0.20 | 微笑声＋健気さ |
| Speed | 1.00 | 中速（ジンより速いが煽らない） |
| **使用シーン** | 接客、日常、ジンへの安心提示、感動 |

##### パターンv2-B：明るいヒロイン（春の陽光×勇気）

| 項目 | 設定 |
|------|------|
| **コンセプト** | 心を袖に着けている。勇気と脆さが両方聞こえる |
| **生成プロンプト** | "Soprano to high mezzo, bright lively natural warmth, fresh spring-like quality, clear enunciation natural upbeat rhythm, youthful timbre, earnest heroine courage and vulnerability" |
| **候補1 voice_id** | `dKEWqxhooCsxSv2JE1HR` |
| **候補2 voice_id** | `aW6MX6qdzElwFbpRTKOU` |
| **候補3 voice_id** | `d0DSWhAkIGQnlGxPCmYl` |
| **プレビュー音声** | `lina_v2_voice_B_1.mp3` / `_B_2.mp3` / `_B_3.mp3` |

| パラメータ | 値 | 対応 |
|-----------|-----|------|
| Stability | 0.48 | 感情の動きを自然に |
| Similarity | 0.80 | 同一 |
| Style | 0.22 | 明るさ＋エネルギー |
| Speed | 1.05 | やや速め（活発さ） |
| **使用シーン** | 驚き、喜び、通訳、コメディ牽引 |

##### パターンv2-C：甘く芯のある声（子守唄×鋼）

| 項目 | 設定 |
|------|------|
| **コンセプト** | 早く大人にならざるを得なかった。甘さの中に責任感 |
| **生成プロンプト** | "High mezzo to soprano, sweet clear, higher than mature woman but grounded, charming mix of sweetness and determination, lullaby quality and surprising steel" |
| **候補1 voice_id** | `lMXb1qqCNIc85poqbYYE` |
| **候補2 voice_id** | `ynso0s1EV1g0RocNY3FT` |
| **候補3 voice_id** | `OfjOCU6LPvncJS6qcBEG` |
| **プレビュー音声** | `lina_v2_voice_C_1.mp3` / `_C_2.mp3` / `_C_3.mp3` |

| パラメータ | 値 | 対応 |
|-----------|-----|------|
| Stability | 0.52 | 甘さと芯のバランス |
| Similarity | 0.80 | 同一 |
| Style | 0.18 | 甘さを控えめに（やりすぎ禁止） |
| Speed | 1.02 | 中速（落ち着きと活発さの中間） |
| **使用シーン** | 夜の会話、支え、怒り、泣き |

---

#### v1 カスタムボイス（参考・低め寄り）— 3パターン×3候補＝計9候補

※ v1は声域がメゾ〜アルト寄りで落ち着いた印象。v2で若さ・高さを補強。

#### パターンA：微笑の安全基地（推奨メイン）

| 項目 | 設定 |
|------|------|
| **コンセプト** | ジンの怖さを保持したまま安心を供給する通訳 |
| **生成プロンプト** | "Middle soprano to mezzo, clear and warm, subtle audible smile, NOT high-pitched, naturally bright but grounded, gentle consonants, quiet inner strength" |
| **候補1 voice_id** | `GtJXbWyVwvzVz92eZbbp` |
| **候補2 voice_id** | `TkLc0dtMn953YWbMGenp` |
| **候補3 voice_id** | `IMZiOmZ2jsNLNxj5HXsl` |
| **プレビュー音声** | `lina_voice_A_1.mp3` / `_A_2.mp3` / `_A_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.55 | 小〜中の抑揚（感情で上下に跳ねない） |
| Similarity | 0.80 | 声質の一貫性 |
| Style | 0.15 | 微笑声を薄く（作り笑い禁止） |
| Speed | 1.00 | 中速（ジンより速いが煽らない） |
| **使用シーン** | 接客、人前の潤滑油、ジンの優しさ証拠提示、沈黙を肯定する間 |

#### パターンB：落ち着きの相棒（ノワール寄り）

| 項目 | 設定 |
|------|------|
| **コンセプト** | 静けさでジンの優しさを増幅する |
| **生成プロンプト** | "Mezzo to alto, smooth and slightly low-temperature, composed steady, NOT whisper, depth and maturity beyond age, stays calm when others panic" |
| **候補1 voice_id** | `GBibz8g80NHuK6MAw18Z` |
| **候補2 voice_id** | `JcfLmyyua8eD1YuH1989` |
| **候補3 voice_id** | `1Q4dRKNDO5F2sJLKetOF` |
| **プレビュー音声** | `lina_voice_B_1.mp3` / `_B_2.mp3` / `_B_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.65 | 安定・落ち着き（対比は明瞭さと語尾で） |
| Similarity | 0.80 | 同一 |
| Style | 0.10 | クセを最小限（低温の静かさ） |
| Speed | 0.92 | やや遅め（協調性・安心寄り） |
| **使用シーン** | 夜の会話、暴力の匂いが近い場面、"地に足"を残す場面 |

#### パターンC：テンポの駆動役（会話牽引）

| 項目 | 設定 |
|------|------|
| **コンセプト** | ジンの寡黙を"会話"として成立させる駆動力 |
| **生成プロンプト** | "Mezzo with solid core, clear articulate, slightly faster pace, brightness from clarity not volume, capable young woman, bridges gaps between people" |
| **候補1 voice_id** | `ukNv9qYUiCcaHCBOayB2` |
| **候補2 voice_id** | `Xz7Of6SqqCWFinoYxrIF` |
| **候補3 voice_id** | `mbs1fkjfVC4F0cjKcF3X` |
| **プレビュー音声** | `lina_voice_C_1.mp3` / `_C_2.mp3` / `_C_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.45 | 力動性を出す（活発さ） |
| Similarity | 0.80 | 同一 |
| Style | 0.25 | 軽い微笑声（明瞭＋エネルギー） |
| Speed | 1.08 | やや速め（力動性と好感度を稼ぐ） |
| **使用シーン** | 外部者との交渉、誤解が生まれやすい場面の通訳、コメディテンポ牽引 |

#### フォールバック（既成ボイス）

| ボイス | voice_id | 用途 |
|--------|----------|------|
| Akari | `EkK6wL8GaH8IgBZTTDGJ` | 明るいカジュアル女声 |
| Sakura | `RBnMinrYKeccY3vaUxlZ` | 落ち着いた若い女声 |
| Yui | `fUjY9K2nAIwlALOwSiwc` | 優しいアニメ系女声 |

#### Audio Tags設計（感情→声変化フロー対応）

```
【通常（落ち着き＋明瞭）→ パターンA】
[happily] いらっしゃいませ。ヨダマリ亭へようこそ。

【安心提示：周囲がジンを怖がる → パターンA】
[quietly] [happily] 大丈夫ですよ。[pauses] この人は、怖くないんです。

【ジンへの直接の安心 → パターンA〜B】
[quietly] 大丈夫。あなたが優しいの、私だけは知ってる。

【支え：ジンが萎縮 → パターンB】
[quietly] [pauses] 無理しなくていい。[pauses] 静かで、ちゃんと伝わってる。

【駆動：緊急・通訳 → パターンC】
[rushed] はいはい、黙ってると誤解されるって。[pauses] 私が言うね。

【不安 → パターンB】
[nervous] [quietly] お客さん…最近全然来なくて…

【泣き → パターンB】
[sad] [whispers] お父さんがいなくなってから… [pauses] [sorrowful] ずっと一人でやってきました。

【驚き（ジンの料理）→ パターンA〜C】
[gasps] [excited] すごい…！ [pauses] これ本当にうちのスープなんですか…？

【信頼・親密 → パターンA】
[quietly] [happily] …おかえりなさい、ジンさん。[pauses] 今日もお疲れ様でした。

【怒り（ジンを守る）→ パターンC】
[angry] [quietly] ふざけないで。[pauses] この人に「怖い顔」を使わせないで。

【悲しみ（置いていかれる不安）→ パターンB】
[sad] [whispers] …置いてかないで。[pauses] 今だけ、そばにいて。
```

#### 演技テクニック→Audio Tags変換表（ヒロイン専用）

| レポートのテクニック | v3 Audio Tagsでの実現方法 |
|-------------------|------------------------|
| 微笑声（audible smiling） | `[happily]` を薄く使う（全文にかけない、冒頭だけ） |
| 語尾の下げ止め＋微上げ | 通常は文末「。」で止め、親密時だけ「…」で余韻 |
| 可愛さを局所的に足す | `[excited]` `[gasps]` は驚き時のみ（常用禁止） |
| 子音を柔らかく | `[quietly]` で破裂を抑える |
| 速度切替（支え↔駆動） | パターンB(Speed:0.92)とC(Speed:1.08)を場面で切替 |
| 冷える（怒り） | `[angry]` + `[quietly]`（金切り声禁止） |
| 息は語頭に薄く | `[sighs]` は文頭1回だけ、語尾には残さない |

#### NG例（ヒロイン専用）

| NG | 理由 | 代わりに |
|----|------|---------|
| 常時 `[happily]` `[excited]` | うるさい。F0が跳ね続ける | 通常は無タグ、感情時だけ局所的に |
| `[whispers]` 固定 | ジンの静けさと同質化→対比が消える | 泣きシーンのみ限定使用 |
| `[shouts]` `[loudly]` | 金切り声→ジンの「非暴力」軸が崩壊 | `[angry] [quietly]` で冷たく |
| Speed 1.2以上 | 早口→刺さる・うるさい | 最大1.08、明瞭さで活発さを出す |
| Stability 0.30以下 | 声がブレすぎ→安心感が消える | 最低0.45 |

---

### ンバボ — ぬいぐるみ（ジンの心的安全基地）

#### 設計原理（声設計レポート準拠）

ンバボは「ジンの唯一の味方」であり、転生先でも同一存在として機能する。
声はキャラのアイデンティティそのもの。設計の中心は：
- ① 聴覚疲労を起こしにくい音質
- ② 安心感を損ねない韻律
- ③ 反復視聴に耐える"うるさくない可愛さ"

**重要原則：「可愛い」をF0の上げすぎで作らない。**
→ 可愛さは「Hトーン局所上げ」「語尾の丸め」「母音の半拍伸ばし」で作る。

#### 音響仕様（レポートの基準プロファイル）

| 項目 | 推奨（基準） | 許容レンジ | v3での実現方法 |
|---|---:|---:|---|
| F0平均（Hz） | 200〜240 | 180〜260 | 低めの男声カスタムボイスで確保 |
| F0ピーク（Hz） | 260〜280 | 〜300 | `[excited]` は局所的に。300Hz超連発禁止 |
| F0レンジ（半音） | 4〜7 | 3〜10 | Stability: 0.65〜0.75で狭レンジ化 |
| 話速（モーラ長） | 0.17〜0.20秒 | 0.16〜0.22秒 | Speed: 0.75〜0.85 + `[pauses]` |
| 息量/ノイズ | 少〜中 | 少〜中高 | `[whispers]` は限定使用。息を"音"にしない |
| 語尾処理 | 丸め下降（↘） | 下降〜水平 | 語尾に「…」or「のう」。常時上げ禁止 |

#### ★ カスタムボイス生成済み（Voice Design v3）— 3パターン×3候補＝計9候補

| 項目 | 設定 |
|------|------|
| **モデル** | `eleven_v3` |
| **キャラ** | 老人口調「ワシ」「じゃのう」。ゆっくり。渋いが可愛い |
| **設計思想** | 低めF0＋小音量＋限定的抑揚。可愛さは温かみと遅さで作る |

##### パターンA：賢者ぬいぐるみ（低音×温かみ）★推奨メイン

| 項目 | 設定 |
|------|------|
| **コンセプト** | 老翁の知恵袋。ジンを見守る安心の声 |
| **生成プロンプト** | "Low-to-mid range, mezzo/low tenor, elderly warmth, very slow deliberate gentle pacing, soft round warm like plush toy, gentle consonants, grandfatherly, calm reassuring slightly sleepy" |
| **候補1 voice_id** | `aNeRPrpjhzphEXSO99aG` |
| **候補2 voice_id** | `uePRdjJshkC01wdX5eck` |
| **候補3 voice_id** | `N5U3IVGaVb33NbXWI4EU` |
| **プレビュー音声** | `nbabo_voice_A_1.mp3` / `_A_2.mp3` / `_A_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.70 | F0レンジ狭め（4〜6半音） |
| Similarity | 0.75 | 声質の一貫性 |
| Style | 0.15 | 温かみの薄いベール（やりすぎ禁止） |
| Speed | 0.78 | モーラ長0.17〜0.20秒相当 |
| **使用シーン** | 通常のそばにいる場面、助言、安心の言葉 |

##### パターンB：ぶっきらぼう可愛い（渋い×キャラ声）

| 項目 | 設定 |
|------|------|
| **コンセプト** | 口は悪いが心は優しい小さなおじいちゃん |
| **生成プロンプト** | "Mid-range, slightly raspy but not harsh, slow grumbling elderly quality, small grumpy old man who is actually kind, round endings, like tiny yakuza boss grandpa in plush form" |
| **候補1 voice_id** | `81hJ1hR82sXHyTo6rDOs` |
| **候補2 voice_id** | `9qJOexYbK01Qdkcx2lnQ` |
| **候補3 voice_id** | `pSxgEEmZlsg8yI4xxRI6` |
| **プレビュー音声** | `nbabo_voice_B_1.mp3` / `_B_2.mp3` / `_B_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.65 | やや広めのレンジ許容（ぶっきらぼう演技用） |
| Similarity | 0.75 | 同一 |
| Style | 0.25 | 渋さとキャラ感を強調 |
| Speed | 0.80 | 標準よりは遅いが、Aよりは速め |
| **使用シーン** | ギャグ、ツッコミ、甘いもの要求、ジンへの一喝 |

##### パターンC：神秘的ぬいぐるみ（静謐×権威）

| 項目 | 設定 |
|------|------|
| **コンセプト** | 多くを見てきた古の存在。言葉を選んで話す |
| **生成プロンプト** | "Mid-range, smooth meditative delivery, very slow each word carefully chosen, gentle but quiet authority, minimal pitch variation but warm resonance, ancient being peaceful wisdom" |
| **候補1 voice_id** | `YtAR8nOX4jfx0RTJlGfC` |
| **候補2 voice_id** | `tdfnZ11ubReXdDH9jeVk` |
| **候補3 voice_id** | `xNMUg9oDoOE9dxODNpBg` |
| **プレビュー音声** | `nbabo_voice_C_1.mp3` / `_C_2.mp3` / `_C_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.75 | レンジ最小（3〜5半音） |
| Similarity | 0.75 | 同一 |
| Style | 0.10 | クセを最小限（静かな権威） |
| Speed | 0.75 | 最も遅い（モーラ長0.19〜0.22秒相当） |
| **使用シーン** | 決意の場面、シリアスな助言、ジンを止める場面 |

#### フォールバック（既成ボイス）

| ボイス | voice_id | 用途 |
|--------|----------|------|
| Ishibashi | `Mv8AjrYZCBkdsmDHNwcB` | 低速設定で代用 |

#### 感情変化チャート（レポート準拠→v3パラメータ変換）

| 状態 | F0変化 | v3パターン | Audio Tags | 演技指示 |
|---|---:|---|---|---|
| 通常（そばにいる） | 基準210Hz | A | `[quietly]` | 口角を上げず「小さく真面目」。子音は丸める |
| 無邪気（ちょい褒め） | +10〜20Hz | A→B | `[happily]`（局所的） | 全体を上げず、単語の山（H）だけ少し上げる |
| 悲しみ（不安） | -10〜20Hz | A→C | `[sad]` `[quietly]` | 言い切りを弱め、母音を半拍伸ばす |
| 恐怖（壊されそう） | +15〜25Hz | A | `[nervous]` `[quietly]` | ピッチは上がるが"揺れない"。息を浅く |
| 喜び（再会） | +10〜15Hz | A→B | `[happily]` `[laughs]`（小さく） | 最後に小さく笑う。甲高い笑いはNG |
| 決意（ジンを止める） | +0〜10Hz | C | タグなし（明瞭化のみ） | 子音を少し立てて。3-4kHzを刺させない |

#### Audio Tags設計（感情→声変化フロー対応）

```
【通常（そばにいる）→ パターンA】
[quietly] [pauses] ジン、だいじょうぶ。ここにいるよ。

【助言（落ち着いた知恵）→ パターンA】
[quietly] 坊主。[pauses] お前さん、考えすぎじゃのう。

【無邪気/食いしん坊（ギャップ可愛さ）→ パターンB】
[happily] [gasps] おおっ！ [pauses] それは…甘味か！？ ワシにも一口よこせ。

【怒り（本気の一喝・稀少）→ パターンB→C】
[angry] [quietly] ンバボー！ [pauses] [quietly] …分かったか、坊主。

【優しさ（泣くジンに）→ パターンA】
[quietly] [sad] …泣くでない。[pauses] ワシがおるじゃろう。

【恐怖（壊されそう）→ パターンA】
[nervous] [quietly] やだ…こわい…[pauses] ジン、にげて…。

【決意（ジンを止める）→ パターンC】
[pauses] お前さん。[pauses] それ以上は…行かせん。

【再会の喜び → パターンA→B】
[happily] [quietly] [laughs] …やっと会えたのう。[pauses] 遅いぞ、坊主。

【独白（ジン不在時）→ パターンC】
[quietly] [pauses] …まだかのう。[sad] あの子は…いつも遅い。
```

#### 演技テクニック→Audio Tags変換表（ンバボ専用）

| レポートのテクニック | v3 Audio Tagsでの実現方法 |
|-------------------|------------------------|
| F0を上げずに可愛さを作る | `[happily]` を局所的に（文頭1語だけ）。全文にかけない |
| 語尾を丸めて安心を作る | 語尾に「…」「のう」＋ `[quietly]` |
| 息量を少なく保つ | `[whispers]` は優しさ場面の1回だけ。常用禁止 |
| 感情幅を小さく・方向だけ明確に | Stability 0.65〜0.75。`[excited]` は食事時のみ |
| モーラ長0.17〜0.20秒の遅さ | Speed: 0.75〜0.85 + 文中 `[pauses]` |
| 甲高い笑いを避ける | `[laughs]` + `[quietly]` の組合せ（小さく低く笑う） |
| 子音の角を落とす | タグなし＋Speed低め（自然に丸くなる） |

#### NG例（ンバボ専用）

| NG | 理由 | 代わりに |
|----|------|---------|
| F0ピーク300Hz超の連発 | 3-4kHz帯に倍音が乗り、聴覚疲労を起こす | 語尾丸め＋Hトーン局所上げで可愛さを作る |
| 常時 `[excited]` `[happily]` | うるさい可愛さ＝安心基地の役割を損ねる | 食事・再会時のみ局所使用 |
| `[whispers]` 常用 | 存在感が消える。ジンの孤独を補強できない | 泣きシーン1回だけ |
| `[shouts]` を多用 | 一喝の価値が下がる＋聴覚負荷 | 一喝は1話に1回まで。`[angry] [quietly]` で代用 |
| Speed 1.0以上 | モーラ長が短くなり「落ち着き」が消える | 最大0.85。間で緩急を作る |
| Stability 0.50以下 | 声がブレて安心感が崩壊 | 最低0.65 |
| 語尾を毎回上げる | 不安が常態化→安全基地の役割を損ねる | 通常は↘。疑問時のみ↗ |
| 息を"音"として入れすぎる | 高域成分↑→シャープネス↑→刺さる | `[quietly]` で対応 or voice_id変更 |

#### 収録チェックリスト（ンバボ専用・v3生成時の確認用）

| チェック項目 | 合格基準 | 失敗兆候 | 対処 |
|---|---|---|---|
| F0平均 | 200〜240Hz付近 | 260Hz超が常態化 | Speed下げ＋`[quietly]` 追加 |
| 高域の刺さり | サ行が痛くない | 「ス」「シ」が耳に残る | `[quietly]` 追加 or voice_id変更 |
| 話速 | 0.17〜0.20秒/モーラ | 詰め込み感 | Speed下げ＋`[pauses]` 追加 |
| 感情レンジ | 狭く安定 | 乱高下している | Stability上げ（0.70→0.75） |
| 甲高さ | 不快感なし | 笑い声が甲高い | `[laughs] [quietly]` で対応 |

#### ンバボ×ジン×リーナ×トール 四者声域分離

| キャラ | F0帯域 | 話速 | 存在感の作り方 |
|--------|---------|------|---------------|
| ジン | 85〜165Hz（低バリトン） | 遅い | 圧と沈黙 |
| **ンバボ** | **200〜240Hz（中低テナー/メゾ）** | **最も遅い** | **温かみと間** |
| リーナ | 220〜350Hz（ソプラノ〜メゾ） | 中速 | 明瞭さと微笑 |
| トール | 200〜330Hz（ハイテナー） | やや速い | 速度と明瞭さ |

→ ンバボはジンより高いがリーナ/トールより遅い。「高さ」ではなく「遅さ」で安心感を差別化。

---

### トール — 少年スリ（第2話から本格登場）

#### ★ カスタムボイス生成済み（Voice Design v3）— 3パターン×3候補＝計9候補

トールは三者関係の「運動」担当。ジン（重心＝静けさで圧を作る）とリーナ（温度＝明るさで場を動かす）
の両方を壊さず、テンポと好奇心で会話を進める第三の速度と温度。
→ 音量ではなく「明瞭さ」で抜ける設計。F0帯域の自然な分離でジンと明確に分かれる。

#### パターンA：無邪気寄り（Bright Youthful）

| 項目 | 設定 |
|------|------|
| **コンセプト** | 好奇心旺盛。質問と実況で会話を回す |
| **生成プロンプト** | "Youthful high-pitched light tenor, bright clear, slightly fast, curious lively intonation, spirited street-smart" |
| **候補1 voice_id** | `DTsGsX9kQILYOBjlqmUe` |
| **候補2 voice_id** | `1Uq79BsL2IC3n6qiw6YI` |
| **候補3 voice_id** | `s15yY6yZuYNkMYSyvCM9` |
| **プレビュー音声** | `thor_voice_A_1.mp3` / `_A_2.mp3` / `_A_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.40 | F0レンジ広め（感情が体に出る） |
| Similarity | 0.75 | 声質の一貫性 |
| Style | 0.25 | 無邪気の弾み |
| Speed | 1.10 | やや速め（モーラ長0.135〜0.145相当） |
| **使用シーン** | 初登場の好奇心、食事の感動、ジンへの驚き |

#### パターンB：標準少年（Balanced Youthful）★推奨メイン

| 項目 | 設定 |
|------|------|
| **コンセプト** | 無邪気⇄生意気を場面で切替可能なバランス型 |
| **生成プロンプト** | "Youthful mid-to-high tenor, versatile earnest and sarcastic, quick-witted, bravado with vulnerability underneath, agility and sharpness" |
| **候補1 voice_id** | `ls52jZdHYfLE1lmMxQ9Q` |
| **候補2 voice_id** | `hajqVpueYjSetOEqm6Ga` |
| **候補3 voice_id** | `YDFQQGam9DbzbifU8Yxq` |
| **プレビュー音声** | `thor_voice_B_1.mp3` / `_B_2.mp3` / `_B_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.45 | 中レンジ（レンジ過多禁止） |
| Similarity | 0.75 | 同一 |
| Style | 0.20 | 標準少年（クセは中程度） |
| Speed | 1.05 | 自然〜やや速（モーラ長0.140〜0.150相当） |
| **使用シーン** | 日常会話、ジンとのやり取り、大半の場面 |

#### パターンC：生意気寄り（Edgy Youthful）

| 項目 | 設定 |
|------|------|
| **コンセプト** | 口が達者・挑発。だが本気の危険で静まる |
| **生成プロンプト** | "Youthful tenor with edge and attitude, dry confident, sharp consonant attacks, sarcastic but not mean, tough-talking but softhearted" |
| **候補1 voice_id** | `z3zBodOA1U6RqfdG13jg` |
| **候補2 voice_id** | `6mRWcrppAWm7DXSkXaHo` |
| **候補3 voice_id** | `TJ6uavg9KRqnbcBkLEJz` |
| **プレビュー音声** | `thor_voice_C_1.mp3` / `_C_2.mp3` / `_C_3.mp3` |

| パラメータ | 値 | レポートとの対応 |
|-----------|-----|----------------|
| Stability | 0.35 | 子音アタック＋語尾の角が立つ |
| Similarity | 0.75 | 同一 |
| Style | 0.30 | 態度を強調（乾いた質感） |
| Speed | 1.12 | 速め（モーラ長0.125〜0.140相当、早口禁止） |
| **使用シーン** | スリ場面、突っかかり、ジンへの挑発 |

#### フォールバック（既成ボイス）

| ボイス | voice_id | 用途 |
|--------|----------|------|
| Akira | `DOL4zlUH4vnnX1hByxsw` | 若い×クリスプな男声 |

#### Audio Tags設計（無邪気⇄生意気スペクトラム対応）

```
【標準少年（クリア/中速/中レンジ）→ パターンB】
おいおっさん、あんた財布落としたぞ。

【無邪気：喜び・成功 → パターンA】
[excited] すげえ！ マジですげえ！ [gasps] なんだこれ！ こんなの食ったことねえよ！

【生意気：突っかかり → パターンC】
なんだよその顔。[pauses] そんな怖い顔して、誰も近づかねえだろ。

【萎縮：ジンの圧に当てられる → パターンB〜A】
[nervous] [stammers] えっ、ちょ、ちょっと待てよ。[pauses] 俺は別に、その、悪いことしようとしたわけじゃ…

【警戒：本気の危険 → パターンB】
[quietly] [pauses] …やべえ。[whispers] あいつら、本気だ。

【疑い → パターンC】
[pauses] うそだろ。あんたの飯、そんなうまいわけないだろ。

【素直（稀少・ギャップ）→ パターンA】
[quietly] [hesitates] …あの、さ。[pauses] [whispers] …ありがとう。

【実況・質問（運動担当）→ パターンB】
[excited] おい見ろよ！ あのおっさん、また怖い顔で料理してる！
なんで極道が飯なんか作ってんだよ？
```

#### 演技テクニック→Audio Tags変換表（トール専用）

| レポートのテクニック | v3 Audio Tagsでの実現方法 |
|-------------------|------------------------|
| F0レンジで無邪気を出す | `[excited]` を喜び時のみ局所的に（常用禁止） |
| 子音アタック↑で生意気を出す | タグなし（Speed上げ＋短文で再現）。強い場面は `[angry]` 軽く |
| 語尾を短く切る | 文を短くし、「。」で止める。語尾に「…」をつけない |
| 疑問上昇で挑発 | 文末を「〜だろ？」「〜じゃねえの？」等の疑問系に |
| 萎縮＝モーラ長↑ | `[nervous]` + `[stammers]` + `[pauses]`の組合せ |
| 短文の頻度で運動量 | 1文を短く、回数を増やす。`[pauses]` で区切る |
| 素直さ（ギャップ）| `[quietly]` + `[hesitates]`（声を高くせず角を取る） |

#### 三者コントラスト設計（v3パラメータ対比）

| パラメータ | ジン | リーナ | トール | 役割分担 |
|-----------|------|--------|--------|---------|
| 声域 | 低バリトン | ミドルソプラノ〜メゾ | ハイテナー〜ライトテナー | F0帯域で自然分離 |
| Speed | 0.85-0.90（遅め） | 0.92-1.08（中速） | 1.05-1.12（やや速） | トールが会話を駆動 |
| Stability | 0.50-0.75（安定寄り） | 0.45-0.65（中間） | 0.35-0.45（揺れ許容） | トールが最も動的 |
| Style | 0.05-0.20（低い） | 0.10-0.25（中間） | 0.20-0.30（高め） | トールが最もクセあり |
| 語尾 | 丸め・着地 | 柔らかいツッコミ | 短く切る・疑問上昇 | 角の差で対比 |
| 音量 | 小〜中 | 中 | 小〜中（**上げない**） | 目立たせるのは明瞭さ |
| 役割 | 結論 | 関係調整 | 質問と実況 | 三者で会話が回る |

#### NG例（トール専用）

| NG | 理由 | 代わりに |
|----|------|---------|
| 常時 `[excited]` `[shouts]` | うるさい→ヒロインのコミカル領域を侵食 | 喜び時のみ `[excited]`、通常はタグなし |
| `[angry]` を多用 | 緊張が常時ON→ジンの「静かな圧」の価値が下がる | 態度は語尾と短文で出す |
| Speed 1.20以上 | 早口→聞き取れない＋刺さる | 最大1.12、レンジ設計で軽快さを作る |
| `[whispers]` 常用 | 少年の存在感が消える | 素直シーンの1回だけ |
| Stability 0.25以下 | 声がガタつく→少年の「安定した若さ」が崩れる | 最低0.35 |

---

### 女の子（シーン6の幼女）
| 項目 | 設定 |
|------|------|
| **推奨ボイス** | Shizuka（柔らかい女声・ピッチ上げ） |
| **voice_id** | 要確認 |
| **モデル** | `eleven_v3` |
| **基本設定** | Stability: 0.45, Similarity: 0.70, Style: 0.10, Speed: 1.10 |
| **キャラ** | 無邪気。怖がらない。核心をつく一言 |

#### 女の子のAudio Tags設計

```
[happily] おじちゃん、おかお、おっきいね！
[excited] このこ、ンバボっていうの！
[happily] [quietly] …おじちゃんのごはん、たべたい。
```

---

## v3 vs v2 比較（なぜv3を採用するか）

| 比較項目 | v2 (eleven_multilingual_v2) | ★ v3 (eleven_v3) |
|---------|---------------------------|-------------------|
| 感情制御 | Stabilityの数値調整のみ | **Audio Tagsでセリフ内に直接指示** |
| 表現力 | 高い | **最高（囁き、叫び、笑い、ため息等）** |
| 言語数 | 29 | **74** |
| 間の表現 | 困難 | `[pauses]` タグで自然な間 |
| 演技指示 | 不可 | `[stammers]` `[hesitates]` 等で可能 |
| コスト | 中 | 高 |
| 遅延 | 低い | やや高い（リアルタイム非推奨） |

→ 漫画動画の事前レンダリング用途なので **遅延は問題なし**。表現力を最優先で v3 を採用。

---

## 既存コードの変更点

`elevenlabs.py` の `text_to_speech_with_timestamps()` で以下を変更：

```python
# 変更前
model_id: str = "eleven_multilingual_v2"

# 変更後
model_id: str = "eleven_v3"
```

※ v3でもタイムスタンプ付きAPIは同様に使用可能。

---

## 制作ワークフローへの組み込み

```
STEP 1: プロット作成 ← 完了
STEP 2: キャラクターデザイン ← 進行中
STEP 3: 画像生成プロンプト作成
STEP 4: 画像生成（Nanobonanza）
STEP 5: 音声生成 ← ★このドキュメントが対応
  5-1. セリフリストにAudio Tagsを付与
  5-2. キャラ別voice_id + voice_settingsで生成
  5-3. タイムスタンプ取得→Remotion用JSONに変換
STEP 6: Remotionで合成（画像＋音声＋字幕＋BGM/SE）
```

---

## 次のステップ

- [x] APIで利用可能な日本語ボイスを一覧取得 ← 完了
- [x] ジン専用カスタムボイス生成（3候補） ← 完了
- [x] リーナ専用カスタムボイス生成（3パターン×3候補＝9候補） ← 完了
- [x] トール専用カスタムボイス生成（3パターン×3候補＝9候補） ← 完了
- [x] ンバボ専用カスタムボイス生成（3パターン×3候補＝9候補） ← 完了
- [x] ナレーター専用カスタムボイス生成（3パターン×3候補＝9候補） ← 完了
- [x] ンバボ声設計レポート→v3パラメータ＋Audio Tags変換 ← 完了
- [x] ナレーター音声設計＋v3パラメータ設計 ← 完了
- [x] elevenlabs.pyをv3対応に更新 ← 完了
- [ ] 全キャラのプレビュー音声を試聴し、ベスト候補を選定
  - [ ] ジン：3候補から1つ
  - [ ] リーナ：9候補からパターン＋候補を1つ
  - [ ] トール：9候補からパターン＋候補を1つ
  - [ ] ンバボ：9候補からパターン＋候補を1つ
  - [ ] ナレーター：9候補からパターン＋候補を1つ
- [ ] 女の子（シーン6）のvoice_idを確定
- [ ] シーン1のセリフリストにAudio Tagsを付与
- [ ] テスト生成→トーン確認→微調整
