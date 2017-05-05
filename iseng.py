from datetime import time, datetime

timestamp_message = [
    1493950428,
    1493950427,
    1493950426,
    1493950426,
    1493950426,
    1493091600,
] #sorted
size = len(timestamp_message)
result = {}
for i in timestamp_message:
    c_hour = datetime.fromtimestamp(i).hour
    if (c_hour < 10):
        c_hour = '0{}'.format(c_hour)
    dist_hour = result.get(c_hour, None)
    if dist_hour is None:
        result[c_hour] = {'total' : 0, 'percentage' : '0%'}
    result[c_hour]['total'] += 1
    result[c_hour]['percentage'] = '{}%'.format(int(result[c_hour]['total'] / size * 100))

print(result)
