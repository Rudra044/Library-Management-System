def success_response(data=None, message="Success", detail=None):
    response = {
        "data": data,
        "message": message,
        "detail": detail or message,
        "status": True
    }
    return response


