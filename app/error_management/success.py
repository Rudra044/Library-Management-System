def success_response(code=None, message="Success", detail=None,id=None):
    response = {
        "code":code,
        "id": id,
        "message": message,
        "detail": detail or message,
        "status": True
    }
    return response


