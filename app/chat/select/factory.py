from app.ai.factory import BaseChatFactory
from app.chat.agent.model import State, Agent
from app.chat.select.model import SelectAgent, get_one_token_model


class SelectAgentFactory(BaseChatFactory):
    def __init__(self, session_id: str) -> None:
        super().__init__("selectAgent", SelectAgent, session_id)
        self.model = get_one_token_model()

    async def create_ans(self, state: State) -> dict[str, int]:
        agent_options = "\n".join([f"{k}. {v['name']}: {v['description']}" for k, v in Agent.items()])
        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        result: SelectAgent = await chain.ainvoke(
            input={
                "agent_options": agent_options,
                "chat_history": state.history,
                "user_message": state.user_message
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"current_agent": result.agent_number}