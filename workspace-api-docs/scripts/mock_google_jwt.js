#!/usr/bin/env node

/**
 * Mock Google OneTap JWT for testing
 * Structure: https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
 */

function generateMockGoogleJWT(options = {}) {
  const {
    email = 'test.user@example.com',
    emailVerified = true,
    name = 'Test User',
    picture = 'https://example.com/photo.jpg',
    givenName = 'Test',
    familyName = 'User',
    aud = 'your-client-id.apps.googleusercontent.com',
    iss = 'https://accounts.google.com',
    sub = '12345678901234567890', // Unique Google user ID
  } = options;

  const now = Math.floor(Date.now() / 1000);
  
  const payload = {
    iss,
    sub,
    aud,
    iat: now,
    exp: now + 3600, // 1 hour
    email,
    email_verified: emailVerified,
    name,
    picture,
    given_name: givenName,
    family_name: familyName,
    locale: 'en',
    hd: 'example.com', // Hosted domain (G Suite)
  };

  // Use any secret for testing (backend will verify via Google API in real scenario)
  // For local testing, backend might accept test tokens
  // Note: Using base64 encoding for mock (not real JWT signature)
  const header = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64');
  const payloadEncoded = Buffer.from(JSON.stringify(payload)).toString('base64');
  const signature = Buffer.from('mock-signature').toString('base64');
  
  return `${header}.${payloadEncoded}.${signature}`;
}

// Parse command line args
const args = process.argv.slice(2);
const options = {};

args.forEach(arg => {
  const [key, value] = arg.split('=');
  if (key === '--email') options.email = value;
  if (key === '--sub') options.sub = value;
  if (key === '--name') options.name = value;
  if (key === '--aud') options.aud = value;
});

const token = generateMockGoogleJWT(options);
console.log(token);
