const https = require('https');

// Jira configuration - adjust these values
const JIRA_BASE_URL = 'https://your-domain.atlassian.net';
const JIRA_EMAIL = process.env.JIRA_EMAIL;
const JIRA_API_TOKEN = process.env.JIRA_API_TOKEN;
const PROJECT_KEY = 'PandaSen';

// Query for tickets in Ready for Testing or On Production
const query = {
  jql: `project = ${PROJECT_KEY} AND status in ("Ready for Testing", "On Production") ORDER BY updated DESC`,
  fields: ['key', 'summary', 'description', 'status', 'issuelinks', 'comments', 'attachments', 'updated'],
  maxResults: 20
};

// Using the correct API endpoint
const options = {
  hostname: 'your-domain.atlassian.net',
  path: `/rest/api/3/search?jql=${encodeURIComponent(query.jql)}&fields=${query.fields.join(',')}&maxResults=${query.maxResults}`,
  method: 'GET',
  headers: {
    'Authorization': `Basic ${Buffer.from(`${JIRA_EMAIL}:${JIRA_API_TOKEN}`).toString('base64')}`,
    'Accept': 'application/json'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    try {
      const result = JSON.parse(data);
      console.log(JSON.stringify(result, null, 2));
    } catch (e) {
      console.error('Error parsing response:', e.message);
      console.log(data);
    }
  });
});

req.on('error', (e) => {
  console.error('Error making request:', e.message);
});

req.end();
