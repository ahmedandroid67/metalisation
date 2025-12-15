# Analytics Tracking System 📊

## Overview

Your app now includes a complete analytics tracking system to monitor:
- **Unique visitors** (daily/total)
- **Total visits**
- **Image generations** (success/failure)
- **Processing time** for each generation
- **Daily statistics**

## How It Works

### SQLite Database
All analytics are stored in `analytics.db` (excluded from Git):
- `visits` table - Page visits with hashed IPs
- `generations` table - Image generation attempts
- `daily_stats` table - Aggregated daily metrics

### Privacy-Friendly
- IPs are SHA256 hashed (not stored in plaintext)
- No personal data collected
- Self-hosted (no external services)

## Viewing Analytics

### Access the Analytics Endpoint

```
GET /api/analytics?key=metalise2025
```

**Example:**
```bash
curl "http://localhost:5000/api/analytics?key=metalise2025"
```

Or visit in browser:
```
http://localhost:5000/api/analytics?key=metalise2025
```

### Response Format

```json
{
  "total": {
    "visits": 150,
    "unique_visitors": 75,
    "successful_generations": 45,
    "failed_generations": 12,
    "total_generations": 57
  },
  "today": {
    "unique_visitors": 8,
    "total_visits": 15,
    "successful_generations": 5,
    "failed_generations": 2,
    "total_generations": 7
  },
  "last_7_days": [
    {
      "date": "2025-12-15",
      "unique_visitors": 8,
      "total_visits": 15,
      "successful_generations": 5,
      "failed_generations": 2
    },
    // ... more days
  ]
}
```

## Security

###  Change the Analytics Key

Update in `.env`:
```env
ANALYTICS_KEY=your_secure_random_key_here
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## What Gets Tracked

### Automatic Tracking

1. **Visit Tracking** - Every time someone visits the app:
   - Hashed IP address
   - User agent
   - Timestamp
   - Date

2. **Generation Tracking** - Every image generation attempt:
   - Success/failure status
   - Whether text was included
   - Error message (if failed)
   - Processing time
   - Timestamp

### No Tracking Of
- Names entered
- Uploaded images
- Generated images
- Personal information

## Deployment

When deploying to Coolify, add to environment variables:
```
ANALYTICS_KEY=your_secure_key_here
```

## Database Management

### View Raw Data

```bash
sqlite3 analytics.db

# View visits
SELECT * FROM visits ORDER BY timestamp DESC LIMIT 10;

# View generations
SELECT * FROM generations ORDER BY timestamp DESC LIMIT 10;

# View daily stats
SELECT * FROM daily_stats ORDER BY date DESC;
```

### Export Data

```bash
# Export to CSV
sqlite3 analytics.db <<!
.headers on
.mode csv
.output analytics_export.csv
SELECT * FROM daily_stats ORDER BY date DESC;
.quit
!
```

### Backup Database

```bash
# Simple copy
cp analytics.db analytics_backup_$(date +%Y%m%d).db

# Or use SQLite backup
sqlite3 analytics.db ".backup 'analytics_backup.db'"
```

## Dashboard (Future Enhancement)

You can create a simple admin dashboard HTML page that:
1. Fetches `/api/analytics?key=YOUR_KEY`
2. Displays charts using Chart.js or similar
3. Shows real-time statistics

Example integration:
```javascript
fetch('/api/analytics?key=YOUR_KEY')
  .then(r => r.json())
  .then(stats => {
    console.log(`Total visitors: ${stats.total.unique_visitors}`);
    console.log(`Today's generations: ${stats.today.total_generations}`);
  });
```

## Files

- `analytics.py` - Tracking module
- `analytics.db` - SQLite database (auto-created)
- `app.py` - Integrated tracking calls

## Notes

- Database is created automatically on first run
- Tracking is non-blocking (won't slow down your app)
- Failed tracking attempts are logged but don't affect functionality
- All analytics are local (no external services)

---

**Access your stats**: `https://your-domain.com/api/analytics?key=metalise2025`
