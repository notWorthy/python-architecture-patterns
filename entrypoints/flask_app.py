from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import domain.model as model
import adapters.orm as orm
import adapters.repository as repository

orm.start_mappers()
# get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
get_session = sessionmaker(bind=create_engine('sqlite:///:memory:'))
app = Flask(__name__)
@app.route("/", methods=['GET'])
def home():
    return "Architecture Patterns with Python home."

@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )

    batchref = model.allocate(line, batches)

    return jsonify({'batchref': batchref}), 201