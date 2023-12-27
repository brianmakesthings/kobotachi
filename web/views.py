# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import requests


# Create your views here.
def index(request):
    # make an http request
    query = """
    query Library {
        category(id: 0) {
            mangas {
                nodes {
                    id
                    title
                }
            }
        }
    }
    """

    query_results = requests.post(
        "http://tachidesk:4567/api/graphql",
        json={"query": query},
    ).json()["data"]

    context = {
        "manga_list": query_results["category"]["mangas"]["nodes"],
    }

    return render(request, "web/index.html", context)


def chapter_list(request, manga_id):
    query = """
    query chapterIndex($mangaId: Int!) {
        manga(id: $mangaId) {
            title
            chapters {
            nodes {
                name
                sourceOrder
                isDownloaded
            }
            }
        }
    }
    """

    chapter_request_string = "http://tachidesk:4567/api/graphql"
    query_results = requests.post(
        chapter_request_string,
        json={"query": query, "variables": {"mangaId": manga_id}},
    ).json()["data"]
    print(query_results["manga"]["chapters"]["nodes"])
    # return HttpResponse(chapter_raw.json())
    return render(
        request,
        "web/chapters.html",
        {
            "chapters": query_results["manga"]["chapters"]["nodes"][::-1],
            "manga_id": manga_id,
            "manga_title": query_results["manga"]["title"],
        },
    )
