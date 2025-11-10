# Verium (VRM) Complete Configuration for AtomicDEX

## ✅ Extracted Parameters from Source Code

All parameters have been extracted from the Verium-1.3.5 source code:

### 1. RPC Port
- **Value:** `33987`
- **Source:** `src/chainparamsbase.cpp:38`**

### 2. Address Prefixes
- **pubtype:** `70` (addresses start with 'V')
- **p2shtype:** `132`
- **wiftype:** `198` (128 + 70)
- **Source:** `src/chainparams.cpp:107-109`**

### 3. Sign Message Prefix
- **Value:** `"Verium Signed Message:\n"`
- **Source:** `src/util/validation.cpp:20`**

### 4. Block Time
- **Value:** `300` seconds (5 minutes) - Note: Variable in practice, but 300 is the reference value
- **Source:** `src/chainparams.cpp:63`**

### 5. SegWit Support
- **Enabled:** ✅ Yes
- **bech32_hrp:** `"vrm"`
- **Source:** `src/chainparams.cpp:113`**

### 6. P2P Port
- **Value:** `36988`
- **Source:** `src/chainparams.cpp:86`**

### 7. Decimals
- **Value:** `8` (standard for UTXO coins)

### 8. BIP44 Coin Type
- **Status:** ⚠️ Need to find or determine
- **Action:** Check SLIP-0044 registry or Verium documentation

### 9. Transaction Fee
- **Default:** `0` (can be set if needed)
- **Note:** Uses minRelayTxFee from policy

## 📝 Complete Coins JSON Configuration

```json
{
  "coin": "VRM",
  "name": "verium",
  "fname": "Verium",
  "sign_message_prefix": "Verium Signed Message:\n",
  "rpcport": 33987,
  "pubtype": 70,
  "p2shtype": 132,
  "wiftype": 198,
  "txfee": 0,
  "segwit": true,
  "bech32_hrp": "vrm",
  "mm2": 1,
  "required_confirmations": 3,
  "avg_blocktime": 300,
  "protocol": {
    "type": "UTXO"
  },
  "derivation_path": "m/44'/XXX'",
  "links": {
    "github": "https://github.com/jayhines91/verium",
    "homepage": "https://vericonomy.com"
  }
}
```

**Note:** Replace `XXX` in derivation_path with the actual BIP44 coin type once found.

## 📋 Next Steps

1. ✅ **Technical Parameters** - All extracted from source code
2. ⚠️ **BIP44 Coin Type** - Need to find or determine
3. ❌ **Electrum Servers** - Need at least 2 servers with SSL
4. ❌ **Explorer URLs** - Need working blockchain explorer
5. ❌ **Icon File** - Need 128x128 PNG icon
6. ❌ **Test Swap** - Need to perform successful atomic swap

## 🔍 Still Needed

### BIP44 Coin Type
Check one of these sources:
- https://github.com/satoshilabs/slips/blob/master/slip-0044.md
- Verium documentation
- If not listed, may need to request assignment or use a custom value

### Infrastructure
- **Electrum Servers:** At least 2 operational ElectrumX servers with SSL certificates
- **Explorer:** Working blockchain explorer URL(s)
- **Icon:** 128x128 PNG file named `vrm.png`

### Testing
- Perform a successful atomic swap
- Document all 5 transaction URLs

