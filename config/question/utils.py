import os
from uuid import uuid4

# 파일 저장 경로, 파일명 함수
def rename_file_to_uuid(instance, filename):
    upload_to = f'{instance.menu}'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex

    if instance:
        filename = '{}_{}.{}'.format(uuid, instance.cname, ext)
    else:
        filename = '{}.{}'.format(uuid, ext)

    return os.path.join(upload_to, filename)