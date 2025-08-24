from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Links
# Create your views here.
import requests
from urllib.parse import urlparse
from sklearn.cluster import KMeans

import pandas as pd

LEETCODE_GRAPHQL_URL="https://leetcode.com/graphql"



def page(request):
    return render(request,'temp.html')



def get_slug(url):
    parsed=urlparse(url)

    path_parsed=parsed.path.strip("/").split("/")
    if len(path_parsed) >=2 and path_parsed[0]=="problems":
        return path_parsed[1]

    return None


def save_data(data,user,url):
  topics=[]
  temp=data.get("data").get("question")
  for i in temp.get("topicTags"):
    topics.append(i.get("name"))
  
  Links.objects.create(
    title=temp.get("title"),
    title_slug=temp.get("titleSlug"),
    difficulty=temp.get("difficulty"),
    tags=topics,
    url=url,
    number=temp.get("questionId"),
    user=user
  )

  


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
    try:
      save_data(data,user,link)

    except Exception:
      return JsonResponse({"message":data.get("data").get("question"),"stat":"Already in Backlog"},status=200)

    
    return JsonResponse({"message":data.get("data").get("question"),"stat":"Added Successfully"},status=200)


# first get all links and store them as a df
# train a kmeans cluster on it
# return 3 links from the most densest cluster
    

def make_df(user):
  leetcode_tags = [
    "Array", "String", "Hash Table", "Dynamic Programming", "Math", "Sorting", "Greedy",
    "Depth-First Search", "Binary Search", "Database", "Matrix", "Tree", "Breadth-First Search",
    "Bit Manipulation", "Two Pointers", "Prefix Sum", "Heap (Priority Queue)", "Simulation",
    "Binary Tree", "Graph", "Stack", "Counting", "Sliding Window", "Design", "Enumeration",
    "Backtracking", "Union Find", "Linked List", "Number Theory", "Ordered Set", "Monotonic Stack",
    "Segment Tree", "Trie", "Combinatorics", "Bitmask", "Divide and Conquer", "Queue", "Recursion",
    "Geometry", "Binary Indexed Tree", "Memoization", "Hash Function", "Binary Search Tree",
    "Shortest Path", "String Matching", "Topological Sort", "Rolling Hash", "Game Theory",
    "Interactive", "Data Stream", "Monotonic Queue", "Brainteaser", "Doubly-Linked List",
    "Randomized", "Merge Sort", "Counting Sort", "Iterator", "Concurrency",
    "Probability and Statistics", "Quickselect", "Suffix Array", "Line Sweep",
    "Minimum Spanning Tree", "Bucket Sort", "Shell", "Reservoir Sampling",
    "Strongly Connected Component", "Eulerian Circuit", "Radix Sort", "Rejection Sampling",
    "Biconnected Component"
  ]

  df= pd.DataFrame()
  for tag in leetcode_tags:
    df[tag]=0

  user_links=Links.objects.filter(user_email=user).values("tags","title","number","url","difficulty")

  rows=[]

  for link in user_links:
    row={}
    for tag in leetcode_tags:
      row[tag]=0

    row["title"] = link["title"]
    row["number"] = link["number"]
    row["url"] = link["url"]
    row["difficulty"] = link["difficulty"]

    for t in link[tags]:
      if t in row:
        row[t]=1

    rows.append(row)

  df=pd.DataFrame(rows)
  return df


def get_link(request):
  user=request.user

    if not user:
        return JsonResponse({"error":"view did not get user"},status=404)

    
    df = make_df(user) 

    X = df.drop(columns=["title", "number", "url", "difficulty"])

    kmeans=KMeans(n_clusters=5,random_state=42)
    kmeans.fit(X)

    

