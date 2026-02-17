from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Session:
    active: bool = False
    total_income: float = 0.0
    total_commission: float = 0.0
    entries: List[Dict] = field(default_factory=list)


class SessionStorage:
    def __init__(self):
        self._store: Dict[int, Session] = {}

    def start_session(self, chat_id: int) -> bool:
        s = self._store.setdefault(chat_id, Session())
        if s.active:
            return False
        s.active = True
        s.total_income = 0.0
        s.total_commission = 0.0
        s.entries.clear()
        return True

    def finish_session(self, chat_id: int):
        s = self._store.get(chat_id)
        if not s or not s.active:
            return None
        summary = {
            'total_income': s.total_income,
            'total_commission': s.total_commission,
            'profit': s.total_income - s.total_commission,
        }
        s.active = False
        s.total_income = 0.0
        s.total_commission = 0.0
        s.entries.clear()
        return summary

    def is_active(self, chat_id: int) -> bool:
        s = self._store.get(chat_id)
        return bool(s and s.active)

    def add_entry(self, chat_id: int, income: float, commission: float) -> bool:
        s = self._store.setdefault(chat_id, Session())
        if not s.active:
            return False
        s.entries.append({'income': income, 'commission': commission})
        s.total_income += income
        s.total_commission += commission
        return True


storage = SessionStorage()
