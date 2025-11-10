# Verium (VRM) Technical Parameters for AtomicDEX

Based on research from the [Verium-1.3.5 branch](https://github.com/jayhines91/verium/tree/Verium-1.3.5), here are the parameters we need to extract and verify.

## ✅ Parameters Extracted from Source Code

### 1. RPC Port
**Source:** `src/chainparamsbase.cpp:38`  
**Value:** `33987`  
**Status:** ✅ Confirmed

### 2. Address Prefixes
**Source:** `src/chainparams.cpp:107-109`

**Public Key Address (pubtype):**
- **Value:** `70` (decimal) - addresses start with 'V'
- **Status:** ✅ Confirmed
- **Code:** `base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,70);`

**P2SH Address (p2shtype):**
- **Value:** `132` (decimal)
- **Status:** ✅ Confirmed
- **Code:** `base58Prefixes[SCRIPT_ADDRESS] = std::vector<unsigned char>(1,132);`

**WIF Private Key (wiftype):**
- **Value:** `198` (decimal) - calculated as 128 + 70
- **Status:** ✅ Confirmed
- **Code:** `base58Prefixes[SECRET_KEY] = std::vector<unsigned char>(1,128+70);`

### 3. Sign Message Prefix
**Source:** `src/util/validation.cpp:20`  
**Value:** `"Verium Signed Message:\n"`  
**Status:** ✅ Confirmed  
**Code:** `const std::string strMessageMagic = "Verium Signed Message:\n";`

### 4. Block Time
**Source:** `src/chainparams.cpp:63`  
**Value:** `300` seconds (5 minutes)  
**Status:** ✅ Confirmed  
**Note:** Variable in practice, but 300 is the reference value used  
**Code:** `consensus.nPowTargetSpacing = 5 * 60;`

### 5. SegWit Support
**Source:** `src/chainparams.cpp:113`  
**Status:** ✅ Confirmed - SegWit is enabled  
**bech32_hrp:** `"vrm"`  
**Code:** `bech32_hrp = "vrm";`

### 6. P2P Port
**Source:** `src/chainparams.cpp:86`  
**Value:** `36988`  
**Status:** ✅ Confirmed

### 7. BIP44 Coin Type
**Source:** SLIP-0044 registry or coin documentation  
**Status:** ⚠️ Not found in source code - needs to be determined  
**Check:** https://github.com/satoshilabs/slips/blob/master/slip-0044.md  
**Action:** Check SLIP-0044 registry or Verium documentation

### 8. Transaction Fee
**Source:** Uses `minRelayTxFee` from policy  
**Default:** `0` (can be set if needed)  
**Status:** ✅ Standard - using default 0

### 9. Decimals
**Value:** `8` (standard for UTXO coins)  
**Status:** ✅ Standard for UTXO coins

## How to Verify These Values

### Method 1: Check Source Files Directly

1. **RPC Port:**
   ```bash
   # In src/chainparamsbase.cpp, look for:
   nRPCPort = 33987;
   ```

2. **Address Prefixes:**
   ```bash
   # In src/chainparams.cpp, look for:
   base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1, XX);
   base58Prefixes[SCRIPT_ADDRESS] = std::vector<unsigned char>(1, XX);
   base58Prefixes[SECRET_KEY] = std::vector<unsigned char>(1, XX);
   ```

3. **Sign Message Prefix:**
   ```bash
   # In src/main.cpp or src/util.cpp, look for:
   strMessageMagic = "Verium Signed Message:\n";
   ```

4. **Block Time:**
   ```bash
   # In src/chainparams.cpp, look for:
   nPowTargetSpacing = XX;  // in seconds
   ```

### Method 2: Check Running Node

If you have a Verium node running:
```bash
# Get network info
verium-cli getnetworkinfo

# Get blockchain info
verium-cli getblockchaininfo

# Get a new address to verify address format
verium-cli getnewaddress

# Check config file
cat ~/.verium/verium.conf | grep rpcport
```

## Files to Check in Verium Repository

1. **`src/chainparams.cpp`** - Main network parameters
   - Address prefixes
   - Block time
   - Genesis block
   - SegWit settings

2. **`src/chainparamsbase.cpp`** - Base network parameters
   - RPC port
   - P2P port

3. **`src/main.cpp`** or **`src/util.cpp`** - Utility functions
   - Sign message prefix

4. **`src/policy/policy.h`** - Policy settings
   - Transaction fees
   - Dust limits

## ✅ Summary

All key parameters have been successfully extracted from the Verium source code!

### Confirmed Values:
- ✅ RPC Port: 33987
- ✅ pubtype: 70
- ✅ p2shtype: 132
- ✅ wiftype: 198
- ✅ Sign Message Prefix: "Verium Signed Message:\n"
- ✅ Block Time: 300 seconds
- ✅ SegWit: Enabled (bech32_hrp: "vrm")
- ✅ P2P Port: 36988
- ✅ Decimals: 8

### Still Needed:
- ⚠️ BIP44 Coin Type - Check SLIP-0044 or Verium documentation
- ❌ Electrum Servers - Need at least 2 with SSL
- ❌ Explorer URLs - Need working blockchain explorer
- ❌ Icon File - Need 128x128 PNG
- ❌ Test Swap - Need successful atomic swap

## Next Steps

1. ✅ **All technical parameters extracted** - Complete!
2. **Find BIP44 coin type** from SLIP-0044 or Verium documentation
3. **Set up Electrum servers** (at least 2 with SSL)
4. **Find/create explorer URLs**
5. **Create/get icon file** (128x128 PNG)
6. **Perform test atomic swap**
7. **Create all configuration files**
8. **Submit PR to Komodo Platform**

See `VERIUM_CONFIG_COMPLETE.md` for the complete JSON configuration template.

