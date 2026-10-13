from django.shortcuts import render

from models.topics import find_topic_by_id
from storage import load_topics


def topic_list(request):
    """Список тем."""
    topics = load_topics()
    context = {"topics": topics}
    return render(request, "topics/topic_list.html", context)


def topic_detail(request, topic_id):
    """Страница отдельной темы."""
    topics = load_topics()
    topic = find_topic_by_id(topics, topic_id)
    context = {"topic": topic}
    return render(
        request,
        "topics/topic_detail.html",
        context,
        status=404 if topic is None else 200,
    )
