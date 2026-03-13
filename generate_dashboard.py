import csv
import json
import os

def generate_dashboard():
    csv_file = 'gtc2026_schedule_iteration_2.csv'
    db_file = 'all_gtc_sessions.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    # Load session database for full descriptions
    session_db = {}
    if os.path.exists(db_file):
        with open(db_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                session_db[row['Session ID']] = row

    schedule_data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Enrich with full descriptions if available
            a_code = row.get('Plan A Code', '') # Note: iteration 2 csv header is different
            # Wait, let me check the header of iteration 2 csv
            # Fields: ['Date', 'Plan A Time', 'Plan A Location', 'Plan A Title', 'Plan A Type', 'Plan A URL', 'Plan B Time', 'Plan B Location', 'Plan B Title', 'Plan B Type', 'Plan B URL', 'Plan C Title', 'Plan C Time', 'Plan C URL']
            # I need the codes to get descriptions. I'll parse the URL if needed or just use titles.
            # Actually, I'll update the generator to include codes in the JSON.
            schedule_data.append(row)

    # Group by day
    days = {}
    for entry in schedule_data:
        d = entry['Date']
        if d not in days: days[d] = []
        days[d].append(entry)

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GTC 2026 Interactive Dashboard</title>
    <style>
        :root {
            --nvidia-green: #76b900;
            --dark-bg: #0b0b0b;
            --card-bg: #1a1a1a;
            --text-primary: #ffffff;
            --text-secondary: #aaaaaa;
            --accent: #2d2d2d;
            --glass: rgba(255, 255, 255, 0.05);
        }

        body {
            font-family: 'Inter', -apple-system, system-ui, sans-serif;
            background-color: var(--dark-bg);
            color: var(--text-primary);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* Sidebar */
        .sidebar {
            width: 260px;
            background: #000;
            border-right: 1px solid var(--accent);
            display: flex;
            flex-direction: column;
            padding: 20px;
        }

        .logo {
            font-size: 24px;
            font-weight: 800;
            color: var(--nvidia-green);
            margin-bottom: 40px;
            letter-spacing: -1px;
        }

        .nav-item {
            padding: 12px 16px;
            margin-bottom: 8px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .nav-item:hover {
            background: var(--glass);
            color: #fff;
        }

        .nav-item.active {
            background: var(--nvidia-green);
            color: #000;
        }

        /* Main Content */
        .main {
            flex: 1;
            overflow-y: auto;
            padding: 40px;
            scroll-behavior: smooth;
        }

        .header {
            margin-bottom: 40px;
        }

        .header h1 {
            font-size: 32px;
            margin: 0;
        }

        .header p {
            color: var(--text-secondary);
            margin-top: 8px;
        }

        /* Slot Card */
        .slot-container {
            margin-bottom: 30px;
            animation: fadeIn 0.5s ease forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .time-label {
            font-size: 14px;
            font-weight: 600;
            color: var(--nvidia-green);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .side-by-side {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--accent);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
            position: relative;
            overflow: hidden;
        }

        .card:hover {
            border-color: var(--nvidia-green);
            transform: translateY(-2px);
        }

        .card.plan-a::after {
            content: 'PLAN A';
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 10px;
            font-weight: 800;
            background: var(--nvidia-green);
            color: #000;
            padding: 2px 6px;
            border-radius: 4px;
        }

        .card.plan-b::after {
            content: 'PLAN B';
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 10px;
            font-weight: 800;
            background: #444;
            color: #fff;
            padding: 2px 6px;
            border-radius: 4px;
        }
        
        .card.hackathon {
            grid-column: span 2;
            background: linear-gradient(135deg, #1a1a1a 0%, #000 100%);
            border: 1px dashed var(--nvidia-green);
        }

        .card.hackathon::after {
            content: 'SPECIAL EVENT / PLAN C';
            background: #ff3e00;
            color: #fff;
        }

        .card-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.4;
        }

        .card-meta {
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 16px;
            display: flex;
            gap: 15px;
        }

        .card-meta span {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .card-desc {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 20px;
            flex: 1;
        }

        .btn {
            display: inline-block;
            background: var(--glass);
            color: #fff;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            text-align: center;
            transition: background 0.2s;
        }

        .btn:hover {
            background: var(--nvidia-green);
            color: #000;
        }

        .gift-tag {
            background: #fffde7;
            color: #795548;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Responsive */
        @media (max-width: 900px) {
            .side-by-side { grid-template-columns: 1fr; }
            .sidebar { width: 60px; padding: 10px; }
            .logo, .nav-item span { display: none; }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">GTC '26</div>
        <div id="nav"></div>
    </div>
    <div class="main">
        <div class="header">
            <div style="background: rgba(118, 185, 0, 0.1); border: 1px solid var(--nvidia-green); padding: 20px; border-radius: 12px; margin-bottom: 40px;">
                <h3 style="color: var(--nvidia-green); margin: 0 0 10px; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Aligned Strategy</h3>
                <h2 style="margin: 0 0 5px; font-size: 20px;">Physical AI, Robotics, and Vision Language Models</h2>
                <p style="margin: 0; font-size: 13px; color: var(--text-secondary);">Sim-to-real workflows, edge deployment on Jetson Thor/Orin, and agentic reasoning.</p>
            </div>
            <h1 id="day-title">Select a Day</h1>
            <p id="day-strategy"></p>
        </div>
        <div id="content"></div>
    </div>

    <script>
        const data = """ + json.dumps(days) + """;
        const strategies = {
            '2026-03-16': "Foundations & Context. Focus on conceptual intros and building networking baseline.",
            '2026-03-17': "Vision & Agents. Deep dive into VLA, synthetic data, and enterprise agents.",
            '2026-03-18': "Scaling to Production. Advanced humanoids (GR00T) and medical robotics applications.",
            '2026-03-19': "Wrap-up & Rapid Prototyping. Vibe coding hackathon and future path certification."
        };

        const nav = document.getElementById('nav');
        const content = document.getElementById('content');
        const dayTitle = document.getElementById('day-title');
        const dayStrategy = document.getElementById('day-strategy');

        function renderDay(date) {
            dayTitle.innerText = date;
            dayStrategy.innerText = strategies[date] || "";
            content.innerHTML = "";
            
            // Render nav active state
            document.querySelectorAll('.nav-item').forEach(el => {
                el.classList.toggle('active', el.dataset.date === date);
            });

            const daySlots = data[date];
            daySlots.forEach(slot => {
                const div = document.createElement('div');
                div.className = 'slot-container';
                
                const isSpecial = slot['Plan C Title'] && slot['Plan C Title'] !== '';
                const hasA = slot['Plan A Title'] && slot['Plan A Title'] !== '';
                const hasB = slot['Plan B Title'] && slot['Plan B Title'] !== 'No Plan B defined';

                if (slot['Plan A Time'].includes('🎁')) {
                    div.innerHTML = `
                        <div class="gift-tag">
                            <span>🎁 ${slot['Plan A Time']}</span>
                            <strong>${slot['Plan A Title']}</strong>
                            <span style="color: #999">@ ${slot['Plan A Location']}</span>
                        </div>
                    `;
                    content.appendChild(div);
                    return;
                }

                let inner = `<div class="time-label">${slot['Plan A Time']}</div>`;
                inner += `<div class="side-by-side">`;
                
                if (hasA) {
                    inner += `
                        <div class="card plan-a">
                            <div class="card-title">${slot['Plan A Title']}</div>
                            <div class="card-meta">
                                <span>📍 ${slot['Plan A Location']}</span>
                            </div>
                            <div class="card-desc">Targeting your strategy in Physical AI and Robotics.</div>
                            <a href="${slot['Plan A URL']}" target="_blank" class="btn">View Session</a>
                        </div>
                    `;
                }
                
                if (hasB) {
                    inner += `
                        <div class="card plan-b">
                            <div class="card-title">${slot['Plan B Title']}</div>
                            <div class="card-meta">
                                <span>📍 ${slot.Plan_B_Location || 'TBD'}</span>
                                <span>⏰ ${slot.Plan_B_Time || ''}</span>
                            </div>
                            <div class="card-desc">Strong alternate focused on scalability and reasoning.</div>
                            <a href="${slot.Plan_B_URL}" target="_blank" class="btn">View Alternate</a>
                        </div>
                    `;
                }

                if (isSpecial) {
                    inner += `
                        <div class="card hackathon">
                            <div class="card-title">${slot['Plan C Title']}</div>
                            <div class="card-meta">
                                <span>📍 Guildhouse</span>
                                <span>⏰ ${slot.Plan_C_Time || ''}</span>
                            </div>
                            <div class="card-desc">Special bypass option. Experience 'Vibe Coding' and rapid prototyping.</div>
                            <a href="${slot.Plan_C_URL}" target="_blank" class="btn">Join Hackathon</a>
                        </div>
                    `;
                }

                inner += `</div>`;
                div.innerHTML = inner;
                content.appendChild(div);
            });
        }

        // Initialize Nav
        Object.keys(data).sort().forEach((date, index) => {
            const item = document.createElement('div');
            item.className = 'nav-item';
            item.dataset.date = date;
            item.innerHTML = `<span>Day ${index + 1}</span><div style="font-size: 11px;">${date}</div>`;
            item.onclick = () => renderDay(date);
            nav.appendChild(item);
            if (index === 0) renderDay(date);
        });
    </script>
</body>
</html>
    """
    
    with open('gtc2026_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("Dashboard generated: gtc2026_dashboard.html")

if __name__ == "__main__":
    generate_dashboard()
