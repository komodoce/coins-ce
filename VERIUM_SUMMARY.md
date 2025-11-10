# Verium (VRM) AtomicDEX Integration - Summary

## What I've Created

I've researched the requirements for adding Verium to AtomicDEX and created the following documents:

### 1. **VERIUM_ATOMICDEX_CHECKLIST.md**
A comprehensive checklist covering all 8 required items for AtomicDEX listing:
- ✅ Coins JSON Configuration
- ✅ Icon File
- ✅ Explorer URL
- ✅ Electrum Servers
- ✅ API IDs (optional)
- ✅ Derivation Path
- ✅ Trezor Coin Name (optional)
- ✅ Successful Swap Confirmation

### 2. **VERIUM_RESEARCH.md**
A detailed research document with:
- Known information about Verium
- Specific locations in source code to find each parameter
- Extraction methods (grep commands, file locations)
- Template configuration structure
- Step-by-step next actions

## What We Know About Verium

✅ **Basic Info:**
- Ticker: VRM
- Full Name: Verium
- Protocol: UTXO-based
- Consensus: Proof-of-Work-Time (PoWT)
- Decimals: 8 (standard for UTXO)
- GitHub: https://github.com/jayhines91/verium
- Website: https://vericonomy.com

## What Still Needs to Be Done

### Immediate Next Steps:

1. **Extract Technical Parameters from Source Code:**
   - Clone/browse: https://github.com/jayhines91/verium
   - Find in `src/chainparams.cpp`:
     - `base58Prefixes[PUBKEY_ADDRESS]` → pubtype
     - `base58Prefixes[SCRIPT_ADDRESS]` → p2shtype
     - `base58Prefixes[SECRET_KEY]` → wiftype
   - Find in `src/chainparamsbase.cpp`:
     - RPC port number
   - Find in `src/main.cpp`:
     - Sign message prefix string
   - Find in `src/chainparams.cpp`:
     - `nPowTargetSpacing` → block time

2. **Find BIP44 Coin Type:**
   - Check: https://github.com/satoshilabs/slips/blob/master/slip-0044.md
   - Or check Verium documentation

3. **Set Up Infrastructure:**
   - Deploy 2+ ElectrumX servers with SSL certificates
   - Ensure public accessibility
   - Set up monitoring

4. **Find Explorer:**
   - Check vericonomy.com for explorer links
   - Test explorer URLs

5. **Get Icon:**
   - Create or obtain 128x128 PNG icon
   - Save as `icons_original/vrm.png`

6. **Test & Swap:**
   - Verify RPC methods work
   - Perform successful atomic swap
   - Document swap transactions

## Files Created

1. ✅ `VERIUM_ATOMICDEX_CHECKLIST.md` - Complete requirements checklist
2. ✅ `VERIUM_RESEARCH.md` - Technical research and extraction guide
3. ✅ `VERIUM_SUMMARY.md` - This summary document

## Quick Reference

**Documentation:**
- Komodo Guide: https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-tutorials/listing-a-coin-on-atomicdex.html
- Verium Repo: https://github.com/jayhines91/verium
- Support: #dev-support on Komodo Discord

**Key Files to Create:**
- `/coins` - Add VRM entry
- `/icons_original/vrm.png` - Icon file
- `/explorers/VRM` - Explorer URLs
- `/electrums/VRM` - Electrum servers
- `/swaps/VRM-XXX.md` - Swap documentation

## Status

🟡 **In Progress** - Research complete, awaiting technical parameter extraction from source code.

Once you have the technical parameters from the Verium codebase, we can:
1. Complete the coins JSON configuration
2. Create all required files
3. Prepare the pull request

