# write_dashboard.py
from pathlib import Path

content = r"""
{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}

{% block content %}
<style>
  :root{
    --bg:#f6f8fb; --card:#ffffff; --muted:#6b7280; --accent:#2563eb; --accent-2:#10b981;
    --surface-shadow: 0 6px 18px rgba(20,20,31,0.06); --radius:12px; --gap:18px;
    font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  }
  .container{ max-width:1180px; margin:28px auto; padding:0 18px; }
  h2{ font-size:32px; margin:0 0 8px; color:#0f172a; }
  .grid{ display:grid; grid-template-columns: 1fr 320px; gap:var(--gap); align-items:start; }
  @media(max-width:900px){ .grid{ grid-template-columns: 1fr; } }
  .card{ background:var(--card); border-radius:var(--radius); padding:18px; box-shadow:var(--surface-shadow);
         border:1px solid rgba(15,23,42,0.04); }
  .card h3{ margin:0 0 10px; font-size:20px; color:#0b1220; }
  .muted{ color:var(--muted); font-size:14px; }
  .small{ font-size:13px; color:var(--muted); }
  table{ width:100%; border-collapse:collapse; font-size:15px; }
  table th, table td{ padding:10px 8px; text-align:left; border-bottom:1px solid rgba(15,23,42,0.04); }
  table thead th{ color:#0b1220; font-weight:600; }
  .btn{ display:inline-block; padding:8px 12px; border-radius:8px; text-decoration:none;
        background:transparent; border:1px solid rgba(15,23,42,0.06); color:#0b1220; font-weight:600; }
  .btn.primary{ background:var(--accent); color:#fff; border:0; }
  .btn.ghost{ background:transparent; border:1px solid rgba(15,23,42,0.06); }
  aside .card + .card{ margin-top:12px; }
  .hero{ display:flex; align-items:center; justify-content:space-between; gap:18px; margin-bottom:16px; }
  .hero .profile{ display:flex; align-items:center; gap:12px; }
  .avatar{ width:56px; height:56px; border-radius:12px; display:inline-flex; align-items:center; justify-content:center;
           background:linear-gradient(135deg,#dbeafe,#e0f2fe); color:#0b1220; font-weight:700; font-size:18px; }
  .chart-wrap{ width:100%; height:320px; }
  .small-note{ text-align:center; color:var(--muted); margin-top:22px; font-size:13px; }
</style>

<div class="container py-5">
  <h2>Student Dashboard</h2>
  <p>Welcome, {{ current_user.name if current_user.is_authenticated else 'student' }}.</p>

  <div class="row g-3 mt-3" style="display:flex; gap:12px; margin-bottom:18px;">
    <div style="flex:1; min-width:200px;">
      <div class="card p-3">My Courses</div>
    </div>
    <div style="flex:1; min-width:200px;">
      <div class="card p-3">Marks & Reports</div>
    </div>
    <div style="flex:1; min-width:200px;">
      <div class="card p-3">Settings</div>
    </div>
  </div>
</div>

<div class="container">
  <div class="hero">
    <div class="profile">
      <div class="avatar">{{ (current_user.name[:2] if current_user.is_authenticated else 'ST') | upper }}</div>
      <div>
        <h2>Welcome, {{ current_user.name if current_user.is_authenticated else "Student" }}</h2>
        <div class="small">Learning style: <strong>{{ getattr(current_user, 'learning_style', 'Not set') }}</strong>
          — <a href="{{ url_for('student.learning_style') }}">Edit</a></div>
      </div>
    </div>

    <div>
      <a class="btn" href="{{ url_for('main.index') }}">Home</a>
      <a class="btn primary" href="{{ url_for('student.add_mark') }}">Add Mark</a>
    </div>
  </div>

  <div class="grid">
    <!-- main column -->
    <div>
      <div class="card">
        <h3>Subject Averages</h3>
        {% if subject_averages %}
          <div class="chart-wrap"><canvas id="avgMarksChart"></canvas></div>
        {% else %}
          <p class="muted">No marks yet. <a href="{{ url_for('student.add_mark') }}">Add your first mark</a></p>
        {% endif %}
      </div>

      <!-- Recent marks table -->
      <div class="card" style="margin:16px 0;">
        <h3>Recent Marks</h3>

        {% if marks %}
          <table>
            <thead>
              <tr><th>Subject</th><th>Marks</th><th>Max</th><th>Date</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {% for m in marks %}
                <tr>
                  <td>{{ m.subject }}</td>
                  <td>{{ m.marks_obtained }}</td>
                  <td>{{ m.max_marks }}</td>
                  <td class="muted">{{ m.exam_date.strftime("%Y-%m-%d") if m.exam_date else "" }}</td>
                  <td>
                    <a href="{{ url_for('student.edit_mark', mark_id=m.id) }}">Edit</a> |
                    <a href="{{ url_for('student.delete_mark', mark_id=m.id) }}"
                       onclick="return confirm('Delete this mark?')">Delete</a>
                  </td>
                </tr>
              {% endfor %}
            </tbody>
          </table>
        {% else %}
          <p class="muted">No marks recorded.</p>
        {% endif %}
      </div>

      <div class="card" style="margin-top:12px;">
        <h3>Attendance</h3>
        {% if attendance_pct is not none %}
          <p><strong>Attendance:</strong> {{ attendance_pct }}% ({{ present_days }} / {{ total_days }})</p>
          <div class="chart-wrap"><canvas id="attendanceChart"></canvas></div>
        {% else %}
          <p class="muted">No attendance recorded yet. <a href="{{ url_for('student.add_attendance') }}">Add attendance</a></p>
        {% endif %}
      </div>
    </div>

    <!-- sidebar -->
    <aside>
      <div class="card recommendations">
        <h3>Personalized Recommendations</h3>
        {% if recommendations %}
          <ul>
            {% for r in recommendations %}
              <li>{{ r }}</li>
            {% endfor %}
          </ul>
        {% else %}
          <p class="muted">No recommendations yet — add marks and attendance.</p>
        {% endif %}
      </div>

      <div class="card" style="margin-top:12px;">
        <h3>Quick Actions</h3>
        <p class="small">Shortcuts</p>
        <p><a class="btn primary" href="{{ url_for('student.add_mark') }}">Add Mark</a></p>
        <p><a class="btn" href="{{ url_for('student.add_attendance') }}">Add Attendance</a></p>
        <p><a class="btn ghost" href="{{ url_for('student.learning_style') }}">Set Learning Style</a></p>
      </div>
    </aside>
  </div>

  <div class="card" style="margin-top:18px;">
    <h3>Notes</h3>
    <p class="muted">This is a student dashboard demo. Charts are client-side visualisations based on server data.</p>
  </div>

  <div class="small-note">EduMentor — built for learning</div>
</div>

<!-- Chart.js CDN -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const subjectAverages = {{ subject_averages | default({}) | tojson | safe }};
const subjects = Object.keys(subjectAverages || {});
const avgPercents = subjects.map(s => subjectAverages[s] || 0);

const rawSubjects   = {{ subjects_raw   | default([]) | tojson | safe }};
const marksObtained = {{ marks_obtained | default([]) | tojson | safe }};
const maxMarks      = {{ max_marks      | default([]) | tojson | safe }};
const presentDays   = Number({{ present_days | default(0) | tojson | safe }});
const totalDays     = Number({{ total_days   | default(0) | tojson | safe }});

function buildBarChart(canvasId, labels, datasets, options) {
  const el = document.getElementById(canvasId);
  if (!el) return null;
  new Chart(el, { type: 'bar', data: { labels, datasets }, options: options || { responsive: true } });
}

if (subjects.length) {
  buildBarChart('avgMarksChart', subjects, [{
    label: 'Average %',
    data: avgPercents,
    backgroundColor: avgPercents.map(() => 'rgba(59,130,246,0.85)')
  }], { scales: { y: { beginAtZero: true, max: 100 } }});
}

if (totalDays > 0) {
  const absent = Math.max(0, totalDays - presentDays);
  new Chart(document.getElementById('attendanceChart'), {
    type: 'pie',
    data: {
      labels: ['Present', 'Absent'],
      datasets: [{ data: [presentDays, absent], backgroundColor: ['#10B981','#EF4444'] }]
    },
    options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
  });
}
</script>
{% endblock %}
"""
out = Path("templates") / "student" / "dashboard.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(content, encoding="utf-8")
print("Wrote", out.resolve())
