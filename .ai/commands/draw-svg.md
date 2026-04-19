# Draw SVG Diagram

図の草稿をSVG形式で作成します。

## 使い方

```
/draw-svg [図の種類] [対象セクション or 説明]
/draw-svg usecase 1.5          # 1.5節のユースケース図
/draw-svg activity クエスト完了  # クエスト完了のアクティビティ図
/draw-svg goal-tree 1.4        # 1.4節のゴールツリー
/draw-svg custom "要求の3層構造"  # カスタム図
```

## 対応する図の種類

| 種類 | コマンド | 用途 |
|------|---------|------|
| ユースケース図 | `usecase` | アクターとシステム機能の関係 |
| アクティビティ図 | `activity` | 処理フローとスイムレーン |
| ゴールツリー | `goal-tree` | ゴールの階層構造（AND/OR分解） |
| 要求階層図 | `requirements` | ビジネス要求→ユーザー要求→機能要求 |
| シーケンス図 | `sequence` | オブジェクト間のメッセージ |
| クラス図 | `class` | クラス構造と関係 |
| カスタム | `custom` | その他の概念図 |

## 出力先

```
assets/diagrams/chapter{章番号}/
  ├── {節番号}-{図の種類}-{連番}.svg
  └── {節番号}-{図の種類}-{連番}.svg
```

例: `assets/diagrams/chapter01/1-5-usecase-01.svg`

## 実行手順

### Step 1: 元情報の取得

指定されたセクションのASCII図またはPlantUMLコードを読み取る。
カスタムの場合は説明文から図の構造を把握する。

### Step 2: SVGの生成

以下のスタイルガイドラインに従ってSVGを生成:

#### 共通スタイル

```svg
<!-- カラーパレット -->
<style>
  .primary { fill: #4A90D9; }      /* メインカラー（青） */
  .secondary { fill: #7CB342; }    /* サブカラー（緑） */
  .accent { fill: #FFB74D; }       /* アクセント（オレンジ） */
  .background { fill: #F5F5F5; }   /* 背景（薄いグレー） */
  .text { fill: #333333; }         /* テキスト（ダークグレー） */
  .line { stroke: #666666; }       /* 線（グレー） */

  /* フォント */
  text {
    font-family: 'Noto Sans JP', 'Hiragino Sans', sans-serif;
    font-size: 14px;
  }

  /* 角丸 */
  rect { rx: 8; ry: 8; }
</style>
```

#### ユースケース図スタイル

```svg
<!-- アクター（人型） -->
<g class="actor">
  <circle cx="0" cy="-20" r="10" fill="#4A90D9"/>
  <line x1="0" y1="-10" x2="0" y2="10" stroke="#4A90D9" stroke-width="2"/>
  <line x1="-15" y1="0" x2="15" y2="0" stroke="#4A90D9" stroke-width="2"/>
  <line x1="0" y1="10" x2="-10" y2="30" stroke="#4A90D9" stroke-width="2"/>
  <line x1="0" y1="10" x2="10" y2="30" stroke="#4A90D9" stroke-width="2"/>
</g>

<!-- ユースケース（楕円） -->
<ellipse rx="80" ry="30" fill="#E3F2FD" stroke="#4A90D9" stroke-width="2"/>

<!-- システム境界 -->
<rect fill="none" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
```

#### アクティビティ図スタイル

```svg
<!-- 開始ノード -->
<circle r="10" fill="#333"/>

<!-- 終了ノード -->
<circle r="12" fill="none" stroke="#333" stroke-width="2"/>
<circle r="8" fill="#333"/>

<!-- アクション（角丸四角形） -->
<rect rx="15" ry="15" fill="#E8F5E9" stroke="#7CB342" stroke-width="2"/>

<!-- 分岐（ひし形） -->
<polygon points="0,-20 20,0 0,20 -20,0" fill="#FFF3E0" stroke="#FFB74D" stroke-width="2"/>

<!-- スイムレーン -->
<rect fill="none" stroke="#DDD" stroke-width="1"/>
<text class="swimlane-header" font-weight="bold"/>
```

