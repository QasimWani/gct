import openai
import os
from gct.constants import PROMPT
import textwrap

class CodeSummarizer:
    def __init__(self, decription_max_len: int = 50, temperature: float = 0.8):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        assert openai.api_key is not None, "You must set the environment variable OPENAI_API_KEY to enable function descriptions with gct"
        
        self.description_max_len = decription_max_len
        self.temperature = temperature


    def summarize(self, code: "list[str]") -> str:
        prompt = self._populate_prompt(code)
        description = self._text_completion(prompt)
        return "<BR />".join(textwrap.wrap(description, 42))

            
    def _text_completion(self, prompt: str) -> str:
        resp = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=self.description_max_len,
            temperature=self.temperature,
        )
        return resp["choices"][0]["text"].split("###")[0]
        
        
    def _populate_prompt(self, lines: "list[str]") -> str:
        assert "<function_code>" in PROMPT, "Prompt must contain a phrase <function_code> with which to populate function code"
        return PROMPT.replace("<function_code>", "\n".join(lines))