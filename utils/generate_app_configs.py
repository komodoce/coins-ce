#!/usr/bin/env python3
import os
import sys
import time
import json
from copy import deepcopy
import requests
from scan_electrums import get_electrums_report
from ensure_chainids import ensure_chainids
from logger import logger


current_time = time.time()
script_path = os.path.abspath(os.path.dirname(__file__))
repo_path = script_path.replace("/utils", "")
os.chdir(script_path)

BINANCE_DELISTED_COINS = [
    "AGIX",
    "ANT",
    "BAL",
    "BIDR",
    "BTT",
    "BUSD",
    "ELF",
    "FIRO",
    "GFT",
    "GRS",
    "IRIS",
    "LOOM",
    "MC",
    "MDX",
    "MIR",
    "NAV",
    "OCEAN",
    "OMG",
    "PAX",
    "QI",
    "REN",
    "REP",
    "SNT",
    "SRM",
    "VGX",
    "VIA",
    "WAVES",
    "YFII",
]

# TODO: Check all coins have an icon.
icons = [
    f
    for f in os.listdir(f"{repo_path}/icons")
    if os.path.isfile(f"{repo_path}/icons/{f}.png")
]
lightwallet_coins = [
    f
    for f in os.listdir(f"{repo_path}/light_wallet_d")
    if os.path.isfile(f"{repo_path}/light_wallet_d/{f}")
]
electrum_coins = [
    f
    for f in os.listdir(f"{repo_path}/electrums")
    if os.path.isfile(f"{repo_path}/electrums/{f}")
]
tendermint_coins = [
    f
    for f in os.listdir(f"{repo_path}/tendermint")
    if os.path.isfile(f"{repo_path}/tendermint/{f}")
]
ethereum_coins = [
    f
    for f in os.listdir(f"{repo_path}/ethereum")
    if os.path.isfile(f"{repo_path}/ethereum/{f}")
]
explorer_coins = [
    f
    for f in os.listdir(f"{repo_path}/explorers")
    if os.path.isfile(f"{repo_path}/explorers/{f}")
]

binance_quote_tickers = [
    "BTC",
    "ETH",
    "BNB",
    "USDT",
    "USDC",
    "TUSD",
    "XRP",
    "TRX",
    "TRY",
    "EUR",
    "BRL",
    "GBP",
    "AUD",
    "RUB",
    "NGN",
    "UAH",
]

with open(f"{repo_path}/explorers/explorer_paths.json", "r") as f:
    explorer_paths = json.load(f)

with open(f"{repo_path}/api_ids/forex_ids.json", "r") as f:
    forex_ids = json.load(f)

with open(f"{repo_path}/api_ids/livecoinwatch_ids.json", "r") as f:
    livecoinwatch_ids = json.load(f)

with open(f"{repo_path}/api_ids/binance_ids.json", "r") as f:
    binance_ids = json.load(f)

with open(f"{repo_path}/api_ids/coingecko_ids.json", "r") as f:
    coingecko_ids = json.load(f)

with open(f"{repo_path}/api_ids/coinpaprika_ids.json", "r") as f:
    coinpaprika_ids = json.load(f)

with open(f"{repo_path}/slp/bchd_urls.json", "r") as f:
    bchd_urls = json.load(f)



