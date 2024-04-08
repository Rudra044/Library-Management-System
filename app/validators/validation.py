def check_user_required_fields(data):
        required_fields = ["email_id", "password"]
        for field in required_fields:
            if field not in data:
                return False
        return True


def check_book_required_fields(data):
        required_fields = ["title", "author", "isbn", "genre"]
        for field in required_fields:
            if field not in data:
                return False
        return True


def check_author_required_fields(data):
        required_fields = ["author_name", "biography", "nationality"]
        for field in required_fields:
            if field not in data:
                return False
        return True