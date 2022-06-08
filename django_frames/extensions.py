import pandas as pd
import pytz
from django.db.models import DateTimeField
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.fields.related import ForeignKey

class FramedModel:

    def _convert_pdtype(cls, value):
        pd_converters = {pd.Timestamp: lambda ts: ts.to_pydatetime()}
        tp = type(value)
        if tp in pd_converters:
            return pd_converters[tp](value)
        else:
            return value

    @classmethod
    def _select_fields(cls, df):
        fields = {str(i).split('.')[-1:][0] for i in cls._meta.fields}  # default includes all fields and annotations
        forwardings = {fwa for fwa in cls.__dict__.keys() if isinstance(getattr(cls, fwa),ForwardManyToOneDescriptor)}
        fields = fields - forwardings
        fields = fields.union({f+'_id' for f in forwardings})
        related_field_names = {cls._meta.model_name,
                               cls._meta.model_name + '_id',
                               cls._meta.model_name + '_set_id'}
        fields = set(df.columns).intersection(fields.union(related_field_names))
        return fields

    @classmethod
    def to_entities(cls, df, pk=None):
        """transpose entities from a dataframe"""
        fields = cls._select_fields(df)
        if not 'id' in df.columns and pk is None:
            df.reset_index(inplace=True)
            df = df.rename(columns={'index': 'id'})
            df.index = df.index.rename('id')
        elif pk is not None:
            df.reset_index(inplace=True)
            if 'id' in df.columns:
                df.drop(axis=1, columns=['id'], inplace=True)
            df = df.rename(columns={pk: 'id'})
            fields = fields - {pk}
        frame = df[fields]
        dtfields = []
        top_object = frame.head(1).iloc[0]
        for aname in list(top_object._index):
            if aname in fields and isinstance(getattr(cls, aname).field, DateTimeField):
                dtfields.append(aname)
        item_list = []
        df_dict = df.drop([c for c in df.columns if c not in fields], axis=1).T.to_dict()
        for indx, attributes in df_dict.items():
            for attr in dtfields:
                dt = attributes[attr].to_pydatetime()
                if dt.tzinfo is None:
                    dt = pytz.utc.localize(dt)
                attributes[attr] = dt
            item_list.append(cls(**attributes))
        return item_list

    @classmethod
    def to_df(cls, qset, fields=None, set_index=True, index_item=0, keep_types=False, join_prefetch=[]):
        """creating dataframes from querysets"""
        if qset.count() == 0:
            raise ValueError('EmptyQuerySet: failed to access first item in queryset, '
                             'function only works with substantial querysets')
        first = qset.first()
        strip_name = lambda s: str(s).split('.')[-1:][0]
        if fields is None:
            # default includes all fields and annotations
            fields = [strip_name(i) for i in qset.model._meta.fields if not isinstance(i, ForeignKey)] \
                     + list(qset.query.annotations.keys()) \
                     + [strip_name(f)+'_id' for f in qset.model._meta.fields if isinstance(f, ForeignKey)]
        frame = pd.DataFrame(qset.values_list(*fields), columns=fields)
        if keep_types is True:
            conversion = {}
            f_item = qset.first()
            typing = {
                int: 'int64',
                str: str,
                float: 'float64'
            }
            for field in fields:
                dtype = type(f_item._getattribute_(field))
                pd_dtype = typing[dtype]  # needs exception handling
                conversion[field] = pd_dtype
            frame = frame.astype(conversion)
        if set_index is True:
            if not fields[index_item].endswith('id') and first._meta.pk.attname != fields[index_item]:
                print('WARNING', f'{fields[index_item]} may not be an incremental key field, '
                                f'assert its singularity by pd.drop_duplicates()')
            frame.set_index(fields[index_item], inplace=True)
        for selector in join_prefetch:
            if selector in qset.first()._prefetched_objects_cache.keys():
                frame = join_prefetched_entities(frame, qset, selector)
        return frame


def join_prefetched_entities(frame, qset, model_name):
    """joins a specific prefetch cache with the related entities"""
    base_frame = pd.DataFrame()
    combine_key = lambda t:  model_name + '_id'
    for item in qset:
        m2m_relation = item._prefetched_objects_cache[model_name]
        key = combine_key(item)
        related_df = FramedModel.to_df(m2m_relation)
        related_df.reset_index(inplace=True)
        related_df = related_df.rename(columns={'id': key})
        related_df['merge_column'] = item.id
        df_m2m = pd.DataFrame.join(related_df, other=frame.loc[frame.index == item.id],
                                   lsuffix=f'_{model_name}_', how='inner', on='merge_column')
        base_frame = pd.concat([base_frame, df_m2m])
    base_frame = base_frame.rename(columns={'merge_column': 'id'})
    base_frame.set_index('id')
    return base_frame