"""QuestForge Streamlit Web UI

StreamlitベースのWebインターフェースです。
タスク管理をRPG風に楽しく視覚化します。
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from uuid import UUID

# questforgeパッケージをインポート可能にする
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from questforge.domain.entities.quest import QuestCategory, DifficultyLevel, QuestStatus
from questforge.infrastructure.persistence.json_repository import (
    JSONQuestRepository,
    JSONHeroRepository,
    JSONBadgeRepository,
)
from questforge.cli.commands import QuestForgeCLI


# ページ設定
st.set_page_config(
    page_title="QuestForge",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# カスタムCSS
st.markdown("""
<style>
    .quest-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 2px solid #e0e0e0;
    }
    .quest-available { background-color: #f0f4ff; border-color: #4a90e2; }
    .quest-in-progress { background-color: #fff9e6; border-color: #f5a623; }
    .quest-completed { background-color: #e8f5e9; border-color: #4caf50; }

    .hero-stats {
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    .level-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background-color: #ffd700;
        color: #000;
        border-radius: 1rem;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .rpg-map {
        padding: 2rem 1rem;
        background: linear-gradient(to bottom, #87CEEB 0%, #98D8C8 50%, #90EE90 100%);
        border-radius: 1rem;
        margin: 1rem 0;
        overflow-x: auto;
    }

    .map-path {
        display: flex;
        align-items: center;
        justify-content: space-around;
        min-width: 800px;
        padding: 1rem;
        position: relative;
    }

    .map-milestone {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        z-index: 2;
    }

    .milestone-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }

    .milestone-label {
        font-weight: bold;
        color: #333;
        background: rgba(255,255,255,0.9);
        padding: 0.25rem 0.5rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
    }

    .milestone-locked {
        opacity: 0.3;
    }

    .milestone-current {
        animation: bounce 1s infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .map-path::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(to right, #4caf50, #ffd700, #ff9800, #f44336, #9c27b0);
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """セッション状態を初期化"""
    if 'quest_repo' not in st.session_state:
        st.session_state.quest_repo = JSONQuestRepository("data/quests.json")
    if 'hero_repo' not in st.session_state:
        st.session_state.hero_repo = JSONHeroRepository("data/heroes.json")
    if 'badge_repo' not in st.session_state:
        st.session_state.badge_repo = JSONBadgeRepository("data/badges.json")
    if 'cli' not in st.session_state:
        st.session_state.cli = QuestForgeCLI(
            st.session_state.quest_repo,
            st.session_state.hero_repo
        )
    if 'current_hero_id' not in st.session_state:
        st.session_state.current_hero_id = None


def get_current_hero():
    """現在のヒーローを取得"""
    if st.session_state.current_hero_id:
        return st.session_state.hero_repo.find_by_id(st.session_state.current_hero_id)
    return None


def difficulty_color(difficulty: DifficultyLevel) -> str:
    """難易度に応じた色を返す"""
    colors = {
        DifficultyLevel.TRIVIAL: "green",
        DifficultyLevel.EASY: "blue",
        DifficultyLevel.NORMAL: "orange",
        DifficultyLevel.HARD: "red",
        DifficultyLevel.EPIC: "purple",
    }
    return colors.get(difficulty, "gray")


def status_emoji(status: QuestStatus) -> str:
    """ステータスに応じた絵文字を返す"""
    emojis = {
        QuestStatus.AVAILABLE: "📋",
        QuestStatus.IN_PROGRESS: "⚔️",
        QuestStatus.COMPLETED: "✅",
        QuestStatus.FAILED: "❌",
        QuestStatus.CANCELLED: "🚫",
    }
    return emojis.get(status, "❓")


def render_rpg_map(hero):
    """RPGマップを表示"""
    if not hero:
        return

    # レベルに応じたマイルストーン
    milestones = [
        {"level": 1, "icon": "🏠", "label": "スタート"},
        {"level": 2, "icon": "🌳", "label": "森の入口"},
        {"level": 3, "icon": "⛰️", "label": "山道"},
        {"level": 5, "icon": "🏰", "label": "城下町"},
        {"level": 7, "icon": "🗻", "label": "高い山"},
        {"level": 10, "icon": "🏛️", "label": "古代神殿"},
        {"level": 15, "icon": "🌋", "label": "火山"},
        {"level": 20, "icon": "👑", "label": "王国"},
    ]

    current_level = hero.level

    map_html = '<div class="rpg-map"><div class="map-path">'

    for milestone in milestones:
        level = milestone["level"]
        icon = milestone["icon"]
        label = milestone["label"]

        # 現在地、到達済み、未到達の判定
        if level == current_level:
            css_class = "milestone-current"
            display_icon = "⚔️"  # ヒーローアイコン
        elif level < current_level:
            css_class = ""
            display_icon = "✅"  # 到達済み
        else:
            css_class = "milestone-locked"
            display_icon = icon

        map_html += f'<div class="map-milestone {css_class}"><div class="milestone-icon">{display_icon}</div><div class="milestone-label">Lv.{level}<br>{label}</div></div>'

    map_html += '</div></div>'

    st.markdown(map_html, unsafe_allow_html=True)


def render_hero_stats(hero):
    """ヒーローの統計情報を表示"""
    if not hero:
        return

    quests = st.session_state.quest_repo.find_by_hero_id(hero.id)
    completed = len([q for q in quests if q.status == QuestStatus.COMPLETED])
    in_progress = len([q for q in quests if q.status == QuestStatus.IN_PROGRESS])

    progress = hero.get_level_progress()
    exp_needed = hero.get_exp_to_next_level()

    st.markdown(f"""
    <div class="hero-stats">
        <h2>⚔️ {hero.name}</h2>
        <p><span class="level-badge">Lv.{hero.level}</span></p>
        <p>💎 総経験値: {hero.total_experience:,}</p>
        <p>🔥 連続達成: {hero.current_streak}日 (最高: {hero.best_streak}日)</p>
        <p>📊 クエスト: {completed}個完了、{in_progress}個進行中</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress, text=f"レベル {hero.level} → {hero.level + 1} (残り{exp_needed} XP)")


def render_quest_card(quest):
    """クエストカードを表示"""
    status_class = f"quest-{quest.status.value.replace('_', '-')}"
    difficulty_col = difficulty_color(quest.difficulty)

    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f"""
        <div class="quest-card {status_class}">
            <h3>{status_emoji(quest.status)} {quest.title}</h3>
            <p>{quest.description}</p>
            <p><span style="color: {difficulty_col};">⭐ {quest.difficulty.name}</span> | 💎 {quest.experience_points} XP</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if quest.status == QuestStatus.AVAILABLE:
            if st.button("▶️ 開始", key=f"start_{quest.id}"):
                try:
                    st.session_state.cli.start_quest(quest.id)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        elif quest.status == QuestStatus.IN_PROGRESS:
            if st.button("✅ 完了", key=f"complete_{quest.id}"):
                try:
                    st.session_state.cli.complete_quest(quest.id)
                    st.success("クエスト完了！ 🎉")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))


def main():
    """メインアプリケーション"""
    init_session_state()

    st.title("⚔️ QuestForge")
    st.markdown("*タスク管理をRPG風に楽しもう！*")

    # サイドバー
    with st.sidebar:
        st.header("🎮 ヒーロー管理")

        heroes = st.session_state.hero_repo.list_all()

        if not heroes:
            st.info("まずはヒーローを作成しましょう！")

            with st.form("create_hero"):
                st.subheader("✨ ヒーロー作成")
                name = st.text_input("名前", placeholder="アリス・ザ・アルケミスト")
                email = st.text_input("メールアドレス", placeholder="alice@example.com")
                submit = st.form_submit_button("作成")

                if submit and name and email:
                    try:
                        st.session_state.cli.create_hero(name, email)
                        heroes = st.session_state.hero_repo.list_all()
                        st.session_state.current_hero_id = heroes[0].id
                        st.success(f"ヒーローを作成しました: {name}")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
        else:
            # ヒーロー選択
            hero_names = {hero.id: hero.name for hero in heroes}
            selected_id = st.selectbox(
                "ヒーローを選択",
                options=list(hero_names.keys()),
                format_func=lambda x: hero_names[x],
                index=0 if not st.session_state.current_hero_id else list(hero_names.keys()).index(st.session_state.current_hero_id)
            )
            st.session_state.current_hero_id = selected_id

            st.divider()

            # 新規ヒーロー作成
            with st.expander("➕ 新しいヒーローを追加"):
                with st.form("add_hero"):
                    name = st.text_input("名前")
                    email = st.text_input("メールアドレス")
                    submit = st.form_submit_button("作成")

                    if submit and name and email:
                        try:
                            st.session_state.cli.create_hero(name, email)
                            st.success(f"ヒーローを作成しました: {name}")
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))

    # メインコンテンツ
    hero = get_current_hero()

    if not hero:
        st.warning("ヒーローを選択またはしてください")
        return

    # RPGマップ表示
    st.subheader("🗺️ 冒険の旅路")
    render_rpg_map(hero)

    # ヒーロー統計
    render_hero_stats(hero)

    # タブ
    tab1, tab2, tab3 = st.tabs(["📋 クエスト一覧", "➕ 新しいクエスト", "📊 統計"])

    with tab1:
        st.header("クエスト一覧")

        # フィルター
        filter_status = st.multiselect(
            "ステータスで絞り込み",
            options=[s.value for s in QuestStatus],
            default=["available", "in_progress"]
        )

        quests = st.session_state.quest_repo.find_by_hero_id(hero.id)
        filtered_quests = [q for q in quests if q.status.value in filter_status]

        if not filtered_quests:
            st.info("クエストが見つかりません。最初のクエストを作成しましょう！")
        else:
            for quest in sorted(filtered_quests, key=lambda q: (q.status.value, -q.experience_points)):
                render_quest_card(quest)

    with tab2:
        st.header("新しいクエスト作成")

        with st.form("create_quest"):
            title = st.text_input("タイトル", placeholder="プロローグを書く")
            description = st.text_area("説明", placeholder="教科書のプロローグ章を執筆する")

            col1, col2 = st.columns(2)

            with col1:
                category = st.selectbox(
                    "カテゴリ",
                    options=[c.value for c in QuestCategory],
                    format_func=lambda x: x.upper()
                )

            with col2:
                difficulty = st.selectbox(
                    "難易度",
                    options=[d.name for d in DifficultyLevel],
                )

            due_days = st.number_input("期限（日数）", min_value=0, max_value=365, value=7, help="0 = 期限なし")

            submit = st.form_submit_button("⚔️ クエスト作成")

            if submit and title:
                try:
                    st.session_state.cli.create_quest(
                        hero.id,
                        title=title,
                        description=description,
                        category=category,
                        difficulty=difficulty.lower(),
                        due_days=due_days if due_days > 0 else None
                    )
                    st.success(f"クエストを作成しました: {title}")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    with tab3:
        st.header("統計")

        quests = st.session_state.quest_repo.find_by_hero_id(hero.id)

        # 統計情報
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("総クエスト数", len(quests))

        with col2:
            completed = len([q for q in quests if q.status == QuestStatus.COMPLETED])
            st.metric("完了", completed)

        with col3:
            in_progress = len([q for q in quests if q.status == QuestStatus.IN_PROGRESS])
            st.metric("進行中", in_progress)

        with col4:
            completion_rate = (completed / len(quests) * 100) if quests else 0
            st.metric("完了率", f"{completion_rate:.1f}%")

        st.divider()

        # 難易度別の統計
        st.subheader("難易度別クエスト数")
        difficulty_counts = {}
        for d in DifficultyLevel:
            count = len([q for q in quests if q.difficulty == d])
            if count > 0:
                difficulty_counts[d.name] = count

        if difficulty_counts:
            st.bar_chart(difficulty_counts)


if __name__ == "__main__":
    main()
