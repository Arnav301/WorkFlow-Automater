export async function executeWorkflow(description, parameters) {
  const res = await fetch('/api/workflows/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description, parameters })
  });
  if (!res.ok) throw new Error(`Execute failed: ${res.status}`);
  return res.json();
}

export async function getWorkflowStatus(workflowId) {
  const res = await fetch(`/api/workflows/${encodeURIComponent(workflowId)}/status`);
  if (!res.ok) throw new Error(`Status failed: ${res.status}`);
  return res.json();
}

export async function health() {
  const res = await fetch('/health');
  return res.ok;
}

export async function listWorkflows() {
  const res = await fetch('/api/workflows');
  if (!res.ok) throw new Error(`List workflows failed: ${res.status}`);
  return res.json();
}

export async function listExecutions() {
  const res = await fetch('/api/executions');
  if (!res.ok) throw new Error(`List executions failed: ${res.status}`);
  return res.json();
}

export async function getExecution(workflowId) {
  const res = await fetch(`/api/executions/${encodeURIComponent(workflowId)}`);
  if (!res.ok) throw new Error(`Get execution failed: ${res.status}`);
  return res.json();
}

export async function listExtracted() {
  const res = await fetch('/api/extracted');
  if (!res.ok) throw new Error(`List extracted failed: ${res.status}`);
  return res.json();
}