class CoinConfig:
    def __init__(self, coin_data: dict, electrum_scan_report: dict):
        self.coin_data = coin_data
        self.electrum_scan_report = electrum_scan_report
        self.data = {}
        self.is_testnet = self.is_testnet_network()
        self.ticker = self.coin_data["coin"].replace("-TEST", "")
        self.base_ticker = self.ticker.split("-")[0]
        self.protocols = {
            "AVAX": "AVX-20",
            "BNB": "BEP-20",
            "ETC": "Ethereum Classic",
            "ETH": "ERC-20",
            "ETH-ARB20": "Arbitrum",
            "EWT": "EWT",
            "FTM": "FTM-20",
            "GLMR": "Moonbeam",
            "HT": "HecoChain",
            "KCS": "KRC-20",
            "MATIC": "Matic",
            "MOVR": "Moonriver",
            "ONE": "HRC-20",
            "QTUM": "QRC-20",
            "RBTC": "RSK Smart Bitcoin",
            "SBCH": "SmartBCH",
            "SLP": "SLPTOKEN",
            "ATOM": "TENDERMINT",
            "OSMO": "TENDERMINT",
            "IRIS": "TENDERMINT",
            "UBQ": "Ubiq",
        }
        self.testnet_protocols = {
            "AVAXT": "AVX-20",
            "BNBT": "BEP-20",
            "FTMT": "FTM-20",
            "tSLP": "SLPTOKEN",
            "tQTUM": "QRC-20",
            "IRISTEST": "TENDERMINT",
            "NUCLEUSTEST": "TENDERMINT",
            "MATICTEST": "Matic",
            "UBQ": "Ubiq",
        }
        self.coin_type = coin_data["protocol"]["type"]
        self.data.update(
            {
                self.ticker: {
                    "coin": self.ticker,
                    "type": "",
                    "name": "",
                    "coinpaprika_id": "",
                    "coingecko_id": "",
                    "livecoinwatch_id": "",
                    "explorer_url": "",
                    "explorer_tx_url": "",
                    "explorer_address_url": "",
                    "supported": [],
                    "active": False,
                    "is_testnet": self.is_testnet,
                    "currently_enabled": False,
                    "wallet_only": False,
                }
            }
        )
        if self.coin_type in ["UTXO", "QRC20", "BCH", "QTUM", "SIA"]:
            try:
                if self.coin_data["sign_message_prefix"]:
                    self.data[self.ticker].update(
                        {"sign_message_prefix": coin_data["sign_message_prefix"]}
                    )
                else:
                    self.data[self.ticker].update({"sign_message_prefix": ""})
            except KeyError as e:
                print(self.ticker + ": Sign message was not found\n")
            if self.ticker in ["BCH", "tBCH"]:
                self.data[self.ticker].update(
                    {"type": "UTXO", "bchd_urls": [], "other_types": ["SLP"]}
                )
        elif self.coin_type in ["ZHTLC"]:
            if self.ticker in lightwallet_coins:
                with open(f"{repo_path}/light_wallet_d/{self.ticker}", "r") as f:
                    lightwallet_servers = json.load(f)
                self.data[self.ticker].update(
                    {"light_wallet_d_servers": lightwallet_servers}
                )
            else:
                self.data[self.ticker].update({"light_wallet_d_servers": []})
        elif self.coin_type in ["SIA"]:
            self.data[self.ticker].update({"nodes": ["SIA"]})

    def get_protocol_info(self):
        if "protocol_data" in self.coin_data["protocol"]:
            protocol_data = self.coin_data["protocol"]["protocol_data"]
            if "consensus_params" in protocol_data:
                # TODO: ZHTLC things
                self.data[self.ticker].update({"type": self.coin_type})
            if "check_point_block" in protocol_data:
                # ZHTLC only
                if "height" in protocol_data["check_point_block"]:
                    self.data[self.ticker].update(
                        {
                            "checkpoint_height": protocol_data["check_point_block"][
                                "height"
                            ]
                        }
                    )
                if "time" in protocol_data["check_point_block"]:
                    self.data[self.ticker].update(
                        {
                            "checkpoint_blocktime": protocol_data["check_point_block"][
                                "time"
                            ]
                        }
                    )

            if "slp_prefix" in protocol_data:
                if self.ticker in ["BCH", "tBCH"]:
                    self.data[self.ticker].update({"allow_slp_unsafe_conf": False})
                    coin_type = "UTXO"
                else:
                    coin_type = "SLP"
                self.data[self.ticker].update(
                    {"type": coin_type, "slp_prefix": protocol_data["slp_prefix"]}
                )
                if "token_id" in protocol_data:
                    self.data[self.ticker].update(
                        {"token_id": protocol_data["token_id"]}
                    )

            elif "platform" in protocol_data:
                # TODO: ERC-like things
                platform = protocol_data["platform"]
                if self.is_testnet:
                    coin_type = self.testnet_protocols[platform]
                else:
                    coin_type = self.protocols[platform]
                self.data[self.ticker].update({"type": coin_type})
                if "contract_address" in protocol_data:
                    self.data[self.ticker].update(
                        {"contract_address": protocol_data["contract_address"]}
                    )
        else:
            self.data[self.ticker].update({"type": self.coin_type})

        self.parent_coin = self.get_parent_coin()
        if self.parent_coin:
            if self.parent_coin != self.ticker:
                self.data[self.ticker].update({"parent_coin": self.parent_coin})

        if self.coin_data["protocol"]["type"] in ["ETH", "QTUM"]:
            if self.ticker in self.protocols:
                coin_type = self.protocols[self.ticker]
            elif self.ticker in self.testnet_protocols:
                coin_type = self.testnet_protocols[self.ticker]
            elif self.parent_coin in self.protocols:
                coin_type = self.protocols[self.parent_coin]
            elif self.parent_coin in self.testnet_protocols:
                coin_type = self.testnet_protocols[self.parent_coin]
            else:
                coin_type = self.coin_data["protocol"]["type"]
            self.data[self.ticker].update({"type": coin_type})

        elif self.coin_data["protocol"]["type"] in ["TENDERMINT", "TENDERMINTTOKEN"]:
            coin_type = self.coin_data["protocol"]["type"]
            self.data[self.ticker].update({"type": coin_type})

    def is_testnet_network(self):
        if "is_testnet" in self.coin_data:
            return self.coin_data["is_testnet"]
        return False

    def get_forex_id(self):
        coin = self.ticker.replace("-segwit", "")
        if coin in forex_ids:
            self.data[self.ticker].update({"forex_id": forex_ids[coin]})

    def get_coinpaprika_id(self):
        coin = self.ticker.replace("-segwit", "")
        if coin in coinpaprika_ids:
            self.data[self.ticker].update({"coinpaprika_id": coinpaprika_ids[coin]})

    def get_coingecko_id(self):
        coin = self.ticker.replace("-segwit", "")
        if coin in coingecko_ids:
            self.data[self.ticker].update({"coingecko_id": coingecko_ids[coin]})

    def get_livecoinwatch_id(self):
        coin = self.ticker.split("-")[0]
        if coin in livecoinwatch_ids:
            self.data[self.ticker].update({"livecoinwatch_id": livecoinwatch_ids[coin]})

    def get_binance_id(self):
        coin = self.ticker.split("-")[0]
        if coin in binance_ids:
            self.data[self.ticker].update({"binance_id": binance_ids[coin]})

    def get_alias_ticker(self):
        if "alias_ticker" in self.coin_data:
            self.data[self.ticker].update(
                {"alias_ticker": self.coin_data["alias_ticker"]}
            )

    def get_asset(self):
        if "asset" in self.coin_data:
            self.data[self.ticker].update({"asset": self.coin_data["asset"]})

    def get_links(self):
        if "links" in self.coin_data:
            self.data[self.ticker].update({"links": self.coin_data["links"]})

    def get_hd_info(self):
        if "derivation_path" in self.coin_data:
            self.data[self.ticker].update(
                {"derivation_path": self.coin_data["derivation_path"]}
            )
        if "trezor_coin" in self.coin_data:
            self.data[self.ticker].update(
                {"trezor_coin": self.coin_data["trezor_coin"]}
            )

    def get_rewards_info(self):
        if self.ticker in ["KMD"]:
            self.data[self.ticker].update(
                {"is_claimable": True, "minimal_claim_amount": "10"}
            )

    def get_address_format(self):
        if "address_format" in self.coin_data:
            self.data[self.ticker].update(
                {"address_format": self.coin_data["address_format"]}
            )

        if self.ticker.find("-segwit") > -1:
            self.data[self.ticker].update({"address_format": {"format": "segwit"}})

    def is_smartchain(self):
        if "sign_message_prefix" in self.coin_data:
            if self.coin_data["sign_message_prefix"] == "Komodo Signed Message:\n":
                self.data[self.ticker]["type"] = "Smart Chain"

    def is_wallet_only(self):
        if "wallet_only" in self.coin_data:
            self.data[self.ticker].update(
                {"wallet_only": self.coin_data["wallet_only"]}
            )

    def get_parent_coin(self):
        """Used for getting filename for related coins/ethereum folder"""
        token_type = self.data[self.ticker]["type"]
        if self.ticker == "RBTC":
            return "RSK"
        if token_type in ["SLP"]:
            if self.data[self.ticker]["is_testnet"]:
                return f"t{token_type}"
            return token_type

        if self.coin_type in ["TENDERMINTTOKEN", "TENDERMINT"]:
            for i in ["IRISTEST", "NUCLEUSTEST"]:
                if self.ticker.find(i) > -1:
                    self.is_testnet = True
                    return i
            for i in ["IBC_IRIS", "IBC_ATOM", "IBC_OSMO"]:
                if self.ticker.find(i) > -1:
                    return i.replace("IBC_", "")

        if self.coin_type not in ["UTXO", "ZHTLC", "BCH", "QTUM"]:
            if self.data[self.ticker]["is_testnet"]:
                key_list = list(self.testnet_protocols.keys())
                value_list = list(self.testnet_protocols.values())
            else:
                key_list = list(self.protocols.keys())
                value_list = list(self.protocols.values())
            if self.ticker in key_list:
                return self.ticker

            if self.ticker == "RBTC":
                token_type = "RSK Smart Bitcoin"
            if token_type in value_list:
                i = value_list.index(token_type)
                return key_list[i]
            logger.warning(f"{token_type} not in value_list")
        return None

    def clean_name(self):
        self.data[self.ticker].update({"name": self.coin_data["fname"]})

    def get_generics(self):
        for i in self.coin_data:
            if i not in self.data[self.ticker]:
                self.data[self.ticker].update({i: self.coin_data[i]})

    def get_electrums(self):
        coin = self.ticker.replace("-segwit", "")
        if self.data[self.ticker]["type"] == "QRC-20":
            if self.is_testnet:
                coin = "tQTUM"
            else:
                coin = "QTUM"

        if coin in electrum_coins:
            with open(f"{repo_path}/electrums/{coin}", "r") as f:
                electrums = json.load(f)
                
        if coin in electrum_scan_report:
            valid_electrums = []
            for x in ["tcp", "ssl", "wss"]:
                # This also filers ws with tcp/ssl server it is grouped with if valid.
                for k, v in electrum_scan_report[coin][x].items():
                    if (
                        current_time - v["last_connection"] < 604800
                    ):  # 1 week grace period
                        for electrum in electrums:
                            electrum["protocol"] = x.upper()
                            e = deepcopy(electrum)
                            if "url" in e:
                                if e["url"] == k:
                                    if "ws_url" in e:
                                        del e["ws_url"]
                                    valid_electrums.append(e)
                            e = deepcopy(electrum)
                            if "ws_url" in e:
                                e["protocol"] = "WSS"
                                if e["ws_url"] == k:
                                    e["url"] = k
                                    del e["ws_url"]
                                    valid_electrums.append(e)
            if len(valid_electrums) > 0:
                valid_electrums = sort_dicts_list(valid_electrums, "url")                 
            self.data[self.ticker].update({"electrum": valid_electrums})
        elif self.coin_type in ["SIA"]:
            self.data[self.ticker].update({"nodes": electrums})

    def get_bchd_urls(self):
        if self.ticker in bchd_urls:
            self.data[self.ticker].update({"bchd_urls": bchd_urls[self.ticker]})

    def get_swap_contracts(self):
        contract_data = None

        if self.ticker in ethereum_coins:
            with open(f"{repo_path}/ethereum/{self.ticker}", "r") as f:
                contract_data = json.load(f)

        elif self.data[self.ticker]["type"] in ["TENDERMINT", "TENDERMINTTOKEN"]:
            with open(f"{repo_path}/tendermint/{self.parent_coin}", "r") as f:
                contract_data = json.load(f)

        elif self.ticker not in electrum_coins:
            if self.parent_coin not in ["SLP", "tSLP", None]:
                with open(f"{repo_path}/ethereum/{self.parent_coin}", "r") as f:
                    contract_data = json.load(f)

        if contract_data:
            if "swap_contract_address" in contract_data:
                self.data[self.ticker].update(
                    {"swap_contract_address": contract_data["swap_contract_address"]}
                )
            if "fallback_swap_contract" in contract_data:
                self.data[self.ticker].update(
                    {"fallback_swap_contract": contract_data["fallback_swap_contract"]}
                )
            if "rpc_nodes" in contract_data:
                if self.data[self.ticker]["type"] in ["TENDERMINT", "TENDERMINTTOKEN"]:
                    key = "rpc_urls"
                else:
                    key = "nodes"
                    
                values = sort_dicts_list(contract_data["rpc_nodes"], "url")       
                self.data[self.ticker].update({key: values})

    def get_explorers(self):
        explorers = None
        coin = self.ticker.replace("-segwit", "")
        if coin in explorer_coins:
            with open(f"{repo_path}/explorers/{coin}", "r") as f:
                explorers = json.load(f)

        elif self.parent_coin in explorer_coins:
            with open(f"{repo_path}/explorers/{self.parent_coin}", "r") as f:
                explorers = json.load(f)

        if explorers:
            for x in explorers:
                for p in explorer_paths:
                    if x.find(p) > -1:
                        self.data[self.ticker].update(explorer_paths[p])
                        break

            self.data[self.ticker].update({"explorer_url": explorers[0]})
            for i in [
                ("explorer_tx_url", "tx/"),
                ("explorer_address_url", "address/"),
                ("explorer_block_url", "block/"),
            ]:
                if i[0] not in self.data[self.ticker]:
                    self.data[self.ticker].update({i[0]: i[1]})


