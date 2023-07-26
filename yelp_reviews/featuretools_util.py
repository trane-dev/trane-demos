import featuretools as ft

def get_entityset(name, df, target_entity, entity_col, time_index, relationships):
    es = ft.EntitySet(name)

    es.add_dataframe(
        dataframe=df,
        dataframe_name="review",
        time_index="date",
        index='review_id',
    )
    
    es.normalize_dataframe(
        base_dataframe_name="review",
        new_dataframe_name="user",
        index="user_id",
        additional_columns=['user.name', 'user.average_stars', 'user.review_count', 'user.type', 
                            'user.votes_funny', 'user.votes_useful', 'user.votes_cool'],
        make_time_index=False,
    )
    es.normalize_dataframe(
        base_dataframe_name="review",
        new_dataframe_name="business",
        index="business_id",
        additional_columns=['business.checkin.type', 'business.full_address',
                            'business.open', 'business.city', 'business.review_count',
                            'business.name', 'business.longitude', 'business.state',
                            'business.stars', 'business.latitude', 'business.type'],
        make_time_index=False,
    )
    es.normalize_dataframe(
        base_dataframe_name="review",
        new_dataframe_name="checkin",
        index="business_id",
        make_time_index=False,
    )

    return es

def get_features(name, df, target_entity, entity_col, time_index, relationships, cutoff_time):
    es = get_entityset(name, df, target_entity, entity_col, time_index, relationships)

    fm, fd = ft.dfs(
        entityset=es,
        target_dataframe_name="business",
        cutoff_time=cutoff_time,
        cutoff_time_in_index=True,
        include_cutoff_time=False,
        verbose=True,
    )

    fm.reset_index(drop=True, inplace=True)
    y = fm.ww.pop('_execute_operations_on_df')
    return fm, y, es