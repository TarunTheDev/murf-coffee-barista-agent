'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useRoomContext } from '@livekit/components-react';
import { motion, AnimatePresence } from 'motion/react';

export function OrderVisualization() {
  const room = useRoomContext();
  const [htmlContent, setHtmlContent] = useState<string>('');
  const [isVisible, setIsVisible] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | undefined>();
  const isShowingRef = useRef(false);

  const muteRemoteAudio = useCallback(
    (shouldMute: boolean) => {
      if (!room) return;
      try {
        room.remoteParticipants.forEach((participant: any) => {
          const trackMap = participant.audioTracks;
          if (!trackMap || typeof trackMap.forEach !== 'function') return;
          trackMap.forEach((publication: any) => {
            publication?.audioTrack?.setVolume(shouldMute ? 0 : 1);
          });
        });
      } catch (error) {
        console.warn('Error muting audio:', error);
      }
    },
    [room],
  );

  const notifyBackendClosed = useCallback(() => {
    if (!room) return;
    try {
      const payload = new TextEncoder().encode('receipt-closed');
      room.localParticipant.publishData(payload, { topic: 'visualization-closed' });
    } catch (error) {
      console.warn('Failed to notify backend:', error);
    }
  }, [room]);

  const closeVisualization = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = undefined;
    }
    setIsVisible(false);
    setHtmlContent('');
    isShowingRef.current = false;
    muteRemoteAudio(false);
    notifyBackendClosed();
  }, [muteRemoteAudio, notifyBackendClosed]);

  const showVisualization = useCallback(
    (html: string) => {
      // Prevent multiple rapid shows
      if (isShowingRef.current) return;
      
      isShowingRef.current = true;
      setHtmlContent(html);
      setIsVisible(true);
      muteRemoteAudio(true);

      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      timeoutRef.current = setTimeout(() => {
        closeVisualization();
      }, 30000);
    },
    [closeVisualization, muteRemoteAudio],
  );

  const handleClose = useCallback(() => {
    closeVisualization();
  }, [closeVisualization]);

  // Listen for visualization payloads from the backend
  useEffect(() => {
    if (!room) return;

    const handleData = (
      payload: Uint8Array,
      participant?: any,
      kind?: any,
      topic?: string,
    ) => {
      if (topic === 'order-visualization') {
        // Ignore if already showing to prevent flicker
        if (isShowingRef.current) return;
        
        const decoder = new TextDecoder();
        const html = decoder.decode(payload);
        showVisualization(html);
      }
    };

    room.on('dataReceived', handleData);

    return () => {
      room.off('dataReceived', handleData);
    };
  }, [room, showVisualization]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return (
    <AnimatePresence mode="wait">
      {isVisible && htmlContent && (
        <motion.div
          key="order-viz-stable"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
          onClick={handleClose}
          style={{ willChange: 'opacity' }}
        >
          <motion.div
            initial={{ y: 20 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.3 }}
            className="relative max-w-2xl w-full max-h-[90vh] overflow-auto rounded-2xl shadow-2xl"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
            style={{ willChange: 'transform' }}
          >
            <button
              onClick={handleClose}
              className="absolute top-4 right-4 z-10 bg-white/90 hover:bg-white text-gray-800 rounded-full w-10 h-10 flex items-center justify-center shadow-lg transition-all hover:scale-110"
              aria-label="Close"
            >
              ✕
            </button>
            <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