def parse_coins_repo(electrum_scan_report):
    ensure_chainids()
    errors = []
    coins_config = {}
    with open(f"{repo_path}/coins", "r") as f:
        coins_data = json.load(f)

    for item in coins_data:
        config = CoinConfig(item, electrum_scan_report)
        config.get_generics()
        config.get_protocol_info()
        config.clean_name()
        config.get_swap_contracts()
        config.get_electrums()
        config.get_explorers()
        config.is_smartchain()
        config.is_wallet_only()
        config.get_address_format()
        config.get_rewards_info()
        config.get_alias_ticker()
        config.get_asset()
        config.get_forex_id()
        config.get_coinpaprika_id()
        config.get_coingecko_id()
        config.get_livecoinwatch_id()
        config.get_binance_id()
        config.get_bchd_urls()
        config.get_hd_info()
        config.get_links()
        coins_config.update(config.data)

    nodata = []
    for coin in coins_config:
        if not coins_config[coin]["explorer_url"]:
            logger.warning(f"{coin} has no explorers!")
        if coins_config[coin]["type"] not in ["SLP"]:
            for field in ["nodes", "electrum", "light_wallet_d_servers", "rpc_urls"]:
                if field in coins_config[coin]:
                    if not coins_config[coin][field]:
                        nodata.append(coin)
            if (
                "nodes" not in coins_config[coin]
                and "electrum" not in coins_config[coin]
                and "rpc_urls" not in coins_config[coin]
            ):
                nodata.append(coin)

    logger.warning(
        f"The following coins are missing required data or failing connections for nodes/electrums {nodata}"
    )
    logger.warning(f"They will not be included in the output")
    if errors:
        logger.error(f"Errors:")
        for error in errors:
            logger.error(error)
    return coins_config, nodata


