from dataclasses import dataclass
from typing import Literal

Decision = Literal["allow", "deny", "ask"]

@dataclass
class PermissionDecision:
    decision: Decision
    reason: str
