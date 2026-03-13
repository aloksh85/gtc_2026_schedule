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
                <div style="margin-top: 15px; padding: 15px; background: #f0f7e6; border-left: 5px solid #76b900; border-radius: 4px;">
                    <strong style="color: #76b900; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Strategic Focus:</strong>
                    <p style="margin: 5px 0 0; font-size: 16px; font-weight: 600; color: #1a1a1a;">Physical AI, Robotics, and Vision Language Models (VLMs)</p>
                    <p style="margin: 5px 0 0; font-size: 13px; color: #555;">Focusing on sim-to-real workflows, edge deployment on Jetson Thor/Orin, and agentic reasoning for autonomous systems.</p>
                </div>
            </header>
    """

    for date in sorted(days.keys()):
        html += f'<div class="day-section"><h2>{date}</h2>'
        html += """
        <table>
            <thead>
                <tr>
                    <th style="width: 33.3%;">Plan A (Primary)</th>
                    <th style="width: 33.3%;">Plan B (Alternate)</th>
                    <th style="width: 33.3%;">Plan C</th>
                </tr>
            </thead>
            <tbody>
        """
        for row in days[date]:
            is_giveaway = '🎁' in row['Plan A Time']
            row_class = ' class="giveaway"' if is_giveaway else ''
            
            a_title = row['Plan A Title']
            a_time = row['Plan A Time']
            a_loc = row['Plan A Location']
            
            b_title = row['Plan B Title']
            b_time = row.get('Plan B Time', '')
            b_loc = row.get('Plan B Location', '')
            
            c_title = row.get('Plan C Title', '')
            c_time = row.get('Plan C Time', '')
            c_loc = row.get('Plan C Location', '')
            
            def format_cell(title, time, loc):
                if not title or title == 'No Plan B defined': return ''
                loc_str = f'<br><span style="color: #666; font-size: 11px;">📍 {loc}</span>' if loc else ''
                time_str = f'<br><span style="color: #76b900; font-size: 11px; font-weight: 600;">⏰ {time}</span>' if time else ''
                return f'<span class="session-title">{title}</span>{time_str}{loc_str}'

            html += f"""
            <tr{row_class}>
                <td>{format_cell(a_title, a_time, a_loc)}</td>
                <td>{format_cell(b_title, b_time, b_loc)}</td>
                <td>{format_cell(c_title, c_time, c_loc)}</td>
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
    
    with open('docs/printable.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated docs/printable.html")

if __name__ == "__main__":
    generate_html()