def get_desktop_repo_coins_data():
    """for this to work, you need atomicdex-desktop cloned into
    the same folder as you cloned the coins repo."""
    desktop_coins_folder = "../../atomicDEX-Desktop/assets/config/"
    contents = os.listdir(desktop_coins_folder)
    for f in contents:
        if f.endswith("coins.json"):
            coins_fn = f
    with open(f"{repo_path}/atomicDEX-Desktop/assets/config/{coins_fn}", "r") as f:
        return json.load(f)


def filter_ssl(coins_config):
    coins_config_ssl = {}
    for coin in coins_config:
        coins_config_ssl.update({coin: coins_config[coin]})
        if "electrum" in coins_config[coin]:
            electrums = []
            for i in coins_config[coin]["electrum"]:
                if "protocol" in i:
                    if i["protocol"] == "SSL":
                        electrums.append(i)
            if len(coins_config_ssl[coin]["electrum"]) == 0:
                del coins_config_ssl[coin]
            else:
                electrums = filter_duplicate_domains(electrums)
                coins_config_ssl[coin]["electrum"] = electrums

        if "nodes" in coins_config[coin]:
            coins_config_ssl[coin]["nodes"] = [
                i for i in coins_config[coin]["nodes"] if i["url"].startswith("https")
            ]

        if "light_wallet_d_servers" in coins_config[coin]:
            coins_config_ssl[coin]["light_wallet_d_servers"] = [
                i
                for i in coins_config[coin]["light_wallet_d_servers"]
                if i.startswith("https")
            ]

    with open(f"{script_path}/coins_config_ssl.json", "w+") as f:
        json.dump(coins_config_ssl, f, indent=4)
    return coins_config_ssl


