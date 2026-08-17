import { db, auth } from '@/lib/firebase';
import {
  doc,
  setDoc,
  getDoc,
  collection,
  query,
  where,
  getDocs,
  serverTimestamp,
  orderBy,
  limit
} from 'firebase/firestore';
import api, { masteryService } from './api';

export interface ConceptMastery {
  conceptId: string;
  foundation: number;
  application: number;
  mastery?: number;
}

export interface MasteryRecord {
  chapterId: string;
  subject: string;
  className: string;
  score: number;
  status: 'NOT_STARTED' | 'LEARNING' | 'PRACTICING' | 'ASSESSMENT_READY' | 'ASSESSING' | 'NEEDS_REMEDIATION' | 'REASSESSING' | 'MASTERED' | 'MASTERED_PROVISIONAL' | 'MASTERED_STABLE' | 'MASTERED_AT_RISK' | 'REVIEW_DUE' | 'RETENTION_CHECK';
  lastAccessed: any;
  attempts: number;
  uid: string;
  progress?: number;
  conceptPerformance?: Record<string, ConceptMastery>;
  evidence?: {
    understand: boolean;
    apply: boolean;
    analyze: boolean;
    transfer: boolean;
    teach: boolean;
    retention?: boolean;
  };
  retention_verified?: boolean;
  retention_at_risk?: boolean;
  last_quiz_score?: number;
  feynman_score?: number;
}

export const progressService = {
  async updateStatus(chapterId: string, subject: string, className: string, status: MasteryRecord['status']) {
    const user = auth.currentUser;
    if (!user) return;

    try {
      const id = `${user.uid}_${chapterId}`;
      const ref = doc(db, 'mastery', id);
      const snap = await getDoc(ref);

      const baseData = snap.exists() ? snap.data() : {
        uid: user.uid,
        chapterId,
        subject,
        className,
        conceptPerformance: {},
        evidence: { understand: false, apply: false, analyze: false, transfer: false, teach: false },
        attempts: 0,
        progress: 0
      };

      await setDoc(ref, {
        ...baseData,
        status,
        lastAccessed: serverTimestamp(),
      }, { merge: true });
    } catch (err) {
      console.error("Error updating status:", err);
    }
  },

  async recordQuizResult(chapterId: string, subject: string, className: string, quizResults: any[]) {
    const user = auth.currentUser;
    if (!user) return;

    try {
      const id = `${user.uid}_${chapterId}`;
      const ref = doc(db, 'mastery', id);
      const snap = await getDoc(ref);

      const currentRecord = snap.exists() ? snap.data() : {
        uid: user.uid,
        chapterId,
        subject,
        className,
        status: 'NOT_STARTED',
        conceptPerformance: {},
        evidence: { understand: false, apply: false, analyze: false, transfer: false, teach: false }
      };

      // Call Backend to process results and calculate new state
      const response = await api.post('/api/mastery/process-results', {
        uid: user.uid,
        class_name: className,
        subject,
        chapter_id: chapterId,
        quiz_results: quizResults,
        current_record: currentRecord
      });

      const { updated_record } = response.data;

      await setDoc(ref, {
        ...updated_record,
        lastAccessed: serverTimestamp(),
      }, { merge: true });

      return response.data;
    } catch (err) {
      console.error("Error recording quiz result:", err);
      throw err;
    }
  },

  async updateMastery(chapterId: string, subject: string, className: string, scoreOrResults: any) {
    if (Array.isArray(scoreOrResults)) {
      return this.recordQuizResult(chapterId, subject, className, scoreOrResults);
    }
    // Legacy support for simple score
    return this.updateStatus(chapterId, subject, className, scoreOrResults >= 0.8 ? 'MASTERED' : 'LEARNING');
  },

  async recordFeynmanScore(chapterId: string, subject: string, className: string, score: number) {
    const user = auth.currentUser;
    if (!user) return;

    try {
      const id = `${user.uid}_${chapterId}`;
      const ref = doc(db, 'mastery', id);
      const snap = await getDoc(ref);

      let currentRecord = snap.exists() ? snap.data() : {
        uid: user.uid,
        chapterId,
        subject,
        className,
        status: 'NOT_STARTED',
        conceptPerformance: {},
        evidence: { understand: false, apply: false, analyze: false, transfer: false, teach: false }
      };

      currentRecord.feynman_score = score;

      const response = await api.post('/api/mastery/calculate-state', {
          class_name: className,
          subject,
          chapter_id: chapterId,
          student_record: currentRecord
      });

      const newState = response.data;
      currentRecord.status = newState.status;
      currentRecord.evidence = newState.evidence;
      currentRecord.progress = newState.progress;

      await setDoc(ref, {
        ...currentRecord,
        lastAccessed: serverTimestamp(),
      }, { merge: true });

      return newState;
    } catch (err) {
      console.error("Error recording feynman score:", err);
    }
  },

  async saveDiagnosticSignals(chapterId: string, signals: Record<string, string>) {
    const user = auth.currentUser;
    if (!user) return;

    try {
      const id = `${user.uid}_${chapterId}`;
      const ref = doc(db, 'mastery', id);
      await setDoc(ref, {
        diagnosticSignals: signals,
        lastDiagnosticAt: serverTimestamp(),
      }, { merge: true });
    } catch (err) {
      console.error("Error saving diagnostic signals:", err);
    }
  },

  async recordError(data: {
    uid: string,
    question_id: string,
    concept_id: string,
    chapter_id: string,
    error_type: string
  }) {
    try {
      const response = await api.post('/api/mastery/record-error', data);
      return response.data;
    } catch (err) {
      console.error("Error recording classified error:", err);
    }
  },

  async getMastery(chapterId: string): Promise<MasteryRecord | null> {
    const user = auth.currentUser;
    if (!user) return null;

    try {
      const id = `${user.uid}_${chapterId}`;
      const ref = doc(db, 'mastery', id);
      const snap = await getDoc(ref);
      if (snap.exists()) {
        return snap.data() as MasteryRecord;
      }
      return null;
    } catch (err) {
      console.error("Error fetching mastery record:", err);
      return null;
    }
  },

  async getStudentMastery(): Promise<MasteryRecord[]> {
    const user = auth.currentUser;
    if (!user) return [];

    try {
      const q = query(collection(db, 'mastery'), where('uid', '==', user.uid));
      const snap = await getDocs(q);
      return snap.docs.map(d => d.data() as MasteryRecord);
    } catch (err) {
      console.error("Error fetching mastery:", err);
      return [];
    }
  },

  async getRecentActivity(count = 5) {
    const user = auth.currentUser;
    if (!user) return [];

    try {
      const q = query(
        collection(db, 'mastery'),
        where('uid', '==', user.uid),
        orderBy('lastAccessed', 'desc'),
        limit(count)
      );
      const snap = await getDocs(q);
      return snap.docs.map(d => d.data());
    } catch (err: any) {
      console.error("Firestore getRecentActivity error:", err);
      // Fallback if index is missing or permission issue
      try {
        const fallbackQ = query(
          collection(db, 'mastery'),
          where('uid', '==', user.uid),
          limit(count)
        );
        const fallbackSnap = await getDocs(fallbackQ);
        return fallbackSnap.docs.map(d => d.data());
      } catch (fallbackErr) {
        console.error("Fallback activity fetch failed:", fallbackErr);
        return [];
      }
    }
  }
};
