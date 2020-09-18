from django.db.models import Q

class SearchField:
    """
    Model fields that will be searched against with.
    Fields can have different weight to affect search rank
    """
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def add_relevant_point(self, record, times=1):
        """
        This function will add the relevant points to the record.
        """
        record.relevant_point += self.weight * times
    
    def cal_relevant_point(self, record, keywords):
        """
        The searching part is delegated to this method,
        different field may implement this method in different ways.
        """
        for keyword in keywords:
            match_times = getattr(record.instance, self.name).count(keyword)
            self.add_relevant_point(record, match_times)
    
    def __repr__(self):
        return f"<SearchField {self.name}>"


class Record:
    def __init__(self, instance, serializer):
        self.instance = instance
        self.serializer = serializer
        self.relevant_point = 0
    
    @property
    def serialize(self):
        return self.serializer(self.instance).data

    @property
    def model_class(self):
        return self.instance._meta.object_name
    
    def __repr__(self):
        return f"<Record of model {self.instance._meta.object_name}>"

class SearchTarget:
    """
    The search target is the model which will be searched
    and whcih fields will be searched.
    """
    def __init__(self, model_class, search_fields, serializer):
        self.model_class = model_class
        self.search_fields = search_fields
        self.serializer = serializer

    def get_records(self):
        """
        This method will wrap up all the django model
        instances into records.
        """
        instances = self.model_class.objects.all()
        records = []
        for instance in instances:
            records.append(Record(instance, self.serializer))
        return records

    def cal_relevant_point(self, keywords):
        records = self.get_records()
        for record in records:
            for field in self.search_fields:
                field.cal_relevant_point(record, keywords)
        return records

    def __repr__(self):
        return f"<SearchTarget for {self.model}>"


class SortRule:
    def __init__(self, key, reverse=False):
        self.key = key
        self.reverse = reverse
    
    def sort(self, records):
        return sorted(records, key=self.key, reverse=self.reverse)

relevant_key = lambda record : record.relevant_point
relevant_rule = SortRule(relevant_key, True)

class APISearchEngine:
    def __init__(self, targets, rules=[]):
        self.targets = targets
        self.rules = rules + [relevant_rule]

    def serialize(self, records):
        data = []
        for record in records:
            data.append({
                "instance" : record.serialize,
                "point"    : record.relevant_point,
                "class"    : record.model_class
            })
        return data

    def remove_irrelevant(self, records):
        return [record for record in records \
                if record.relevant_point != 0]
    
    def sort(self, records):
        for rule in self.rules:
            records = rule.sort(records)
        return records

    def search(self, keywords, res_num=None):
        records = []
        for target in self.targets:
            records += target.cal_relevant_point(keywords)
        
        records = self.remove_irrelevant(records)
        records = self.sort(records)

        if res_num != None:
            records = records[:res_num]

        # serialize the records
        result = self.serialize(records)
        return result
    