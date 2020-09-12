from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .engine import APISearchEngine, SortRule
from .searchConfig import blogTarget, questionTarget, view_rule


class SearchView(APIView):

    def get(self, request, format=None, **kwargs):
        keywords = request.query_params.get('keywords', None)
        keywords = keywords.split(",")

        # determine which model should be include in the
        # searching scope.
        targets = [blogTarget, questionTarget]
        target_map = {
            "Blog": blogTarget,
            "Question": questionTarget,
        }
        exclude = request.query_params.get('exclude', None)
        rules = []
        if exclude != None:
            targets.remove(target_map[exclude])
            if exclude == "Question":
                like_rule = SortRule(lambda record : record.instance.like_num, True)
                rules.append(like_rule)
        
        # chcek if the resuld should be sorted in chronological order.
        new2old = request.query_params.get('new2old', True)
        new2old = False if new2old == "false" else True
        date_rule = SortRule(lambda record : record.instance.date, new2old)
        
        rules.append(view_rule)
        rules.append(date_rule)
        searchEngine = APISearchEngine(targets, rules)

        # check how many results the engine should return.
        res_num = request.query_params.get('res_num', None)
        if res_num != None:
            res_num = int(res_num)
        query_results = searchEngine.search(keywords, res_num)

        return Response(query_results, status=status.HTTP_200_OK)
