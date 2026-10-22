"""Builds the SomaiyaSat read-only mission report from SQLite data."""
import html
import os
import webbrowser

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "website", "index.html")


def safe(value):
    """Escape database values before placing them in HTML."""
    return html.escape(str(value if value is not None else ""))


def build(db):
    rows = db.packets()
    passes = db.passes()
    sent = sum(1 for row in rows if row[4] == "SENT")
    deferred = sum(1 for row in rows if row[4] == "DEFERRED")
    waiting = sum(1 for row in rows if row[4] == "WAITING")
    latest = passes[0] if passes else None
    link = max(0, min(100, int(latest[1]))) if latest else 0
    signal_class = "good" if link >= 60 else "medium" if link >= 35 else "low"
    signal_text = "Strong" if link >= 60 else "Moderate" if link >= 35 else "Weak"

    packet_rows = "".join(
        "<tr>"
        f"<td class='mono'>#{safe(r[0])}</td>"
        f"<td><span class='mode'>{safe(r[1])}</span></td>"
        f"<td>{safe(r[2])} <span class='muted'>bytes</span></td>"
        f"<td><span class='urgency'>{safe(r[3])}/5</span></td>"
        f"<td><span class='status {safe(r[4]).lower()}'>{safe(r[4])}</span></td>"
        f"<td class='reason'>{safe(r[5]) or '—'}</td></tr>"
        for r in rows
    ) or "<tr><td colspan='6' class='empty'>No packets yet. Add packets in the desktop planner, then build this report.</td></tr>"

    pass_rows = "".join(
        "<article class='pass-card'>"
        f"<div class='pass-top'><span class='pass-label'>GROUND PASS</span><span class='pass-number'>#{safe(p[0])}</span></div>"
        f"<div class='pass-signal'>{safe(p[1])}% <span>signal strength</span></div>"
        f"<div class='mini-stats'><div><b>{safe(p[2])}</b><span>Sent</span></div>"
        f"<div><b>{safe(p[3])}</b><span>Deferred</span></div>"
        f"<div><b>{safe(p[4])}s</b><span>Time left</span></div></div></article>"
        for p in passes
    ) or "<div class='empty-panel'>No ground passes recorded yet.</div>"

    last_pass_label = f"Pass #{safe(latest[0])} · {safe(latest[2])} sent · {safe(latest[3])} deferred" if latest else "Run a ground pass in the desktop planner to populate this report."
    html_page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SomaiyaSat | Mission Downlink Report</title>
