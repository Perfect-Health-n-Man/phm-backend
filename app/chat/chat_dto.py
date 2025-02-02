from quart import Response, jsonify

class ChatDto:
    answer: str
    form: list[str]
    def __init__(self, answer: str, form: list[str]):
        self.answer = answer
        self.form = form

    def to_json(self) -> Response:
        return jsonify({
            "answer": self.answer,
            "form": self.form
        })

    def to_str(self) -> str:
        return f"answer: {self.answer}\n\n" + "\n".join([f"{str(i + 1)}. {s}" for i, s in enumerate(self.form)])
