from dataclasses import dataclass, field

@dataclass
class Finding:
    row_number: int
    data: dict[str, str]
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def finding_id(self) -> str:
        return self.data.get("id", "").strip()

    @property
    def status(self) -> str:
        return self.data.get("implementation_status", "").strip().upper()
