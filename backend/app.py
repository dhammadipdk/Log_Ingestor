# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Log
from datetime import datetime
from sqlalchemy import or_, and_

app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/ingest', methods=['POST'])
def ingest():
    try:
        log_data = request.get_json()
        log = Log(
            level=log_data['level'],
            message=log_data['message'],
            resourceId=log_data['resourceId'],
            timestamp=datetime.strptime(log_data['timestamp'], '%Y-%m-%dT%H:%M:%SZ'),
            traceId=log_data.get('traceId'),
            spanId=log_data.get('spanId'),
            commit=log_data.get('commit'),
            parentResourceId=log_data['metadata'].get('parentResourceId')
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': 'Log ingested successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    try:
        search_criteria = request.get_json()
        query = Log.query

        for key, value in search_criteria.items():
            if key == 'timestamp':
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                query = query.filter(getattr(Log, key) == value)
            elif key in ['level', 'message', 'resourceId', 'traceId', 'spanId', 'commit', 'metadata.parentResourceId']:
                query = query.filter(getattr(Log, key).ilike(f"%{value}%"))
            else:
                query = query.filter(getattr(Log, key) == value)

        results = query.all()
        return jsonify([log.to_dict() for log in results])

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/filter', methods=['GET'])
def filter_logs():
    level = request.args.get('level')
    resourceId = request.args.get('resourceId')
    message = request.args.get('message')
    timestamp = request.args.get('timestamp')
    traceId = request.args.get('traceId')
    spanId = request.args.get('spanId')
    commit = request.args.get('commit')
    parentResourceId = request.args.get('metadata.parentResourceId')

    print(f"Filter Parameters: level={level}, resourceId={resourceId}, timestamp={timestamp}, traceId={traceId}, spanId={spanId}, commit={commit}, parentResourceId={parentResourceId}")

    query = Log.query
    filters = []

    if level:
        filters.append(Log.level.ilike(f"%{level}%"))
    if resourceId:
        filters.append(Log.resourceId.ilike(f"%{resourceId}%"))
    if timestamp:
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        filters.append(Log.timestamp == timestamp)
    if traceId:
        filters.append(Log.traceId.ilike(f"%{traceId}%"))
    if spanId:
        filters.append(Log.spanId.ilike(f"%{spanId}%"))
    if commit:
        filters.append(Log.commit.ilike(f"%{commit}%"))
    if parentResourceId:
        filters.append(Log.parentResourceId.ilike(f"%{parentResourceId}%"))
    if message:
        filters.append(Log.message.ilike(f"%{message}%")) 

    if filters:
        query = query.filter(db.and_(*filters))

    results = query.all()

    return jsonify([log.to_dict() for log in results])

if __name__ == '__main__':
    app.run(port=3000, debug=True)
