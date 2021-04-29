from flask import request, jsonify, make_response
from datetime import datetime
from db import Invite, User, InviteCalendar, Calendar, db, init
from weather import get_weather
from lib import createUserId
from config import app


def createErrorResponse(error: str):
    return jsonify({
        "error": error
    })


@app.route('/api/calendar/invite', methods=['POST'])
def calendar():
    userAgent = request.headers.get('User-Agent')
    if request.method == 'POST' and userAgent:
        userId = createUserId(request.remote_addr, userAgent)

        if not User.query.get(userId):
            user = User(id=userId)
            db.session.add(user)
        invite = Invite(ownerId=userId)
        db.session.add(invite)
        db.session.commit()
        return make_response(invite.json(), 201)


@app.route('/api/calendar/invite/<int:inviteId>', methods=['GET', 'PUT'])
def inviteLink(inviteId: int):
    if request.method == 'GET':
        data = Invite.query.get(inviteId)
        if data:
            return make_response(data.json(), 200)
        else:
            return make_response(createErrorResponse("Not Found"), 404)
    elif request.method == 'PUT':
        invite = Invite.query.get(inviteId)
        if not invite:
            return make_response(createErrorResponse("Invite ID Not Found"), 404)
        calendarId = request.form.get('id')
        if not calendarId:
            return make_response(createErrorResponse("Missing Public Calendar ID"), 400)
        calendar = Calendar.query.get(calendarId)
        if not calendar:
            calendar = Calendar(id=calendarId)
            db.session.add(calendar)
        invite_calendar = InviteCalendar.query.get([inviteId, calendarId])
        if not invite_calendar:
            invite_calendar = InviteCalendar(inviteId=inviteId, calendarId=calendarId)
            db.session.add(invite_calendar)
        
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
