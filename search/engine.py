from django.db.models import Q

class SearchField:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __repr__(self):
        return f"<SearchField {self.name}>"


class SearchTarget:
    def __init__(self, modelName, model,
                 fields, timefield, serializer):
        self.modelName = modelName
        self.model = model
        self.fields = fields
        self.serializer = serializer
        self.timefield = timefield
    
    def get_field_by_name(self, name):
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def __repr__(self):
        return f"<SearchTarget for {self.model}>"


class QueryResult:
    def __init__(self, target, record):
        self.modelName = target.modelName
        self.target = target
        self.record = record
        self.relevantPoints = 0

    def count_relevance(self, keyword):
        for field in self.target.fields:
            match_times = getattr(self.record, field.name).count(keyword)
            self.increase_relevance(field, match_times)
    
    def increase_relevance(self, field, times):
        self.relevantPoints += field.weight * times
    
    def serialize(self):
        return {
            "model": self.modelName,
            "record": self.target.serializer(self.record).data
        }

    def __repr__(self):
        return f"<QueryResult: [{self.modelName}] relevant points: {self.relevantPoints}>"


class QueryResultList:
    def __init__(self):
        self.resultList = []
        self.index = 0

    def append(self, result):
        self.resultList.append(result)

    def remove(self, result):
        return self.resultList.remove(result)

    def serialize(self):
        data = []
        for result in self.resultList:
            data.append(result.serialize())
        return data

    def exclude(self, exclude):
        rest = []
        for result in self.resultList:
            if result.modelName != exclude:
                rest.append(result)
        self.resultList = rest
        

    def sort(self, new2old):

        self.resultList = sorted(
            self.resultList,
            key=lambda result: getattr(result.record, result.target.timefield),
            reverse=new2old
        )
        
        self.resultList = sorted(
            self.resultList,
            key=lambda result: result.relevantPoints,
            reverse=True
        )
    
    def __iter__(self):
        return self
 
    def __next__(self):
        if self.index < len(self.resultList):
            index = self.index
            self.index += 1
            return self.resultList[index]
        else:
            raise StopIteration

    def __repr__(self):
        return f"<QueryResultList: {self.resultList}>"


class APISearchEngine:
    def __init__(self, searchTargets=None):
        self.searchTargets = searchTargets

    def register(self, target):
        self.searchTargets.append(target)

    def db_query(self, keywords, time=True):
        query_results = QueryResultList()
        for target in self.searchTargets:
            records = None
            for keyword in keywords:
                Qr = None
                for field in target.fields:
                    q = Q(**{"%s__icontains" % field.name: keyword})
                    Qr = Qr | q if Qr != None else q

                # get all the records which contains the `keyword` in the `field`
                res = target.model.objects.filter(Qr).distinct()
                records = res | records if records != None else res
            
            for record in records:
                query_results.append(QueryResult(target, record))

        return query_results    

    def search(self, keywords, new2old=True, exclude=None):
        query_results = self.db_query(keywords)
        for result in query_results:
            for keyword in keywords:
                result.count_relevance(keyword)
        
        if exclude is not None:
            query_results.exclude(exclude)

        query_results.sort(new2old)
        return query_results.serialize()
