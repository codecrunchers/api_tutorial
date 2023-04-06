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
        return '<Folder %r>' % self.username


from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////test.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()


    @app.route("/", methods=["GET"])
    def index():
        return "<h2>Test API</h2>"

    @app.route("/folders", methods=["GET", "POST"])
    def server_request():
        if flask.request.method == 'POST':
            payload = request.json
            f = Folder(name=payload["folder_name"])            
            db.session.add(f)
            db.session.commit()
            return {"status": json.dumps(f, cls=AlchemyEncoder)}
        elif flask.request.method == 'GET':
            fs = Folder.query.all()
            return {"status":json.dumps(fs,cls=AlchemyEncoder)}
        else:
            return {"status":"error, not implemented"}


    return app

if __name__ == "__main__":
    app =create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


