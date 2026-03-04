import { NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";

const HEARTBEAT_PATH = path.join(process.cwd(), "../HEARTBEAT.md");

export async function GET() {
  try {
    const content = await fs.readFile(HEARTBEAT_PATH, "utf-8");
    return NextResponse.text(content);
  } catch (error) {
    console.error("Error reading HEARTBEAT.md:", error);
    return NextResponse.text("Failed to read HEARTBEAT.md", { status: 500 });
  }
}
