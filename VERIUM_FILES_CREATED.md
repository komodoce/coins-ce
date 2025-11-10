# Verium (VRM) Files Created for AtomicDEX

## ✅ Files Successfully Created

### 1. Icon File
- **File:** `icons_original/vrm.png`
- **Status:** ✅ Created (copied from verium-01.png)
- **Note:** Image is currently 781x800 pixels. Needs to be resized to 128x128.
- **Action:** Run the resize script: `./utils/icons_resize.sh` or manually resize to 128x128

### 2. Electrum Servers
- **File:** `electrums/VRM`
- **Status:** ✅ Created
- **Servers:**
  - electrum01-vrm.vericonomy.com:50002 (SSL)
  - electrum02-vrm.vericonomy.com:50002 (SSL)
- **WebSocket URLs:** Included for both servers (port 50004)

### 3. Explorer URLs
- **File:** `explorers/VRM`
- **Status:** ✅ Created
- **Explorers:**
  - https://verium-explorer.vericonomy.com/
  - https://explorer-vrm.vericonomy.com/

### 4. Explorer Paths
- **File:** `explorers/explorer_paths.json`
- **Status:** ✅ Updated
- **Note:** Added common URL patterns (tx/, address/, block/). These may need verification based on actual explorer implementation.

## ⚠️ Notes

1. **Icon Resize:** The icon file needs to be resized from 781x800 to 128x128. You can:
   - Run: `./utils/icons_resize.sh` (requires ImageMagick)
   - Or manually resize using any image editor

2. **Explorer URL Patterns:** The explorer paths I added use common patterns:
   - Transaction: `tx/`
   - Address: `address/`
   - Block: `block/`
   
   **Please verify these match your actual explorer URLs** and update `explorers/explorer_paths.json` if different.

3. **Contact Information:** I used `support@vericonomy.com` for the Electrum servers. Please update if you have different contact information.

4. **BIP44 Coin Type:** Still needed to complete the coins configuration. Check SLIP-0044 or Verium documentation.

## 📋 Next Steps

1. ✅ Icon file created (needs resize)
2. ✅ Electrum servers file created
3. ✅ Explorer file created
4. ✅ Explorer paths added (needs verification)
5. ⚠️ Resize icon to 128x128
6. ⚠️ Verify explorer URL patterns
7. ⚠️ Find BIP44 coin type
8. ⚠️ Add coins JSON configuration to `coins` file
9. ⚠️ Perform test atomic swap
10. ⚠️ Create swap documentation file

## 🔍 Verification Needed

- [ ] Verify explorer URL patterns match actual explorer implementation
- [ ] Update contact information in Electrum servers file if needed
- [ ] Resize icon file to 128x128
- [ ] Find BIP44 coin type for Verium

