from flask import Flask, request, jsonify, Blueprint
from flask_migrate import Migrate
from app.models.models import db, Author
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.utils import new_add, delete, update_details
from app.services.library_services import author_filter, author_id_all_filter, author_id_filter, author_all, author_get
from app.error_management.success import success_response
from app.error_management.error import error_response
from app.validators.validation import check_author_required_fields


bp = bp = Blueprint('autho', __name__, url_prefix='/auth')

@bp.route('/author/add', methods=['POST'])
@jwt_required()
def add_author():
    user_id = get_jwt_identity()
    data = request.json
    author_name = data.get('author_name')
    biography = data.get('biography')
    nationality = data.get('nationality') 
    if not check_author_required_fields(data):
         return error_response("0400",  'Mandatory fields need to be provided')

    if author_filter(user_id, author_name, biography):
        return error_response("0400", 'Author is already added by you.')
    else:
             
        new_author = Author(author_name=author_name, biography=biography, nationality=nationality
                        ,profile_id=user_id)
        new_add(new_author)
        return success_response(201, "Success", "New author added")
    

@bp.route('/author', defaults={'author_id': None}, methods=['GET'])
@bp.route('/author/<int:author_id>', methods=['GET'])
def get_author(author_id=None): 
    if author_id is None:
        all_authors = author_all()
        author_list = []
        for author in all_authors:
            author_list.append({
                 'id': author.id,
                 'author_name': author.author_name, })
        return jsonify(author_list)
    author_details = author_get(author_id)
    if author_details:
        return jsonify({
            'id': author_details.id,
            'author_name': author_details.author_name,
            'biography': author_details.biography,
            'nationality': author_details.nationality, })
    else:
        return error_response("0404", 'Author not found') 
    

@bp.route('/author/delete', defaults={'author_id': None}, methods=['DELETE'])
@bp.route('/author/delete/<int:author_id>', methods=['DELETE'])
@jwt_required()
def delete_author_details(author_id):
    user_id = get_jwt_identity()
    if author_id is None:
        authors = author_id_all_filter(user_id)
        for author in authors:
            delete(author)
            return success_response(200, "Success", "All authors added by you are deleted.")

    author = author_id_filter(user_id, author_id)
    if author:
        delete(author)
        return success_response(200, "Success", "Author Details deleted")

    else:
        return error_response("0404",  'Author not found') 


@bp.route('/author/update/<int:author_id>', methods=['PATCH'])
@jwt_required()
def update_author_details(author_id):
    user_id = get_jwt_identity()
    data = request.json
    author_name = data.get('author_name')
    biography = data.get('biography')
    nationality = data.get('nationality')

    author = author_id_filter(user_id, author_id)
    if not author:
        return error_response("0404",  'Author not found') 
    
    if author_name:
        author.author_name = author_name
    if biography:
        author.biography = biography
    if nationality:
        author.nationality = nationality
    update_details()
    return success_response(200, "Success", "Author details updated successfully")
