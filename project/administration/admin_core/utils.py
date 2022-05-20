def get_order_attr(order_by_attr, default_attr, order_list):
    if order_by_attr in order_list:
        return order_by_attr
    else:
        return default_attr

def order_by_context_fill(context, order_attr, order_list):
    if order_attr in order_list:
        context['order_by'] = order_attr

        if order_attr[0] == '-':
            context['last_order_type'] = 'desc'
        else:
            context['last_order_type'] = 'asc'
    return context