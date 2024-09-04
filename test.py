from collections import defaultdict, Counter
class User:
    def __init__(self, id):
        self.id = id 
        
class UserRecommend:
    def __init__(self, history: list, k: int):
        self.k = k 
        self.UserHistory = defaultdict(set)
        
        for id, place in history.items():
            self.UserHistory[id].add(place)
            
        self.counter = Counter([place for _, place in history.items()])
        self.userRecommendation = defaultdict(list)
        
        for id in set(history.keys()):
            sorted_city = sorted([(count, city) for city, count in self.counter.items()])
            sorted_city = [city for count, city in self.sorted_city if city not in self.UserHistory[id]]
            self.userRecommendation[id].append(sorted_city)
        
    def reccomend(self, id) -> list: 
        # lets get rid of the cities if it alrfeady visited 
        return self.userRecommendation[id]
        
'''
[
    (1, "New York")
    (2, "Paris")
    (3, "Milan")
    (1, "Milan")
    (3, "Paris")
    (2, "Milan")
    (3, "Rome")
]
'''