/**
 * Mock Google OneTap JWT for testing
 * Structure: https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
 * 
 * Install: npm install jsonwebtoken
 * Usage: node mock_google_jwt.js --email "test@example.com" --sub "123456789"
 */

const jwt = require('jsonwebtoken');

const args = require('minimist')(process.argv.slice(2));

function generateMockGoogleJWT(options = {}) {
  const {
    email = 'test.user@example.com',
    emailVerified = true,
    name = 'Test User',
    picture = 'https://example.com/photo.jpg',
    givenName = 'Test',
    familyName = 'User',
    aud = 'test-client-id.apps.googleusercontent.com',
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

  // Use any secret for testing
  // Backend may need to accept test tokens in dev environment
  const token = jwt.sign(payload, 'test-secret-key-for-dev-only');
  
  return token;
}

// Parse command line args
const email = args.email || 'test.user@example.com';
const sub = args.sub || `${Date.now()}${Math.random().toString(36).substring(7)}`;
const name = args.name || 'Test User';
const givenName = args.givenName || name.split(' ')[0];
const familyName = args.familyName || name.split(' ')[1] || 'User';

const token = generateMockGoogleJWT({
  email,
  sub,
  name,
  givenName,
  familyName,
  emailVerified: true
});

// Output only the token (for piping)
console.log(token);
