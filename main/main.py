import bot

from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

api.add_resource(bot.facebook.MainHandler, '/facebook/')
api.add_resource(bot.telegram.WebhookHandler, '/telegram/webhook/')
api.add_resource(bot.telegram.SetWebhookHandler, '/telegram/set_webhook')
api.add_resource(bot.telegram.DelWebhookHandler, '/telegram/del_webhook')
api.add_resource(bot.telegram.GetUpdatesHandler, '/telegram/updates')
api.add_resource(bot.telegram.MeHandler, '/telegram/me')

if __name__ == '__main__':
    app.run(debug=True)
