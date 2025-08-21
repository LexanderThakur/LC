from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import requests
from urllib.parse import urlparse

LEETCODE_GRAPHQL_URL="https://leetcode.com/graphql"



def page(request):
    return render(request,'index.html')



def get_slug(url):
    parsed=urlparse(url)

    path_parsed=parsed.path.strip("/").split("/")
    if len(path_parsed) >=2 and path_parsed[0]=="problems":
        return path_parsed[1]

    return None

@csrf_exempt
def submit_link(request):
    user=request.user

    if not user:
        return JsonResponse({"error":"view did not get user"},status=404)

    d = json.loads(request.body)
    link = d.get("link")
    slug = get_slug(link)

    query = """
    query getQuestion($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        titleSlug
        difficulty
        likes
        dislikes
        isPaidOnly
        content
        topicTags {
          name
          slug
        }
      }
    }
    """

    variables={"titleSlug":slug}
    response=requests.post(
        LEETCODE_GRAPHQL_URL,
        json={"query":query,"variables":variables}
    )


    data=response.json()
    return JsonResponse({"message":data},status=200)



    