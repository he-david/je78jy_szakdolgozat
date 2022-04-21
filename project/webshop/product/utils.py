from collections import deque

from .models import Category

def get_all_children(category_id, include_self):
    children_queue = deque()
    res_arr = []
    children_queue.append(category_id)
    not_first = False

    while len(children_queue) != 0:
        curr_item = children_queue.pop()
        if include_self or not_first:
            res_arr.append(curr_item)
        else:
            not_first = True
        curr_children = list(Category.objects.filter(parent_id=curr_item).values('id'))

        for item in curr_children:
            children_queue.append(item['id'])
    return res_arr