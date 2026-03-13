import csv
import os

def generate_html():
    csv_file = 'gtc2026_schedule_iteration_2.csv'
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    days = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['Date']
            if date not in days:
                days[date] = []
            days[date].append(row)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.5;
                color: #1a1a1a;
                margin: 0;
                padding: 40px;
                background-color: #fff;
            }
            .container { max-width: 1000px; margin: 0 auto; }
            header { border-bottom: 2px solid #76b900; padding-bottom: 20px; margin-bottom: 40px; }
            h1 { font-size: 28px; margin: 0; color: #76b900; }
            h2 { font-size: 20px; margin-top: 40px; border-bottom: 1px solid #eee; padding-bottom: 8px; color: #333; }
            .day-section { page-break-after: always; }
            .day-section:last-child { page-break-after: auto; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; table-layout: fixed; }
            th { border-bottom: 2px solid #333; padding: 12px 8px; text-align: left; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; background: #f9f9f9; }
            td { border-bottom: 1px solid #eee; padding: 12px 8px; vertical-align: top; font-size: 14px; word-wrap: break-word; }
            .time-col { width: 15%; font-weight: 600; color: #555; }
            .plan-col { width: 35%; }
            .loc-col { width: 15%; font-size: 12px; color: #666; }
            .plan-b-col { width: 35%; }
            .plan-c-col { width: 20%; font-size: 12px; font-style: italic; }
            
            .session-title { font-weight: 700; color: #000; margin-bottom: 4px; display: block; }
            .session-code { font-family: monospace; font-size: 12px; color: #76b900; background: #f0f7e6; padding: 2px 4px; border-radius: 4px; }
            .giveaway { background-color: #fffde7; }
            .giveaway td { font-style: italic; color: #795548; }

            @media print {
                body { padding: 0; }
                .container { max-width: 100%; }
                header { margin-bottom: 20px; }
            }
        </style>
        <title>GTC 2026 Schedule</title>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>NVIDIA GTC 2026 — Final Schedule</h1>
                <p>Personalized Strategy: Physical AI, Robotics, and Vision Language Models</p>
            </header>
    """

    for date in sorted(days.keys()):
        html += f'<div class="day-section"><h2>{date}</h2>'
        html += """
        <table>
            <thead>
                <tr>
                    <th class="time-col">Time</th>
                    <th class="plan-col">Plan A (Primary)</th>
                    <th class="loc-col">Location</th>
                    <th class="plan-b-col">Plan B (Alternate)</th>
                    <th class="loc-col">Location</th>
                    <th class="plan-c-col">Plan C</th>
                </tr>
            </thead>
            <tbody>
        """
        for row in days[date]:
            is_giveaway = '🎁' in row['Plan A Time']
            row_class = ' class="giveaway"' if is_giveaway else ''
            
            a_title = row['Plan A Title']
            b_title = row['Plan B Title']
            c_title = row.get('Plan C Title', '')
            
            a_html = f'<span class="session-title">{a_title}</span>'
            b_html = f'<span class="session-title">{b_title}</span>'
            c_html = f'<span class="session-title">{c_title}</span>' if c_title else ''
            
            html += f"""
            <tr{row_class}>
                <td class="time-col">{row['Plan A Time']}</td>
                <td class="plan-col">{a_html}</td>
                <td class="loc-col">{row['Plan A Location']}</td>
                <td class="plan-b-col">{b_html}</td>
                <td class="loc-col">{row.get('Plan B Location', 'TBD')}</td>
                <td class="plan-c-col">{c_html}</td>
            </tr>
            """
        html += "</tbody></table></div>"

    html += """
            <div style="text-align: center; margin-top: 50px;" class="no-print">
                <button onclick="window.print()" style="padding: 12px 24px; background: #76b900; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    Print to PDF
                </button>
            </div>
            <style>
                @media print { .no-print { display: none; } }
            </style>
        </div>
    </body>
    </html>
    """
    
    with open('gtc2026_printable.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated gtc2026_printable.html")

if __name__ == "__main__":
    generate_html()
