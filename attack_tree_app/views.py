from django.shortcuts import render
from django.http import JsonResponse
from .models import TreeNode


def index(request):
    return render(request, 'attack_tree_app/index.html')


def create_node(request):
    label = request.POST.get('label', '')
    value = int(request.POST.get('value', 0))
    parent_id = request.POST.get('parent_id', None)
    node_type = request.POST.get('type', '')  # 'sibling' or 'child'

    parent = None
    if parent_id:
        parent = TreeNode.objects.get(pk=parent_id)

    if node_type == 'sibling':
        # Assuming parent's parent is the new node's parent
        new_node = TreeNode(label=label, value=value, parent=parent.parent)
    else:
        # 'child'
        new_node = TreeNode(label=label, value=value, parent=parent)

    new_node.save()

    return JsonResponse({'status': 'success', 'node_id': new_node.id})


def get_tree(request):
    # Logic to get the tree data
    # You can serialize the TreeNode queryset into JSON and return it
    nodes = TreeNode.objects.all()
    data = [{'id': node.id, 'label': node.label, 'value': node.value,
             'parent_id': node.parent.id if node.parent else None} for node in nodes]
    return JsonResponse(data, safe=False)


def sum_route(request):
    node_id = request.POST.get('node_id')
    node = TreeNode.objects.get(pk=node_id)

    # Calculate the sum along the path to the root
    total = 0
    while node:
        total += node.value
        node = node.parent

    return JsonResponse({'sum': total})


def export_tree(request):
    nodes = TreeNode.objects.all()
    data = [{'id': node.id, 'label': node.label, 'value': node.value,
             'parent_id': node.parent.id if node.parent else None} for node in nodes]
    return JsonResponse(data, safe=False)


def import_tree(request):
    data = json.loads(request.body)
    TreeNode.objects.all().delete()  # Clear existing tree
    nodes_map = {}
    for item in data:
        node = TreeNode(
            id=item['id'], label=item['label'], value=item['value'])
        nodes_map[item['id']] = node
        node.save()
    for item in data:
        if item['parent_id']:
            nodes_map[item['id']].parent = nodes_map[item['parent_id']]
            nodes_map[item['id']].save()
    return JsonResponse({'status': 'success'})
