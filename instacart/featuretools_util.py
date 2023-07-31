import featuretools as ft

def get_entityset(name, df, target_entity, entity_col, time_index, relationships):
    es = ft.EntitySet(name)

    print("Adding dataframe...")
    print(f"dataframe_name={target_entity}, time_index={time_index}, index=__id__")
    es.add_dataframe(
        dataframe=df.reset_index(),
        dataframe_name=target_entity,
        time_index=time_index,
        index='__id__',
    )

    graph, graph_rel = {}, {}
    for relationship in relationships:
        if relationship[2] not in graph:
            graph[relationship[2]] = []
            graph_rel[relationship[2]] = []
        graph[relationship[2]].append(
            {"key": relationship[3], "target": relationship[0], "target_key": relationship[1]}
        )
        graph_rel[relationship[2]].append(relationship[0])
    
    parent = {}

    def get_prefix(entity):        
        recursion = entity
        prefix = ""
        while parent[recursion[0]] is not None:
            prefix = f"{recursion[1]}." + prefix
            recursion = parent[recursion[0]]
        return prefix
    
    def get_keys(entity, key):
        return [get_prefix(entity) + key] if isinstance(key, str) else [get_prefix(entity) + k for k in key]
 
    def get_upstream_keys(entity, key):
        key = get_keys(entity, key)
        
        recursion, recursion_lag = entity, None
        while recursion is not None:
            if recursion_lag is not None and recursion_lag[1] in graph_rel[recursion[1]]:
                ind = graph_rel[recursion[1]].index(recursion_lag[1])
                if isinstance(graph[recursion[1]][ind]["target_key"], str):
                    if get_prefix(recursion_lag) + graph[recursion[1]][ind]["target_key"] in key:
                        key.remove(get_prefix(recursion_lag) + graph[recursion[1]][ind]["target_key"])
                        key.append(get_prefix(recursion) + graph[recursion[1]][ind]["key"])
                else:
                    if set([get_prefix(recursion_lag) + k for k in graph[recursion[1]][ind]["target_key"]]) <= set(key):
                        for k, t_k in zip(graph[recursion[1]][ind]["key"], graph[recursion[1]][ind]["target_key"]):
                            key.remove(get_prefix(recursion_lag) + t_k)
                            key.append(get_prefix(recursion) + k)
 
            recursion_lag = recursion
            recursion = parent[recursion[0]]
        
        return key[0] if len(key) == 1 else key

    # Run DFS to find deps
    idx = 0
    parent[idx] = None
    df = df.add_prefix(get_prefix((0, target_entity)))
    candidate_entities = [(idx, target_entity)]
    
    while len(candidate_entities) > 0:
        current_entity = candidate_entities.pop()
        if current_entity[1] not in graph:
            continue
 
        for neighbor in graph[current_entity[1]]:
            idx += 1
            parent[idx] = current_entity
            target_key = get_upstream_keys((idx, neighbor["target"]), neighbor["target_key"])
            
            print("Normalizing dataframe...")
            print(f"base_dataframe_name={current_entity[1]}, new_dataframe_name={neighbor['target']}, index={target_key}")
            print(f"Additional columns: {[col for col in df.columns if col.startswith(neighbor['target']) and col != time_index]}")
            es.normalize_dataframe(
                base_dataframe_name=current_entity[1],
                new_dataframe_name=neighbor["target"],
                index=target_key,
                additional_columns=[col for col in df.columns if col.startswith(neighbor["target"]) and col != time_index],
                make_time_index=False,
            )
            
            candidate_entities.append((idx, neighbor["target"]))

    print("Normalizing dataframe...")
    print(f"base_dataframe_name={target_entity}, new_dataframe_name={entity_col}, index={entity_col}")
    es.normalize_dataframe(
        base_dataframe_name=target_entity if "." not in entity_col else entity_col.split(".")[-2],
        new_dataframe_name=entity_col,
        index=entity_col,
        make_time_index=False,
    )

    return es

def get_features(name, df, target_entity, entity_col, time_index, relationships, cutoff_time):
    es = get_entityset(name, df, target_entity, entity_col, time_index, relationships)

    fm, fd = ft.dfs(
        entityset=es,
        target_dataframe_name=entity_col,
        cutoff_time=cutoff_time,
        cutoff_time_in_index=True,
        include_cutoff_time=False,
        verbose=True,
    )

    fm.reset_index(drop=True, inplace=True)
    y = fm.ww.pop('_execute_operations_on_df')
    return fm, y