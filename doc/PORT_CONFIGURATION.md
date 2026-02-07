# Port Configuration Changes

## Summary

Updated dashboard and monitor server to use **less common ports** with **randomization** to avoid conflicts with common services.

## Changes Made

### Previous Configuration
- Default port: **8080** (very common, high conflict risk)
- Fixed sequential port selection
- Many users would experience port conflicts

### New Configuration
- Default port: **9080** (less common range)
- Randomized port selection from **9080-9099** range
- Fallback to nearby ports if occupied

## Why These Ports?

The **9080-9099** range was chosen because:
- ✅ Not used by common services (Apache, nginx, Node.js typically use 8000-8999)
- ✅ Still in user port range (1024-49151)
- ✅ Easy to remember (9080 = 8080 + 1000)
- ✅ Unlikely to conflict with other applications
- ✅ 20 ports available for randomization

## Files Updated

### Scripts
1. **scripts/dashboard_server.py**
   - Changed default from `8080` to `9080`
   - Updated environment variable default
   - Updated help text to explain less common port choice

2. **scripts/monitor_server.py**
   - Changed default from `8080` to `9082`
   - Different port to avoid conflict with dashboard

3. **scripts/launch_dashboard.py**
   - Added randomization: starts from random port in 9080-9099 range
   - Increased max_attempts from 10 to 20
   - Improved port wrapping logic

4. **scripts/verify_setup.py**
   - Updated port check from `8080` to `9080`
   - Updated alternative ports list
   - Updated instructions in next steps

### Documentation
5. **doc/DASHBOARD_README.md** - All examples updated to 9080
6. **doc/LAPTOP_FAQ.md** - All examples updated to 9080
7. **LAPTOP_SETUP.md** - All examples updated to 9080
8. **scripts/QUICKSTART.md** - All examples updated to 9080

## Behavior

### Dashboard Server (`dashboard_server.py`)
- Default: Port **9080**
- Override: `--port <number>`
- Environment: `GAIA_DASHBOARD_PORT=9090`

### Monitor Server (`monitor_server.py`)
- Default: Port **9082**
- Override: `--port <number>`
- Environment: `GAIA_MONITOR_PORT=9085`

### Launcher (`launch_dashboard.py`)
- Automatic: Randomly selects from **9080-9099**
- Smart: Tries nearby ports if first choice occupied
- Fallback: Wraps to 9080 range if needed

## Examples

### Before (8080 - Common Conflicts)
```bash
python scripts/dashboard_server.py
# Error: Port 8080 already in use by Apache/nginx/other service
```

### After (9080+ - Rare Conflicts)
```bash
python scripts/dashboard_server.py
# 🚀 GAIA Project Dashboard serving on http://127.0.0.1:9080
# Much less likely to conflict!
```

### Launcher (Automatic Random Port)
```bash
python scripts/launch_dashboard.py
# 🚀 GAIA Dashboard Launcher
# 🔍 Finding available port...
# ✓ Using port 9087  # Randomly selected from 9080-9099
# 🌐 Starting dashboard server...
# 🌍 Opening browser...
```

## Benefits

1. **Fewer Conflicts**: 9080+ range rarely used by other services
2. **Randomization**: Launcher picks random starting point
3. **Better UX**: Users less likely to see "port in use" errors
4. **Memorable**: 9080 is easy to remember (8080 + 1000)
5. **Flexible**: Can still override with `--port` flag

## Testing

All functionality tested:
- ✅ `verify_setup.py` checks port 9080
- ✅ `dashboard_server.py` starts on 9080 by default
- ✅ `launch_dashboard.py` randomly selects from 9080-9099
- ✅ Help text updated with new defaults
- ✅ Documentation updated throughout

## Migration Guide

### For Users
**No action needed!** The new defaults work automatically.

If you had scripts using port 8080, update them:
```bash
# Old
python scripts/dashboard_server.py --port 8080

# New (use new default)
python scripts/dashboard_server.py

# Or keep old port explicitly
python scripts/dashboard_server.py --port 8080
```

### For Automation
If you have environment variables set:
```bash
# Old
export GAIA_DASHBOARD_PORT=8080

# New (optional, uses 9080 by default)
export GAIA_DASHBOARD_PORT=9080
```

## Port Reference

| Service | Old Port | New Port | Notes |
|---------|----------|----------|-------|
| Dashboard | 8080 | 9080 | Less common, randomized |
| Monitor | 8080 | 9082 | Separate from dashboard |
| Launcher | 8080-8089 | 9080-9099 | Random selection |

## Technical Details

### Random Port Selection Algorithm
```python
def find_available_port(start_port=None, max_attempts=20):
    if start_port is None:
        # Start from random port in less common range
        start_port = random.randint(9080, 9099)
    
    # Try ports sequentially from random start
    for offset in range(max_attempts):
        port = start_port + offset
        if is_available(port):
            return port
```

### Why Randomization?
- **Load Distribution**: Multiple users don't all try 9080 first
- **Parallel Development**: Reduces conflicts when running multiple instances
- **Security**: Slightly harder to predict (minor benefit)

## Conclusion

The dashboard now uses **less common ports (9080+)** with **smart randomization** to minimize conflicts while maintaining ease of use. Users can still override with `--port` flag when needed.

---

**Date**: 2026-02-07  
**Status**: ✅ Implemented and Tested  
**Compatibility**: Backwards compatible (old `--port 8080` still works)
