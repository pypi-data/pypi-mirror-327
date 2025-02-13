"""Reward models for evaluating responses."""

from databricks.kie.research_common.reward_model_utils import DEFAULT_CONTEXT_REWARD_MODEL_ID, generate_reward_rating


class RewardModel():
    """Model that assigns a reward to a response."""

    def __call__(self, prompt: str, response: str) -> float:
        raise NotImplementedError()


class ContextRewardModel(RewardModel):
    """Reward model that gets reward score by prompting GPT."""

    def __init__(self, model_id: str = DEFAULT_CONTEXT_REWARD_MODEL_ID):
        self.model_id = model_id

    def __call__(self, prompt: str, response: str) -> float:
        return float(generate_reward_rating(prompt, response, self.model_id))
