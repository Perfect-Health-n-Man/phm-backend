from app.ai.factory import BaseChatFactory
from .model import Judgement
from app.chat.agent.model import State, Agent


class CheckFactory(BaseChatFactory):
    def __init__(self, session_id: str) -> None:
        super().__init__("checkAnswer", Judgement, session_id)

    async def create_ans(self, state: State) -> dict[str, str | bool]:
        agent_options = "\n".join([f"{k}. {v['name']}: {v['description']}" for k, v in Agent.items()])
        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        result: Judgement = chain.invoke(
            input={
                "agent_options": agent_options,
                "chat_history": state.history,
                "user_message": state.user_message,
                "answer": state.messages[-1].to_str(),
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        if result.judge or state.loop>0:
            return {
                "current_judge": True,
                "judgement_reason": result.reason
            }
        else:
            return {
                "current_judge": result.judge,
                "judgement_reason": result.reason,
                "loop": state.loop+1,
            }