<style>
:root{{--bg:#07111f;--panel:#101f33;--panel2:#132740;--line:#243a53;--text:#edf5ff;--muted:#9bb0c8;--cyan:#55d6ff;--green:#51dfa0;--orange:#ffbf69;--red:#ff737d}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(ellipse at 80% -15%,#163b5d 0,transparent 38%),var(--bg);color:var(--text);font:15px/1.55 'Segoe UI',Arial,sans-serif}}
.wrap{{max-width:1180px;margin:auto;padding:0 24px}}.topline{{height:4px;background:linear-gradient(90deg,#4bd8ff,#6287ff,#8d76ff)}}
header{{padding:34px 0 28px;border-bottom:1px solid var(--line)}}.brandrow{{display:flex;align-items:center;gap:13px}}.logo{{width:48px;height:48px;border-radius:15px;display:grid;place-items:center;background:#15344d;border:1px solid #2d5975;font-size:25px}}
.eyebrow{{color:var(--cyan);font-size:11px;font-weight:800;letter-spacing:2.1px;text-transform:uppercase}}h1{{font-size:clamp(25px,4vw,38px);line-height:1.15;margin:4px 0 7px;letter-spacing:-.7px}}.subtitle{{color:var(--muted);margin:0;max-width:650px}}.live{{margin-left:auto;align-self:flex-start;border:1px solid #285b4e;background:#0d2a29;color:var(--green);padding:7px 11px;border-radius:30px;font-size:11px;font-weight:800;letter-spacing:1px;white-space:nowrap}}
main{{padding:27px 0 46px}}.section-head{{display:flex;align-items:end;justify-content:space-between;gap:15px;margin:28px 0 13px}}.section-head h2{{margin:0;font-size:18px;letter-spacing:-.2px}}.section-head p{{margin:3px 0 0;color:var(--muted);font-size:13px}}.stamp{{color:var(--muted);font-size:12px}}
.hero-grid{{display:grid;grid-template-columns:1.2fr 1fr;gap:16px}}.panel,.metric,.pass-card{{background:linear-gradient(145deg,rgba(20,41,64,.96),rgba(12,27,44,.98));border:1px solid var(--line);border-radius:17px;box-shadow:0 12px 35px #0002}}.signal-panel{{padding:23px}}.signal-title{{color:var(--muted);font-size:12px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase}}.signal-number{{display:flex;align-items:baseline;gap:12px;margin:8px 0 14px}}.signal-number strong{{font-size:49px;line-height:1;font-weight:750;letter-spacing:-2px}}.signal-number span{{font-size:13px;color:var(--green);font-weight:700}}.bar{{height:10px;background:#26384d;border-radius:10px;overflow:hidden}}.bar i{{display:block;height:100%;width:{link}%;background:{'#51dfa0' if link >= 60 else '#ffbf69' if link >= 35 else '#ff737d'};border-radius:10px}}.scale{{display:flex;justify-content:space-between;color:#7f96b0;font-size:11px;margin-top:8px}}.lastpass{{margin-top:20px;padding-top:15px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}.lastpass b{{display:block;color:var(--text);font-size:14px;margin-bottom:3px}}
.metrics{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}.metric{{padding:19px;position:relative;overflow:hidden}}.metric:after{{content:'';position:absolute;width:70px;height:70px;border-radius:50%;right:-25px;top:-27px;background:#55d6ff0b}}.metric-label{{color:var(--muted);font-size:12px}}.metric-value{{font-size:32px;font-weight:750;line-height:1.3;margin:5px 0 2px}}.metric-foot{{font-size:11px;color:#7892ac}}.accent-green{{color:var(--green)}}.accent-orange{{color:var(--orange)}}.accent-cyan{{color:var(--cyan)}}.accent-good{{color:var(--green)}}.accent-medium{{color:var(--orange)}}.accent-low{{color:var(--red)}}
.table-panel{{overflow:hidden}}.table-scroll{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;min-width:760px}}thead{{background:#142940}}th{{text-align:left;color:#9db5cf;font-size:11px;text-transform:uppercase;letter-spacing:1px;padding:14px 16px;font-weight:800}}td{{padding:14px 16px;border-top:1px solid #1c3047;color:#dbe8f7;font-size:13px}}tbody tr:hover{{background:#ffffff05}}.mono{{font-family:Consolas,monospace;color:#86dfff}}.mode{{display:inline-block;border:1px solid #31516e;background:#142f49;border-radius:6px;padding:3px 7px;font-size:11px;font-weight:800}}.urgency{{color:#ffd28c;font-weight:700}}.muted{{color:var(--muted);font-size:11px}}.status{{display:inline-block;border-radius:20px;padding:4px 9px;font-size:10px;font-weight:900;letter-spacing:.6px}}.status.sent{{background:#123e35;color:var(--green)}}.status.deferred{{background:#49341f;color:var(--orange)}}.status.waiting{{background:#29364a;color:#c5d4e8}}.reason{{color:#9fb3ca;max-width:300px}}.empty,.empty-panel{{color:var(--muted);text-align:center;padding:28px}}
.passes{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.pass-card{{padding:17px}}.pass-top{{display:flex;justify-content:space-between;align-items:center}}.pass-label{{font-size:10px;letter-spacing:1.5px;color:var(--cyan);font-weight:900}}.pass-number{{font-size:12px;color:var(--muted)}}.pass-signal{{font-size:28px;font-weight:750;margin:12px 0 15px}}.pass-signal span{{font-size:11px;font-weight:400;color:var(--muted)}}.mini-stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;border-top:1px solid var(--line);padding-top:13px}}.mini-stats b,.mini-stats span{{display:block}}.mini-stats b{{font-size:16px}}.mini-stats span{{color:var(--muted);font-size:11px}}.how-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.how{{padding:17px;border:1px solid var(--line);border-radius:13px;background:#0b1a2b}}.how-num{{color:var(--cyan);font-size:11px;font-weight:900;letter-spacing:1px}}.how h3{{font-size:14px;margin:7px 0 5px}}.how p{{font-size:12px;color:var(--muted);margin:0}}footer{{border-top:1px solid var(--line);padding:20px 0 28px;color:#7188a2;font-size:11px}}.footrow{{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}}
@media(max-width:760px){{.hero-grid{{grid-template-columns:1fr}}.passes,.how-grid{{grid-template-columns:1fr}}.wrap{{padding:0 15px}}.live{{display:none}}header{{padding-top:25px}}.section-head{{align-items:start;flex-direction:column}}}}
</style></head><body><div class="topline"></div>
<header><div class="wrap"><div class="brandrow"><div class="logo">🛰️</div><div><div class="eyebrow">Mission operations · Data routing</div><h1>SomaiyaSat Downlink Report</h1><p class="subtitle">A live snapshot of packet readiness, downlink signal quality, and ground-pass outcomes.</p></div><div class="live">● LOCAL SIMULATION</div></div></div></header>
<main class="wrap">
<div class="section-head"><div><h2>Mission overview</h2><p>Summary calculated from the local SQLite database.</p></div><span class="stamp">Read-only report</span></div>
<div class="hero-grid"><section class="panel signal-panel"><div class="signal-title">Latest ground-station signal</div><div class="signal-number"><strong>{link}%</strong><span class="accent-{signal_class}">{signal_text} signal</span></div><div class="bar" role="img" aria-label="Signal strength {link} percent"><i></i></div><div class="scale"><span>0% · Weak</span><span>60% · Strong</span><span>100%</span></div><div class="lastpass"><b>Latest pass status</b>{last_pass_label}</div></section>
<div class="metrics"><div class="metric"><div class="metric-label">Total packets</div><div class="metric-value">{len(rows)}</div><div class="metric-foot">All recorded packet entries</div></div><div class="metric"><div class="metric-label">Successfully sent</div><div class="metric-value accent-green">{sent}</div><div class="metric-foot">Marked SENT</div></div><div class="metric"><div class="metric-label">Deferred packets</div><div class="metric-value accent-orange">{deferred}</div><div class="metric-foot">Signal or time constraint</div></div><div class="metric"><div class="metric-label">Waiting packets</div><div class="metric-value accent-cyan">{waiting}</div><div class="metric-foot">Not yet sent</div></div></div></div>
<div class="section-head"><div><h2>Packet manifest</h2><p>Each row shows the packet's current status and the planner's recorded reason.</p></div></div><section class="panel table-panel"><div class="table-scroll"><table><thead><tr><th>Packet ID</th><th>Mode</th><th>Data size</th><th>Urgency</th><th>Status</th><th>Decision note</th></tr></thead><tbody>{packet_rows}</tbody></table></div></section>
<div class="section-head"><div><h2>Ground-pass history</h2><p>Most recent pass appears first. Values are read from SQLite.</p></div></div><div class="passes">{pass_rows}</div>
<div class="section-head"><div><h2>How the planner works</h2><p>Three steps in the current simulation.</p></div></div><div class="how-grid"><article class="how"><div class="how-num">01 / PRIORITISE</div><h3>Order packets</h3><p>Python packet classes assign priority, so important telemetry is considered before lower-priority data.</p></article><article class="how"><div class="how-num">02 / CHECK</div><h3>Respect link and time</h3><p>The simulation checks each packet's minimum signal requirement and transmission time within a 60-second pass.</p></article><article class="how"><div class="how-num">03 / RECORD</div><h3>Save the outcome</h3><p>Packet decisions and pass summaries are stored in SQLite and displayed here when the report is built.</p></article></div>
</main><footer><div class="wrap footrow"><span>SOMAIYASAT · DOWNLINK PLANNER</span><span>Educational simulation only · No real satellite connection</span></div></footer></body></html>'''
    os.makedirs(os.path.dirname(SITE), exist_ok=True)
    with open(SITE, "w", encoding="utf-8") as file:
        file.write(html_page)
    webbrowser.open("file://" + SITE)
    return SITE
