def register_or_update_user(user_doc_ref, user_data):
    # {userId}ドキュメントをアップデートする（無ければ作成する）
    try:
        if user_doc_ref.get().to_dict() :
            user_doc_ref.update(user_data)
            return {'message': "User settings have been updated successfully."}, 200
        else:
            user_doc_ref.set(user_data)
            return {'message': "User registration completed successfully."}, 200
    except ValueError as e:
        return {'message': f"Invalid data format: {e}"}, 400
    except Exception as e:
        return {'message': f"An error occurred while saving or updating user data: {e}"}, 500

def get_user(user_doc_ref):
    try:
        user_data = user_doc_ref.get().to_dict()
        if user_data:
            return {
                "name": user_data["name"],
                "email": user_data["email"],
                "gender": user_data["gender"],
                "birthday": user_data["birthday"],
                "height": user_data["height"],
                "weight": user_data["weight"],
                "goals": user_data["goals"]
            },200
        else:
            return {"message": "User not found"}, 404
    except Exception as e:
        return {"message": f"An error occurred while getting user data: {e}"}, 500

def delete_user(user_doc_ref):
    # チャットデータは消してない
    try:
        if not user_doc_ref.get().to_dict() :
            return {"message":"User does not exist"}, 404
        else:
            user_doc_ref.delete()
            return {"message":"User settings have been successfully deleted"}, 200
    except Exception as e:
        return {"message":f"An error occurred while deleting user data: {e}"}, 500
