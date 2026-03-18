"""Exercise 2: Flight Data Pipeline

This pipeline runs every 15 minutes. It reads a CSV dump of flight position
reports, enriches them with weather data, and writes results to a database.
Operations reports that the pipeline started timing out after the data volume
grew from 10K to 500K records per run.

Read the code below, then answer the analysis questions at the bottom.
"""

import csv
import json
import sqlite3
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from typing import Any


@dataclass
class FlightRecord:
    flight_id: str
    callsign: str
    latitude: float
    longitude: float
    altitude: int
    speed: int
    heading: int
    timestamp: str


def load_flight_data(csv_content: str) -> list[FlightRecord]:
    """Parse CSV content into FlightRecord objects."""
    records = []
    reader = csv.DictReader(StringIO(csv_content))
    for row in reader:
        record = FlightRecord(
            flight_id=row["flight_id"],
            callsign=row["callsign"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            altitude=int(row["altitude"]),
            speed=int(row["speed"]),
            heading=int(row["heading"]),
            timestamp=row["timestamp"],
        )
        records.append(record)
    return records


def fetch_weather(lat: float, lon: float) -> dict[str, Any]:
    """Fetch weather data for a coordinate. ~150ms per call."""
    url = f"https://weather-api.example.com/v1/current?lat={lat}&lon={lon}"
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read().decode())


def enrich_with_weather(records: list[FlightRecord]) -> list[dict[str, Any]]:
    """Add weather data to each flight record."""
    enriched = []
    for record in records:
        weather = fetch_weather(record.latitude, record.longitude)
        enriched_record = {
            "flight_id": record.flight_id,
            "callsign": record.callsign,
            "lat": record.latitude,
            "lon": record.longitude,
            "alt": record.altitude,
            "speed": record.speed,
            "heading": record.heading,
            "timestamp": record.timestamp,
            "wind_speed": weather.get("wind_speed"),
            "wind_dir": weather.get("wind_direction"),
            "temperature": weather.get("temperature"),
            "visibility": weather.get("visibility"),
        }
        enriched.append(enriched_record)
    return enriched


def normalize_callsign(callsign: str) -> str:
    """Normalize callsign to uppercase with no extra whitespace."""
    result = ""
    for char in callsign:
        if char != " ":
            result = result + char.upper()
    return result


def filter_valid_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter out records with invalid coordinates."""
    valid = []
    for record in records:
        lat = record["lat"]
        lon = record["lon"]
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            valid.append(record)
    return valid


def write_to_database(records: list[dict[str, Any]], db_path: str) -> int:
    """Write enriched records to SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flight_positions (
            flight_id TEXT,
            callsign TEXT,
            lat REAL,
            lon REAL,
            alt INTEGER,
            speed INTEGER,
            heading INTEGER,
            timestamp TEXT,
            wind_speed REAL,
            wind_dir REAL,
            temperature REAL,
            visibility REAL,
            ingested_at TEXT
        )
    """)

    count = 0
    for record in records:
        cursor.execute(
            """INSERT INTO flight_positions
               (flight_id, callsign, lat, lon, alt, speed, heading,
                timestamp, wind_speed, wind_dir, temperature, visibility,
                ingested_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record["flight_id"],
                normalize_callsign(record["callsign"]),
                record["lat"],
                record["lon"],
                record["alt"],
                record["speed"],
                record["heading"],
                record["timestamp"],
                record["wind_speed"],
                record["wind_dir"],
                record["temperature"],
                record["visibility"],
                datetime.now().isoformat(),
            ),
        )
        count += 1

    conn.commit()
    conn.close()
    return count


def run_pipeline(csv_content: str, db_path: str) -> dict[str, Any]:
    """Main pipeline entry point."""
    # Step 1: Parse all records into memory
    records = load_flight_data(csv_content)

    # Step 2: Enrich every record with weather
    enriched = enrich_with_weather(records)

    # Step 3: Filter invalid records
    valid = filter_valid_records(enriched)

    # Step 4: Write to database
    written = write_to_database(valid, db_path)

    return {
        "total_parsed": len(records),
        "total_enriched": len(enriched),
        "total_valid": len(valid),
        "total_written": written,
    }


# ---------------------------------------------------------------------------
# ANALYSIS QUESTIONS
#
# 1. MEMORY: The pipeline loads all 500K records into memory at once
#    (`load_flight_data` returns a full list). What's the memory impact?
#    How would you make this streaming/chunked?
#
# 2. NETWORK: `enrich_with_weather` makes one HTTP call per record.
#    With 500K records at 150ms each, how long does this step take?
#    What strategies would you use to reduce this? (Hint: batching,
#    caching, spatial bucketing)
#
# 3. ERROR HANDLING: What happens if one CSV row has a non-numeric
#    altitude? What happens if the weather API returns a 500? How would
#    you add resilience without losing good records?
#
# 4. DATABASE: Records are inserted one at a time with individual
#    INSERT statements. Why is this slow? What's the faster alternative?
#    (Hint: executemany, batch inserts, COPY)
#
# 5. STRING OPS: `normalize_callsign` builds a string character by
#    character. What's the Pythonic way? What's the performance
#    difference at scale?
#
# 6. ORDERING: Filtering happens AFTER weather enrichment. Why is this
#    wasteful? What should the pipeline order be?
#
# 7. PIPELINE DESIGN: If this needs to scale to 5M records, how would
#    you redesign it? Consider: streaming, parallel processing, message
#    queues, incremental processing.
# ---------------------------------------------------------------------------
