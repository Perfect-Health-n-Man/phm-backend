class User:
    name: str
    email: str
    gender: str
    birthday: str
    height: int
    weight: int
    goals: list[str]

    def __init__(self, name: str, email: str, gender: str, birthday: str, height: int, weight: int, goals: list[str]):
        self.name = name
        self.email = email
        self.gender = gender
        self.birthday = birthday
        self.height = height
        self.weight = weight
        self.goals = goals

    def to_dict(self):
        return {
            "user_info": {
                "name": self.name,
                "email": self.email,
                "gender": self.gender,
                "birthday": self.birthday,
                "height": self.height,
                "weight": self.weight,
                "goals": self.goals,
            }
        }
    @staticmethod
    def from_json(json):
        return User(
            name = json["name"],
            email = json["email"],
            gender = json["gender"],
            birthday = json["birthday"],
            height = json["height"],
            weight = json["weight"],
            goals = json["goals"],
        )