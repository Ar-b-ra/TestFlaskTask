import argparse
import logging
from http import HTTPStatus

from flask import Blueprint, Flask, request
from flask_restx import Api, Resource, fields

from src.db_worker import DatabaseWorker

swagger_blueprint = Blueprint("swagger", __name__, url_prefix="/docs")

app = Flask(__name__, template_folder="templates")
api = Api(app, doc="/swagger", validate=True)
app.register_blueprint(swagger_blueprint)

execute_model = api.model(
    "Execute",
    {
        "db_number": fields.Integer(required=True),
        "query": fields.String(required=True),
    },
)


@api.route("/execute")
class QueueWorker(Resource):
    @api.doc(
        responses={
            200: "Query executed successfully",
            400: "Invalid arguments",
            500: "Internal server error",
        }
    )
    @api.expect(execute_model)
    def post(self):
        data = request.json
        db_number = data["db_number"]
        query = data["query"]
        logging.info(f"db_number: {db_number}, query: {query}")
        result = DatabaseWorker.execute_query(db_number, query)
        return result, HTTPStatus.OK


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="0.0.0.0", type=str, help="Адрес хоста")
    parser.add_argument("--port", "-p", default=8000, type=int, help="Порт")

    args = parser.parse_args()

    # Выводим адрес хоста и порт
    logging.debug(f"Host = {args.host}, port = {args.port}")

    host = args.host
    port = args.port
    app.run(host=host, port=port, debug=True)
