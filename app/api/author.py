from flask import Flask, request, jsonify, Blueprint
from flask_migrate import Migrate
from app.models.models import db, Author
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.utils import new_add, delete, update_details

bp = bp = Blueprint('autho', __name__, url_prefix='/auth')

@bp.route('/author/add', methods=['POST'])
@jwt_required()
def add_author():
    user_id = get_jwt_identity()
    data = request.json
    author_name = data.get('author_name')
    biography = data.get('biography')
    nationality = data.get('nationality') 
    if author_name and biography:
        if Author.query.filter(db.and_(Author.profile_id == user_id, Author.author_name == author_name 
                                    , Author.biography == biography)).first():
            return jsonify({'error':'Author is already added by you.'}),400
        else:
             
            new_author = Author(author_name=author_name, biography=biography, nationality=nationality
                        ,profile_id=user_id)
            new_add(new_author)
            
            return jsonify({'message': 'New author added'})
    else:
        return jsonify({'error': 'Provide valid fields' }),400
    

@bp.route('/author', defaults={'author_id': None}, methods=['GET'])
@bp.route('/author/<int:author_id>', methods=['GET'])
def get_author(author_id=None): 
    if author_id is None:
        all_authors = Author.query.all()
        author_list = []
        for author in all_authors:
            author_list.append({
                 'id': author.id,
                 'author_name': author.author_name, })
        return jsonify(author_list)
    author_details = Author.query.get(author_id)
    if author_details:
        return jsonify({
            'id': author_details.id,
            'author_name': author_details.author_name,
            'biography': author_details.biography,
            'nationality': author_details.nationality, })
    else:
        return jsonify({'error': 'Author not found'}),404
    

@bp.route('/author/delete', defaults={'author_id': None}, methods=['DELETE'])
@bp.route('/author/delete/<int:author_id>', methods=['DELETE'])
@jwt_required()
def delete_author_details(author_id):
    user_id = get_jwt_identity()
    if author_id is None:
        authors = Author.query.filter(Author.profile_id == user_id).all()
        for author in authors:
            delete(author)
        return jsonify({'message': 'All authors added by you are deleted.'})
    author = Author.query.filter(db.and_(Author.profile_id == user_id, Author.id == author_id)).first()
    if author:
        delete(author)
        return jsonify({'message': 'Author Details deleted'})
    else:
        return jsonify({'error': 'Author is not added by you.'}),400


@bp.route('/author/update/<int:author_id>', methods=['PATCH'])
@jwt_required()
def update_author_details(author_id):
    user_id = get_jwt_identity()
    data = request.json
    author_name = data.get('author_name')
    biography = data.get('biography')
    nationality = data.get('nationality')

    author = Author.query.filter(db.and_( Author.profile_id == user_id, Author.id == author_id )).first()
    if not author:
        return jsonify({'error':'Book is not present.'}),404
    
    if author_name:
        author.author_name = author_name
    if biography:
        author.biography = biography
    if nationality:
        author.nationality = nationality
    update_details()
    return jsonify({'message': 'Author details updated successfully'})