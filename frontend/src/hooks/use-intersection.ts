"use client";
import { useEffect, useRef, useCallback } from "react";

export function useIntersection(onIntersect: () => void) {
  const callbackRef = useRef(onIntersect);
  callbackRef.current = onIntersect;

  const sentinelRef = useRef<HTMLDivElement | null>(null);

  const setRef = useCallback((node: HTMLDivElement | null) => {
    sentinelRef.current = node;
  }, []);

  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) callbackRef.current();
      },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  });

  return setRef;
}
