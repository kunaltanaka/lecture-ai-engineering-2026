"""第3回 発展(a): 演習の学習支援エージェントを、エージェントを組み立てる部分だけ ADK で書き直したもの。

INSTRUCTIONS と tools.py のツールは app/ のものをそのまま使う。
動かし方（リポジトリの直下で）:
    PYTHONPATH=. uv run --with google-adk adk run adk_agent/glossary_agent
"""

import os

from google.adk.agents import Agent

from app import tools
from app.agent import INSTRUCTIONS

# 既定は演習と同じ Gemini。環境変数 LOCAL_LLM_BASE があるときだけ、OpenAI 互換のローカル LLM を LiteLLM 経由で呼ぶ
# （Gemini の API キーが無い環境で動作を確かめるため。提出時は Gemini で動く）。
if os.getenv("LOCAL_LLM_BASE"):
    from google.adk.models.lite_llm import LiteLlm

    MODEL = LiteLlm(
        model="openai/" + os.environ["LOCAL_LLM_MODEL"],
        api_base=os.environ["LOCAL_LLM_BASE"],
        api_key="local",
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
else:
    MODEL = "gemini-3.5-flash-lite"

root_agent = Agent(
    model=MODEL,
    name="glossary_agent",
    instruction=INSTRUCTIONS,
    tools=[tools.search_glossary, tools.get_lecture_summary],
)
