import { initializeApp, getApps } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const isProduction = process.env.NODE_ENV === 'production';

const apiKey = process.env.NEXT_PUBLIC_FIREBASE_API_KEY;
const projectId = process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID;

if (isProduction && typeof window !== 'undefined' && (!apiKey || apiKey.includes('Dummy') || !projectId)) {
  console.error('CRITICAL: Missing or invalid production Firebase configuration. Please configure NEXT_PUBLIC_FIREBASE_API_KEY and NEXT_PUBLIC_FIREBASE_PROJECT_ID.');
}

const firebaseConfig = {
  apiKey: apiKey || (isProduction ? 'dummy-prod-key' : "AIzaSyDummyKeyForGurukulAI2026"),
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "com-ncert-projectgurukul-e5e60.firebaseapp.com",
  projectId: projectId || (isProduction ? 'com-ncert-projectgurukul-e5e60' : "com-ncert-projectgurukul-e5e60"),
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "com-ncert-projectgurukul-e5e60.appspot.com",
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "1234567890",
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || "1:1234567890:web:abcdef"
};

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const auth = getAuth(app);
export const db = getFirestore(app);
