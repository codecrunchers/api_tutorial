from flask import Flask, current_app, request
from flask_sqlalchemy import SQLAlchemy
import flask
import json
db = SQLAlchemy()




class Folder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Folder %r>' % self.name


from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    excludes = ["query", "query_class", "registry"]

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x not in self.excludes]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
    


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///tmp/test.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()



    @app.errorhandler(404)
    def page_not_found(error):
        return {"status":"Resource not found, are you sure e.g. the endpoint and id are correct"}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"status":"You have made an invalid request , check your paramaters and endpoint"}, 400


    @app.errorhandler(500)
    def internal_server_error(error):
        return {"status":"Unhandeled interal error, please report"}, 500

    def render(f):
        return  json.dumps(f ,cls=AlchemyEncoder)


    @app.route("/", methods=["GET"])
    def index():
        return "<h2>Test API</h2>"

    @app.route("/api/v1/folders", methods=["GET"])
    def query_all():
        folders = db.paginate(db.select(Folder))
        print(folders.items)
        response = {"status": folders.items}
        return render(response)

    @app.route("/api/v1/folders/<int:folder_id>", methods=["GET"])
    def query(folder_id):
        f = db.get_or_404(Folder, folder_id) # bug, validate int
        response = {"status": f}
        return render(response)

     
    @app.route("/api/v1/folders/<int:folder_id>", methods=["DELETE"])
    def delete(folder_id):
        f = db.get_or_404(Folder, folder_id) # bug, validate int
        db.session.delete(f)
        db.session.commit()
        response = {"status": f}
        return render(response)

    @app.route("/api/v1/folders", methods=["POST", "PUT"])
    def server_request():
        if flask.request.method == 'POST':
            payload = request.json
            f = Folder(name=payload["folder_name"])            
            db.session.add(f)
        elif flask.request.method == 'PUT':
            payload = request.json
            folder_name = payload.get("folder_name")
            id = payload.get("id")
            f = db.get_or_404(Folder, id)
            f.name = folder_name        
            db.session.add(f)
        
        db.session.commit()
        response = {"status": f}
        return render(response)


    return app

if __name__ == "__main__":
    app =create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


