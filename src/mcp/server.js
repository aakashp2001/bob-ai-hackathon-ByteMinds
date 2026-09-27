import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

import {
  getPersonProfile,
  getInvestigatorTips,
  getCctvSightings,
  getCaseData,
  getCorrelationResults,
  createBackendError
} from './backendClient.js';

const server = new McpServer({
  name: 'missing-person-case',
  version: '1.0.0'
}, {
  capabilities: { tools: {} }
});

function createToolResult(payload) {
  return {
    content: [{
      type: 'text',
      text: JSON.stringify(payload, null, 2)
    }]
  };
}

function toolErrorResponse(code, details = {}) {
  const error = createBackendError(code, details);
  return createToolResult({
    error: {
      code: error.code,
      message: error.message
    }
  });
}

server.registerTool('get_person_profile', {
  description: 'Retrieve the family-provided missing-person profile for a fictional case.',
  inputSchema: {
    caseNumber: z.string().min(1, 'caseNumber is required').describe('Fictional missing-person case number.')
  }
}, async ({ caseNumber }) => {
  try {
    return createToolResult(await getPersonProfile(caseNumber));
  } catch (error) {
    return toolErrorResponse(error.code || 'INVALID_BACKEND_RESPONSE', { caseNumber });
  }
});

server.registerTool('get_investigator_tips', {
  description: 'Retrieve all mock investigator tips without modifying or scoring them.',
  inputSchema: {
    caseNumber: z.string().min(1, 'caseNumber is required').describe('Fictional missing-person case number.')
  }
}, async ({ caseNumber }) => {
  try {
    return createToolResult(await getInvestigatorTips(caseNumber));
  } catch (error) {
    return toolErrorResponse(error.code || 'INVALID_BACKEND_RESPONSE', { caseNumber });
  }
});

server.registerTool('get_cctv_sightings', {
  description: 'Retrieve mock CCTV descriptions and preserve source IDs.',
  inputSchema: {
    caseNumber: z.string().min(1, 'caseNumber is required').describe('Fictional missing-person case number.')
  }
}, async ({ caseNumber }) => {
  try {
    return createToolResult(await getCctvSightings(caseNumber));
  } catch (error) {
    return toolErrorResponse(error.code || 'INVALID_BACKEND_RESPONSE', { caseNumber });
  }
});

server.registerTool('get_case_data', {
  description: 'Retrieve the full case context from the backend contract.',
  inputSchema: {
    caseNumber: z.string().min(1, 'caseNumber is required').describe('Fictional missing-person case number.')
  }
}, async ({ caseNumber }) => {
  try {
    return createToolResult(await getCaseData(caseNumber));
  } catch (error) {
    return toolErrorResponse(error.code || 'INVALID_BACKEND_RESPONSE', { caseNumber });
  }
});

server.registerTool('get_correlation_results', {
  description: 'Retrieve backend correlation results without recalculating scores.',
  inputSchema: {
    caseNumber: z.string().min(1, 'caseNumber is required').describe('Fictional missing-person case number.')
  }
}, async ({ caseNumber }) => {
  try {
    return createToolResult(await getCorrelationResults(caseNumber));
  } catch (error) {
    return toolErrorResponse(error.code || 'INVALID_BACKEND_RESPONSE', { caseNumber });
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('MCP server started');
}

main().catch((error) => {
  console.error('Server error:', error.message || error);
  process.exit(1);
});
