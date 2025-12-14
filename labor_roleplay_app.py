"""
労務相談ロールプレー訓練システム
人事労務担当者の対応力を向上させるための訓練アプリ
"""

import streamlit as st
import pyperclip
from prompt_templates import PROMPT_TEMPLATES, generate_prompt

# ページ設定
st.set_page_config(
    page_title="労務相談ロールプレー訓練システム",
    page_icon="👥",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    .template-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
        transition: box-shadow 0.3s;
    }
    .template-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .prompt-preview {
        background-color: #f0f0f0;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9rem;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }
    .custom-section {
        background-color: #fff;
        border: 2px dashed #1f77b4;
        border-radius: 8px;
        padding: 2rem;
        margin-top: 2rem;
    }
    .success-message {
        padding: 1rem;
        border-radius: 4px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = ""
if 'copy_success' not in st.session_state:
    st.session_state.copy_success = False

# ヘッダー
st.markdown('<div class="main-title">👥 労務相談ロールプレー訓練システム</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">人事労務担当者のスキル向上を支援します</div>', unsafe_allow_html=True)

# タブの作成
tab1, tab2, tab3 = st.tabs(["📋 テンプレート選択", "✏️ カスタム作成", "ℹ️ 使い方"])

# タブ1: テンプレート選択
with tab1:
    st.markdown("### 事前準備されたシナリオから選択")
    st.markdown("様々な労務相談のケースを用意しています。シナリオを選択してプロンプトを生成してください。")
    
    # カテゴリーでフィルタリング
    categories = ["すべて"] + list(set([t['category'] for t in PROMPT_TEMPLATES]))
    selected_category = st.selectbox("📁 カテゴリーで絞り込み", categories)
    
    # テンプレートの表示
    filtered_templates = PROMPT_TEMPLATES if selected_category == "すべて" else [
        t for t in PROMPT_TEMPLATES if t['category'] == selected_category
    ]
    
    cols_per_row = 2
    for i in range(0, len(filtered_templates), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(filtered_templates):
                template = filtered_templates[i + j]
                with col:
                    with st.container():
                        st.markdown(f"#### {template['title']}")
                        st.markdown(f"<span class='category-badge' style='background-color: #e3f2fd; color: #1976d2;'>{template['category']}</span>", unsafe_allow_html=True)
                        
                        with st.expander("詳細を見る"):
                            st.markdown("**相談内容:**")
                            st.write(template['consultation'])
                            st.markdown("**背景:**")
                            st.write(template['background'])
                            st.markdown("**相談者の態度:**")
                            st.write(template['attitude'])
                        
                        if st.button(f"このシナリオを選択", key=f"select_{i+j}", use_container_width=True):
                            st.session_state.selected_template = template
                            st.session_state.generated_prompt = generate_prompt(template)
                            st.session_state.copy_success = False
                            st.rerun()
    
    # 生成されたプロンプトの表示
    if st.session_state.generated_prompt:
        st.markdown("---")
        st.markdown("### 📝 生成されたプロンプト")
        
        if st.session_state.selected_template:
            st.info(f"選択中: **{st.session_state.selected_template['title']}**")
        
        # プロンプトプレビュー
        st.markdown('<div class="prompt-preview">' + st.session_state.generated_prompt.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)
        
        # コピーボタン
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("📋 クリップボードにコピー", use_container_width=True):
                try:
                    pyperclip.copy(st.session_state.generated_prompt)
                    st.session_state.copy_success = True
                    st.rerun()
                except:
                    st.warning("クリップボードへのコピーに失敗しました。下のテキストエリアから手動でコピーしてください。")
        
        with col2:
            if st.button("🗑️ クリア", use_container_width=True):
                st.session_state.selected_template = None
                st.session_state.generated_prompt = ""
                st.session_state.copy_success = False
                st.rerun()
        
        if st.session_state.copy_success:
            st.success("✅ クリップボードにコピーしました!AIチャットに貼り付けて使用してください。")
        
        # テキストエリアでも表示(手動コピー用)
        st.text_area("プロンプトテキスト(手動コピー用)", st.session_state.generated_prompt, height=200)

# タブ2: カスタム作成
with tab2:
    st.markdown("### オリジナルのシナリオを作成")
    st.markdown("独自の労務相談シナリオを作成できます。すべての項目を入力してプロンプトを生成してください。")
    
    with st.form("custom_prompt_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            custom_title = st.text_input("シナリオタイトル", placeholder="例: 突然の退職申し出への対応")
            custom_category = st.selectbox("カテゴリー", ["メンタルヘルス", "労働時間", "ハラスメント", "育児・介護", 
                                                         "退職・解雇", "賃金", "人事異動", "採用・試用期間", 
                                                         "職場環境", "休暇・休業", "安全衛生", "その他"])
        
        with col2:
            custom_attitude = st.text_input("相談者の態度", 
                                           placeholder="例: 不安が強く、涙ぐむこともあるが、具体的な事実は話せる")
        
        custom_consultation = st.text_area("相談内容", height=100,
                                          placeholder="例: メンタル不調で休職していたが復職したいです。主治医の診断書はもらっています。")
        
        custom_background = st.text_area("背景情報", height=100,
                                        placeholder="例: 二度目のメンタル不調休職のため、会社としてどうしてよいか悩んでいる。")
        
        submit_button = st.form_submit_button("プロンプトを生成", use_container_width=True)
        
        if submit_button:
            if all([custom_consultation, custom_background, custom_attitude]):
                custom_template = {
                    'title': custom_title or "カスタムシナリオ",
                    'category': custom_category,
                    'consultation': custom_consultation,
                    'background': custom_background,
                    'attitude': custom_attitude
                }
                st.session_state.selected_template = custom_template
                st.session_state.generated_prompt = generate_prompt(custom_template)
                st.session_state.copy_success = False
                st.success("✅ プロンプトを生成しました!下にスクロールして確認してください。")
            else:
                st.error("すべての必須項目を入力してください。")
    
    # カスタムプロンプトの表示
    if st.session_state.generated_prompt and st.session_state.selected_template:
        if st.session_state.selected_template.get('title') == custom_title or custom_title == "":
            st.markdown("---")
            st.markdown("### 📝 生成されたプロンプト")
            
            st.markdown('<div class="prompt-preview">' + st.session_state.generated_prompt.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 クリップボードにコピー", key="copy_custom", use_container_width=True):
                    try:
                        pyperclip.copy(st.session_state.generated_prompt)
                        st.session_state.copy_success = True
                        st.rerun()
                    except:
                        st.warning("クリップボードへのコピーに失敗しました。下のテキストエリアから手動でコピーしてください。")
            
            with col2:
                if st.button("🗑️ クリア", key="clear_custom", use_container_width=True):
                    st.session_state.selected_template = None
                    st.session_state.generated_prompt = ""
                    st.session_state.copy_success = False
                    st.rerun()
            
            if st.session_state.copy_success:
                st.success("✅ クリップボードにコピーしました!AIチャットに貼り付けて使用してください。")
            
            st.text_area("プロンプトテキスト(手動コピー用)", st.session_state.generated_prompt, height=200, key="custom_text_area")

# タブ3: 使い方
with tab3:
    st.markdown("### 📖 このシステムの使い方")
    
    st.markdown("""
    #### 🎯 目的
    このシステムは、人事労務担当者が労務相談に対応するスキルを向上させるための訓練ツールです。
    
    #### 📋 使用手順
    
    1. **シナリオを選択**
       - 「テンプレート選択」タブから事前準備されたシナリオを選択するか、
       - 「カスタム作成」タブで独自のシナリオを作成します。
    
    2. **プロンプトを生成**
       - 選択したシナリオから自動的にプロンプトが生成されます。
    
    3. **プロンプトをコピー**
       - 「クリップボードにコピー」ボタンをクリックしてプロンプトをコピーします。
    
    4. **AIチャットで実践**
       - コピーしたプロンプトをClaude等のAIチャットに貼り付けます。
       - AIが「相談者」役となり、あなたは「人事労務担当者」として対応します。
    
    5. **対話を進める**
       - 相談者からの質問や訴えに対して、適切に対応してください。
       - 法的知識だけでなく、共感力やコミュニケーションスキルも重要です。
    
    6. **評価を受ける**
       - 対話が終了すると、AIが「特定社会保険労務士」として
       - あなたの対応を法的観点とコミュニケーション観点から評価し、アドバイスを提供します。
    
    #### 💡 活用のポイント
    
    - **多様なシナリオで練習**: さまざまなケースを経験することで対応力が向上します
    - **繰り返し実践**: 同じシナリオでも異なるアプローチを試してみましょう
    - **評価を活かす**: AIからのフィードバックを次回の対応に活かしましょう
    - **カスタムシナリオ**: 実際に直面した(または直面しそうな)ケースで訓練できます
    
    #### ⚠️ 注意事項
    
    - このシステムは訓練用です。実際の労務相談では専門家に相談してください
    - 生成されたシナリオはフィクションです
    - 評価結果は参考情報として活用してください
    """)
    
    st.markdown("---")
    st.markdown("### 📊 用意されているカテゴリー")
    
    col1, col2, col3 = st.columns(3)
    categories_list = list(set([t['category'] for t in PROMPT_TEMPLATES]))
    
    for i, category in enumerate(categories_list):
        count = len([t for t in PROMPT_TEMPLATES if t['category'] == category])
        with [col1, col2, col3][i % 3]:
            st.markdown(f"**{category}** ({count}件)")

# サイドバー
with st.sidebar:
    st.markdown("### 📊 統計情報")
    st.metric("登録シナリオ数", len(PROMPT_TEMPLATES))
    st.metric("カテゴリー数", len(set([t['category'] for t in PROMPT_TEMPLATES])))
    
    st.markdown("---")
    st.markdown("### 🔗 関連リンク")
    st.markdown("- [労働基準法](https://elaws.e-gov.go.jp/document?lawid=322AC0000000049)")
    st.markdown("- [労働契約法](https://elaws.e-gov.go.jp/document?lawid=419AC0000000128)")
    st.markdown("- [厚生労働省](https://www.mhlw.go.jp/)")
    
    st.markdown("---")
    st.markdown("### ℹ️ バージョン情報")
    st.markdown("Version 1.0.0")
    st.markdown("© 2024 労務相談訓練システム")
