from __future__ import annotations

import random
from collections import defaultdict

from .models import RemediationAction, TrainingSummary


class PrioritizedReplayBuffer:
    def __init__(self) -> None:
        self._items: list[tuple[float, tuple[str, RemediationAction, float, str]]] = []

    def add(self, priority: float, transition: tuple[str, RemediationAction, float, str]) -> None:
        self._items.append((priority, transition))
        self._items.sort(key=lambda item: item[0], reverse=True)
        self._items = self._items[:250]

    def sample(self, size: int) -> list[tuple[str, RemediationAction, float, str]]:
        if not self._items:
            return []
        top = self._items[: min(size, len(self._items))]
        return [item[1] for item in top]


class MeshRemediationAgent:
    def __init__(self) -> None:
        self.actions = list(RemediationAction)
        self.q_values: dict[str, dict[RemediationAction, float]] = defaultdict(lambda: defaultdict(float))
        self.buffer = PrioritizedReplayBuffer()
        self.random = random.Random(12)

    def encode_state(self, severity: float, freshness_ratio: float, criticality: int) -> str:
        sev_bucket = min(int(severity // 20), 4)
        freshness_bucket = min(int(freshness_ratio), 4)
        crit_bucket = min(max(criticality // 2, 1), 5)
        return f"s{sev_bucket}-f{freshness_bucket}-c{crit_bucket}"

    def best_action(self, state: str) -> RemediationAction:
        scores = self.q_values[state]
        if not scores:
            return RemediationAction.ALERT_HUMAN
        return max(self.actions, key=lambda action: scores[action])

    def train(self, episodes: int = 120) -> TrainingSummary:
        histogram = {action.value: 0 for action in self.actions}
        rewards: list[float] = []

        for _ in range(episodes):
            severity = self.random.uniform(18, 98)
            freshness_ratio = self.random.uniform(0.5, 4.5)
            criticality = self.random.randint(3, 10)
            state = self.encode_state(severity, freshness_ratio, criticality)
            action = self.random.choice(self.actions) if self.random.random() < 0.28 else self.best_action(state)
            reward = self._reward(action, severity, freshness_ratio, criticality)
            next_state = self.encode_state(max(8, severity - reward / 4), max(0.2, freshness_ratio - reward / 20), criticality)
            histogram[action.value] += 1
            rewards.append(reward)
            self.buffer.add(abs(reward), (state, action, reward, next_state))
            self._replay()

        average_reward = round(sum(rewards) / max(len(rewards), 1), 3)
        return TrainingSummary(episodes=episodes, average_reward=average_reward, action_histogram=histogram)

    def _reward(self, action: RemediationAction, severity: float, freshness_ratio: float, criticality: int) -> float:
        if action == RemediationAction.BACKFILL:
            return 20 + freshness_ratio * 3 + criticality - severity * 0.1
        if action == RemediationAction.REBUILD:
            return 24 + criticality * 1.2 - severity * 0.08
        if action == RemediationAction.USE_FALLBACK:
            return 16 + severity * 0.03 + criticality * 0.5
        if action == RemediationAction.ROLLBACK:
            return 14 + severity * 0.02
        if action == RemediationAction.ALERT_HUMAN:
            return 12 + criticality * 0.8 - severity * 0.04
        if action == RemediationAction.SKIP:
            return -12 - severity * 0.08
        return -4

    def _replay(self) -> None:
        alpha = 0.18
        gamma = 0.82
        for state, action, reward, next_state in self.buffer.sample(12):
            next_best = max((self.q_values[next_state][candidate] for candidate in self.actions), default=0.0)
            current = self.q_values[state][action]
            self.q_values[state][action] = current + alpha * (reward + gamma * next_best - current)

