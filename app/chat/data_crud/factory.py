import json

from app.ai.factory import BaseChatFactory
from .model import CRUDTask
from ..agent.model import State
from ..chat_dto import ChatDto
from app.firestore import client


class DataCRUDFactory(BaseChatFactory):
    def __init__(self, session_id) -> None:
        super().__init__("judgeCRUD", CRUDTask, session_id)

    async def create_ans(self, state: State) -> dict[str, list[ChatDto]]:
        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        user_data = await self.get_data(state.user_id)
        result: CRUDTask = await chain.ainvoke(
            input={
                "datetimeNow": state.datetimeNow,
                "chat_history": state.history,
                "user_message": state.user_message,
                "user_data": json.dumps(user_data, indent=2),
                "user_id": state.user_id,
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        ans = await self.data_crud(result)
        return {"messages": [ans]}

    @staticmethod
    async def get_data(user_id: str) -> dict:
        data = await client.document("users/" + user_id).get()
        return data.to_dict()

    def update_nested_dict(self, data, path, new_value):
        if len(path) == 1:
            if type(new_value) is dict:
                data[path[0]].update(new_value)
            else:
                data[path[0]] = new_value
            return data
        if path[0] not in data:
            data[path[0]] = {}
        data[path[0]] = self.update_nested_dict(data[path[0]], path[1:], new_value)
        return data

    def delete_nested_dict(self, data, path):
        if len(path) == 1:
            if path[0] in data:
                del data[path[0]]
            return data
        if path[0] in data and isinstance(data[path[0]], dict):
            data[path[0]] = self.delete_nested_dict(data[path[0]], path[1:])
            # 空の辞書を削除する場合は以下のコメントを解除
            if not data[path[0]]:
                del data[path[0]]
        return data

    async def data_crud(
            self,
            result: CRUDTask,
        ) -> ChatDto:
        answer = result.answer
        operation = result.operation
        document_path = result.document_path
        data_path = result.data_path
        contents = json.loads(result.contents)
        try:
            doc_ref = await client.document(document_path).get()
            data = doc_ref.to_dict()
            if contents not in ["", dict()]:
                data = self.update_nested_dict(data, data_path, contents)
        except Exception:
            return ChatDto(answer="データの操作に失敗しました。もう一度試してください。", form=[])
        match operation:
            case "CREATE":
                await client.document(document_path).set(data)
                answer += "\n\nデータを作成しました。"
            case "READ":
                answer += "\n\n取得したデータ:\n" + json.dumps(data, indent=2)
            case "UPDATE":
                await client.document(document_path).set(data)
                answer += "\n\nデータを更新しました。"
            case "DELETE":
                data = self.delete_nested_dict(data, data_path)
                await client.document(document_path).set(data)
                answer += "\n\nデータを削除しました。"
            case _:
                answer="そのデータの操作は制限されています。"
        return ChatDto(answer=answer, form=[])