def item_exists(i, electrums):
    for e in electrums:
        if "url" in e and "url" in i:
            if i["url"] == e["url"]:
                return True
        if "ws_url" in e and "ws_url" in i:
            if i["ws_url"] == e["ws_url"]:
                return True
    return False


def filter_duplicate_domains(electrums):
    domains = {}
    for i in electrums:
        domain = i["url"].split(":")[0]
        if domain not in domains:
            domains.update({domain: {i['protocol']: i['url']}})
        else:
            domains[domain].update({i['protocol']: i['url']})
    for i in domains:
        if "SSL" in domains[i] and "TCP" in domains[i]:
            for e in electrums:
                if e["url"].startswith(i) and e["protocol"] == "TCP":
                    electrums.remove(e)
    return electrums
    

    

def filter_tcp(coins_config, coins_config_ssl):
    coins_config_tcp = {}
    for coin in coins_config:
        coins_config_tcp.update({coin: coins_config[coin]})
        # Omit komodo_proxy: true nodes - these are web only.
        if "nodes" in coins_config[coin]:
            coins_config_tcp[coin]["nodes"] = [
                i for i in coins_config[coin]["nodes"] if "komodo_proxy" not in i
            ]
        if "electrum" in coins_config[coin]:
            electrums = []
            # Prefer SSL
            if coin in coins_config_ssl:
                if len(coins_config_ssl[coin]["electrum"]) > 0:
                    electrums = coins_config_ssl[coin]["electrum"]
            for i in coins_config[coin]["electrum"]:
                if "komodo_proxy" in i:
                    if i["komodo_proxy"] == True:
                        continue
                if item_exists(i, electrums) == False:
                    if "protocol" in i:
                        # SSL is ok for legacy desktop so we allow them, else some coins with only SSL will be omited.
                        if i["protocol"] != "WSS":
                            electrums.append(i)
                    else:
                        electrums.append(i)

            if len(coins_config_tcp[coin]["electrum"]) == 0:
                del coins_config_tcp[coin]
            else:
                electrums = filter_duplicate_domains(electrums)
                coins_config_tcp[coin]["electrum"] = electrums

    with open(f"{script_path}/coins_config_tcp.json", "w+") as f:
        json.dump(coins_config_tcp, f, indent=4)
    return coins_config_tcp


