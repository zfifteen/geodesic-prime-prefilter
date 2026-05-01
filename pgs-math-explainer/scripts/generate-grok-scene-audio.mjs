import { mkdir, readFile, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";

const apiKey = process.env.XAI_API_KEY?.trim();
if (!apiKey) {
  throw new Error("XAI_API_KEY is required");
}

const scenes = JSON.parse(await readFile("scene-narration.json", "utf8"));
await mkdir("audio", { recursive: true });

const timings = [];
for (let i = 0; i < scenes.length; i += 1) {
  const scene = scenes[i];
  const filename = `audio/${String(i + 1).padStart(2, "0")}-${scene.id}.mp3`;
  const response = await fetch("https://api.x.ai/v1/tts", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: scene.text,
      voice_id: "sal",
      language: "en",
    }),
  });
  if (!response.ok) {
    throw new Error(`xAI TTS failed for ${scene.id}: ${response.status} ${await response.text()}`);
  }
  await writeFile(filename, Buffer.from(await response.arrayBuffer()));

  const probe = spawnSync(
    "ffprobe",
    ["-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
    { encoding: "utf8" },
  );
  if (probe.status !== 0) {
    throw new Error(`ffprobe failed for ${filename}: ${probe.stderr}`);
  }
  const audioDuration = Number.parseFloat(probe.stdout.trim());
  if (!Number.isFinite(audioDuration) || audioDuration <= 0) {
    throw new Error(`invalid audio duration for ${filename}`);
  }
  timings.push({ id: scene.id, audio: filename, audioDuration });
  console.log(`${scene.id} ${audioDuration.toFixed(3)} ${filename}`);
}

const pad = 1.2;
let cursor = 0;
const scheduled = timings.map((item) => {
  const start = cursor;
  const duration = item.audioDuration + pad;
  cursor += duration;
  return { ...item, start, duration };
});
scheduled[scheduled.length - 1].duration += 3;
const totalDuration = scheduled.reduce((sum, item) => sum + item.duration, 0);

await writeFile(
  "audio/scene-timings.json",
  `${JSON.stringify({ totalDuration, pad, scenes: scheduled }, null, 2)}\n`,
);

console.log(`total ${totalDuration.toFixed(3)}`);
