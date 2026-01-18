# Workflow: Review & Improvement

執筆したセクションのレビューと改善を行うワークフローです。

## Trigger

- AI草稿を人間が修正した後
- 既存のセクションを改善したい時
- 品質チェックを実施したい時

## Prerequisites

- [ ] レビュー対象のセクションが存在する
- [ ] `progress.md` で該当セクションの状態を確認済み

## Steps

### 1. Load Context

レビューに必要な情報を読み込む：

```
@agents.md のレビューガイドライン
@style-guide.md の品質基準
@plan.md のセクション目的
対象セクションの内容
```

### 2. Invoke Agent for Review

以下のプロンプトでレビューを依頼：

```
あなたは『デジタル・アルケミー』の編集者です。

@agents.md の "When Reviewing Content" ガイドラインに従ってレビューしてください。

**レビュー対象**:
[章番号].[節番号] [タイトル]

**セクション内容**:
```
[ここに対象セクションの全文を貼り付け]
```

**レビュー観点**:
1. 技術的正確性
2. @style-guide.md への準拠
3. @plan.md で定義された目的の達成度
4. 読者への魅力（ワクワク感、分かりやすさ）
5. 前後のセクションとの整合性

**期待する形式**:
@agents.md の "Response Format > For Review Feedback" に従ってください。
```

### 3. Agent Response Format

エージェントは以下の形式で応答：

```markdown
## Strengths

1. **[Strong point 1]**: [Specific explanation]
2. **[Strong point 2]**: [Specific explanation]

## Improvements Needed

### High Priority

1. **[Issue]**: [Current state]
   - **Suggestion**: [Specific improvement]
   - **Example**:
   ```
   [Before]
   [After]
   ```

### Medium Priority

2. **[Issue]**: [Current state]
   - **Suggestion**: [Specific improvement]

### Low Priority

3. **[Issue]**: [Optional improvement]

## Additional Suggestions

- [Enhancement idea 1]
- [Enhancement idea 2]

## Compliance Check

- [x] Technical accuracy: ✓
- [x] Style guide: ✓
- [ ] Word count: 現在2800文字（目安内）
- [x] Code examples: ✓ (2 examples)
- [x] AI perspective: ✓
- [ ] Section flow: 前セクションへの参照が弱い

## Overall Assessment

**Quality Score**: 7.5/10
**Recommendation**: Medium priority の改善後、完成とする
```

### 4. Human Decision

レビュー結果を検討し、以下のいずれかを選択：

**Option A: 改善を適用**
- フィードバックを元に修正
- `progress.md` を 🟦 人間修正中 に更新

**Option B: 再レビュー依頼**
- 特定の観点について深掘り
- 代替案を要求

**Option C: 完成と判断**
- `progress.md` を ✅ 完成 に更新

### 5. Apply Improvements

採用する改善点を適用：

```bash
# セクションファイルを編集
# 修正内容を保存
```

### 6. Update Progress

`progress.md` を更新：

```
状態: 🟨 AI草稿 → 🟦 人間修正中 → 🟩 レビュー待ち → ✅ 完成
備考: [主な変更点を記載]
```

## Iteration

必要に応じて、以下のサイクルを繰り返す：

```
修正 → レビュー → 修正 → レビュー → ...
```

通常は1-2回の反復で完成を目指す。

## Output

- 改善されたセクションファイル
- 更新された `progress.md`
- レビュー履歴（オプション）

## Review Types

### Quick Review

軽微なチェックのみ：

```
@agents.md に従い、以下の観点のみチェックしてください：
- 技術的正確性
- スタイルガイド準拠

簡潔なフィードバックで構いません。
```

### Comprehensive Review

詳細なレビュー：

```
@agents.md に従い、包括的なレビューを実施してください。
すべての観点を詳細にチェックし、具体的な改善案を提示してください。
```

### Focused Review

特定の観点に絞ったレビュー：

```
@agents.md に従い、以下の観点についてレビューしてください：
- [特定の観点1]
- [特定の観点2]

他の観点は既にレビュー済みです。
```

## Quality Gates

セクションを「完成」とするための基準：

### Must Have (必須)

- [ ] 技術的に正確
- [ ] style-guide.md に準拠
- [ ] plan.md の目的を達成
- [ ] 実行可能なコード例あり
- [ ] AI時代の視点あり

### Should Have (推奨)

- [ ] ワクワク感がある
- [ ] 初心者にも理解できる
- [ ] 前後のセクションとつながっている
- [ ] 適切な文字数（2000-4000）
- [ ] 図の説明が適切

### Nice to Have (あれば良い)

- [ ] 演習問題がある
- [ ] 参考リソースが豊富
- [ ] AIプロンプト例が実用的
- [ ] コラムや補足が充実

## Example Review Session

### Input

```
セクション: 3.1 詠唱（プロンプト）による具現化
内容: [3200文字の草稿]
```

### Agent Feedback

```markdown
## Strengths

1. **魅力的な導入**: 「詠唱」という比喩が効果的
2. **実践的なコード例**: 実際に動くプロンプト例が良い

## Improvements Needed

### High Priority

1. **技術的正確性**: プロンプトエンジニアリングの説明が古い
   - Suggestion: 2025年の最新手法に更新

### Medium Priority

2. **文字数**: 現在2100文字、やや薄い
   - Suggestion: ハンズオンセクションを拡充

## Overall Assessment

Quality Score: 7/10
Recommendation: High priorityを修正後、再レビュー
```

### Human Action

1. 技術的正確性を修正
2. ハンズオンを追加（800文字）
3. 再レビューを依頼

### Second Review

```markdown
## Improvements Confirmed

✓ 技術的正確性: 最新手法に更新済み
✓ 文字数: 2900文字に増加

## Overall Assessment

Quality Score: 8.5/10
Recommendation: 完成として良い
```

### Final Action

`progress.md` を ✅ 完成 に更新

## Related Workflows

- `draft.md` - 草稿生成
- `plan-next.md` - 次のタスク決定
- `refine.md` - 完成後の磨き込み（全体の整合性チェック）

## Tips

### 効率的なレビュー

1. **段階的に**: 一度に全てを完璧にしようとしない
2. **優先順位**: High → Medium → Low の順で対応
3. **反復**: 大きな改善は複数回に分ける

### レビューのタイミング

1. **草稿直後**: 構造と方向性の確認
2. **修正後**: 詳細な品質チェック
3. **完成前**: 最終確認

### 人間の判断が重要

AIの提案は参考情報。最終判断は人間が行う。

- 本書の独自性を損なう提案は却下
- 読者への共感は人間の感覚で判断
- 実験的な表現は積極的に残す
