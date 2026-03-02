import { defineWalletSetup } from '@synthetixio/synpress-cache';
import { Phantom } from '@synthetixio/synpress-phantom/playwright';

// Seed phrase for test wallet (should be in .env)
const TEST_SEED_PHRASE = process.env.TEST_WALLET_SEED || 'test test test test test test test test test test test test';
const WALLET_PASSWORD = process.env.TEST_WALLET_PASSWORD || 'TestPassword123!';

export default defineWalletSetup(WALLET_PASSWORD, async (context, walletPage) => {
  console.log('Setting up Phantom wallet...');
  
  // Create Phantom instance
  const phantom = new Phantom(context, walletPage, WALLET_PASSWORD);
  
  // Import wallet using seed phrase
  await phantom.importWallet(TEST_SEED_PHRASE);
  
  console.log('Phantom wallet setup complete');
});