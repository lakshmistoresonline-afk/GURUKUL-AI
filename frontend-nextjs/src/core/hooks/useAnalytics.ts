import { useEffect, useRef } from 'react';
import { studentApi } from '@/services/api/student_api';
import { useAuth } from '../context/AuthContext';

export const useAnalytics = (conceptId?: string) => {
  const { user } = useAuth();
  const heartbeatInterval = useRef<any>(null);

  useEffect(() => {
    if (!user) return;

    // Log concept view if provided
    if (conceptId) {
      studentApi.logEvent('CONCEPT_VIEWED', { concept_id: conceptId });
    }

    // Start heartbeat (every 30s)
    heartbeatInterval.current = setInterval(() => {
      studentApi.logEvent('SESSION_HEARTBEAT', {
        concept_id: conceptId,
        path: window.location.pathname
      });
    }, 30000);

    return () => {
      if (heartbeatInterval.current) {
        clearInterval(heartbeatInterval.current);
      }
    };
  }, [user, conceptId]);
};
