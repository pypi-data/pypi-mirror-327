from enum import Enum


class GetSettingsResponse200AiResourceProvider(str, Enum):
    ANTHROPIC = "anthropic"
    CUSTOMAI = "customai"
    DEEPSEEK = "deepseek"
    GROQ = "groq"
    MISTRAL = "mistral"
    OPENAI = "openai"
    OPENROUTER = "openrouter"

    def __str__(self) -> str:
        return str(self.value)
