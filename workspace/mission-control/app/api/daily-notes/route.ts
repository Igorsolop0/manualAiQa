import { NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";

const MEMORY_DIR = path.join(process.cwd(), "../memory");

export async function GET() {
  try {
    // Read daily notes from memory/YYYY-MM-DD.md files
    const files = await fs.readdir(MEMORY_DIR);
    const dailyFiles = files
      .filter((f) => f.match(/^\d{4}-\d{2}-\d{2}\.md$/))
      .sort()
      .reverse()
      .slice(0, 7); // Last 7 days

    const notes = await Promise.all(
      dailyFiles.map(async (filename) => {
        const filePath = path.join(MEMORY_DIR, filename);
        const content = await fs.readFile(filePath, "utf-8");
        const match = content.match(/^# (.+)$/m);
        const title = match ? match[1] : filename;

        return {
          date: filename.replace(".md", ""),
          title,
          content: content.substring(0, 300) + "...", // Preview
        };
      })
    );

    return NextResponse.json(notes);
  } catch (error) {
    console.error("Error reading daily notes:", error);
    return NextResponse.json({ error: "Failed to read daily notes" }, { status: 500 });
  }
}
