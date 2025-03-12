import heapq
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, name):
        node = self.root
        for char in name:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

class TradeGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.traders = {}

    def add_trader(self, trader, shares):
        self.traders[trader] = shares

    def add_trade_request(self, giver, receiver, share_type, quantity):
        if giver in self.traders and receiver in self.traders:
            self.graph[giver].append((receiver, share_type, quantity))

    def execute_trades(self):
        max_heap, min_heap = [], []
        for trader, shares in self.traders.items():
            for share, qty in shares.items():
                heapq.heappush(max_heap, (-qty, trader, share))
                heapq.heappush(min_heap, (qty, trader, share))
        
        matched_trades = []
        while max_heap and min_heap:
            max_qty, seller, share1 = heapq.heappop(max_heap)
            min_qty, buyer, share2 = heapq.heappop(min_heap)

            trade_qty = min(-max_qty, min_qty)
            matched_trades.append((seller, buyer, share1, share2, trade_qty))

            if -max_qty > trade_qty:
                heapq.heappush(max_heap, (max_qty + trade_qty, seller, share1))
            if min_qty > trade_qty:
                heapq.heappush(min_heap, (min_qty - trade_qty, buyer, share2))

        return matched_trades

# Adding traders and their available shares
trie = Trie()
trade_graph = TradeGraph()

for name in ["Anshu", "Ayush", "Harshit", "Dipanshu"]:
    trie.insert(name)

trade_graph.add_trader("Anshu", {"AAPL": 10, "TSLA": 5})
trade_graph.add_trader("Ayush", {"TSLA": 7, "GOOGL": 3})
trade_graph.add_trader("Harshit", {"GOOGL": 6, "MSFT": 4})
trade_graph.add_trader("Dipanshu", {"MSFT": 8, "AAPL": 2})

# Defining trade requests
trade_graph.add_trade_request("Anshu", "Ayush", "AAPL", 5)
trade_graph.add_trade_request("Ayush", "Harshit", "TSLA", 4)
trade_graph.add_trade_request("Harshit", "Dipanshu", "GOOGL", 3)
trade_graph.add_trade_request("Dipanshu", "Anshu", "MSFT", 2)

# Execute trades and print results
matched_trades = trade_graph.execute_trades()
print("\nMatched Trades:")
for seller, buyer, share1, share2, qty in matched_trades:
    print(f"{seller} exchanges {qty} of {share1} with {buyer} for {share2}")