#### ゴールツリースタイル

```svg
<!-- ゴールノード -->
<rect rx="5" ry="5" fill="#E3F2FD" stroke="#4A90D9" stroke-width="2"/>

<!-- AND/ORラベル -->
<text font-size="10" fill="#666">[AND]</text>
<text font-size="10" fill="#666">[OR]</text>

<!-- 接続線 -->
<path stroke="#666" stroke-width="1.5" fill="none"/>
```

### Step 3: ファイル保存

1. 出力ディレクトリが存在しない場合は作成
2. SVGファイルを保存
3. 対応するセクションのMarkdownに画像参照を追記（オプション）

```markdown
![ユースケース図](../../assets/diagrams/chapter01/1-5-usecase-01.svg)
```

### Step 4: 確認

生成したSVGのパスをユーザーに報告。

## SVGテンプレート

### 基本テンプレート

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 800 600"
     width="800" height="600">

  <defs>
    <style>
      .primary { fill: #4A90D9; }
      .secondary { fill: #7CB342; }
      .accent { fill: #FFB74D; }
      .text { fill: #333; font-family: 'Noto Sans JP', sans-serif; }
      .line { stroke: #666; stroke-width: 2; fill: none; }
    </style>
  </defs>

  <title>図のタイトル</title>

  <!-- 図の内容 -->

</svg>
```

### ユースケース図テンプレート

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">
  <defs>
    <style>
      .actor-body { stroke: #4A90D9; stroke-width: 2; fill: none; }
      .actor-head { fill: #4A90D9; }
      .usecase { fill: #E3F2FD; stroke: #4A90D9; stroke-width: 2; }
      .system-boundary { fill: #FAFAFA; stroke: #999; stroke-width: 2; }
      .connection { stroke: #666; stroke-width: 1.5; fill: none; }
      .label { font-family: 'Noto Sans JP', sans-serif; font-size: 12px; fill: #333; }
    </style>
  </defs>

  <title>QuestForge ユースケース図</title>

  <!-- システム境界 -->
  <rect class="system-boundary" x="150" y="30" width="500" height="440" rx="10"/>
  <text x="400" y="55" text-anchor="middle" class="label" font-size="16" font-weight="bold">QuestForge</text>

  <!-- アクター: 勇者 -->
  <g transform="translate(70, 150)">
    <circle class="actor-head" cx="0" cy="-25" r="12"/>
    <line class="actor-body" x1="0" y1="-13" x2="0" y2="15"/>
    <line class="actor-body" x1="-20" y1="0" x2="20" y2="0"/>
    <line class="actor-body" x1="0" y1="15" x2="-15" y2="40"/>
    <line class="actor-body" x1="0" y1="15" x2="15" y2="40"/>
    <text class="label" x="0" y="60" text-anchor="middle">勇者</text>
  </g>

  <!-- ユースケース -->
  <g transform="translate(400, 120)">
    <ellipse class="usecase" rx="100" ry="35"/>
    <text class="label" x="0" y="5" text-anchor="middle">クエストを作成する</text>
  </g>

  <!-- 接続線 -->
  <line class="connection" x1="90" y1="150" x2="300" y2="120"/>

</svg>
```

## 注意事項

- 日本語フォントは `Noto Sans JP` を推奨（Webフォント対応）
- viewBoxを適切に設定してレスポンシブに
- アクセシビリティのため `<title>` と `<desc>` を含める
- 線の太さは2px程度で統一（細すぎると見づらい）
- 色は本書のカラーパレットに準拠

## 既存ASCII図からの変換例

**入力（ASCII）:**
```
┌─────────────────────────────────────┐
│     ビジネス要求（Why of Why）       │
├─────────────────────────────────────┤
│     ユーザー要求（Why）              │
├─────────────────────────────────────┤
│     機能要求（What/How）             │
└─────────────────────────────────────┘
```

**出力（SVG）:**
3層の積み重ね図形として、グラデーションと影付きで視覚的に表現。
