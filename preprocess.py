import re
import pandas as pd

def preprocess(data):
    data = data.replace('\u202f', ' ')
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{1,2}\s*(?:AM|PM|am|pm))\s*-\s*([^:]+):\s*(.*)'
    messages = []
    for line in data.splitlines():
        match = re.match(pattern, line)
        if match:
            date_time, sender, message = match.groups()
            messages.append({
                'date_time': date_time,
                'sender': sender,
                'message': message
            })
    df=pd.DataFrame(messages)
    df['date_time_clean'] = df['date_time'].str.replace('\u202f', ' ').str.lower()
    df['dt'] = pd.to_datetime(df['date_time_clean'], format='%d/%m/%y, %I:%M %p')
    df['day'] = df['dt'].dt.day
    df['month'] = df['dt'].dt.month
    df['year'] = df['dt'].dt.year
    df['time_24h'] = df['dt'].dt.strftime('%H:%M')
    df = df.drop(columns=['date_time_clean'])
    df = df.drop(columns=['date_time'])
    df['day_name']=df['dt'].dt.day_name()
    df[['hour', 'minute']] = df['time_24h'].str.split(':', expand=True)
    df = df.drop(columns=['time_24h'])
    period = []
    for hour in df['hour']:
        hour = int(hour)
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour+1:02d}")
        else:
            period.append(f"{hour:02d}-{hour+1:02d}")
    df['period'] = period
    return df