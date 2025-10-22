import re
import pandas as pd

def preprocess(data):
    # Pattern for 12-hour format with AM/PM (case insensitive)
    pattern_12h = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    # Pattern for 24-hour format
    pattern_24h = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # Try 12-hour format first (case insensitive)
    messages_12h = re.split(pattern_12h, data, flags=re.IGNORECASE)[1:]
    dates_12h = re.findall(pattern_12h, data, flags=re.IGNORECASE)
    
    # Try 24-hour format
    messages_24h = re.split(pattern_24h, data)[1:]
    dates_24h = re.findall(pattern_24h, data)
    
    # Choose the format that has more matches
    if len(dates_12h) >= len(dates_24h) and dates_12h:
        messages = messages_12h
        dates = dates_12h
        time_format = '12h'
    elif dates_24h:
        messages = messages_24h
        dates = dates_24h
        time_format = '24h'
    else:
        # Fallback: try to detect format from first few lines
        lines = data.split('\n')[:5]
        for line in lines:
            if re.search(r'\d{1,2}:\d{2}\s[ap]m', line, flags=re.IGNORECASE):
                time_format = '12h'
                break
            elif re.search(r'\d{1,2}:\d{2}\s-', line):
                time_format = '24h'
                break
        else:
            time_format = '12h'  # Default fallback
        
        # Re-try with detected format
        if time_format == '12h':
            messages = re.split(pattern_12h, data, flags=re.IGNORECASE)[1:]
            dates = re.findall(pattern_12h, data, flags=re.IGNORECASE)
        else:
            messages = re.split(pattern_24h, data)[1:]
            dates = re.findall(pattern_24h, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Convert message_date type based on detected format
    parse_success = False
    if time_format == '12h':
        formats_to_try = [
            '%d/%m/%Y, %I:%M %p - ',
            '%d/%m/%y, %I:%M %p - ',
            '%d/%m/%Y, %I:%M %p -',
            '%d/%m/%y, %I:%M %p -',
            '%d/%m/%Y, %I:%M %p',
            '%d/%m/%y, %I:%M %p',
        ]
    else:
        formats_to_try = [
            '%d/%m/%Y, %H:%M - ',
            '%d/%m/%y, %H:%M - ',
            '%d/%m/%Y, %H:%M -',
            '%d/%m/%y, %H:%M -',
            '%d/%m/%Y, %H:%M',
            '%d/%m/%y, %H:%M',
        ]

    for fmt in formats_to_try:
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format=fmt)
            parse_success = True
            break
        except Exception:
            continue

    if not parse_success:
        # Robust fallback: let pandas infer per-element with dayfirst
        df['message_date'] = pd.to_datetime(df['message_date'], dayfirst=True, errors='coerce', format='mixed')

    # Drop rows that failed to parse and rename
    df = df.dropna(subset=['message_date']).rename(columns={'message_date': 'date'})

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df