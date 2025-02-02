from app.chat.agent.model import State
from app.chat.check.model import Judgement
from app.chat.normal.model import AiAns
from app.chat.rag.model import AiRagAns
from app.chat.select.model import SelectAgent
from app.chat.tasks.model import Tasks

Response = Tasks | AiAns | AiRagAns | SelectAgent | Judgement | State