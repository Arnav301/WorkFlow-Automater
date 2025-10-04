import React, { useEffect, useState } from 'react'
import { Routes, Route, Link, NavLink } from 'react-router-dom'
import { executeWorkflow, getWorkflowStatus, health, listWorkflows, listExecutions, getExecution, listExtracted } from './api'
import { BoltIcon, CheckCircleIcon, XMarkIcon, ClockIcon } from './icons'

export default function App() {
  const [healthy, setHealthy] = useState(true)
  const [desc, setDesc] = useState('Login and extract dashboard data')
  const [params, setParams] = useState({ username: '', password: '' })
  const [running, setRunning] = useState(false)
  const [workflowId, setWorkflowId] = useState('')
  const [status, setStatus] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    health().then(setHealthy).catch(() => setHealthy(false))
  }, [])

  useEffect(() => {
    if (!workflowId) return
    const iv = setInterval(async () => {
      try {
        const s = await getWorkflowStatus(workflowId)
        setStatus(s)
        if (s && (s.status === 'completed' || s.status === 'failed')) {
          setRunning(false)
          clearInterval(iv)
        }
      } catch (e) {
        setError(String(e))
        setRunning(false)
        clearInterval(iv)
      }
    }, 1000)
    return () => clearInterval(iv)
  }, [workflowId])

  async function onRun(e) {
    e.preventDefault()
    setError('')
    setStatus(null)
    setRunning(true)
    try {
      const res = await executeWorkflow(desc, params)
      setWorkflowId(res.workflow_id)
    } catch (e) {
      setError(String(e))
      setRunning(false)
    }
  }

  return (
    <div className="page">
      <TopBar healthy={healthy} />
      <main className="container">
        <Routes>
          <Route path="/" element={<Dashboard {...{status, running, onRun, desc, setDesc, params, setParams, workflowId, error}} />} />
          <Route path="/workflows" element={<WorkflowsPage />} />
          <Route path="/executions" element={<ExecutionsPage />} />
          <Route path="/extracted" element={<ExtractedPage />} />
        </Routes>
      </main>
    </div>
  )
}

function TopBar({ healthy }) {
  return (
    <header className="topbar">
      <div className="brand">
        <span className="logo">⚡</span>
        <span>Workflow Automator</span>
      </div>
      <nav className="nav">
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/workflows">Workflows</NavLink>
        <NavLink to="/executions">Executions</NavLink>
        <NavLink to="/extracted">Extracted Data</NavLink>
      </nav>
      <div>
        <span className={`badge ${healthy ? 'ok' : 'bad'}`}>{healthy ? 'API Online' : 'API Offline'}</span>
      </div>
    </header>
  )
}

function Dashboard({ status, running, onRun, desc, setDesc, params, setParams, workflowId, error }){
  return (
    <>
      <Metrics status={status} />
      <section className="card">
        <div className="card-header">
          <h2>New Workflow</h2>
          <button className="btn primary" onClick={onRun} disabled={running}>
            <span className="icon">+</span> Run
          </button>
        </div>
        <form className="form" onSubmit={onRun}>
          <label>
            <span>Description</span>
            <textarea value={desc} onChange={e => setDesc(e.target.value)} rows={3} placeholder="Describe what to automate..." />
          </label>
          <div className="grid">
            <label>
              <span>Username</span>
              <input value={params.username} onChange={e => setParams(p => ({ ...p, username: e.target.value }))} placeholder="username" />
            </label>
            <label>
              <span>Password</span>
              <input type="password" value={params.password} onChange={e => setParams(p => ({ ...p, password: e.target.value }))} placeholder="password" />
            </label>
          </div>
          <button type="submit" className="btn" disabled={running}>Execute</button>
        </form>
      </section>

      <section className="cards">
        <Stat title="Total Executions" value={status?.steps?.length ?? 0} icon={<BoltIcon />} />
        <Stat title="Successful" value={status?.steps?.filter(s => s.status === 'completed').length ?? 0} icon={<CheckCircleIcon />} />
        <Stat title="Failed" value={status?.status === 'failed' ? 1 : 0} icon={<XMarkIcon />} />
        <Stat title="Running" value={running ? 1 : 0} icon={<ClockIcon />} />
      </section>

      <section className="card">
        <div className="card-header">
          <h3>Execution Details</h3>
          {workflowId && <code className="muted">{workflowId}</code>}
        </div>
        <Timeline status={status} />
        {error && <div className="error">{error}</div>}
      </section>
    </>
  )
}

function Placeholder({ title, subtitle }){
  return (
    <section className="card">
      <div className="card-header"><h2>{title}</h2></div>
      <div className="empty">
        <div style={{textAlign:'center'}}>
          <div className="pill">No data yet</div>
          <div style={{marginTop:10}} className="muted">{subtitle}</div>
          <div style={{marginTop:14}}>
            <Link className="btn" to="/">Go to Dashboard</Link>
          </div>
        </div>
      </div>
    </section>
  )
}

