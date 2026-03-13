import csv

# 1. Load all sessions to get metadata
db = {}
with open('all_gtc_sessions.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        db[row['Session ID']] = row

# 3. Load Plan B pairings
plan_b_data = []
with open('plan_b_verified.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        plan_b_data.append(row)

# Provide fallback URLs for Plan A if not in db
def get_url(code):
    if code in db and db[code]['Link']: return db[code]['Link']
    if code == 'OPEN': return ''
    return f"https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-{code.lower()}/"
    
def get_brief(code):
    if code in db: return db[code]['Brief']
    return ""

csv_out = []
md_out = []

md_out.append("# GTC 2026 Schedule — Iteration 2")
md_out.append("\n## Daily Strategy Notes")
md_out.append("- **Monday (Mar 16):** Foundations & Context. Recommend conceptual intros over heavy coding labs.")
md_out.append("- **Tuesday (Mar 17):** Vision & Agents. Deep dive into VLA, synthetic data, enterprise agents.")
md_out.append("- **Wednesday (Mar 18):** Scaling to Production. Surgical robots, humanoids (GR00T), edge panels.")
md_out.append("- **Thursday (Mar 19):** Wrap-up & Travel. Avoid 4-hour hackathons if user has evening flight.")
md_out.append("\n---\n")

# Giveaways data — available times per day
giveaways = {
    '2026-03-16': [
        ('8:00 AM - 5:00 PM', '[Free Developer Training ($90)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2493/)', 'Signia Hotel 2F', '[Free AI Infra Training ($200)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2494/)', 'Signia Hotel 2F (Paseo)'),
        ('2:00 - 4:00 PM', '[Free NVIDIA Associate Certification](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-c82415/)', 'Exam Center', '', ''),
    ],
    '2026-03-17': [
        ('8:00 AM - 5:00 PM', '[Free Developer Training ($90)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2493/)', 'Signia Hotel 2F', '[Free AI Infra Training ($200)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2494/)', 'Signia Hotel 2F (Paseo)'),
        ('9:00 - 11:00 AM, 4:00 - 6:00 PM', '[Free NVIDIA Associate Certification](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-c82415/)', 'Exam Center', '', ''),
    ],
    '2026-03-18': [
        ('8:00 AM - 5:00 PM', '[Free Developer Training ($90)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2493/)', 'Signia Hotel 2F', '[Free AI Infra Training ($200)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2494/)', 'Signia Hotel 2F (Paseo)'),
        ('11:00 AM - 4:00 PM', '[Free NVIDIA Associate Certification](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-c82415/)', 'Exam Center', '[Physical AI & OpenUSD Cert Info](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-c81931/)', '8:00-8:45 AM'),
    ],
    '2026-03-19': [
        ('8:00 AM - 5:00 PM', '[Free Developer Training ($90)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2493/)', 'Signia Hotel 2F', '[Free AI Infra Training ($200)](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-2494/)', 'Signia Hotel 2F (Paseo)'),
        ('8:00 AM - 1:00 PM', '[Free NVIDIA Associate Certification](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-c82415/)', 'Exam Center', '', ''),
    ],
}

# Group by day
from collections import defaultdict
days = defaultdict(list)
for row in plan_b_data:
    days[row['Date']].append(row)

for date in sorted(days.keys()):
    md_out.append(f"## {date}")
    md_out.append("| Time | Plan A | Plan A Location | Plan B | Plan B Location | Plan C |")
    md_out.append("|---|---|---|---|---|---|")
    
    # Add giveaway rows first
    if date in giveaways:
        for g in giveaways[date]:
            md_out.append(f"| 🎁 {g[0]} | {g[1]} | {g[2]} | {g[3]} | {g[4]} | |")
    
    for row in days[date]:
        a_code = row['Plan A Code']
        a_title = row['Plan A Title']
        a_loc = db[a_code]['Room'] if a_code in db else 'Room Unknown'
        a_url = get_url(a_code)
        
        b_code = row['Plan B Code']
        b_title = row['Plan B Title']
        b_url = row.get('Plan B Link', '')
        b_type = row.get('Plan B Type', '')
        
        b_loc = db[b_code]['Room'] if b_code in db and 'Room' in db[b_code] else 'TBD'
        b_time = db[b_code]['Time'] if b_code in db and 'Time' in db[b_code] else ''
        
        c_code = row.get('Plan C Code', '')
        c_title = row.get('Plan C Title', '')
        c_url = db[c_code]['Link'] if c_code in db else ''
        c_time = db[c_code]['Time'] if c_code in db else ''
        c_loc = db[c_code]['Room'] if c_code in db else ''
        
        csv_out.append({
            'Date': date,
            'Plan A Time': row['Time'],
            'Plan A Location': a_loc,
            'Plan A Title': a_title,
            'Plan A Type': '',
            'Plan A URL': a_url,
            'Plan B Time': b_time,
            'Plan B Location': b_loc,
            'Plan B Title': b_title,
            'Plan B Type': b_type,
            'Plan B URL': b_url,
            'Plan C Title': c_title,
            'Plan C Time': c_time,
            'Plan C Location': c_loc,
            'Plan C URL': c_url
        })
        
        # Markdown cell formatting
        a_link = f"[{a_title}]({a_url})" if a_url else a_title
        b_link = f"[{b_title}]({b_url})" if b_url else b_title
        
        a_desc = get_brief(a_code)
        b_desc = get_brief(b_code)
        
        a_cell = f"**{a_link}**<br>*{a_code}*"
        if a_desc: a_cell += f"<br>{a_desc[:100]}..."
        
        b_time_label = f"<br>⏰ {b_time}" if b_time else ''
        b_cell = f"**{b_link}**<br>*{b_code}*{b_time_label}" if b_code != 'OPEN' else f"*{b_title}*"
        if b_desc: b_cell += f"<br>{b_desc[:100]}..."
        
        c_cell = ""
        if c_code:
            c_link = f"[{c_title}]({c_url})" if c_url else c_title
            c_desc = get_brief(c_code)
            c_cell = f"**{c_link}**<br>*{c_code}*"
            if c_time: c_cell += f"<br>⏰ {c_time}"
            if c_loc: c_cell += f"<br>📍 {c_loc}"
            if c_desc: c_cell += f"<br>{c_desc[:100]}..."
        
        md_out.append(f"| {row['Time']} | {a_cell} | {a_loc} | {b_cell} | {b_loc} | {c_cell} |")
        
    md_out.append("\n")

with open('gtc2026_schedule_iteration_2.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(md_out))

with open('gtc2026_schedule_iteration_2.csv', 'w', newline='', encoding='utf-8') as f:
    fields = ['Date', 'Plan A Time', 'Plan A Location', 'Plan A Title', 'Plan A Type', 'Plan A URL', 'Plan B Time', 'Plan B Location', 'Plan B Title', 'Plan B Type', 'Plan B URL', 'Plan C Title', 'Plan C Time', 'Plan C Location', 'Plan C URL']
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(csv_out)
    
print("Created Iteration 2 files successfully!")
