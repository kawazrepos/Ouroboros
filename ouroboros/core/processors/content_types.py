# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/9/23
#
__author__ = 'giginet'

from .base import BaseProcessor

class ContentTypeProcessor(BaseProcessor):

    name = 'ContentTypeProcessor'
    convert_table = {}

    # app_label, modelが変わったモデルに追従する
    # (((app_label, model), (app_label, model)), )
    content_type_names = (
        (('auth', 'user'), ('personas', 'persona')),
        (('commons', 'material'), ('attachments', 'material')),
        (('mcomments', 'markitupcomment'), ('comments', 'comment')),
    )
    content_type_table_name = 'django_content_type'

    targets = (
        'stars_star.content_type_id',
        'django_comments.content_type_id',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        src_ct = self.src_meta.tables[self.content_type_table_name]
        dst_ct = self.dst_meta.tables[self.content_type_table_name]

        src_records = [r._asdict() for r in self.src_session.query(src_ct.select()).all()]
        dst_records = [r._asdict() for r in self.dst_session.query(dst_ct.select()).all()]

        # 変換テーブルを作成する
        for src_record in src_records:
            model, app_label = self._convert_names(src_record['model'], src_record['app_label'])
            dst_record = self._search_record(dst_records, model=model, app_label=app_label)
            if dst_record:
                self.convert_table.update({src_record['id']: dst_record['id']})

    def convert(self):
        for target in self.targets:
            table_name, column_name = target.split('.')
            print("Convert content type of {} in {}".format(column_name, table_name))
            table = self.dst_meta.tables[table_name]
            for r in self.dst_session.query(table.select()).all():
                record = r._asdict()
                # 変換前のCTを取り出す
                src_ct = record[column_name]
                if src_ct in self.convert_table.keys():
                    # もし、CTの変換先が見つかったら
                    record[column_name] = self.convert_table[src_ct]
                    self._partial_update(table, record, column_name)
                else:
                    # もし、CTの変換先が見つからなかったら
                    # そのレコードをdropする
                    print("Content Type {} is not found.".format(src_ct))
                    delete = table.delete().where(table.c.id==record['id'])
                    self.dst_session.execute(delete)
            self.dst_session.commit()

    def _convert_names(self, app_label, model):
        """
        Kawaz2のapp_labelとmodelを渡して、それがKawaz3側でリネームされていたら
        リネームされたペアを返す
        されてなかったら入力値をペアで返す
        """
        for src, dst in self.content_type_names:
            if src[0] == app_label and src[1] == model:
                return dst
        return app_label, model
