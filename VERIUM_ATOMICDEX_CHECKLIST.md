# Verium (VRM) AtomicDEX Listing Checklist

Based on the [Komodo AtomicDEX listing requirements](https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/listing-a-coin-on-atomicdex.html), here's what's needed to add Verium to AtomicDEX.

## ✅ Required Items

### 1. Coins JSON Configuration (`coins` file)
**Location:** Add entry to `/coins` file

**Required Parameters for UTXO coins:**
- [ ] `coin`: "VRM" (ticker symbol)
- [ ] `name`: "verium" (lowercase, data directory name - typically `~/.verium/`)
- [ ] `fname`: "Verium" (full name)
- [ ] `rpcport`: [Need from Verium codebase] (default RPC port)
- [ ] `pubtype`: [Need from Verium codebase] (public key address prefix)
- [ ] `p2shtype`: [Need from Verium codebase] (P2SH address prefix)
- [ ] `wiftype`: [Need from Verium codebase] (WIF private key prefix)
- [ ] `mm2`: 1 (trading compatibility)
- [ ] `required_confirmations`: [Recommend 3-6] (number of confirmations for swaps)
- [ ] `avg_blocktime`: [Need from Verium] (average block time in seconds)
- [ ] `protocol`: `{"type": "UTXO"}`
- [ ] `sign_message_prefix`: [Need from Verium codebase] (e.g., "Verium Signed Message:\n")
- [ ] `derivation_path`: [Need BIP44 path] (e.g., "m/44'/XXX'")
- [ ] `decimals`: 8 (default for UTXO, verify if different)
- [ ] `txfee`: [Optional, default 0] (transaction fee in satoshis)
- [ ] `segwit`: [true/false] (if SegWit is supported)
- [ ] `bech32_hrp`: [Optional] (if SegWit, the bech32 human-readable part)

**Optional Parameters:**
- [ ] `trezor_coin`: [If Trezor compatible] (Trezor coin name)
- [ ] `links`: `{"github": "...", "homepage": "..."}` (project links)
- [ ] `orderbook_ticker`: [If sharing orderbook with another coin]

**Where to find these values:**
- Check Verium source code: https://github.com/jayhines91/verium
- Look in `src/chainparams.cpp` or similar for address prefixes
- Check `src/main.cpp` for sign message prefix
- RPC port typically in `src/chainparamsbase.cpp` or config files

### 2. Icon File (Required)
**Location:** `/icons_original/vrm.png`

**Requirements:**
- [ ] Format: PNG
- [ ] Dimensions: At least 128x128 pixels
- [ ] Filename: `vrm.png` (lowercase ticker, no protocol suffix)
- [ ] File must exist in `icons_original/` folder

### 3. Explorer URL (Required for UTXO coins)
**Location:** `/explorers/VRM` (no file extension, all caps)

**Requirements:**
- [ ] Valid JSON array with at least one explorer URL
- [ ] Multiple explorer URLs recommended
- [ ] Format: `["https://explorer1.com/", "https://explorer2.com/"]`
- [ ] Add explorer path suffixes to `/explorers/explorer_paths.json` if needed

**Example:**
```json
["https://verium-explorer.example.com/"]
```

### 4. Electrum Servers (Required)
**Location:** `/electrums/VRM` (no file extension, all caps)

**Requirements:**
- [ ] At least 2 Electrum servers required
- [ ] Valid JSON array format
- [ ] Each server must have:
  - `url`: "hostname:port" or "ip:port"
  - `protocol`: "SSL" or "TCP" (SSL required for WebDEX)
  - `contact`: Array with contact information (email, discord, etc.)
  - `disable_cert_verification`: [Optional, default false]
  - `ws_url`: [Optional] WebSocket URL for WebDEX

**Example format:**
```json
[
  {
    "url": "electrum1.verium.org:50002",
    "protocol": "SSL",
    "contact": [
      {"email": "admin@verium.org"},
      {"discord": "username#1234"}
    ]
  },
  {
    "url": "electrum2.verium.org:50002",
    "protocol": "SSL",
    "contact": [
      {"email": "admin@verium.org"}
    ]
  }
]
```