function Metrics({ status }) {
  return (
    <section className="cards">
      <Stat title="Progress" value={`${status?.progress ?? 0}%`} icon={<BoltIcon />} />
      <Stat title="Status" value={status?.status ?? 'idle'} icon={<ClockIcon />} />
      <Stat title="Current Step" value={status?.current_step?.action ?? '-'} icon={<BoltIcon />} />
      <Stat title="Vision" value={String(status?.vision_enabled ?? false)} icon={<BoltIcon />} />
    </section>
  )
}

function Stat({ title, value, icon }) {
  return (
    <div className="stat">
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <div className="stat-title">{title}</div>
        <div className="stat-value">{value}</div>
      </div>
    </div>
  )
}

function Timeline({ status }) {
  const steps = status?.steps ?? []
  return (
    <ul className="timeline">
      {steps.length === 0 && <li className="muted">No steps yet</li>}
      {steps.map((s, idx) => (
        <li key={idx} className="timeline-item">
          <div className={`dot ${s.status === 'completed' ? 'ok' : 'pending'}`}></div>
          <div>
            <div className="timeline-title">{s.step}</div>
            <div className="timeline-sub">{s.details || s.status}</div>
          </div>
        </li>
      ))}
    </ul>
  )
}

// List Pages
function WorkflowsPage(){
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [err, setErr] = useState('')
  useEffect(() => {
    let mounted = true
    listWorkflows()
      .then(d => { if (mounted){ setItems(d.items || []); setLoading(false) }})
      .catch(e => { if (mounted){ setErr(String(e)); setLoading(false) }})
    return () => { mounted = false }
  }, [])
  return (
    <section className="card">
      <div className="card-header"><h2>Workflows</h2></div>
      {loading ? <div className="empty"><div className="pill">Loading...</div></div> :
       items.length === 0 ? <div className="empty"><div className="pill">No workflows yet</div></div> : (
        <div style={{overflowX:'auto'}}>
          <table className="table">
            <thead><tr><th>ID</th><th>Name</th><th>Description</th><th>Steps</th></tr></thead>
            <tbody>
              {items.map(it => (
                <tr key={it.workflow_id}>
                  <td><code className="muted">{it.workflow_id}</code></td>
                  <td>{it.name}</td>
                  <td className="muted">{it.description}</td>
                  <td>{it.steps_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {err && <div className="error">{err}</div>}
    </section>
  )
}

function ExecutionsPage(){
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [err, setErr] = useState('')
  useEffect(() => {
    let mounted = true
    listExecutions()
      .then(d => { if (mounted){ setItems(d.items || []); setLoading(false) }})
      .catch(e => { if (mounted){ setErr(String(e)); setLoading(false) }})
    return () => { mounted = false }
  }, [])
  return (
    <section className="card">
      <div className="card-header"><h2>Executions</h2></div>
      {loading ? <div className="empty"><div className="pill">Loading...</div></div> :
       items.length === 0 ? <div className="empty"><div className="pill">No executions yet</div></div> : (
        <div style={{overflowX:'auto'}}>
          <table className="table">
            <thead><tr><th>ID</th><th>Status</th><th>Progress</th><th>Last Step</th><th>Steps Completed</th></tr></thead>
            <tbody>
              {items.map(it => (
                <tr key={it.workflow_id}>
                  <td><code className="muted">{it.workflow_id}</code></td>
                  <td>{it.status}</td>
                  <td>{it.progress}%</td>
                  <td className="muted">{it.last_step?.action || '-'}</td>
                  <td>{it.steps_completed}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {err && <div className="error">{err}</div>}
    </section>
  )
}

function ExtractedPage(){
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [err, setErr] = useState('')
  useEffect(() => {
    let mounted = true
    listExtracted()
      .then(d => { if (mounted){ setItems(d.items || []); setLoading(false) }})
      .catch(e => { if (mounted){ setErr(String(e)); setLoading(false) }})
    return () => { mounted = false }
  }, [])
  return (
    <section className="card">
      <div className="card-header"><h2>Extracted Data</h2></div>
      {loading ? <div className="empty"><div className="pill">Loading...</div></div> :
       items.length === 0 ? <div className="empty"><div className="pill">No extracted data yet</div></div> : (
        <div style={{display:'grid', gap:12}}>
          {items.map(it => (
            <div key={it.workflow_id} className="table-like">
              <div style={{marginBottom:6}}><code className="muted">{it.workflow_id}</code></div>
              <pre style={{whiteSpace:'pre-wrap', background:'rgba(255,255,255,0.03)', padding:12, borderRadius:10, border:'1px solid var(--border)'}}>{JSON.stringify(it.data, null, 2)}</pre>
            </div>
          ))}
        </div>
      )}
      {err && <div className="error">{err}</div>}
    </section>
  )
}
