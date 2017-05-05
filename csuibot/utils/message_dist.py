import requests
from datetime import datetime
from .. import app

class MessageDist:

    def get_message_dist(self, group_id):
        group_message_timestamp_update = self.get_group_message_timestamp_update(group_id)
        message_dist = self.calc_message_dist(group_message_timestamp_update)
        return message_dist

    def get_group_message_timestamp_update(self, group_id):
        telebot_update_url = 'https://api.telegram.org/bot{}/getUpdates'.format(app.config['TELEGRAM_BOT_TOKEN'])
        try:
            telebot_updates = requests.post(telebot_update_url).json()
        except requests.exceptions.Timeout:
            return []
        status = telebot_updates['ok']
        if status is False:
            return []
        else:
            results = telebot_updates['result']
            group_message_updates = []
            for f in results:
                if f.get('edited_message', None) != None:
                    group_message_updates.append(f['edited_message']['date'])
                else:
                    group_message_updates.append(f['message']['date'])
            return group_message_updates

    def calc_message_dist(self, timestamp_message):
        size = len(timestamp_message)
        result = {}
        x_hour = 0
        for i in timestamp_message:
            c_hour = datetime.fromtimestamp(i).hour
            while (x_hour < c_hour):
                m_hour = x_hour
                if (m_hour < 10):
                    m_hour = '0{}'.format(m_hour)
                m_hour = str(m_hour)
                result[m_hour] = {'total': 0, 'percentage': '0%'}
                x_hour += 1
            if (c_hour < 10):
                c_hour = '0{}'.format(c_hour)
            c_hour = str(c_hour)
            dist_hour = result.get(c_hour, None)
            if dist_hour is None:
                result[c_hour] = {'total': 0, 'percentage': '0%'}
            result[c_hour]['total'] += 1
            result[c_hour]['percentage'] = '{}%'.format(int(result[c_hour]['total'] / size * 100))
        return result
