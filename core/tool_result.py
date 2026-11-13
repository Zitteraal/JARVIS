from dataclasses import dataclass

@dataclass(frozen=True)
class ToolResult:
    status: str
    message: str

    @classmethod
    def success(cls, message: str, verified: bool = True) -> "ToolResult":
        return cls("success" if verified else "unverified", message)

    @classmethod
    def failure(cls, message: str) -> "ToolResult":
        return cls("failed", message)

    def to_llm_string(self) -> str:
        if self.status == "success": return f"SUCCESS (verified): {self.message}"
        elif self.status == "unverified": return f"UNVERIFIED: {self.message}"
        else: return f"FAILED: {self.message}"