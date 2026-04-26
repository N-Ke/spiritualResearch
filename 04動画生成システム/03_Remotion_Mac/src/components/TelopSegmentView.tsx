import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { TelopSegment } from "../types";

/**
 * テキスト内の {keyword} をハイライト付きで分割レンダリング
 * 例: "アドセンスだけで{月50万円}を稼いでいた" 
 *   → ["アドセンスだけで", <span style={highlight}>月50万円</span>, "を稼いでいた"]
 */
function renderHighlightedText(text: string) {
  const parts = text.split(/(\{[^}]+\})/g);
  return parts.map((part, i) => {
    if (part.startsWith("{") && part.endsWith("}")) {
      const keyword = part.slice(1, -1);
      return (
        <span
          key={i}
          style={{
            color: "#FFD700",
            textShadow:
              "0 2px 8px rgba(255,180,0,0.5), 0 0px 2px rgba(0,0,0,0.9)",
          }}
        >
          {keyword}
        </span>
      );
    }
    return <React.Fragment key={i}>{part}</React.Fragment>;
  });
}

/**
 * TelopSegmentView (SKILL.md準拠 + キーワードハイライト)
 * 
 * Sequence内でマウントされるため useCurrentFrame() は0始まり。
 */
export const TelopSegmentView: React.FC<{ segment: TelopSegment }> = ({ segment }) => {
  const frame = useCurrentFrame();
  const duration = segment.durationFrames;

  // フェードイン: 10フレーム
  const fadeIn = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  // フェードアウト: 最後6フレーム
  const fadeOut = interpolate(frame, [Math.max(0, duration - 6), duration], [1, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  const opacity = Math.min(fadeIn, fadeOut);

  // スライドイン: 下から15px
  const slideY = interpolate(frame, [0, 10], [15, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center" }}>
      <div
        style={{
          width: "100%",
          padding: "50px 80px 48px 80px",
          minHeight: "180px",
          background:
            "linear-gradient(to top, rgba(0,0,0,0.90) 0%, rgba(0,0,0,0.78) 55%, rgba(0,0,0,0) 100%)",
          opacity,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 100,
        }}
      >
        <div
          style={{
            transform: `translateY(${slideY}px)`,
            fontSize: 60,
            fontWeight: 800,
            fontFamily:
              "'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif",
            color: "white",
            textShadow:
              "0 2px 8px rgba(0,0,0,0.8), 0 0px 2px rgba(0,0,0,0.9)",
            WebkitTextStroke: "1px rgba(0,0,0,0.3)",
            lineHeight: 1.4,
            whiteSpace: "pre-line",
            textAlign: "center",
          }}
        >
          {renderHighlightedText(segment.text)}
        </div>
      </div>
    </AbsoluteFill>
  );
};
