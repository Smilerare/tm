import hashlib
def md5(str):
    import hashlib
    str=str.encode("utf-8")
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
s="123456"
print(md5(s))
import django.utils.timezone as timezone

createDate = timezone.now
print(createDate)