**Important Notes:**
- Use Certbot for SSL certificates to avoid validation issues
- Servers are monitored and failing servers result in delisting
- Contact info is critical for emergency situations

### 5. API IDs (Optional but Recommended)
**Location:** `/api_ids/` folder

**Files to update:**
- [ ] `coingecko_ids.json`: Add `"VRM": "verium"` (or correct ID)
- [ ] `coinpaprika_ids.json`: Add `"VRM": "vrm-verium"` (or correct ID)
- [ ] `binance_ids.json`: [If applicable]
- [ ] `forex_ids.json`: [If applicable]
- [ ] `livecoinwatch_ids.json`: [If applicable]

### 6. Derivation Path (Required)
- [ ] BIP44 derivation path (e.g., "m/44'/XXX'")
- [ ] Check Satoshi Labs SLP-044 for coin type number
- [ ] Format: `"derivation_path": "m/44'/XXX'"`

### 7. Trezor Coin Name (Optional)
- [ ] Check https://trezor.io/coins for compatibility
- [ ] If supported, add `"trezor_coin": "Verium"` (or exact name from Trezor)

### 8. Successful Swap Confirmation (Required)
**Location:** `/swaps/VRM.md` (or similar)

**Requirements:**
- [ ] Must perform a successful atomic swap using Komodo DeFi Framework
- [ ] Document the 5 transaction URLs:
  1. Taker fee sent
  2. Maker payment
  3. Taker payment
  4. Taker payment spent
  5. Maker payment spent
- [ ] Create markdown file documenting the successful swap

**Resources:**
- Learn about atomic swaps: [Komodo Documentation](https://developers.komodoplatform.com)
- Activating a coin: [Documentation Link]
- Walkthrough: [Documentation Link]

## 📋 Information Needed from Verium Codebase

**See `VERIUM_RESEARCH.md` for detailed extraction instructions and research findings.**

To complete the configuration, we need to gather the following from https://github.com/jayhines91/verium:

1. **RPC Port**: Default RPC port number (check `src/chainparamsbase.cpp`)
2. **Address Prefixes** (check `src/chainparams.cpp`):
   - Public key address prefix (pubtype) - `base58Prefixes[PUBKEY_ADDRESS]`
   - P2SH address prefix (p2shtype) - `base58Prefixes[SCRIPT_ADDRESS]`
   - WIF private key prefix (wiftype) - `base58Prefixes[SECRET_KEY]`
3. **Sign Message Prefix**: Format like "Verium Signed Message:\n" (check `src/main.cpp`)
4. **Block Time**: Average block time in seconds (check `nPowTargetSpacing` in `src/chainparams.cpp`)
5. **SegWit Support**: Whether SegWit is enabled (check chainparams for segwit activation)
6. **BIP44 Coin Type**: Derivation path coin type number (check SLIP-0044 or coin docs)
7. **Decimals**: Number of decimal places (typically 8 for UTXO - verify)
8. **Explorer URLs**: Working blockchain explorer URLs (check vericonomy.com)
9. **Electrum Servers**: At least 2 operational ElectrumX servers with SSL support

## 🔍 Next Steps

1. **Review Verium Codebase**: Check the GitHub repo for technical specifications
2. **Set Up Electrum Servers**: Ensure at least 2 ElectrumX servers are running
3. **Test RPC Methods**: Verify all required RPC methods are available
4. **Perform Test Swap**: Complete a successful atomic swap
5. **Prepare Files**: Create all required configuration files
6. **Submit PR**: Create pull request to Komodo Platform coins repository

## 📞 Support

If you need help:
- Join `#dev-support` channel on [Komodo Platform Discord](https://discord.gg/komodoplatform)
- Email: [email protected] or [email protected]

## 📚 References

- [Komodo AtomicDEX Listing Guide](https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/listing-a-coin-on-atomicdex.html)
- [Verium GitHub Repository](https://github.com/jayhines91/verium)
- [ElectrumX Documentation](https://electrumx.readthedocs.io/)
- [BIP44 Derivation Paths](https://github.com/satoshilabs/slips/blob/master/slip-0044.md)

