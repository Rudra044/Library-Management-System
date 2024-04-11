def success_response(code=None, message="Success", detail=None,data=None):
    response = {
        "code":code,
        "data": data,
        "message": message,
        "detail": detail or message,
        "status": True
    }
    return response


