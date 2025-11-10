# Verium (VRM) Technical Research for AtomicDEX

## Research Summary

This document contains findings from researching Verium's codebase and specifications needed for AtomicDEX integration.

## Known Information

### Basic Information
- **Ticker:** VRM
- **Full Name:** Verium
- **Protocol Type:** UTXO-based (similar to Bitcoin)
- **Consensus:** Proof-of-Work-Time (PoWT) - CPU-mineable, ASIC/GPU resistant
- **Decimals:** 8 (standard for UTXO coins)
- **GitHub Repository:** https://github.com/jayhines91/verium

### Characteristics
- Variable block times that adjust with mining power
- Designed for scalability and transaction speed
- CPU-mineable cryptocurrency

## Information Still Needed

The following parameters need to be extracted from the Verium source code:

### 1. RPC Port
- **Location:** Typically in `src/chainparamsbase.cpp` or `src/chainparams.cpp`
- **Look for:** `BASE_RPC_PORT` or `RPCPort` definition
- **Common values:** 33987, 33988, or similar

### 2. Address Prefixes
**Location:** `src/chainparams.cpp` or similar file

Look for these definitions:
```cpp
base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,XX);
base58Prefixes[SCRIPT_ADDRESS] = std::vector<unsigned char>(1,XX);
base58Prefixes[SECRET_KEY] = std::vector<unsigned char>(1,XX);
```

- **pubtype:** First byte value for PUBKEY_ADDRESS (public key addresses)
- **p2shtype:** First byte value for SCRIPT_ADDRESS (P2SH addresses)
- **wiftype:** First byte value for SECRET_KEY (WIF private keys)

### 3. Sign Message Prefix
**Location:** `src/main.cpp` or `src/util.cpp`

Look for:
```cpp
std::string strMessageMagic = "Verium Signed Message:\n";
```
or similar string definition.

**Expected format:** `"Verium Signed Message:\n"`

### 4. Block Time
**Location:** `src/chainparams.cpp`

Look for:
```cpp
nPowTargetSpacing = XX; // in seconds
```

Or check the consensus parameters for target block time.

### 5. SegWit Support
**Location:** `src/chainparams.cpp` or consensus parameters

Check if SegWit is enabled:
- Look for `SEGWIT_ACTIVATION_HEIGHT` or similar
- Check if `segwit` is set to `true` in chain parameters
- If SegWit is enabled, also need `bech32_hrp` (bech32 human-readable part)

### 6. BIP44 Coin Type
**Location:** Check SLIP-0044 registry or coin's documentation

- Check https://github.com/satoshilabs/slips/blob/master/slip-0044.md
- Or look in the coin's documentation/GitHub for BIP44 coin type
- Format: `"m/44'/XXX'"` where XXX is the coin type number

### 7. Transaction Fee
**Location:** `src/chainparams.cpp` or `src/main.cpp`

Look for:
```cpp
minRelayTxFee = XX;
```
or default transaction fee settings.

### 8. Explorer URLs
- Check Verium's official website: https://vericonomy.com
- Look for blockchain explorer links
- Common explorers: cryptoscope.io, blockexplorer.com, or custom explorers

### 9. Electrum Servers
- Need at least 2 operational ElectrumX servers
- Must support SSL (port 50002) for WebDEX compatibility
- Contact information required for each server

## How to Extract Information

### Method 1: Clone and Search Repository
```bash
git clone https://github.com/jayhines91/verium.git
cd verium/src
grep -r "PUBKEY_ADDRESS\|SCRIPT_ADDRESS\|SECRET_KEY" .
grep -r "RPCPort\|rpcport\|RPC_PORT" .
grep -r "Signed Message" .
grep -r "nPowTargetSpacing" .
```

### Method 2: Check Online Code Browser
- Visit: https://github.com/jayhines91/verium
- Navigate to `src/chainparams.cpp`
- Look for the base58 prefix definitions
- Check `src/chainparamsbase.cpp` for RPC port

### Method 3: Check Running Node
If you have a Verium node running:
```bash
# Get network info
verium-cli getnetworkinfo

# Get blockchain info (may contain block time)
verium-cli getblockchaininfo

# Get a new address to see address format
verium-cli getnewaddress

# Check RPC port in config
cat ~/.verium/verium.conf | grep rpcport
```

## Example Configuration Template

Once we have the values, here's the template structure:

```json
{
  "coin": "VRM",
  "name": "verium",
  "fname": "Verium",
  "sign_message_prefix": "Verium Signed Message:\n",
  "rpcport": [TO_BE_DETERMINED],
  "pubtype": [TO_BE_DETERMINED],
  "p2shtype": [TO_BE_DETERMINED],
  "wiftype": [TO_BE_DETERMINED],
  "txfee": [TO_BE_DETERMINED],
  "mm2": 1,
  "required_confirmations": 3,
  "avg_blocktime": [TO_BE_DETERMINED],
  "protocol": {
    "type": "UTXO"
  },
  "derivation_path": "m/44'/[TO_BE_DETERMINED]'",
  "links": {
    "github": "https://github.com/jayhines91/verium",
    "homepage": "https://vericonomy.com"
  }
}
```

## Next Steps

1. **Extract Technical Parameters:**
   - Clone or browse the Verium GitHub repository
   - Extract RPC port, address prefixes, sign message prefix, block time
   - Determine BIP44 coin type

2. **Set Up Infrastructure:**
   - Set up at least 2 ElectrumX servers with SSL certificates
   - Ensure servers are publicly accessible
   - Set up monitoring for server uptime

3. **Find Explorer:**
   - Identify working blockchain explorer URLs
   - Test explorer URLs to ensure they're accessible
   - Note explorer URL patterns for `explorer_paths.json`

4. **Test Compatibility:**
   - Verify all required RPC methods are available
   - Test basic wallet operations
   - Perform a test atomic swap

5. **Create Configuration Files:**
   - Complete the coins JSON entry
   - Create Electrum servers file
   - Create explorer file
   - Prepare icon file (if not already available)

6. **Document Successful Swap:**
   - Perform a successful atomic swap
   - Document all 5 transaction URLs
   - Create swap documentation file

## Resources

- **Verium GitHub:** https://github.com/jayhines91/verium
- **Verium Website:** https://vericonomy.com
- **Komodo Documentation:** https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/listing-a-coin-on-atomicdex.html
- **BIP44 Registry:** https://github.com/satoshilabs/slips/blob/master/slip-0044.md
- **ElectrumX Docs:** https://electrumx.readthedocs.io/

