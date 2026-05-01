import { mkdir, readFile, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";

const timingData = JSON.parse(await readFile("audio/scene-timings.json", "utf8"));
await mkdir("scene-videos", { recursive: true });

const baseVideo = "pgs-math-explainer.mp4";
const concatLines = [];

for (let i = 0; i < timingData.scenes.length; i += 1) {
  const scene = timingData.scenes[i];
  const sceneNumber = String(i + 1).padStart(2, "0");
  const visualStart = i * 25;
  const sceneDuration = scene.audioDuration + 1.2;
  const stopPad = Math.max(0, sceneDuration - 25);
  const output = `scene-videos/${sceneNumber}-${scene.id}-voiced.mp4`;
  const videoFilter = [
    "fps=30",
    "scale=1920:1080",
    "setsar=1",
    `tpad=stop_mode=clone:stop_duration=${stopPad.toFixed(3)}`,
    `trim=duration=${sceneDuration.toFixed(3)}`,
    "setpts=PTS-STARTPTS",
  ].join(",");
  const audioFilter = [
    "apad",
    `atrim=duration=${sceneDuration.toFixed(3)}`,
    "asetpts=PTS-STARTPTS",
  ].join(",");
  const args = [
    "-y",
    "-ss",
    visualStart.toFixed(3),
    "-t",
    "25",
    "-i",
    baseVideo,
    "-i",
    scene.audio,
    "-filter_complex",
    `[0:v]${videoFilter}[v];[1:a]${audioFilter}[a]`,
    "-map",
    "[v]",
    "-map",
    "[a]",
    "-c:v",
    "libx264",
    "-pix_fmt",
    "yuv420p",
    "-r",
    "30",
    "-c:a",
    "aac",
    "-b:a",
    "192k",
    "-movflags",
    "+faststart",
    output,
  ];
  const result = spawnSync("ffmpeg", args, { encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(`ffmpeg failed for ${scene.id}:\n${result.stderr}`);
  }
  concatLines.push(`file '${sceneNumber}-${scene.id}-voiced.mp4'`);
  console.log(`${scene.id} ${sceneDuration.toFixed(3)} ${output}`);
}

await writeFile("scene-videos/concat.txt", `${concatLines.join("\n")}\n`);

const concat = spawnSync(
  "ffmpeg",
  [
    "-y",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "scene-videos/concat.txt",
    "-c",
    "copy",
    "pgs-math-explainer-scene-synced-grok-voiceover.mp4",
  ],
  { encoding: "utf8" },
);
if (concat.status !== 0) {
  throw new Error(`ffmpeg concat failed:\n${concat.stderr}`);
}

console.log("final pgs-math-explainer-scene-synced-grok-voiceover.mp4");
