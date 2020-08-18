from .engine import SearchField, SearchTarget, APISearchEngine
from blog.models import Blog
from blog.serializers import BlogSerializer

from question.models import Question
from question.serializers import QuestionSerializer

titleField      = SearchField("title", 2)
contentField    = SearchField("content", 1)

fields = [
    titleField,
    contentField
]

blogTarget      = SearchTarget("Blog", Blog, fields, "date", BlogSerializer)
questionTarget  = SearchTarget("Question", Question, fields, "date",QuestionSerializer)

targets = [
    blogTarget,
    questionTarget
]

searchEngine = APISearchEngine(targets)
