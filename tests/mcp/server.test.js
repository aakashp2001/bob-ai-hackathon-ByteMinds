import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const serverPath = path.join(projectRoot, 'src', 'mcp', 'server.js');

test('MCP server discovers all five tools and serves a profile through stdio', async () => {
  const client = new Client({ name: 'mcp-contract-test', version: '1.0.0' });
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [serverPath],
    cwd: projectRoot,
    env: {
      ...process.env,
      BACKEND_BASE_URL: 'http://127.0.0.1:9',
      BACKEND_TIMEOUT_MS: '100'
    }
  });

  await client.connect(transport);
  const tools = await client.listTools();
  const toolNames = tools.tools.map((tool) => tool.name).sort();

  assert.deepEqual(toolNames, [
    'get_case_data',
    'get_cctv_sightings',
    'get_correlation_results',
    'get_investigator_tips',
    'get_person_profile'
  ]);

  const result = await client.callTool({
    name: 'get_person_profile',
    arguments: { caseNumber: 'MP-2026-0042' }
  });
  const profile = JSON.parse(result.content[0].text);
  assert.equal(profile.error.code, 'BACKEND_UNAVAILABLE');

  await client.close();
});
