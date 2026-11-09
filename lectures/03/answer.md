# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：
- 1つの質問での LLM 呼び出し回数（`requests`）：
- 追加したツールと、docstring に書いた説明：

## 宿題

- 取り組んだレベル：発展（a）ADK で書き直す
- やったこと：`adk_agent/glossary_agent/` に `__init__.py`（`from . import agent`）と `agent.py` を作った。`INSTRUCTIONS` と `search_glossary`・`get_lecture_summary` は `app/` のものをそのまま使い、ADK の `Agent(model, name, instruction, tools)` でエージェントを組み立てた。`app/`、`pyproject.toml`、`uv.lock` は変えていない。`adk run adk_agent/glossary_agent` で動かし、演習と同じ質問を 2 つ投げた。
  - 実行環境：Gemini の API キーを使わず、desktopkunal のローカルLLM（`swift-1.5-27b-sym.mq4`）で動かした。`agent.py` は、環境変数 `LOCAL_LLM_BASE` があるときだけ `LiteLlm`（OpenAI 互換）でローカルLLMを呼び、無いときは既定の `gemini-3.5-flash-lite` を使う。起動は `PYTHONPATH=. uv run --with google-adk --with litellm adk run ...`。Gemini 側の経路は、API キーは通ったが前払いクレジット切れ（402 RESOURCE_EXHAUSTED）で、動作を確認できなかった。
  - 比べたのは、ADK 版と演習の Pydantic AI 版（`app.agent`）を、同じローカルLLMで動かした結果。ADK 側には推論オフ（`enable_thinking=False`）を指定したが、Pydantic AI 側は既定のままで、条件がそろっていない。
- 結果：
  - **書き方の違い**：Pydantic AI は `Agent(instructions=...)` を作り、`agent.tool_plain(関数)` で後からツールを登録し、モデルは `run_sync(..., model=)` で実行時に渡す。ADK は `Agent(model=, name=, instruction=, tools=[関数, ...])` に全部を 1 回で渡し、モデルも最初に決める。ADK は `name` が必須で、フォルダ名・`root_agent` という名前・`__init__.py` の 1 行といった決まりごとがある（`adk run` がそれを探す）。ツールは、どちらも普通の Python 関数（型ヒントと docstring がそのままツール定義になる）で、書き換えずに使えた。
  - **ツール呼び出しは同じ**：「宿題の3レベル」は `search_glossary(query='3レベル')` を 1 回、「LoRAとQLoRAの違いは？」は `search_glossary('LoRA')` と `search_glossary('QLoRA')` を 1 つずつ。どちらの質問でも、2 つのフレームワークで同じだった（同じ指示とツールなら、モデルの選ぶ動きは同じ）。
  - **回答の違い**：「3レベル」はどちらも、基礎・実装・発展で、どれか 1 つ取り組めば完了、採点は原則なし、第1回、と同じ内容だった。Pydantic AI 版には「`answer-md` を参照」という、用語集にない補足が付いた。LoRA/QLoRA は、どちらも表で違いを示し、第2回の扱いと補足（ランク r）まで書いた。ADK 版の末尾は「📖 関連：第2回」、Pydantic AI 版は「📌 関連：第2回」で、形式が少し違った。
  - **見えにくさの違い**：`--trace` のような表示は ADK の `adk run` にはなく、ツール呼び出しはイベント（`function_call`）を自分で読まないと見えなかった。
- 気づき・疑問：
  - 指示とツールを共通にしておくと、フレームワークを替えても、ふるまいはほとんど変わらなかった。ふるまいを決めているのは、フレームワークより指示・ツールの docstring・モデルだと分かる。
  - 回答の違いが、フレームワークの違いなのか、推論オフなどの設定やゆらぎなのかは、1 回ずつの実行では区別できなかった。
  - ADK のモデル指定は `LiteLlm` で他のモデルに替えられたが、Gemini 以外では `litellm` を足す必要がある。Gemini 側は上のとおり 402 で確認できていないので、そちらの動作は未確認。
