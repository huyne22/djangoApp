from django.db.models import Count
from .models import Category, Course


def load_course(params = {}):
    q = Course.objects.all()
    kw = params.get('kw')
    if kw:
        q = q.objects.filter(name__icontains=kw)
    cate = params.get('cate')
    if cate:
        q = q.objects.filter(category_id=cate)

def count_course_by_cate():
    return Category.objects.annotate(count = Count('course__id')).values('id', 'name', 'count').order_by('-id')