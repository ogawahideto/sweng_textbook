# Project Context

このファイルは、AIアシスタントがプロジェクト全体を理解するための情報をまとめています。

## Project Overview

**Title**: 『「楽しい」ソフトウェアエンジニアリングの教科書 - デジタル・アルケミー：伝統の美学とAIで紡ぐ創造の地図』

**Type**: 技術教科書

**Target Audience**:
- ソフトウェアエンジニアリングを学ぶ学生
- AI時代のエンジニアを目指す初学者
- 伝統的な技術とAIの融合に興味がある実務者

**Unique Value**:
- AI時代の視点を取り入れたソフトウェアエンジニアリング
- 技術を「楽しむ」「美しい」視点で捉える
- 実践的で、読者が試せる内容

## Project Structure

```
textbook/
├── .ai/                   # AI設定・ワークフロー（標準）
│   ├── agents.md              # AIエージェント定義
│   ├── context/              # プロジェクトコンテキスト
│   └── workflows/            # 標準ワークフロー
│
├── plan.md                # 書籍企画
├── progress.md            # 進捗管理
├── style-guide.md         # 執筆スタイル
├── README.md              # 環境ガイド
│
├── templates/             # テンプレート
│   ├── chapter-template.md
│   └── section-template.md
│
└── chapters/              # コンテンツ
    ├── prologue/
    ├── part1/ (構想の美学)
    ├── part2/ (構築のダイナミズム)
    ├── part3/ (守護者の誇り)
    ├── part4/ (チーム・オーケストラ)
    └── appendix/
```

## Key Files

### Configuration

- `.ai/agents.md` - AIエージェントの役割・振る舞い定義
- `style-guide.md` - 執筆スタイルガイド
- `plan.md` - 書籍全体の企画・構成

### Management

- `progress.md` - 進捗管理表（状態追跡）
- `README.md` - 環境の使い方ガイド

### Workflows

- `.ai/workflows/draft.md` - 草稿生成ワークフロー
- `.ai/workflows/review.md` - レビューワークフロー
- `.ai/workflows/plan-next.md` - タスク計画ワークフロー

### Templates

- `templates/chapter-template.md` - 章のテンプレート
- `templates/section-template.md` - 節のテンプレート

## Book Structure

### Parts & Chapters

1. **プロローグ**: ソフトウェアエンジニアリングは「魔法の地図」である

2. **第1部：構想の美学** (Requirements & Modeling)
   - 第1章: ドメインという名の異世界探検
   - 第2章: 悠久のアーキテクチャ

3. **第2部：構築のダイナミズム** (Implementation & AI-Driven)
   - 第3章: モダン・アルケミー
   - 第4章: リファクタリング：彫刻を磨く喜び

4. **第3部：守護者の誇り** (Testing & Maintenance)
   - 第5章: 無敵の軍団を作る
   - 第6章: 進化する生命体

5. **第4部：チーム・オーケストラ** (Process & Ethics)
   - 第7章: アジャイルという名の冒険パーティ
   - 第8章: エンジニアの倫理と未来への責任

6. **付録**
   - AIへの詠唱集
   - コード鑑賞コラム
   - レベルアップ・マップ

詳細は `plan.md` を参照

## Writing Philosophy

### Core Concepts

1. **美学的アプローチ**
   - 技術を「美しい」視点で捉える
   - エレガントな解決策を追求

2. **AI時代の視点**
   - 伝統的な技術の理解
   - AIとの協働方法
   - 両者の融合

3. **実践重視**
   - 理論だけでなく、実践例
   - 読者が試せるコード
   - ハンズオン形式

4. **ワクワク感**
   - 技術を「楽しむ」
   - 知的興奮を提供
   - 冒険のような学び

### Writing Style

- **親しみやすい**: 読者に語りかける文体
- **専門性**: 技術的正確性を保つ
- **具体的**: 抽象論で終わらない
- **比喩豊富**: 身近な例で説明

詳細は `style-guide.md` を参照

## Workflow Overview

### Standard Process

```
1. Plan Next Task
   ↓
2. Generate Draft (AI)
   ↓
3. Human Review & Edit
   ↓
4. AI Review & Suggestions
   ↓
5. Final Revision
   ↓
6. Mark Complete
```

### State Transitions

```
⬜ 未着手
  ↓
🟨 AI草稿
  ↓
🟦 人間修正中
  ↓
🟩 レビュー待ち
  ↓
✅ 完成
```

## Quality Standards

### Section Requirements

- **Length**: 2000-4000 characters
- **Code**: Executable examples
- **Figures**: Clear descriptions
- **AI Perspective**: Included
- **Style**: Compliant with style-guide.md

### Completion Criteria

- [ ] Technically accurate
- [ ] Style guide compliant
- [ ] Achieves section objectives
- [ ] Engaging and exciting
- [ ] Connected to adjacent sections

## Collaboration Model

### Human Responsibilities

- Final decision making
- Unique perspectives and experiences
- Selecting concrete examples
- Reader empathy
- Quality judgment

### AI Responsibilities

- Structured draft generation
- Comprehensive information gathering
- Organizing existing knowledge
- Text refinement
- Consistency checking

## Current Status

Check `progress.md` for:
- Overall progress (%)
- Section-by-section status
- Recent completions
- Next planned tasks

## Version Control

### Recommended Practice

```bash
# Initialize git (if not done)
git init

# Daily commits
git add chapters/
git commit -m "Update section X.Y"

# Weekly backups
git tag -a v0.1-week1 -m "Week 1 progress"
```

### Backup Strategy

- Commit after each section completion
- Tag at major milestones
- Push to remote repository (optional)

## Tools & Resources

### Recommended Tools

- **AI Assistants**: Claude, ChatGPT, GitHub Copilot
- **Markdown Editors**: VSCode, Obsidian, Typora
- **Diagrams**: Mermaid, draw.io, Excalidraw
- **Version Control**: Git

### Reference Materials

- Technical books on software engineering
- AI/ML documentation
- Design pattern references
- Code example repositories

## Troubleshooting

### Common Issues

**Issue**: 執筆が進まない
**Solution**: `plan-next.md` で気分転換できるタスクを提案

**Issue**: 品質に不安
**Solution**: `review.md` で詳細レビューを実施

**Issue**: スタイルが一貫しない
**Solution**: `style-guide.md` を再確認、既存セクションを参照

**Issue**: AIの提案が合わない
**Solution**: プロンプトを具体化、または人間の判断を優先

## Contact & Support

### For Questions

- Review `README.md` for usage instructions
- Check `.ai/agents.md` for AI capabilities
- Consult `style-guide.md` for writing conventions
- Read `plan.md` for book structure

### Feedback

- Track issues in progress.md notes
- Document lessons learned
- Iterate on workflows as needed

---

**Last Updated**: 2026-01-18
**Version**: 1.0
