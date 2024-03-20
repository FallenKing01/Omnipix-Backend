from Domain.extension import notificationsCollection
from Utils.Exceptions.customException import CustomException


def getNotificationRepo(employeeId):

    notifications = []

    query = notificationsCollection.where('employeeId', '==', employeeId).get()

    if query:
        for doc in query:
            notifications.append(doc.to_dict())

    return notifications

def updateNotificationsRepo(notificationId):

    query = notificationsCollection.where('id', '==', notificationId).get()

    if query:
        for doc in query:
            doc.reference.update({"wasSeen":True})
    else:
        raise CustomException(404, "Notification not found")