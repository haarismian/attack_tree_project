from django.db import models


class TreeNode(models.Model):
    label = models.CharField(max_length=100, default='')
    value = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    root = models.ForeignKey('self', null=True, blank=True,
                             related_name='descendants', on_delete=models.CASCADE)
