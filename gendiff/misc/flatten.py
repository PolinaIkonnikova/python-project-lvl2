def flatten(node_list):
    result = []

    def walk(lst):
        for item in lst:
            if isinstance(item, list):
                walk(item)
            else:
                result.append(item)
    walk(node_list)
    return result
