from flask import abort
from flask_restx import Namespace, Resource
from Domain.extension import authorizations
from Utils.Exceptions.customException import CustomException
from Infrastructure.Repositories.notificationsRepo import *
nsNotifications = Namespace("notifications", authorizations=authorizations,
                                 description="Notifications operations")

@nsNotifications.route("/<string:employeeId>")
class GetNotifications(Resource):
    # method_decorators = [jwt_required()]
    # @nsNotifications.doc(security="jsonWebToken")
    @nsNotifications.doc(params={'employeeId': 'The ID of the employee for which to retrieve notifications'})
    def get(self, employeeId):

        try:
            notifications = getNotificationRepo(employeeId)
            return notifications

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsNotifications.route("/seen/<string:notificationId>")
class UpdateNotifications(Resource):
    # method_decorators = [jwt_required()]
    # @nsNotifications.doc(security="jsonWebToken")
    @nsNotifications.doc(params={'notificationId': 'The ID of the notification to update'})
    def put(self, notificationId):

        try:
            updateNotificationsRepo(notificationId)

            return {"message":"Notification updated"}

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
