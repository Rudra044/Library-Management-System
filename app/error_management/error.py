def error_response(error_code, detail=None):

    category, actual_error = error_code[0], error_code[1:3]

    category_desc = error_category.get(category, 'Unknown Category')
    response = {
        "code": error_code[1:],
        "category": category_desc,
        "detail": detail,
        "status": False 
    }

    
    return response

error_category = {
    '0': 'Validation Error',
    '1': 'Internal Error',
}