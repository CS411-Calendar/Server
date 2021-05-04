from flask import request, jsonify, make_response
from datetime import datetime
from db import Invite, Calendar, Attendee, db, init
from weather import get_weather
from config import app
from sqlalchemy.orm import sessionmaker


def createErrorResponse(error: str):
    return jsonify({
        "error": error
    })


@app.route('/api/calendar/invite', methods=['POST'])
def calendar():
    contentType = request.headers.get('Content-Type')

    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')

        try:
            start = datetime.strptime(data.get('start'), '%Y-%m-%d')
            end = datetime.strptime(data.get('end'), '%Y-%m-%d')
        except:
            return make_response(createErrorResponse("Date must be of format Year-Month-Day"), 400)

        location = data.get('location')

        if not email or not isinstance(email, str):
            return make_response(
                createErrorResponse("Missing Key-Value string field email"),
                400
            )

        if not name or not isinstance(name, str):
            return make_response(createErrorResponse("Missing Key-Value string field name"), 400)

        calendar, newCalendar = Calendar.createOrGet(email)

        if newCalendar:
            db.session.add(calendar)

        invite = Invite(start=start, end=end, location=location, name=name, to=email)
        db.session.add(invite)
        db.session.commit()
        return make_response(invite.json(), 201)


@app.route('/api/calendar/invite/<int:inviteId>', methods=['GET', 'PUT'])
def inviteLink(inviteId: int):
    if request.method == 'GET':
        data = Invite.query.get(inviteId)
        attendees = Attendee.query.filter(Attendee.inviteId == inviteId)
        if data:
            return make_response(jsonify({
                "inviteJson": data.toDict(), 
                "attendeeJson": [attendee.toDict() for attendee in attendees]
            }), 200)
        else:
            return make_response(createErrorResponse("Not Found"), 404)
    elif request.method == 'PUT':
        data = request.json
        invite = Invite.query.get(inviteId)

        if not invite:
            return make_response(createErrorResponse("Invite ID Not Found"), 404)

        calendarId = data.get('id')
        if not calendarId:
            return make_response(createErrorResponse("Missing Public Calendar ID"), 400)

        calendar, newCalendar = Calendar.createOrGet(calendarId)
        if newCalendar:
            db.session.add(calendar)

        attendee, newAttendee = Attendee.createOrGet(inviteId, calendarId)
        if not newAttendee:
            db.session.add(attendee)
        
        db.session.commit()
        return make_response(invite_calendar.json(), 201)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'GET':
        lat, lon = request.args.get('lat'), request.args.get('long')
        try:
            forecast = get_weather(float(lat), float(lon))
        except Exception as e:
            return 'Internal Server Error', 500
        return jsonify(forecast), 200


if __name__ == '__main__':
    init()
    app.run()
