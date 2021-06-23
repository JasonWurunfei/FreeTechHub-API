from .engine import SearchField, SearchTarget, APISearchEngine, SortRule
from blog.models import Blog
from blog.serializers import BlogSerializer
from question.models import Question
from question.serializers import QuestionSerializer
from user.models import User
from user.serializers import UserSerializer

class TagSearchField(SearchField):
    def __init__(self):
        super().__init__("tags", 3)
    
    def cal_relevant_point(self, record, keywords):
        tags = record.instance.tags.all()
        for keyword in keywords:
            for tag in tags:
                if tag.tag_name == keyword:
                    self.add_relevant_point(record)


class TitleSearchField(SearchField):
    def __init__(self):
        super().__init__("title", 2)


class ContentSearchField(SearchField):
    def __init__(self):
        super().__init__("content", 1)


class UsernameSearchField(SearchField):
    def __init__(self):
        super().__init__("username", 100)

tagSearchField      = TagSearchField()
titleField          = TitleSearchField()
contentField        = ContentSearchField()
usernameSearchField = UsernameSearchField()

fields = [
    titleField,
    contentField,
    tagSearchField
]

blogTarget     = SearchTarget(Blog,     fields, BlogSerializer)
questionTarget = SearchTarget(Question, fields, QuestionSerializer)
userTarget     = SearchTarget(User, [usernameSearchField], UserSerializer)

def view_key(record):
    return 0 if isinstance(record.instance, User) else record.instance.view_num

view_rule = SortRule(view_key, True)

targets = [
    blogTarget,
    questionTarget,
    userTarget
]