def filter_wss(coins_config):
    coins_config_wss = {}
    for coin in coins_config:
        if "electrum" in coins_config[coin]:
            electrums = []
            for i in coins_config[coin]["electrum"]:
                if "protocol" in i:
                    if i["protocol"] == "WSS":
                        electrums.append(i)
                else:
                    logger.warning(f"No protocol data in {i}")
            if len(electrums) > 0:
                coins_config_wss.update({coin: coins_config[coin]})
                coins_config_wss[coin]["electrum"] = electrums
        elif "nodes" in coins_config[coin]:
            nodes = []
            for i in coins_config[coin]["nodes"]:
                if "ws_url" in i:
                    nodes.append(i)
            if len(nodes) > 0:
                coins_config_wss.update({coin: coins_config[coin]})
                coins_config_wss[coin]["nodes"] = nodes
        else:
            logger.warning(f"{coin} not checked for WSS filter yet, including anyway.")
            coins_config_wss.update({coin: coins_config[coin]})

    with open(f"{script_path}/coins_config_wss.json", "w+") as f:
        json.dump(coins_config_wss, f, indent=4)
    return coins_config_wss


def generate_binance_api_ids(coins_config):
    kdf_coins = coins_config.keys()
    r = requests.get("https://defi-stats.komodo.earth/api/v3/binance/ticker_price")
    binance_tickers = r.json()
    pairs = []
    for ticker in binance_tickers:
        pair = ticker["symbol"]
        for quote in binance_quote_tickers:
            if ticker["symbol"].startswith(quote):
                pair = (quote, ticker["symbol"].replace(quote, ""))
                break
            elif ticker["symbol"].endswith(quote):
                pair = (ticker["symbol"].replace(quote, ""), quote)
                break
        pairs.append(pair)
    unknown_ids = [i for i in pairs if isinstance(i, str)]
    known_ids = [i for i in pairs if isinstance(i, tuple)]

    if unknown_ids:
        logger.warning(f"Unknown ids: {unknown_ids}")

    api_ids = {}
    known_id_coins = list(set([i[0] for i in known_ids] + [i[1] for i in known_ids]))
    for coin in kdf_coins:
        ticker = coin.split("-")[0]
        if ticker in known_id_coins:
            if ticker not in BINANCE_DELISTED_COINS:
                api_ids.update({coin: ticker})

    with open(f"{repo_path}/api_ids/binance_ids.json", "w") as f:
        json.dump(api_ids, f, indent=4)

    # To use for candlestick data, reference api_ids/binance_ids.json
    # to get the base and quote id for a pair then concatentate them with no separator
    # Example candlestick url: https://api.binance.com/api/v3/klines?symbol=BNBBTC&interval=1d&limit=1000
    # Valid interval values are listed at https://binance-docs.github.io/apidocs/spot/en/#public-api-definitions


