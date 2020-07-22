from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TagSerializer
from .models import Tag
from blog.models import Blog
from blog.serializers import BlogSerializer
from question.models import Question
from question.serializers import QuestionSerializer
from django.contrib.contenttypes.models import ContentType


# Create your views here.
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

        

class QueryByTagView(APIView):
    """
    This view should return a list of all the blogs or questions which 
    are tagged by the tag with the tag name indecated in the tag_name
    portion of the URL.
    """
    def get(self, request, format=None, **kwargs):
        """
        Return a list of all blogs or questions or both.
        """
        type_ = self.request.query_params.get('type', None)
        tag_name = self.request.query_params.get('tag_name', None)

        # Tagged item type specified
        if type_ != None and tag_name != None:
            target_type = ContentType.objects.get(
                app_label=type_, model=type_)
            items = target_type.model_class().objects.filter(
                tags__tag_name__contains=tag_name)
            
            if type_ == "blog":
                return Response([BlogSerializer(blog).data for blog in items])
            elif type_ == "question":
                return Response([QuestionSerializer(question).data for question in items])
            else:
                return Response("Unknow tagged item type",
                status=status.HTTP_400_BAD_REQUEST)

        # Tagged item type specified, return all
        elif type_ == None and tag_name != None:
            blogs = Blog.objects.filter(tags__tag_name__contains=tag_name)
            data = {"blogs": [BlogSerializer(blog).data for blog in blogs]}
            questions = Question.objects.filter(tags__tag_name__contains=tag_name)
            data.update({"questions": [QuestionSerializer(question).data for question in questions]})
            return Response(data)

        # invalid parameters
        elif type_ != None and tag_name == None:
            return Response("tag name is not provided",
             status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("no query parameter is provided",
             status=status.HTTP_400_BAD_REQUEST)

        