def sort_dict(d):
    return {k: d[k] for k in sorted(d)}

def sort_dicts_list(data, sort_key):
    return sorted(data, key=lambda x: x[sort_key])



if __name__ == "__main__":
    skip_scan = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "no-scan":
            skip_scan = True
    if skip_scan is False:
        electrum_scan_report = get_electrums_report()
    else:
        # Use existing scan data
        with open(f"{script_path}/electrum_scan_report.json", "r") as f:
            electrum_scan_report = json.load(f)

    coins_config, nodata = parse_coins_repo(electrum_scan_report)
    # Includes failing servers
    with open(f"{script_path}/coins_config_unfiltered.json", "w+") as f:
        json.dump(coins_config, f, indent=4)
    generate_binance_api_ids(coins_config)

    # Remove failing servers
    for coin in nodata:
        del coins_config[coin]
    with open(f"{script_path}/coins_config.json", "w+") as f:
        json.dump(coins_config, f, indent=4)
        
    coins_config_ssl = filter_ssl(deepcopy(coins_config))
    coins_config_wss = filter_wss(deepcopy(coins_config))
    coins_config_tcp = filter_tcp(deepcopy(coins_config), coins_config_ssl)
    for coin in coins_config:
        r = f"{coin}: [SSL {coin in coins_config_ssl}] [TCP {coin in coins_config_tcp}] [WSS {coin in coins_config_wss}]"
        if (
            coin in coins_config_tcp
            and coin in coins_config_ssl
            and coin in coins_config_wss
        ):
            logger.info(r)
        else:
            logger.calc(r)
    for coin in nodata:
        logger.warning(f"{coin}: [SSL False] [TCP False] [WSS False]")
    
    logger.info(f"\nTotal coins: {len(coins_config)}")
    logger.info(f"Total coins with SSL: {len(coins_config_ssl)}")
    logger.info(f"Total coins with TCP: {len(coins_config_tcp)}")
    logger.info(f"Total coins with WSS: {len(coins_config_wss)}")
